from django.test import Client, TestCase
from django.db.models import Max
from datetime import date
from .models import *
import json

class CovidTestCase(TestCase):

    def setUp(self):

        #create 3 user objects to use
        #to be used for testing valid patient
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

        #to be used for a doctor
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
        doctor = Doctor.objects.create(user=user_2, hospital=hospital)

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

        #create a patient
        appointment = Appointment.objects.create(doctor=doctor, date=date.today())
        patient = Patient.objects.create(user=user_1, doctor=doctor, hospital=doctor.hospital,
                                            condition="None", initial_date=date.today(), 
                                            last_visit=date.today(), current_possibility=0.0,
                                            previous_possibility=0.0, appointments=appointment)

        #add the symptoms
        symptoms = Symptom.objects.filter(symptom_type="most_common")
        patient.update_symptoms(symptoms)

    #Database Test Block

    def test_valid_patient(self):
        """Test a valid patient"""

        #get patient to test
        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)

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

        
    #Doctor Views Testing Block

    def test_doctor_index(self):
        """Test for doctor index page"""
        user = User.objects.get(username="ivan")

        c = Client()

        c.login(
            username='ivan',
            password='ivan@123'
        )

        response = c.get("/doctors/doctor")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["patients_number"], 1)


    def test_doctor_appointments(self):
        """Test for doctor appointments"""

        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)
        appointment = Appointment.objects.get(doctor=patient.doctor)

        c = Client()

        c.login(
            username='ivan',
            password='ivan@123'
        )

        response = c.get("/doctors/appointments")
    
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, 'utf8'),
            {
                "appointments": [{"id": patient.id,
                "name": patient.__str__(),
                "date": appointment.date.strftime("%m/%d/%y")
             }]}
        )

    def test_display_patient(self):
        """Test for doctor display_patient() view function"""
        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)

        c = Client()

        c.login(
            username='ivan',
            password='ivan@123'
        )

        response = c.get(f"/doctors/patient/{patient.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["patient"].current_possibility, 
                        patient.current_possibility)


    def test_display_medications(self):
        """Test for the doctors display medications"""

        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)

        c = Client()
        c.login(
            username='ivan',
            password='ivan@123'
        )

        response = c.get(f"/doctors/medications?id={patient.id}")

        #since there are no medications yet, we should have one object for
        #displaying none.
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf8'), {
            'medications': [{'medication': 'None', 'date': date.today().strftime("%m/%d/%y")}]
            })

    def test_display_patients(self):
        """Test for the doctors patient view"""
        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)

        c = Client()
        c.login(
            username='ivan',
            password='ivan@123'
        )

        response = c.get(f"/doctors/patients")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf8'),
        {
            "patients": [{
                "id": patient.id,
                "name": patient.__str__(),
                "date": patient.last_visit.strftime("%m/%d/%y")
            }]
        }
        )

    def test_doctor_recovered(self):
        """Test for doctor's recovered() view function"""

        c = Client()
        c.login(
            username='ivan',
            password='ivan@123'
        )

        response = c.get("/doctors/recovered")

        #the returned json should be empy because we have no recovered patient
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf8'), {
            "recovered": []
        })

    #Test block for the patients application

    def test_patient_index(self):
        """Test for user's index view"""

        c = Client()
        c.login(
            username='salomon',
            password='salomon@123'
        )
        response = c.get("/patients/patients")

        self.assertEqual(response.status_code, 200)

    
    def test_get_user_checkup(self):
        """Test the user's checkup view with a 'GET' request"""
        
        c = Client()
        c.login(
            username='salomon',
            password='salomon@123'
        )

        response = c.get("/patients/checkup")

        #check if the view renders with non erros
        self.assertEqual(response.status_code, 200)

    
    def test_user_appointment(self):
        """Test for user appointment view"""

        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)

        c = Client()
        c.login(
            username='salomon',
            password='salomon@123'
        )
        response = c.get("/patients/appointment")

        #check if the current patient has an appointment
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["patient"], patient)

    def test_user_appointment_checkup(self):
        """
        -Test if the user checkup() view gives an appointment
        -A patient should not be in the Results class
        """

        user = User.objects.get(username="eric")

        c = Client()
        c.login(
            username='eric',
            password='eric@123'
        )

        response = c.post("/patients/checkup", {
            "1": 1, "2": 2, "3": 3, "4": 0, "5": 0,
            "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
            "11": 0, "12": 0, "13": 0, 
            "complication": "None"
        })

        patient = Patient.objects.get(user=user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["possibility"], 60.0)

        #test if appointment for user has been created
        #get the current user appointment first
        appointments = Appointment.objects.all()

        for appointment in appointments:
            if appointment.get_patient() == patient:
                current_appoint = appointment

         
        #check if the appointment objects match
        self.assertEqual(response.context["appointment"], current_appoint)

        #Check if patient is not in Result
        try:
            result = Result.objects.get(user=user)
        except Result.DoesNotExist:
            result = None

        self.assertEqual(result, None)

    def test_user_recovered_checkup(self):
        """- Test user checkup view when the user has recovered
        where the checkup data is kept in the results table
        """

        user = User.objects.get(username="salomon")

        c = Client()
        c.login(
            username='salomon',
            password='salomon@123'
        )    

        response = c.post("/patients/checkup", {
            "1": 0, "2": 0, "3": 3, "4": 0, "5": 0,
            "6": 0, "7": 7, "8": 8, "9": 0, "10": 0,
            "11": 0, "12": 0, "13": 0, 
            "complication": "None"
        })

        #check if the the patient is asymptomatic now
        self.assertTrue(response.context["healed"])

        #check that the user is now an object of the Result class
        try:
            result = Result.objects.get(user=user)
        except Result.DoesNotExist:
            result = None

        self.assertNotEqual(result, None)

    def test_user_degenerated_checkup(self):
       
        #Testing checkup view for a patient who got infected again
        

        user = User.objects.get(username="salomon")
        patient = Patient.objects.get(user=user)

        c = Client()
        c.login(
            username='salomon',
            password='salomon@123'
        )

        #first call view with non-concerning symptoms
        c.post("/patients/checkup",{
            "1": 0, "2": 0, "3": 3, "4": 0, "5": 0,
            "6": 0, "7": 7, "8": 8, "9": 0, "10": 0,
            "11": 0, "12": 0, "13": 0, 
            "complication": "None"
        })

        #Now give user concerning symptoms
        response = c.post("/patients/checkup", {
            "1": 1, "2": 2, "3": 3, "4": 0, "5": 0,
            "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
            "11": 0, "12": 0, "13": 0, 
            "complication": "None"
        })

        self.assertEqual(response.status_code, 200)

        #Check that user is deleted from the results table
        #and check if the patient is not asymptomatic 
        try:
            result = Result.objects.get(user=user)
        except Result.DoesNotExist:
            result = None

        self.assertEqual(result, None)
        self.assertFalse(patient.asymptomatic)

        #check from the view return if the patient was existing already
        self.assertTrue(response.context["existing"])