document.addEventListener('DOMContentLoaded', () => { 

    /**
     * Block dealing with the postmain api
     */

    //reset checkup form when the clear button is pressed
    document.addEventListener('click', (e) => {
        if (e.target.id == "clear-form"){
            document.querySelector("#checkup-form").reset();
        }
    })
    
    document.addEventListener("submit", (e) => {
        if (e.target.id === "country-cases-form") {
            e.preventDefault()
            const country = document.querySelector("#country-name").value; 


            fetch("https://api.covid19api.com/summary")
            .then(response => response.json())
            .then(data => {
                var countries_info = data["Countries"]
                countries_info.forEach(element => {
                    if (element["Country"] == country.trim()) {
                        const data = element;

                        //update country name
                        document.querySelector("#selected-country-name").innerHTML = data.Country;
                        console.log(data.country);

                        //total and new cases
                        document.querySelector("#total-cases").innerHTML = data.TotalConfirmed;
                        document.querySelector("#new-cases").innerHTML = "+" + data.NewConfirmed;
                        //total recovered and new recovered
                        document.querySelector("#total-recovered").innerHTML = data.TotalRecovered;
                        document.querySelector("#new-recovered").innerHTML = "+" + data.NewRecovered;
                        //total deaths and new deaths
                        document.querySelector("#total-deaths").innerHTML = data.TotalDeaths;
                        document.querySelector("#new-deaths").innerHTML = "+" + data.NewDeaths;
                    }
                });
            })
            .catch(error => {
                console.log("Error", error);
            })
        }     
    });

    //patient information update form
    const update_form = Handlebars.compile(document.querySelector("#user-edit-template").innerHTML);
    const get_update_form = data => {
        
        //send information to template and updated the div
        var update_form_div = update_form(data);
        document.querySelector("#updatable-info").innerHTML = update_form_div;
    }

    //patient updated information template
    const updated_information = Handlebars.compile(
        document.querySelector("#updated-user-information-template").innerHTML);
    const display_updated_information = data => {

        //send infomation to template and update the div
        var updated_info_div = updated_information(data);
        document.querySelector("#updatable-info").innerHTML = updated_info_div;
    }

    //functiont to update patient information
    function update_user_information(id, email, phone, gender){
        
        //make a call to the server for infomation to be updated
        fetch(`/patients/update_information?id=${id}&email=${email}&phone=${phone}&gender=${gender}`)
        .then(response => response.json())
        .then(data => {
            
            //call another function to use template to update patient information
            display_updated_information(data);
        })
    }

    /**
     * Set of click events 
     */
    document.addEventListener('click', (event) => {

        if (event.target.id == "edit-user-information"){

            //get current patient information
            var email = document.getElementById("user-email").innerText;
            var phone = parseInt(document.getElementById("user-phone").innerText);
            var gender = document.getElementById("user-gender").innerText;

            //call function to display the patient information update form
            get_update_form({"email": email, "phone": phone, "gender": gender});
        }

    });

    /**
     * Set of form submissions 
     */
    document.addEventListener("submit", (event) =>{
        const form = event.target;

        if (form.id == "update-user-info"){
            event.preventDefault()

            //get new patient info and current patient id
            var email = document.querySelector("#email").value;
            var phone = document.querySelector("#phone").value;
            var gender = document.querySelector("#gender").value;
            var id = parseInt(document.querySelector("#patient-id").innerText);
            
            //call function that calls the server to update patient information
            update_user_information(id, email, phone, gender);
        }
    })
});