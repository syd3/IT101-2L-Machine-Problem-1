import os

def open_case(city):
    filename = f"{city}Case.txt"
    
    data = {}
    total_confirmed = 0
    with open(filename, 'r') as file:
        next(file)

        print(f"\nData for {city.title()}:\n")
        print('-' * 30)
        for line in file:
            barangay, confirmed, active, recovered, suspect, probable, deceased = line.strip().split(',')
            total_cases = int(active) + int(recovered) + int(deceased)
            data[barangay] = {
                'Confirmed': total_cases,
                'Active': int(active),
                'Recovered': int(recovered),
                'Suspect': int(suspect),
                'Probable': int(probable),
                'Deceased': int(deceased)
            }
            total_confirmed += total_cases

            print(f"Barangay: {barangay.title()}\nConfirmed: {total_cases}\nActive: {active}")
            print(f"Recovered: {recovered}\nSuspect: {suspect}\nProbable: {probable}")
            print(f"Deceased: {deceased}")
            print('-' * 30)

    print(f"\nTotal confirmed cases: {total_confirmed}\n")
    return data

def update_file(city, data):
    filename = f"{city}Case.txt"
    with open(filename, 'w') as file:
        file.write("Barangay,Confirmed,Active,Recovered,Suspect,Probable,Deceased\n")
        for barangay, cases in data.items():
            line = f"{barangay},{cases['Confirmed']},{cases['Active']},{cases['Recovered']},{cases['Suspect']},{cases['Probable']},{cases['Deceased']}\n"
            file.write(line)

def update_case(data, barangay, field, value, city):
    if barangay not in data:
        print("Barangay does not exist.\n")
        return
    if field not in data[barangay]:
        print("Invalid field.\n")
        return

    current_value = data[barangay][field]
    data[barangay][field] = value + current_value
    if field == 'Recovered' and not (value > data[barangay]['Active']):
        data[barangay]['Active'] -= value
    elif field == "Deceased" and not (value > data[barangay]['Active']):
        data[barangay]['Active'] -= value
    elif field not in ['Suspect', 'Probable'] and value > data[barangay]['Active']:
        print(f"{field} cases cannot exceed the active cases.\n")
        return

    update_file(city, data)
    print("Updated city case data.\n")

def add_barangay(data, barangay, city):
    if barangay in data:
        print("Barangay already exists.\n")
        return

    while True:
        try:
            active = int(input("Enter active cases: "))
            recovered = int(input("Enter recovered cases: "))
            suspect = int(input("Enter suspect cases: "))
            probable = int(input("Enter probable cases: "))
            deceased = int(input("Enter deceased cases: "))
            confirmed = active + recovered + deceased
            break
        except ValueError:
            print("Invalid input.\n")
    
    data[barangay] = {
        'Confirmed': confirmed,
        'Active': active,
        'Recovered': recovered,
        'Suspect': suspect,
        'Probable': probable,
        'Deceased': deceased
    }

    update_file(city, data)
    print("Updated city case data.\n")

def delete_barangay(data, barangay, city):
    if barangay not in data:
        print("Barangay does not exist.\n")
        return

    del data[barangay]

    update_file(city, data)
    print("Updated city case data.\n")

def create_case(city):
    filename = f"{city}Case.txt"
    if os.path.exists(filename):
        print("City already exists.\n")
        return

    data = {}
    has_data = False
    while True:
        barangay = input("Enter barangay (or 'exit' to finish): ").upper().strip()
        if barangay == 'EXIT':
            if has_data:
                break
            else:
                print("Please complete the field before exiting.\n")
                continue
        elif not barangay:
            print("Please enter a valid input.\n")
            continue
        elif barangay in data:
            print("Barangay already exists.\n")
            continue
        else:
            has_data = True

        while True:
            try:
                active = int(input("Enter active cases: "))
                recovered = int(input("Enter recovered cases: "))
                suspect = int(input("Enter suspect cases: "))
                probable = int(input("Enter probable cases: "))
                deceased = int(input("Enter deceased cases: "))
                confirmed = active + recovered + deceased
                break
            except ValueError:
                print("Invalid input.\n")
                continue

        data[barangay] = {
            'Confirmed': confirmed,
            'Active': active,
            'Recovered': recovered,
            'Suspect': suspect,
            'Probable': probable,
            'Deceased': deceased
        }

    update_file(city, data)
    print("City case data created successfully.\n")

def main():
    cityList = []
    path = os.path.dirname(os.path.realpath(__file__))
    while True:
        userInput = input("1 - Enter a city\n2 - Create a new case for a city\n> ")
        if userInput == "1":
            for f_name in os.listdir(path):
                if "Case" in f_name and f_name.endswith(".txt") and f_name not in cityList:
                    cityList.append(f_name)

            print("\nList of cities available:")
            for c in sorted(cityList):
                print(c.replace('Case.txt', '').title())

            city = input("\nEnter city: ").lower()
            if city not in [i.replace('Case.txt', '').lower() for i in cityList]:
                print("Invalid city. Please try again.\n")
                continue

            action = input("Choose action:\n1 - Open Case\n2 - Update Case\n3 - Add Barangay\n4 - Delete Barangay\n5 - Exit\n> ")
            if action == '5':
                break
            elif action == '1':
                open_case(city)
            elif action == '2':
                data = open_case(city)
                
                barangay = input("Enter barangay: ").upper()
                field = input("Enter field to update: ").title()
                if field == "Confirmed":
                    print("The confirmed field does not take any input.\n")
                    continue
                value = int(input("Enter value to be added: "))

                update_case(data, barangay, field, value, city)
            elif action == '3':
                data = open_case(city)

                while True:
                    barangay = input("Enter barangay to add: ").upper().strip()
                    if barangay:
                        confirm = input("Are you sure (Y/N)? ").lower()
                        if confirm == "n":
                            continue
                        elif confirm == "y":
                            add_barangay(data, barangay, city)
                            break
                        else:
                            print("Invalid input. Please enter only Y/N.\n")
                            continue
                    else:
                        print("Please enter a valid name.\n")
                        continue
            elif action == '4':
                data = open_case(city)
                
                while True:
                    barangay = input("Enter barangay to delete: ").upper().strip()
                    if barangay:
                        confirm = input("Are you sure (Y/N)? ").lower()
                        if confirm == "n":
                            continue
                        elif confirm == "y":
                            delete_barangay(data, barangay, city)
                            break
                        else:
                            print("Invalid input. Please enter only Y/N.\n")
                            continue
                    else:
                        print("Please enter a valid name.\n")
                        continue
            else:
                print("Invalid input. Please choose a valid option.\n")
        elif userInput == "2":
            city = input("\nEnter city: ").title()
            create = create_case(city)
            if not create:
                continue
        else:
            print("Invalid input. Please choose a valid option.")
            continue

if __name__ == '__main__':
    main()