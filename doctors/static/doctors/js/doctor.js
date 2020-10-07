document.addEventListener("DOMContentLoaded", () => {

    //const function to display a selected group between all patients or recovered ones.
    const patients_template = Handlebars.compile(document.querySelector("#selected-patient-list").innerHTML);
    const display_patients = data => {
        const patient_list = patients_template({"patients": data});
        document.querySelector("#selected-list").innerHTML = patient_list;
    }

    //function to get patients and dispaly them.
    function get_patients() {

        fetch(`/doctor_patients`)
        .then(response => response.json())
        .then(data => {
            display_patients(data);
        })
        .catch(error => {
            console.log("Error", error);
        });
    }

    //function to get recovered patients and display them (the template is same as for patients)
    function get_recovered() {

        fetch(`/recovered`)
        .then(response => response.json())
        .then(data => {
            display_patients(data);
        })
        .catch(error => {
            console.log("Error", error);
        });
    }

    //function to get all doctor appointments and display them.
    const appointments_template = Handlebars.compile(document.querySelector("#selected-appointment-list").innerHTML);
    function get_appointments() {

        fetch(`/doctor_appointments`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const appointment_list = appointments_template({"appointements": data});
            document.querySelector("#selected-list").innerHTML = appointment_list;
        })
        .catch(error => {
            console.log("Error", error)
        });
    }

    //configure all click areas to display groups
    document.querySelector("#appointments-list").onclick = () => {
        get_appointments();
    }

    document.querySelector("#patients-list").onclick = () => {
        get_patients();
    }

    document.querySelector("#recovered-list").onclick = () => {
        get_recovered();
    }
    

    
});