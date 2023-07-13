from peewee import *
from db.models import *

db = peewee.SqliteDatabase('db/database.db')
db.connect()


query = """
CREATE VIEW resultados_view AS
SELECT highway, km, item, COUNT(*) AS count
FROM Results
GROUP BY highway, km, item
"""

db.execute_sql(query)
db.close()


query = (Results
         .select(Results.highway,
                 fn.MIN(Results.km).alias('km_ini'),
                 fn.MAX(Results.km).alias('km_final'))
         .group_by(Results.highway))


with db.atomic():
    for row in query:
        Rodovias.create(highway=row.highway, km_ini=row.km_ini, km_final=row.km_final)

print("Tabela 'rodovias' criada e valores de km inicial e final inseridos com sucesso!")

db.close()

query = (Results
         .select(Results.name, fn.MIN(Results.km).alias('km_ini'), fn.MAX(Results.km).alias('km_final'))
         .group_by(Results.name))


with db.atomic():
    for row in query:
        Videos.create(name=row.name, km_ini=row.km_ini, km_final=row.km_final)


db.close()

print("Tabela 'Videos' criada e valores de km_ini e km_final inseridos com sucesso!")



