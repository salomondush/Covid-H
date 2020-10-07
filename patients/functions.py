from common.models import *
from django.http import Http404
import requests

from datetime import date

def cases(country="Rwanda"):
    """generates data related to current covid-19 situation depending on cases
    parameters:
        - country
    returns: A tuple whose first value is a dictionary or json containing a 
            selected countries cases, and the second value is also a dictionary
            of worldwide related data.
    """
    res = requests.get("https://api.covid19api.com/summary", verify=False)
    if res.status_code != 200:
        raise Http404("ERROR: API request unsuccessful")
    else:
        data = res.json()
        #check if API is under caching
        if data["Message"]:
            raise Http404(data["Message"])
        countries = data["Countries"]
        for country_info in countries:
            if country_info["Country"] == country:
                country_data = country_info
        #get global data
        world_data = data["Global"]  

    return (country_data, world_data)


def get_doctor():
    """generates a suitable doctor to the patient depending on availability
    parameters: None

    returns: A doctor object with less patients.
    """
    try:
        doctors = Doctor.objects.all()
    except Doctor.DoesNotExist:
        raise Http404("No hospital instance found!")
    doctors_list = []

    for doctor in doctors:
        doctors_list.append(doctor.patients.count())
    
    #sort doctors patient count list
    doctors_list.sort()
    
    for doctor in doctors:
        if doctor.patients.count() == doctors_list[0]:
            return doctor


def get_weight(sy_list):
    """Classifying user's symptoms and calculating infection probabilty
    parameters:
        - sy_list (a list of symptoms)
    returns: a tuple with a boolean true for higher possibility and false 
            for low, the possibility value, and the symptoms object list.
    """
    symptoms_object = []
    possibility = 0
    for i in sy_list:
        if int(i) != 0:
            try:
                symptom = Symptom.objects.get(pk=int(i))
                possibility += symptom.weight 
                symptoms_object.append(symptom)
            except Symptom.DoesNotExist:
                raise Http404(f"symptom with id: {i} not found")
    return (possibility, symptoms_object)
    #if possibility > 50:
        #return (True, possibility, symptoms_object)
    
    #else:
        #return (False, possibility, symptoms_object)

def get_appointment_date(condition, complication):
    """generate appointment to the patient depending on conditino and complication
    parameters
        - conditino
        - complicatoin
    returns: appointment date depending on the user's condition
    """
    today = date.today()

    #a user should be assumed as critical if there's a complication
    if complication:
        condition = "Critical"

    #set critical and regular appointments
    if condition == "Critical":
        appointment = date(today.year, today.month, (today.day + 1))
    else:
        appointment = date(today.year, today.month, (today.day + 5))
    return appointment


def age_calculation(birthdate):
    """Calculates age given birthdate of someone
    parameters:
        - birthdate
    returns: an integer which corresponds to the age depending on the given
    birthdate.
    """
    today = date.today()
    age =  today.year -  birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    return age


def arrange_symptoms(symptoms):
    """arranges symptoms by type
    parameters:
        - symptoms list
    returns: a list whose values are lists of less common, most common
            and serious symptoms respectively.
    """
    common = []
    less_common = []
    serious = []
    for symptom in symptoms:
        if symptom.symptom_type == "most_common":
            common.append(symptom)
        elif symptom.symptom_type == "less_common":
            less_common.append(symptom)
        else:
            serious.append(symptom)
    return [common, less_common, serious]

def get_appointments(user):
    """gets all appointments related to a given user
    parameters:
        - user
    returns: a list of appointment objects related to the given user
    """
    try:
        appointments = Appointment.objects.order_by("-date")
    except Appointment.DoesNotExist:
        raise Http404("Appointments not found")
    
    user_appointments = []
    for appointment in appointments:
        if appointment.get_patient == user:
            user_appointments.append(appointment)

    return user_appointments
