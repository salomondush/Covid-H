from django.urls import path

from . import views

urlpatterns = [
    path("patients", views.index, name="patients"),
    path("login", views.patient_login, name="user_login"),
    path("register", views.register, name="user_register"),
    path("checkup", views.checkup, name="checkup"),
    path("country", views.country_cases, name="country_cases"),
    path("appointment", views.appointment, name="user_appointment"),
    path("update_information", views.update_user_information, name="edit_user"),
    path("logout", views.logout_view, name="user_logout"),
]