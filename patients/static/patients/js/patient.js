document.addEventListener('DOMContentLoaded', () => {


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

            //make a fetch to the server
           /* fetch(`/country_cases?country_name=${country}`)
            .then(response => response.json())
            .then(data => {
                //update country name
                document.querySelector("#country-name").innerHTML = data.Country;

                //total and new cases
                document.querySelector("#total-cases").innerHTML = data.TotalConfirmed;
                document.querySelector("#new-cases").innerHTML = data.NewConfirmed;
                //total recovered and new recovered
                document.querySelector("#total-recovered").innerHTML = data.TotalRecovered;
                document.querySelector("#new-recovered").innerHTML = data.NewRecovered;
                //total deaths and new deaths
                document.querySelector("#total-deaths").innerHTML = data.TotalDeaths;
                document.querySelector("#new-deaths").innerHTML = data.NewDeaths;
            })
            .catch(error => {
                console.log("Error", error)
            });*/
        }     
    });
});