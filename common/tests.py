from django.test import Client, TestCase
from django.db.models import Max
from datetime import date
from .models import *

class CovidTestCase(TestCase):

    def setUp(self):

        #create 3 user objects to use
        user_1 = User.objects.create_user("salomon", "salomon@gmail.com", "salomon@123",
        phone="0780556610",
        first_name="Salomon",
        last_name="Dushimirimana",
        country="Rwanda",
        city="Kigali",
        date_of_birth=date(2001, 1, 1),
        is_doctor=False)
        user_1.save()

        #to be used for testing validity
        User.objects.create_user("eric", "eric@gmail.com", "eric@123",
        phone="0780556610",
        first_name="Eric",
        last_name="Dufitimana",
        country="Rwanda",
        city="Kigali",
        date_of_birth=date(2007, 1, 1),
        is_doctor=False)
        user_1.save()

        user_2 = User.objects.create_user("ivan", "ivan@gmail.com", "ivan@123",
        phone="0780566100",
        first_name="ivan",
        last_name="valery",
        country="Rwanda",
        city="Kigali",
        date_of_birth=date(2000, 1, 1),
        is_doctor=True)
        user_2.save()

        #create a hospital object
        hospital = Hospital.objects.create(name="King Faiscal Hospital", location="Kigali")

        #create a doctor object 
        Doctor.objects.create(user=user_2, hospital=hospital)

        #reate symptoms
        Symptom.objects.create(name="Fever", weight=20, symptom_type="most_common")
        Symptom.objects.create(name="Dry Cough", weight=20, symptom_type="most_common")
        Symptom.objects.create(name="Tiredness", weight=20, symptom_type="most_common")
        Symptom.objects.create(name="Aches and pains", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="Sore throat", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="Diarrhea", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="Conjunctivitis", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="headache", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="Loss of taste or smell", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="a rash on skin, or discolouration of fingers or toes", weight=1.4, symptom_type="less_common")
        Symptom.objects.create(name="Difficulty breathing or shortness of breath", weight=10, symptom_type="serious")
        Symptom.objects.create(name="Chest pain or pressure", weight=10, symptom_type="serious")
        Symptom.objects.create(name="Loss of speech or movement", weight=10, symptom_type="serious")

    def test_valid_patient(self):
        """Test a valid patient"""
        user = User.objects.get(username="salomon")
        userDoc = User.objects.get(username="ivan")
        doctor = Doctor.objects.get(user=userDoc)
        appointment = Appointment.objects.create(doctor=doctor, date=date.today())

        patient = Patient.objects.create(user=user, doctor=doctor, hospital=doctor.hospital,
                                            condition="None", initial_date=date.today(), 
                                            last_visit=date.today(), current_possibility=0.0,
                                            previous_possibility=0.0, appointments=appointment)

        #add the symptoms
        symptoms = Symptom.objects.filter(symptom_type="most_common")
        patient.update_symptoms(symptoms)

        return self.assertTrue(patient.is_valid_patient() and patient.asymptomatic == False)

    def test_valid_user(self):
        """Test a valid user"""
        user = User.objects.get(username="salomon")

        return self.assertFalse(user.is_valid_user())

    def test_invalid_user_1(self):
        """Test invalid user with no set username"""
        user = User.objects.get(username="eric")

        user.username = ""
        user.save()

        valid_user = user.is_valid_user()
        user.username="eric"
        user.save()

        return self.assertFalse(valid_user)

    def test_invalid_user_2(self):
        """Test invalid user with invalid date of birth"""
        user = User.objects.get(username="eric")

        original_date = user.date_of_birth
        user.date_of_birth = date(1800, 1, 1)
        user.save()

        valid_user = user.is_valid_user()
        user.date_of_birth = original_date
        user.save()

        return self.assertFalse(valid_user)

        

