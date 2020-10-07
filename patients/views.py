from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from datetime import date
from patients.functions import *
from common.models import *

##How to import models from the common application

# Create your views here.

def patient_login(request):
    if request.method == 'GET':
        return render(request, "patients/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)##how does authenticate know which model to use ???

        if user is not None:
            #check if the user is not doctor 
            if user.is_doctor == True:
                return render(request, "patients/login.html", {
                    "message": "Patient not found!"
                })
            else:
                login(request, user)
                return HttpResponseRedirect(reverse("patients"))
        else:
            return render(request, "patients/login.html", {
                "message": "Invalid Username and/or Password"
            })


def register(request):
    """register new patient into our database
    parameters:
    - request
    returns: After registering new doctor into our database, it 
            redirects the user to the patient's index page.
    """
    if request.method == 'GET':
        return render(request, "patients/register.html")
    else:
        username = request.POST["username"]
        phone_number = request.POST["phone"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        country = "Rwanda" #!you can change this after
        city = request.POST["city"]
        email = request.POST["email"]
        date_of_birth = request.POST["birth"]
        password = request.POST["password"]

        #let's try to create the user
        try:
            user = User.objects.create_user(
                username, email, password,
                phone=phone_number,
                first_name=firstname, 
                last_name=lastname, 
                city=city,
                country=country, 
                date_of_birth=date_of_birth, 
                is_doctor=False
            ) 
            user.save()
        except IntegrityError: 
            return render(request, "patients/register.html", {
                "message": "Username not already taken!"
            })

        login(request, user)
        return HttpResponseRedirect(reverse("patients"))


@login_required(redirect_field_name="user_login", login_url="/patients/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))


@login_required(redirect_field_name="user_login", login_url="/patients/login")
def index(request):
    """get info about all countries with Covid cases.

    parameters:
        - request

    returns: renders the index template with a list of all countries and dictionaries
    containing worldwide and default country 'Rwanda' corona virus cases info
    """
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 
                 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 
                 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 
                 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 
                 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', 
                 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', "Côte d'Ivoire", 'Denmark', 'Djibouti', 'Dominica', 
                 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 
                 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 
                 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See (Vatican City State)', 
                 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', ' Islamic Republic of', 'Iraq', 'Ireland', 
                 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea (South)', 'Kuwait', 
                 'Kyrgyzstan', 'Lao PDR', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 
                 'Luxembourg', 'Macedonia', ' Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 
                 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 
                 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 
                 'Pakistan', 'Palestinian Territory', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 
                 'Portugal', 'Qatar', 'Republic of Kosovo', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 
                 'Saint Lucia', 'Saint Vincent and Grenadines', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 
                 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 
                 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 
                 'Syrian Arab Republic (Syria)', 'Taiwan', ' Republic of China', 'Tajikistan', 'Tanzania', ' United Republic of', 
                 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 
                 'United Arab Emirates', 'United Kingdom', 'United States of America', 'Uruguay', 'Uzbekistan', 
                 'Venezuela (Bolivarian Republic)', 'Viet Nam', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe'];
    cases_data = cases()
    world = cases_data[1]
    country = cases_data[0]

    return render(request, "patients/index.html", {
        "world": world,
        "country": country,
        "countries": countries
        })


def country_cases(request):

    #get country data.
    country = request.GET.get("country_name")
    cases_data = cases(country.strip())

    return JsonResponse({
        "country": cases_data[0]
    })

@login_required(redirect_field_name="user_login", login_url="/patients/login")
def checkup(request):
    """displays the check up if the method is get, and process the user check up
    if the method is POST
    parameters:
        -request
    returns: check-up page if GET and results page if POST
    """
    if request.method == 'GET':
        #get all the complications and symptoms
        try:
            complications = Complication.objects.all()
            symptoms = Symptom.objects.all()
        except Complication.DoesNotExist:
            raise Http404("No Complications yet!")
        except Symptom.DoesNotExist:
            raise Http404("No Symptoms yet!")
        
        sy1 = symptoms[0]
        sy2 = symptoms[1]
        sy3 = symptoms[2]
        sy4 = symptoms[3]
        sy5 = symptoms[4]
        sy6 = symptoms[5]
        sy7 = symptoms[6]
        sy8 = symptoms[7]
        sy9 = symptoms[8]
        sy10 = symptoms[9]
        sy11 = symptoms[10]
        sy12 = symptoms[11]
        sy13 = symptoms[12]

        #return all symptoms and complications for the check-up page.
        return render(request, "patients/checkup.html", {
            "complications": complications,
            "sy1": sy1,
            "sy2": sy2,
            "sy3": sy3,
            "sy4": sy4,
            "sy5": sy5,
            "sy6": sy6,
            "sy7": sy7,
            "sy8": sy8,
            "sy9": sy9,
            "sy10": sy10,
            "sy11": sy11,
            "sy12": sy12,
            "sy13": sy13
        })

    else:
        #threshold btn low and high possibilty and criticl and mild
        appointment_threshold = 50
        critical_threshold = 80

        #Collect all symptoms and analyse them.
        sy1 = request.POST["1"]
        sy2 = request.POST['2']
        sy3 = request.POST['3']
        sy4 = request.POST['4']
        sy5 = request.POST['5']
        sy6 = request.POST['6']
        sy7 = request.POST['7']
        sy8 = request.POST['8']
        sy9 = request.POST['9']
        sy10 = request.POST['10']
        sy11 = request.POST['11']
        sy12 = request.POST['12']
        sy13 = request.POST['13']

        complication_id = request.POST["complication"] #this should be an ID integer

        sy_list = [sy1, sy2, sy3, sy4, sy5, sy6, sy7, sy8, sy9, sy10, sy11, sy12, sy13]

        #use get_weight() to calculate infection possibility
        weight_data = get_weight(sy_list)
        possibility = weight_data[0]
        symptoms_object_list = weight_data[1]

        #if possibility > 50
        if possibility >= appointment_threshold:
            try:
                
                #check if user has a complication and get it or assign it to false to prevent later errors.
                if complication_id != 'None':
                    complication = Complication.objects.get(pk=int(complication_id))
                else:
                    complication = False;

                #delete from results table
                result = Result.objects.get(user=request.user)
                result.delete()
            except Complication.DoesNotExist:
                raise Http404("Selected Complication Does not Exist")
            except Result.DoesNotExist:
                pass
            
            #generate automatic doctor
            doctor = get_doctor()

            #check if user is patient and update, if not add them
            try:
                patient = Patient.objects.get(user=request.user)
                hospital = Hospital.objects.filter(doctor=doctor).first()
                patient.complications.add(complication)
                improvenment = patient.update_symptoms(weight_data[2])

                return render(request, "patients/results.html", {
                    "existing": True,
                    "possibility": round(patient.current_possibility, 1),
                    "appointment": patient.appointment,
                    "condition": patient.condition,
                    "improvenment": round(improvenment, 1)
                })

            except Patient.DoesNotExist: 
                if possibility >= critical_threshold:
                    condition = "Critical"
                else:
                    condition = "Mild"

                #create appointment and patient instance.
                appointment_date = get_appointment_date(condition, complication)
                appointment = Appointment.objects.create(doctor=doctor, date=appointment_date)
                patient = Patient.objects.create(user=request.user, doctor=doctor, hospital=doctor.hospital,
                                                condition=condition, initial_date=date.today(), 
                                                last_visit=date.today(), current_possibility=possibility,
                                                previous_possibility=0.0, appointments=appointment)

                #now add complication and symptoms for the new patient
                if complication:
                    patient.complications.add(complication)


                for symptom in symptoms_object_list:
                    patient.symptoms.add(symptom)

                return render(request, "patients/results.html", {
                    "possibility": round(possibility, 1),
                    "appointment":appointment,
                    "condition": condition
                })
        
        else:

            #the user won't need any appointment, so info about him should be kept in the result table
            today_date = date.today()
            try:
                result = Result.objects.get(user=request.user)
                new_possibility = possibility
                improvenment = result.update_result(new_possibility)

                return render(request, "patients/results.html", {
                    "possibility": round(result.new_possibility, 1),
                    "condition": "Asymptomatic",
                    "improvenment": round(improvenment, 1),
                })
            except Result.DoesNotExist:
                #if the user is not in results, it means that he is new and asymptomatic or
                # it's a patient with reduced symptoms
                try:
                    patient = Patient.objects.get(user=request.user)
                    if patient.asymptomatic == False:

                        patient.asymptomatic = True
                        patient.save()

                        #update patient symptoms
                        improvenment = patient.update_symptoms(symptoms_object_list)

                        #insert the patient into results
                        Result.objects.create(user=request.user, last_possibility=patient.previous_possibility,
                                              new_possibility=possibility, date=today_date)

                        return render(request, "patients/results.html", {
                            "possibility": round(patient.current_possibility, 1),
                            "condition": patient.condition,
                            "improvenment": round(improvenment, 1),
                            "healed": True
                        })
                except Patient.DoesNotExist:
                    
                    #This means that the user is completely new on check-up
                    result = Result.objects.create(user=request.user, new_possibility=possibility, date=today_date)
                    
                    return render(request, "patients/results.html", {
                        "possibility": round(result.new_possibility, 1),
                        "condition": "Asymptomatic"
                    })

@login_required(redirect_field_name="user_login", login_url="/patients/login")
def appointment(request):
    """This function returns the user's appointment details if GET, and adds new
    symptoms to the user when the method is get.
    parameters:
        - request
    returns: appointment page 
    """
    if request.method == 'GET': 
        #get appointment and patient related information
        try:
            patient = Patient.objects.get(user=request.user)
            complications = Complication.objects.all()
        except Appointment.DoesNotExist:
            return render(request, "patients/error.html", {
                "error": "You have no appointments yet"
            })
        except Patient.DoesNotExist:
            raise Http404("Patient matching appointment id not found!")

        #age calculation
        patient_age = age_calculation(patient.user.date_of_birth)
        doctor_age = age_calculation(patient.doctor.user.date_of_birth)

        #symptom categorization
        symptoms = patient.symptoms.all()
        arranged_symptoms = arrange_symptoms(symptoms)

        #get all appointments related to the user
        user_appointments = get_appointments(request.user)

        return render(request, "patients/appointment.html", {
            "appointment": patient.appointments,
            "patient": patient,
            "patient_age": patient_age,
            "doctor_age": doctor_age,
            "common": arranged_symptoms[0],
            "less_common": arranged_symptoms[1],
            "serious": arranged_symptoms[2],
            "old_appointments": user_appointments,
            "patient_complications": patient.complications.all(),
            "complications": complications
        })

    else:
        #when a user adds a complication to the appointment
        complication = request.POST["complication"]

        #get patient object
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            raise Http404("Patient adding Complication does not exist")

        #add complication to patients complication lists
        patient.complications.add(complication)

        #redirect the user back
        return HttpResponseRedirect(reverse("user_appointment"))