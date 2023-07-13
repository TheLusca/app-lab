import csv
from peewee import *
from playhouse.sqlite_ext import *
from db.models import *


db = peewee.SqliteDatabase('db/database.db')
db.connect()


sql_create_table = '''
CREATE TABLE IF NOT EXISTS DerivedTable (
    highway INTEGER,
    km REAL,
    buraco INTEGER DEFAULT 0,
    remendo INTEGER DEFAULT 0,
    trinca INTEGER DEFAULT 0,
    placa INTEGER DEFAULT 0,
    drenagem INTEGER DEFAULT 0
)
'''
db.execute_sql(sql_create_table)

sql_insert_data = '''
INSERT INTO DerivedTable (highway, km, buraco, remendo, trinca, placa, drenagem)
SELECT highway, km,
       SUM(CASE WHEN item = 'buraco' THEN 1 ELSE 0 END) AS buraco,
       SUM(CASE WHEN item = 'remendo' THEN 1 ELSE 0 END) AS remendo,
       SUM(CASE WHEN item = 'trinca' THEN 1 ELSE 0 END) AS trinca,
       SUM(CASE WHEN item = 'placa' THEN 1 ELSE 0 END) AS placa,
       SUM(CASE WHEN item = 'drenagem' THEN 1 ELSE 0 END) AS drenagem
FROM Results
GROUP BY highway, km
'''
db.execute_sql(sql_insert_data)

print("Tabela 'DerivedTable' criada e dados inseridos com sucesso!")



registros = Results.select()


dados_derivados = {}


for registro in registros:
    highway = registro.highway
    km = registro.km
    item = registro.item.lower()  

    if (highway, km) not in dados_derivados:
        dados_derivados[(highway, km)] = {'buraco': 0, 'remendo': 0, 'trinca': 0, 'placa': 0, 'drenagem': 0}

    dados_derivados[(highway, km)][item] += 1


with db.atomic():
    for (highway, km), item_counts in dados_derivados.items():
        DerivedTable.update(
            buraco=DerivedTable.buraco + item_counts['buraco'] + 1,
            remendo=DerivedTable.remendo + item_counts['remendo'] + 1,
            trinca=DerivedTable.trinca + item_counts['trinca'] + 1,
            placa=DerivedTable.placa + item_counts['placa'] + 1,
            drenagem=DerivedTable.drenagem + item_counts['drenagem'] + 1
        ).where((DerivedTable.highway == highway) & (DerivedTable.km == km)).execute()


registros_atualizados = DerivedTable.select()
for registro in registros_atualizados:
    print(f"highway: {registro.highway}, km: {registro.km}, buraco: {registro.buraco}, remendo: {registro.remendo}, trinca: {registro.trinca}, placa: {registro.placa}, drenagem: {registro.drenagem}")

print("Valores incrementados na tabela 'DerivedTable' com sucesso!")


arquivo_csv = f'output/{registro.highway}_output_table.csv'

registros = DerivedTable.select()

with open(arquivo_csv, mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['highway', 'km', 'buraco', 'remendo', 'trinca', 'placa', 'drenagem'])

    for registro in registros:
        writer.writerow([registro.highway, registro.km, registro.buraco, registro.remendo, registro.trinca, registro.placa, registro.drenagem])

print("Tabela 'DerivedTable' exportada para o arquivo 'derived_table.csv' com sucesso!")

