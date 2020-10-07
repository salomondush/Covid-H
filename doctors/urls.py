from django.urls import path
from . import views

urlpatterns = [
    path("doctor", views.index, name="doctors"),
    path("patient", views.patient, name="doctor_patient"),
    path("recovered", views.recovered, name="recovered"),
    path("patients", views.patients, name="doctor_patients"),
    path("appointments", views.appointments, name="doctor_appointments"), 
    path("login", views.doctor_login, name="doctor_login"),
    path("register", views.register, name="doctor_register"),
    path("logout", views.logout, name="doctor_logout")
]