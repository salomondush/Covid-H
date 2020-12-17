from common.models import *
from django.http import Http404
import requests

from datetime import date, datetime

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

def get_patients_list(patients):
    """receives a a list of patient objects and extracts id, name,
    and date.
    parameters: patients -- List of patients

    return: patients_list -- a list of individual patients with
    required info.
    """
    patients_list = [] #holds lists of individual patients

    for patient in patients:
        p_dict = {} #holds data for one patient

        #populate the dictionary
        p_dict["id"] = patient.id
        p_dict["name"] = patient.__str__()
        p_dict["date"] = patient.last_visit.strftime("%m/%d/%y")

        #add the dict containing useful patient data to the list
        patients_list.append(p_dict)
       

    return patients_list
 
def get_appointments_list(appointments):
    """receives a a list of appointment objects and extracts id, name,
    and date.
    parameters: appointments -- List of appointments

    return: appointments_list -- a list of individual patients with
    required info.
    """
    
    appointments_list = [] #holds lists of individual appointments

    for appointment in appointments:
        a_dict = {} #holds data for one appointment

        #populate data into the appointment dictionary
        if appointment.get_patient():
            a_dict["id"] = appointment.get_patient().id
            a_dict["name"] = appointment.get_patient().__str__()
            a_dict["date"] = appointment.date.strftime("%m/%d/%y")

            appointments_list.append(a_dict)#add the dict of individualr appointment to list 

    return appointments_list 



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


def age_calculation(birthdate):
    """Calculates age given birthdate of someone
    parameters:
        - birthdate
    returns: an integer which corresponds to the age depending on the given
    birthdate.
    """
    today = date.today()
    age =  today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

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


    

def edit_user_information(id, email, phone_number, gender):
    """updates certain fields about a patient
    parameters
        -email
        -phone_number
        -gender
    returns: a list of updated fields
    """
     #get patient and update these fields
    try:
        user = User.objects.get(pk=id)
    except Patient.DoesNotExist:
        raise Http404("Can't edit patient information, Not found!")

    user.phone = phone_number
    user.gender = gender
    user.email = email
    user.save()

    #return to calling function the updated list
    return [user.phone, user.gender, user.email]

def retrieve_patient_info(request, id):
    """this function retrives patient related infomation
    parameters:
        -id
    returns: dictionary containing patient related information
    """

    try:
        patient = Patient.objects.get(pk=id)
        doctor = Doctor.objects.get(user=request.user)
        complications = Complication.objects.all()
        symptoms = Symptom.objects.all()
    except Patient.DoesNotExist:
        raise Http404("Patient Does Not Exist")
    except Doctor.DoesNotExist:
        raise Http404("Current doctor does not exist")

    #calculate age and categorize symptoms
    patient_age = age_calculation(patient.user.date_of_birth)

    arranged_symptoms = arrange_symptoms(patient.symptoms.all())

    all_appointments = get_appointments_list(Appointment.objects.filter(doctor=doctor).order_by("-date"))

    #get current patient specific appointmnts
    user_appointments = []
    for appointment in all_appointments:
        if appointment["name"] == patient.user.__str__():
            user_appointments.append(appointment)

    return {
            "patient_age": patient_age,
            "symptoms": symptoms,
            "patient": patient,
            "common": arranged_symptoms[0],
            "less_common": arranged_symptoms[1],
            "serious": arranged_symptoms[2],
            "patient_complications": patient.complications.all(),
            "old_appointments": user_appointments,
            "complications": complications
    }

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
