import sqlite3
from dateutil.parser import parse
import pandas as pd

# Gets the total ammount of credit card charges (does not include payments)
def get_total_charges(csv_data):
    total = 0
    for row in csv_data:
        transaction = float(row[2])
        if transaction > 0:
            total += transaction
    return round(total, 2)

# Gets the start date for the report as last date in the csv data
def get_start_date(csv_data):
    return parse(csv_data[len(csv_data)-1][0])

# Gets the end date for the report as the first date in the csv data.
def get_end_date(csv_data):
    return parse(csv_data[0][0])

def get_perdiem(state, city):
    perdiem = 0
    perdiem_rates = {}
    # Connecting to the database
    db = sqlite3.connect('./data/PerDiemRates.db')
    # Creating a cursor to allow traversal of the connected database
    cur = db.cursor()
    # Determining per diem rate based on location
    find_location_query = f"SELECT * FROM perdiem WHERE state='{state}' AND destination = '{city}'"
    cur.execute(find_location_query)
    rows = cur.fetchall()
    # If the location is not in the database, then default to the base rate
    if len(rows) == 0:
        perdiem = 59.00
        db.close()
        return perdiem
    # If there is not date range tied to the per diem, set perdiem to the value in the database
    # If there are date ranges, add those ranges and their associated per diem rates to the perdiem_rates dictionary
    if len(rows) == 1:
        perdiem = float(rows[0][5])
        db.close()
        return perdiem
    else:
        for row in rows:
            perdiem_rates[parse(row[3]), parse(row[4])] = float(row[5])
        db.close()
        return perdiem_rates

# Get the total per diem earned for the duration of the trip
def get_total_perdiem_for_trip(state, city, csv_data):
    if type(get_perdiem(state, city)) is float:
        end_date = get_end_date(csv_data)
        start_date = get_start_date(csv_data)
        duration = ((end_date - start_date).days + 1)
        perdiem = get_perdiem(state, city)
        return duration * perdiem
    elif type(get_perdiem(state, city)) is dict:
        date_range = pd.date_range(get_start_date(csv_data), get_end_date(csv_data))
        total_perdiem = 0
        perdiem_rates = get_perdiem(state, city)
        for key in perdiem_rates.keys():
            for date in date_range:
                if date >= key[0] and date <= key[1]:
                    total_perdiem += perdiem_rates[key]
                else:
                    total_perdiem += (59.00 / len(perdiem_rates)) 
        return round(total_perdiem, 2)
    