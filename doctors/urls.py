from django.urls import path
from . import views

urlpatterns = [
    path("doctor", views.index, name="doctors"),
    path("recovered", views.recovered, name="recovered"),
    path("patients", views.patients, name="doctor_patients"),
    path("appointments", views.appointments, name="doctor_appointments"), 
    path("medication", views.add_medication, name="medication"),
    path("edit_patient", views.edit_patient, name="edit_patient"),
    path("patient_appointments", views.patient_appointments, name="patient_appointments"), 
    path("medications", views.display_medications, name="medications"),
    path("login", views.doctor_login, name="doctor_login"),
    path("register", views.register, name="doctor_register"),
    path("logout", views.logout_doctor, name="doctor_logout"),
    path("remove", views.remove_symptom, name="remove_symptom"),
    path("patient/<int:patient_id>", views.display_patient, name="get_patient")
]