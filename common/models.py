from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date
# Create your models here.

##Add more information on these models
class User(AbstractUser):
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    is_doctor = models.BooleanField()
    gender = models.CharField(max_length=1, blank=True)

    def is_valid_user(self):
        return ((len(self.username) > 0) and (len(self.gender) > 0)
                and (len(self.email) > 0) and (self.date_of_birth 
                > date(1818, 1, 1)))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

        #You can also use hasattr to avoid the need for exception catching:
        #hasattr.(u, "doctor"), which returns "True" or "False"

class Hospital(models.Model):
    name = models.CharField(max_length=100) 
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"



class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="doctors")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

        

class Symptom(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    symptom_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Complication(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_appointments")
    date = models.DateField() 

    def get_patient(self):
        return self.appointment_patients.first()

    
    def __str__(self):
        return self.date.strftime("%m/%d/%y") 

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patients")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital_patients")#FIXME: redudant

    condition = models.CharField(max_length=10)
    symptoms = models.ManyToManyField(Symptom, blank=True)
    asymptomatic = models.BooleanField(default=False)
    complications = models.ManyToManyField(Complication, blank=True)
    appointments = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="appointment_patients", blank=True)
    initial_date = models.DateField()
    last_visit = models.DateField()

    #columns used to measure progress
    previous_possibility = models.FloatField()
    current_possibility = models.FloatField()
    progress = models.FloatField(default=0.0)

    #this function will return a measure of progress
    def update_symptoms(self, new_symptoms): 
        self.symptoms.clear()

        #add all new symptoms and re-calculate the new possiblity
        new_possibility = 0
        for symptom in new_symptoms:
            new_possibility += symptom.weight
            self.symptoms.add(symptom)

        #update possiblity and condition
        self.previous_possibility = self.current_possibility
        self.current_possibility = new_possibility

        #automatically update the condition 
        if new_possibility >= 80:
            self.condition = "Critical"
            self.asymptomatic = False
        elif new_possibility < 80 and new_possibility > 50:
            self.condition = "Mild"
            self.asymptomatic = False
        else:
            self.condition = "Asymptomatic"

        #now, update the last visit date
        self.last_visit = date.today()
        self.progress = self.current_possibility - self.previous_possibility
        self.save() 

        return self.progress

    def add_symptom(self, symptom): 

        #add symptom and update the current possibility
        self.symptoms.add(symptom)
        self.previous_possibility = self.current_possibility
        self.current_possibility += symptom.weight

        #update patient's progress
        self.progress = self.current_possibility - self.previous_possibility
        self.save()

        return self.progress

    def remove_symptom(self, symptom): 

        #search for a matching symptom and remove it
        self.symptoms.remove(symptom)

        #update current possibility
        self.previous_possibility = self.current_possibility
        self.current_possibility -= symptom.weight

        #updsate the patient's progress
        self.progress = self.current_possibility - self.previous_possibility
        self.save()

        return self.progress

    def is_valid_patient(self):
        return (self.current_possibility >= 50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medications")
    medication = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return f"{self.medication}"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    last_possibility = models.FloatField(default=0.0)
    new_possibility = models.FloatField()
    date = models.DateField()

    def update_result(self, new_possibility): 
        self.last_possibility = self.new_possibility
        #update the new possiblity and date
        self.new_possibility = new_possibility
        self.date = date.today()

        self.save() 

        return self.last_possibility - self.new_possibility
"""Adding migrations to apps Now, run python manage.py migrate --fake-initial , 
   and Django will detect that you have an initial migration and that the tables 
   it wants to create already exist, and will mark the migration as already applied.
"""