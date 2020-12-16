document.addEventListener("DOMContentLoaded", () => {

    /**
     * template accessing methods
     */
    //const function to display a selected group between all patients or recovered ones.
    const patients_template = Handlebars.compile(document.querySelector("#selected-patient-list").innerHTML);
    const display_patients = data => {
        const patient_list = patients_template({"patients": data});
        document.querySelector("#selected-list").innerHTML = patient_list;
    }

    //uses template to display prevous appointments
    const display_previous_appointments = data => {
        var appointment_list = patients_template({"patients": data});
        document.querySelector("#add-complication-see-appointments").innerHTML = appointment_list;
    }

    //displayes template for doctor to add medications
    const medications_template = Handlebars.compile(document.querySelector("#medication-template").innerHTML);
    const display_medications_chart = data => {
        console.log(data["medications"]);
        var medication_div = medications_template({"medications": data["medications"]});
        document.querySelector("#information-medications").innerHTML = medication_div;
    }

    //patient information update form
    const update_form = Handlebars.compile(document.querySelector("#person-edit-template").innerHTML);
    const display_update_form = data => {
        
        //send information to template and updated the div
        var update_form_div = update_form(data);
        document.querySelector("#updatable-info").innerHTML = update_form_div;
    }

    //patient updated information template
    const updated_information = Handlebars.compile(
        document.querySelector("#updated-patient-information-template").innerHTML);
    const display_updated_information = data => {

        //send infomation to template and update the div
        var updated_info_div = updated_information(data);
        document.querySelector("#updatable-info").innerHTML = updated_info_div;
    }

    /**
     * Set of functions
     */

    //function to get patients and dispaly them.
    function get_patients(){

        fetch(`/doctors/patients`)
        .then(response => response.json())
        .then(data => {
            
            console.log(data); //FIXME:
            //update header and call function to display current patients
            document.querySelector("#selected").innerHTML = "Current Patients List";
            display_patients(data);
        })
        .catch(error => {
            console.log("Error", error);
        });
    }

    //function to get recovered patients and display them (the template is same as for patients)
    function get_recovered() {

        fetch(`/doctors/recovered`)
        .then(response => response.json())
        .then(data => {

            console.log(data); //FIXME:
            //update header and call function to display recovered patients
            document.querySelector("#selected").innerHTML = "Recovered List";
            display_patients(data);
        })
        .catch(error => {
            console.log("Error", error);
        });
    }

    //function to get all doctor appointments and display them.
    function get_appointments() {

        fetch(`/doctors/appointments`)
        .then(response => response.json()) 
        .then(data => {

            console.log(data); //FIXME:
            //update header and call function to display appointments
            document.querySelector("#selected").innerHTML = "Appointments List";
            display_patients(data);
        })
        .catch(error => {
            console.log("Error", error)
        });
    }

    //function to get specific previous appointments to the user
    function previous_appointments(id){
        console.log(id);
        fetch(`/doctors/patient_appointments?id=${id}`)
        .then(response => response.json())
        .then(data => {
            display_previous_appointments(data);
        })
        .catch(error => {
            console.log("Error", error)
        });
    }

    //function get's list of medications from the server
    function get_medications(id){

        fetch(`/doctors/medications?id=${id}`)
        .then(response => response.json())
        .then(data => {
            display_medications_chart(data);
        })
        .catch(error => {
            console.log("Error", error);
        });
    }

    //function to add medication
    function add_medication(id, medication){

        fetch(`/doctors/medication?id=${id}&medication=${medication}`)
        .then(response => response.json())
        .then(data => {

            //create span to store date
            const span = document.createElement("span");
            span.className = "text-muted float-right";
            span.innerHTML = data.date;

            //create list item and add medication with span representing date
            const list = document.createElement('li');
            list.className = "list-group-item";
            list.innerHTML = data.medication;
            list.append(span);

            document.querySelector("#medications-set").append(list);
        })
        .catch(error => {
            console.log("Error", error);
        })
    }

    //functiont to update patient information
    function update_patient_information(id, email, phone, gender){
        
        //make a call to the server for infomation to be updated
        fetch(`/doctors/edit_patient?id=${id}&email=${email}&phone=${phone}&gender=${gender}`)
        .then(response => response.json())
        .then(data => {
            
            //call another function to use template to update patient information
            display_updated_information(data);
        })
    }

    //function to remove a particular symptom 
    function remove_symptom(patient_id, symptom, li){ 

        fetch(`/doctors/remove?symptom=${symptom}&id=${patient_id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {

                //remove the symptom item from list
                li.parentElement.removeChild(li);
            }
        })
        .catch(error => {
            console.log("Error", error)
        })
    }

    /**
     * Set of click events 
     */

    //configure all click areas
    document.addEventListener("click", (event) => {
    
        if (event.target.id == "see-previous-appointments"){//see previous appointments

            //get patient id and call function to display previous appointmnts
            var id = document.getElementById("see-previous-appointments").getAttribute("data-value")
            previous_appointments(id)
            
        } else if (event.target.id == "display-medications"){//display medications

            //get patient id and call function to display the medication div
            var id = document.getElementById("display-medications").getAttribute("data-value")
            get_medications(id)

        }  else if (event.target.id == "edit-patient-information"){//edit some patient information
            
            //get current patient information
            var email = document.getElementById("patient-email").innerText;
            var phone = parseInt(document.getElementById("patient-phone").innerText);
            var gender = document.getElementById("patient-gender").innerText;
           
            //call function to display the patient information update form
            display_update_form({"email": email, "phone": phone, "gender": gender});

        } else if (event.target.id == "appointments-list"){ //see appointments
            get_appointments();
        } else if (event.target.id == "patients-list"){//see current patients
            get_patients();
        } else if (event.target.id == "recovered-list"){//see recovered patients
            get_recovered();
        } else if (event.target.classList.contains("remove")){

            //get the parent element and get the inner text
            let parent = event.target.parentElement;
            let symptom = parent.innerText.slice(0, parent.innerText.lastIndexOf("."));

            //get current patient id
            let patient_id = parseInt(document.querySelector("#patient-id").innerText);

            //call method to remove symptom
            remove_symptom(patient_id, symptom, parent);
        }
    });

    /**
     * Set of form submissions
     */
    //configure all patient page form submission
    document.addEventListener("submit", (event) => {
        const form = event.target;

        if (form.id == "add-medication-form"){
            event.preventDefault();

            //get medication and patient id
            var medication = document.querySelector("#medication-text").value;
            var id = document.getElementById("display-medications").getAttribute("data-value")

            //call function to add medication
            add_medication(id, medication);
        } else if (form.id == "update-patient-info"){
            event.preventDefault();

            //get new patient info and current patient id
            var email = document.querySelector("#email").value;
            var phone = document.querySelector("#phone").value;
            var gender = document.querySelector("#gender").value;
            var patient_id = parseInt(document.querySelector("#patient-id").innerText);

            //call function that calls the server to update patient information
            update_patient_information(patient_id, email, phone, gender);
        }
    });  
});