import os

def open_case(city):
    filename = f"{city}Case.txt"
    if not os.path.exists(filename):
        print("City does not exist.")
        return {}

    data = {}
    total_confirmed = 0
    with open(filename, 'r') as file:
        next(file)
        print(f"\nData for {city.title()}:\n")
        print('-' * 30)
        for line in file:
            barangay, confirmed, active, recovered, suspect, probable, deceased = line.strip().split(',')
            data[barangay] = {
                'Confirmed': int(confirmed),
                'Active': int(active),
                'Recovered': int(recovered),
                'Suspect': int(suspect),
                'Probable': int(probable),
                'Deceased': int(deceased)
            }

            total_confirmed += int(confirmed)

            print(f"Barangay: {barangay.title()}")
            print(f"Confirmed: {confirmed}")
            print(f"Active: {active}")
            print(f"Recovered: {recovered}")
            print(f"Suspect: {suspect}")
            print(f"Probable: {probable}")
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
    # if field == 'Recovered' and value > current_value:
    #     print("Recovered cases cannot exceed the current value.\n")
    #     return

    data[barangay][field] = value
    if field == 'Recovered':
        data[barangay]['Active'] -= (value - current_value)

    update_file(city, data)
    print("Updated city case data.\n")

def add_barangay(data, barangay, city):
    if barangay in data:
        print("Barangay already exists.\n")
        return

    data[barangay] = {
        'Confirmed': 0,
        'Active': 0,
        'Recovered': 0,
        'Suspect': 0,
        'Probable': 0,
        'Deceased': 0
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
    while True:
        barangay = input("Enter barangay (or 'exit' to finish): ")
        if barangay == 'exit':
            break

        if barangay in data:
            print("Barangay already exists.\n")
            continue

        confirmed = int(input("Enter confirmed cases: "))
        active = int(input("Enter active cases: "))
        recovered = int(input("Enter recovered cases: "))
        suspect = int(input("Enter suspect cases: "))
        probable = int(input("Enter probable cases: "))
        deceased = int(input("Enter deceased cases: "))

        data[barangay] = {
            'Confirmed': confirmed,
            'Active': active,
            'Recovered': recovered,
            'Suspect': suspect,
            'Probable': probable,
            'Deceased': deceased
        }

    with open(filename, 'w') as file:
        file.write("Barangay,Confirmed,Active,Recovered,Suspect,Probable,Deceased\n")
        for barangay, cases in data.items():
            line = f"{barangay},{cases['Confirmed']},{cases['Active']},{cases['Recovered']},{cases['Suspect']},{cases['Probable']},{cases['Deceased']}\n"
            file.write(line)

    print("City case data created successfully.\n")

def main():
    while True:
        userInput = input("1 - Enter a city\n2 - Create a new case for a city\n> ")
        if userInput == "1":
            city = input("Enter city (Cabuyao or StaRosa): ").lower()
            if city not in ['cabuyao', 'starosa']:
                print("Invalid city. Please try again.\n")
                continue
        elif userInput == "2":
            pass

        action = input("Choose action (open, update, add, delete, create, exit): ").lower()

        if action == 'exit':
            break

        if action == 'open':
            open_case(city)
        elif action == 'update':
            data = open_case(city)
            if not data:
                continue

            barangay = input("Enter barangay: ").upper()
            field = input("Enter field to update: ").title()
            value = int(input("Enter new value: "))

            update_case(data, barangay, field, value, city)
        elif action == 'add':
            data = open_case(city)
            if not data:
                continue

            barangay = input("Enter barangay to add: ").upper()
            add_barangay(data, barangay, city)
        elif action == 'delete':
            data = open_case(city)
            if not data:
                continue

            barangay = input("Enter barangay to delete: ").upper()
            delete_barangay(data, barangay, city)
        elif action == 'create':
            create_case(city)
        else:
            print("Invalid action. Please try again.\n")

if __name__ == '__main__':
    main()