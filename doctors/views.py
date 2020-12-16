from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from patients.functions import *

from common.models import *
from datetime import date

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
def logout_doctor(request):
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

    #call function to calculate doctor age
    age = age_calculation(doctor.user.date_of_birth)

    #call method to filter for valid appointments
    appointments = get_appointments_list(doctor.doctor_appointments.all())

    context = {
        "hospital": doctor.hospital,
        "doctor": doctor,
        "appointments_number": len(appointments),
        "patients_number": doctor.patients.filter(asymptomatic=False).count(),
        "recovered_number": asymptomatic_patients,
        "age": age 
    }
    #return information
    return render(request, "doctors/index.html", context)


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

    #now get the doctors appointments with the most recent first.
    appointments = get_appointments_list(doctor.doctor_appointments.all().order_by("-date"))

    return JsonResponse({
        "appointments": appointments
    })


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def display_patient(request, patient_id):
    """this function returns a ptient details if GET, and allows the doctor to 
    add any medications or symptoms to the user.
    parameters
        -request
        -patient_id
    returns: patient_page
    """

    if request.method == "GET":

        data = retrieve_patient_info(request, patient_id)

        return render(request, "doctors/patient.html", data)
    
    else:
        #add symptom or complication
        new_symptom = request.POST["symptom"]
        new_complication = request.POST["complication"]

        #get patient instance
        try:
            patient = Patient.objects.get(pk=patient_id)
            print(patient.user.username)
        except Patient.DoesNotExist:
            raise Http404(f"Cant add symptom {new_symptom} or complication (Patient {patient_id} Does Not Exist)")

         #check if any symptom or complication was selected
        if new_symptom != "None":
            symptom = Symptom.objects.get(name=new_symptom.strip())
            patient.add_symptom(symptom) 

        if new_complication != "None":
            complication = Complication.objects.get(name=new_complication.strip())
            patient.complications.add(complication)

    #redirect to reload page with new symptom
    return HttpResponseRedirect(reverse("get_patient", args=(patient_id,)))


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def remove_symptom(request):

    symptom = request.GET.get("symptom")
    patient_id = request.GET.get("id")

    #get patient and symptom instance
    try:
        symptom = Symptom.objects.get(name=symptom.strip())
        patient = Patient.objects.get(pk=patient_id)
    except (Symptom.DoesNotExist, Patient.DoesNotExist):
        raise Http404(f"Symptom {symptom} does not exist or patient {patient_id}")

    #call instance method to update patient symptoms
    patient.remove_symptom(symptom)

    return JsonResponse({
        "success": True
    })


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def patient_appointments(request):

    user_id = request.GET.get("id")

    data = retrieve_patient_info(request, user_id)

    return JsonResponse({
        "appointments": data["old_appointments"]
    })


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def display_medications(request):

    patient_id = request.GET.get("id")

    #get patient
    try:
        patient = Patient.objects.get(pk=patient_id)
        medications = Medication.objects.filter(patient=patient).order_by("-date")
    except Patient.DoesNotExist:
        raise Http404("Patient for medications not found!")

    data = []
    for medic in medications:
        data.append({"medication": medic.medication, "date": medic.date.strftime("%m/%d/%y")})
    
    #if no medication yet populate the data list with Nones
    if len(data) == 0:
        data = [{"medication": "None", "date": date.today().strftime("%m/%d/%y")}]

    return JsonResponse({
        "medications": data
    })


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def add_medication(request):

    patient_id = request.GET.get("id")
    medication = request.GET.get("medication")

    #retrive patient
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise Http404("Can't add medication, patient not found!")

    #create medication object
    current_date = date.today()
    Medication.objects.create(patient=patient, medication=medication, date=current_date)

    #return medication back as JS to be updated
    return JsonResponse({
        "medication": medication,
        "date": current_date.strftime("%m/%d/%y")
    })


@login_required(redirect_field_name="doctor_login", login_url="/doctor/login")
def edit_patient(request):
    """This function can also be called by the patient, when editing info
    """
    
    email = request.GET.get("email")
    phone_number = request.GET.get("phone")
    gender = request.GET.get("gender")
    patient_id = request.GET.get("id")

    #call helper function to update patient fields
    updated_list = edit_patient_information(patient_id, email, phone_number, gender)

    return JsonResponse({
        "phone": updated_list[0],
        "email": updated_list[2],
        "gender": updated_list[1]
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

    #filter patients from asymptomatics
    patient_objects = doctor.patients.all()
    patients = []

    for patient in patient_objects:
        if patient.asymptomatic == False:
            patients.append(patient)


    #now get the doctors patient instances
    patients = get_patients_list(patients)

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
        "recovered": get_patients_list(recovered)
    })

