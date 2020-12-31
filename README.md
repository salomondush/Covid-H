# Web Programming with Python and Javascript: Final project

# Covid-H
In times of the novel Coronavirus pandemic, we have seen the introduction of different technological tools to help restrict the spread of the virus, to simplify the job of healthcare workers, and educate the public about safety measures. Fortunately, with the vaccine being fully developed and in action, we are at a steep advantage of mitigating the disease before it takes more lives. Now more than ever, we need an efficient way of identifying infected people and connect them to nearby hospitals minimizing further spread of the disease. So, Covid-H is a coronavirus symptoms screening web prototype that could connect critical patients with doctors through automatic appointment and also provide updated covid-19 cases per country and worldwide to users by enforcing a daily check-up system. In addition to that, users can learn more about how the virus spreads and healthy prevention measures. To simplify the work of healthcare workers, doctors are able to manage patients through medication recommendations, organising patients in groups of recovered and non-recovered (still sick), viewing and managing appointments, and adding/removing symptoms/complications. In this way, we can make certain a timely response to new cases that might put people at risk and wear out health care workers. Therefore, in this way, we can ensure that the vaccine is administered with no further loss of people's lives.

The project runs on the Django python web framwork, javascript on the frontend, and a Sqlite3 default database. It also utilises Postman covid API to incorporate updated covid-19 information worldwide. Also, all web-pages are mobile responsive.

## installation
- Install required python packages inorder to run this web application by running ```pip3 install -r requirements.txt```
- Run the below commands in order to make and apply migrations ```python3 manage.py makemigrations``` and 
```python3 manage.py migrate```
- Run the project using ```python3 manage.py runserver``` and navigate to the doctor's app to register a user, or patient's directory to register a patient 

# Files and directories

## common - main directory
Holds the landing page between the patient and doctor applications and the the models including classes that the whole applications 
runs on. Also, it includes the entire testCase for the whole application.


* templates/common - subdirectory
    - index.html: displays the landing page between the doctors and the patients application.

static files:

* static/patients - subdirectory

    - css - subdirectory
        - common.css: Holds the whole css needed to visually render the design and look of the landing page interface.

    - img - subdirectory
        - c.jpg: image which can be taken as the logo for the Covid-H application

- views.py: holds a view function that help direct the user to the patients or doctors app.

- tests.py: Contains the entire testCase for the whole application including a database class validity test block that tests for valid patient, valid user, and invalid users. A doctor views testing block testing the doctor's index, doctors_appointments, display_patient, display_medication, display_patients, recovered views. A patients views test block testing patitn's index, checkup, and appointment view functions.

- urls.py: contains urls specific to the common app directory.

- complications.csv: Contains all complications, their name and weight.
- symptoms.csv: Contains all symptoms, their names, weight, and commonality.



## patients - Main application directory
Allows users to get wildwide and country specifica covid-19 cases and information using the postman API.
Users can also take a symptom screening checkup to which the program decides how to proceed accordingly
dendeing on the infection probability. Critical possibilities are offered emergency appointments at the
nearest healthy center with a less occupied doctor

* templates/patients - subdirectory
    - appointment.html: displays the user's current appointment.
    - checkup.html: holds the form for user symptom screening.
    - error.html: displays errors.
    - index.html: provides user with covid-19 related informaition worldwide and country wide allowing
    user to navigate any country of choice
    - layout.html: holds the template for all pages
    - login.html: provides login fields to the user
    - register.html: provides fields for registering to the user
    - results.html: displays symptom screening results to the user depending on the infection possibility

* static/patients - subdirectory

    - css - subdirectory
        - design.css: Holds the whole css needed to visually render the design and look of the user interface.

    - js - subdirectory
        - patient.js: Contains javascript code the helps a user to make coronavirus information queries to the API, edit, and update user information.

    - img - subdirectory
        - u.png: dummy image representing user.

- functions.py: holds all helper functions that assist view functions of both patients and doctor app including cases, get_doctor, get_patients_list, get_appointments_list, get_weight, age_calculation, arrange_symptoms, edit_user_information, retrieve_patient_info, get_appointment_date, and get_appointments functions. 

- views.py: holds all view functions like patient_login, register, logout_view, index, country_cases, checkup, appointment, and update_user_information that help a patient check cases world wide, take checkups, view self appointments, add complications, and edit self information.

- urls.py: holds all url patterns that help in user navigation from pages to pages within the patients app.

## doctors - Main application directory
Allows doctors to manage patients and patient related information. A doctor can add or remove
symptoms/complications and edit patient information. The doctors dashboard provides him with the a group of
appointments, still sick patients, and recovered patients where a doctor is able to navigate each profile.

* templates/doctors - subdirectory
    - index.html: includes the presentation and functionality of the doctor dashboard
    - patient.html: displays the selected patient's profile for the doctor to operate on.
    - layout.html: template for all of the html files.
    - login.html: provides login fields to the doctor.
    - register.html: provides register fields to the doctor.

* static/doctors - subdirectory
    - css - subdirecotry
        - doctor.css: holds the whole css 
        that dictates the disign of all doctor's html pages.

    - js - subdirectory
        - doctor.js: holds the entire js code that helps to carry out the functionality of the doctors app including viewing patient's previous appointments, displaying medication, editing user and doctor information, getting appointments, patients list, recovered list, removing a symptom, and adding medications.

    - img - subdirectory
        - u.png: Contains the image dummy representing both any user.

* views.py: holds all app view functions like doctor_login that allows login, register for new doctor entry, logout, index that loads the doctor's dashboard, appointments that returns the number of doctor appointments, display_patient that loads the patient.html file containing all patient related information and also allows doctor to add symptom or complication, remove_symptom that removes patient's symptom, patient_appointments that retrieves all patient past appointments, display_medication that shows history of medications, add_medication that adds medications to a patients profile, edit_patient that updates patient's information, patients that retrievies all current patients, and recovered that retrieves all recovered patients. All of which allows a doctor to manage patients Efficiently.

* urls.py: A collection of all urls to different views within the doctor's app

## db.dqlite3
Default database for the application containing all tables and related data.

## .github - main
Github actions that run the project testCase on push to this repository

## docker-compose.yml - main
Holds yml insturctions for mergin our web and database containers 

## Dockerfile - main
Holds instructions for setting up our web container. 

### Note: It is more convinient to run the application without docker. When using Docker, it will require a manual setup of all symptoms and complications into the postgres database.
