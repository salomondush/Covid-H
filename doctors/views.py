from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from patients.functions import age_calculation, arrange_symptoms

from common.models import *

# Create your views here.

def doctor_login(request):
    """Logs the user in
    Parameters:
        -request
    return: the login page, an error when it arises, and redirects the user to the index function
    """
    if request.method == 'GET':
        return render(request, "doctors/login.html")
    else:
        #authentcate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #check if user is doctor or not
            if user.is_doctor == True:
                login(request, user)
                return HttpResponseRedirect(reverse("doctors"))
            else:
                return render(request, "doctors/login.html", {
                "message": "Doctor not found!"
            })
        else:
            return render(request, "doctors/login.html", {
                "message": "Invalid Username and/or Password"
            })

def register(request):
    """registers the user.
    Parameters:
        -request
    returns: Error if user already exists, redirects to the doctors index function.
    """
    if request.method == 'GET':
        return render(request, "doctors/register.html")
    else:
        username = request.POST["username"]
        phone_number = request.POST["phone"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        country = "Rwanda" #!you can change this after. Its causing a MultiValueDictKeyError
        email = request.POST["email"]
        city = request.POST["city"]
        date_of_birth = request.POST["birth"]
        password = request.POST["password"]
        #hospital = request.POST["hospital"]#! update the HTML

        #get hospital instance for the doctor
        try:
            hospital = Hospital.objects.get(name=hospital)
        except Hospital.DoesNotExist:
            raise Http404("Hospital selected does not exist")

        #let's try to create user
        try:
            #username, email, and password are positional arguments
            user = User.objects.create_user(
                username, email, password,
                phone=phone_number,
                first_name=firstname, 
                last_name=lastname, 
                country=country,
                city=city,
                date_of_birth=date_of_birth, 
                is_doctor=True
            ) 
            user.save()

            #create doctor instance using the user who is a doctor
            Doctor.objects.create(user=user, hospital=hospital)
        except IntegrityError:
            return render(request, "doctors/register.html", {
                "message": "Username already taken!"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("doctors"))


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def logout(request):
    """Logs the current user out
    parameters:
        -request
    returns: redirects the user to the doctor login function"""
    logout(request)
    return HttpResponseRedirect(reverse("doctor_login"))


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def index(request):
    """Loads the doctor's index page
    parameters:
        - request
    retuns: information needed to load the index page"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        raise Http404("Doctor with current user instance unavailable!")

    #counting patients who have recovered or are asymptomatic
    asymptomatic_patients = doctor.patients.filter(asymptomatic=True).count()

    age = age_calculation(doctor.user.date_of_birth)

    #return information
    return render(request, "doctors/index.html", {
        "hospital": doctor.hospital,
        "doctor": doctor,
        "appointments_number": doctor.doctor_appointments.count(),
        "patients_number": doctor.patients.count(),
        "recovered_number": asymptomatic_patients,
        "age": age
    })

@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def appointments(request):
    """retrives all appointment objects related to the current doctor object
    parameters:
        - request
    returns: a json of a list of appointment objects
    """
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        raise Http404("Doctor with current user instance not found!")

    #now get the doctors appointments
    appointments = doctor.doctor_appointments.all()

    return JsonResponse({
        "appointments": appointments
    })

@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def patients(request):
    """retrieves all patient objects related to the current doctor 
    parameters:
        - request
    returns: a json of a list of the doctors patient objects
    """
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        raise Http404("Doctor with current user instance not found!")

    #now get the doctors patient instances
    patients = doctor.patients.all()

    return JsonResponse({
        "patients": patients
    })

@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def recovered(request):
    """retrieves information related to the current doctor's patients who are asymptomatic
    parameters:
        - request
    returns: a json list of recovered patients
    """
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        raise Http404("Doctor with current user instance not found!")

    #first ge the doctors patients
    patients = doctor.patients.all()

    #filter those that are asymptomatic to be in recovered
    recovered = []
    for patient in patients:
        if patient.asymptomatic == True:
            recovered.append(patient)
        else:
            pass 

    return JsonResponse({
        "recovered": recovered
    })

@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def patient(request, patient_id):
    """Loads all information related to a certian patient and allows to doctor to add complications
    parameters:
        -request
        -patient_id: the id of the patient object we have to use
        
    returns: if GET, it returns the patient page with required patient information. If the doctor
    adds a complication to the user it adds the complication to the user's current complications
    and redirects to the doctor patient function"""

    if request.method == "GET":
        #get appointment and patient related information
        try:
            patient = Patient.objects.get(pk=patient_id)
            appointment = patient.appointments.order_by("-date").first() 
            complications = Complication.objects.all() 
            doctor = Doctor.objects.get(user=request.user)     
        except Appointment.DoesNotExist:
            return render(request, "patients/error.html", {
                "error": "You have no appointments yet"
            })
        except Patient.DoesNotExist:
            raise Http404("Patient matching appointment id not found!")

        #age calculation
        patient_age = age_calculation(patient.user.date_of_birth)
        doctor_age = age_calculation(doctor.user.date_of_birth)

        #symptom categorization
        symptoms = patient.symptoms.all()
        arranged_symptoms = arrange_symptoms(symptoms)

        return render(request, "patients/appointment.html", {
            "nature": "Patient",
            "doctor": doctor,
            "appointment": appointment,
            "patient": patient,
            "patient_age": patient_age,
            "doctor_age": doctor_age,
            "common": arranged_symptoms[0],
            "less_common": arranged_symptoms[1],
            "serious": arranged_symptoms[2],
            "old_appointments": patient.appointements.all(),
            "complications": complications
        })

    else:
        #when a user adds a complication to the appointment
        complication = request.POST["complication"]

        #get patient object
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            raise Http404("Patient adding Complication does not exist")

        #add complication to patients complication lists
        patient.complications.add(complication)

        #redirect the user back
        return HttpResponseRedirect(reverse("doctor_patient"))

