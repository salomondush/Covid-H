import csv
from .models import Symptom, Complication

def main():
    #open the symptoms file and import it's data into the database
    symptoms = open("symptoms.csv", "r")
    reader = csv.reader(symptoms)

    for symptom, weight, symptom_type in reader:
        Symptom.objects.create(name=symptom, weight=float(weight), symptom_type=symptom_type)

    #open the complications file and import it's data into the database
    complications = open("complications.csv", "r")
    reader = csv.reader(complications)

    for complication_name in complications:
        Complication.objects.create(name=complication_name)


if __name__ == "__main__":
    main()
