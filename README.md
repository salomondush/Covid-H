# Final Project

Web Programming with Python and Javascript

# Covid-H
    A coronavirus symptoms screening web prototype that could connect critical 
    patients with doctors through automatic appointment and also provide updated 
    covid-19 cases per country and worldwide to users. 

    .github:
        - Github actions that run the project testCase on push
    docker-compose.yml:
        - holds yml instructions for merging our web and database containers
    Dockerfile:
        - holds instructuions for setting up our web container
Note: 
    it is more convinient to run the application without docker. When using Docker
    it will require manaul setup of all symptoms and complications into the database.

# common app:
    Holds the landing page between the two applications and the the models that
    the whole applications depends on. Also, it includes the entire testCase 
    for the whole application.



# patients app:
    Allows users to get wildwide and country specifica covid-19 cases and information
    using the postman API. Users can also take a symptom screening checkup to which 
    the program decides how to proceed accordingly dendeing on the infection probability.
    Critical possibilities are offered emergency appointments at the nearest healthy center 
    with a less occupied doctor

# doctors app:
    Allows doctors to manage patients and patient related information. A doctor can add
    or remove symptoms/complications and edit patient information. The doctors dashboard
    provides him with the a group of appointments, still sick patients, and recovered 
    patients where a doctor is able to navigate each profile.

