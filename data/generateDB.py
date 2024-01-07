import csv
import sqlite3

# Do not run this file unless you are updating the database.
# Will need to delete the exisitng entries first.

# Connecting to the database
db = sqlite3.connect('./data/PerDiemRates.db')
# Creating a cursor to allow traversal of the connected database
cur = db.cursor()
# Opens a csv file and inserts the values into a already initialized database
with open('./data/FY2024_PerDiemMasterRatesFile.csv', newline='') as csvFile:
    csvData = csv.reader(csvFile)
    # Skipping the header
    next(csvData)
    for row in csvData:
        entries = [row[1], row[2], row[4], row[5], row[7][1:]]
        cur.execute('''
                    INSERT INTO perdiem(state, destination, season_begin, season_end, rate)
                    VALUES("{0}", "{1}", "{2}", "{3}", {4})
                '''.format(*entries))
        db.commit()

db.close()