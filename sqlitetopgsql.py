# convert db.sqlite3 to csv

import sqlite3

conn = sqlite3.connect('db.sqlite3')

c = conn.cursor()

c.execute("SELECT medicine_name, medicine_description, medicine_image, medicine_price FROM vedassist_medicine")

medicine_details = []

already_added = ['Ahiphenasava', 'Amritarishta', 'Aragwadharishtam', 'Angoorasava', 'Abhayarishta']

row = c.fetchall()

for row in row:
    medicine_details.append(
        {
            "medicine_name": row[0],
            "medicine_description": row[1],
            "medicine_image": row[2],
            "medicine_price": row[3]
        }
    ) if row[0] not in already_added else None

print(medicine_details)

print(len(medicine_details))
        
conn.close()

# connect to postgresql db on vercel

import psycopg2
import os

DATABASE_URL = 'postgres://default:J7BIvaHgmd3l@ep-solitary-breeze-37314604-pooler.us-east-1.postgres.vercel-storage.com:5432/verceldb'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

c = conn.cursor()

c.execute("SELECT medicine_name, medicine_description, medicine_image, medicine_price FROM vedassist_medicine")

old_medicine_details = []

row = c.fetchall()

for row in row:
    old_medicine_details.append(
        {
            "medicine_name": row[0],
            "medicine_description": row[1],
            "medicine_image": row[2],
            "medicine_price": row[3]
        }
    )
    
print("\nOLD MEDICINE DETAILS: \n", old_medicine_details)


#insert medicine_details into postgresql db on vercel

for medicine in medicine_details:
    c.execute("INSERT INTO vedassist_medicine (medicine_name, medicine_description, medicine_image, medicine_price, medicine_view_count) VALUES (%s, %s, %s, %s, 0)", (medicine["medicine_name"], medicine["medicine_description"], medicine["medicine_image"], medicine["medicine_price"]))
    conn.commit()
    


c.execute("SELECT medicine_name, medicine_description, medicine_image, medicine_price FROM vedassist_medicine")

new_medicine_details = []

row = c.fetchall()

for row in row:
    new_medicine_details.append(
        {
            "medicine_name": row[0],
            "medicine_description": row[1],
            "medicine_image": row[2],
            "medicine_price": row[3]
        }
    )
    
print("\nNEW MEDICINE DETAILS: \n", new_medicine_details)


conn.close()
        