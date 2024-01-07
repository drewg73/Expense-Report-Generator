from reportData import *
import csv

def main():
    CSV_DATA = []

    csv_input = input("Enter the relative path for the csv file: ")
    # Getting data from csv file
    with open(csv_input, newline='') as csv_file:
        reader = csv.reader(csv_file)
        # Skipping the header row 
        next(reader)

        for row in reader:
            CSV_DATA.append(row) 

    state = input("Enter State abbriviation: ")
    city = input ("Enter city name: ")

    total_charges = get_total_charges(CSV_DATA)
    duration = ((get_end_date(CSV_DATA) - get_start_date(CSV_DATA)).days + 1)
    total_perdiem = get_total_perdiem_for_trip(state, city, CSV_DATA)

    print(
        f"""
    ===============================
    REPORT
    ===============================
    TRIP DURATION: {duration} days
    TOTAL CHARGES: {format(total_charges, '.2f')}
    TOTAL PER DIEM: {format(total_perdiem, '.2f')}
    NET GAIN: {format((total_perdiem - total_charges), '.2f')}
    ===============================
    """
    )

main()