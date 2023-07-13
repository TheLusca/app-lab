import csv 
import peewee
from db.models import *

db = peewee.SqliteDatabase('database.db')


with open('data/GH010189.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        
        coluna1 = row[0]
        coluna2 = row[1]
        coluna3 = row[2]
        coluna4 = row[3]
        coluna5 = row[4]

        results = Results(
            name=str(row[0]),
            km=float(row[1]),
            distance=float(row[2]),
            highway=int(row[3]),
            item=str(row[4])
        )
        
        results.save()
        

print('Import realizado com sucesso')
db.close()





