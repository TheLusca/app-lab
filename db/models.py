import peewee
from peewee import *

db = peewee.SqliteDatabase('db/database.db')


class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        database = db

class Results(BaseModel):
        id = IntegerField(primary_key=True)
        name = CharField()
        km = FloatField()
        distance = FloatField()
        highway = IntegerField()
        item = CharField()

class Rodovias(BaseModel):
    id = IntegerField(primary_key=True)
    highway = IntegerField()
    km_ini = FloatField()
    km_final = FloatField()

class DerivedTable(BaseModel):
    id = IntegerField(primary_key=True)
    highway = IntegerField()
    km = FloatField()
    buraco = IntegerField()
    remendo = IntegerField()
    trinca = IntegerField()
    placa = IntegerField()
    drenagem = IntegerField()

class Videos(BaseModel):
    name = CharField()
    km_ini = FloatField()
    km_final = FloatField()

if __name__ == '__main__':
    try:
        if not Results.table_exists():
            Results.create_table()
            print("Tabela 'Results' criada com sucesso!")
        else: 
            print("Tabela 'Results' já existe!")
       
        if not Rodovias.table_exists():
            Rodovias.create_table()
            print("Tabela 'Rodovias' criada com sucesso!")
        else:
            print("Tabela 'Rodovias' já existe!")
           
        if not Videos.table_exists():
            Videos.create_table()
            print("Tabela 'Videos' criada com sucesso!")
        else:
            print("Tabela 'Videos' já existe!")
            
        if not DerivedTable.table_exists():
            DerivedTable.create_table()
            print("Tabela 'DerivedTable' criada com sucesso!")
        else:
            print("Tabela 'DerivedTable' já existe!")

    except peewee.OperationalError as e:
        print("Erro ao criar tabela:", str(e))