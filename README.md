# Final Project

Web Programming with Python and Javascript

# Covid-H
    A coronavirus symptoms screening web prototype that could connect critical patients with doctors through automatic appointment and also provide updated covid-19 cases per country and worldwide to users. 

    .github:
        - Github actions that run the project testCase on push
    docker-compose.yml:
        - holds yml instructions for merging our web and database containers
    Dockerfile:
        - holds instructuions for setting up our web container
Note: 
    it is more convinient to run the application without docker. When using Docker it will require manaul setup of all symptoms and complications into the database.

# common app:
    Holds the landing page between the two applications and the the models that the whole applications depends on. Also, it includes the entire testCase for the whole application.


templates:
    - index.html: displays the landing page between the doctors and the patients application.

python files:
    - views.py: holds a view function that help direct the user to the patients or doctors app.
    - tests.py: Holds the entire testCase for the whole application


# patients app:
    Allows users to get wildwide and country specifica covid-19 cases and information using the postman API. Users can also take a symptom screening checkup to which the program decides how to proceed accordingly dendeing on the infection probability. Critical possibilities are offered emergency appointments at the nearest healthy center with a less occupied doctor

templates:
    - appointment.html: displays the user's current appointment
    - checkup.html: holds the form for user symptom screening
    - error.html: displays erros
    - index.html: provides user with covid-19 related informaition worldwide and country wide allowing user to navigate any country of choice
    - layout.html: holds the template for all pages
    - login.html: provides login fields to the user
    - register.html: provides fields for registering to the user
    - results.html: displays symptom screening results to the user depending on the infection possibility

python files:
    - functions.py: holds all helper functions that assit view functions of both patients and doctor app
    - views.py: holds all app views that allow the described processes to occur
    - urls.py: holds all url patterns that help in user navigation from pages to pages within the patients app.

static/patients files:
    - css/design.css: Holds the whole css needed to visually render the design and look of the user interface.
    - js/patient.js: Includes all javascript code that helps in the above specified functionality


# doctors app:
    Allows doctors to manage patients and patient related information. A doctor can add or remove symptoms/complications and edit patient information. The doctors dashboard provides him with the a group of appointments, still sick patients, and recovered patients where a doctor is able to navigate each profile.

templates:
    - index.html: includes the presentation and functionality of the doctor dashboard
    - patient.html: displays the selected patient's profile for the doctor to operate on.
    - layout.html: template for all of the html files.
    - login.html: provides login fields to the doctor.
    - register.html: provides register fields to the doctor.

pythong files:
    - views.py: holds all app view functions that assist in the above specified functionality of the doctors app
    - urls.py: holds all urls patterns for the doctors app

static/doctors files:
    - css/doctor.css: holds the whole css for the doctors application
    - js/doctor.js: holds the entire js code that helps to carry out the functionality of the doctors app


