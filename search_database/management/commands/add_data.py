import pandas as pd
from django.core.management.base import BaseCommand
from search_database.models import Question
from sqlalchemy import create_engine
from django.conf import settings

class Command(BaseCommand):
  help = "A command to add data from an Excel file to the database"

  def handle(self, *args, **options):
    excel_file = r'filtered_data2.xlsx'
    data = pd.read_excel(excel_file)
    
    # header_row = 0
    # data.columns = data.iloc[header_row]
    # data.columns = data.iloc[0]
    # data.columns = data.columns.fillna('unnamed')
    data.fillna('Data Not Available', inplace=True)
    # index = ["DBO12"+str(c) for c in range(len(data))]
    # data['index'] = index
    # first_column = data.pop('index')
    # data.insert(0, 'index', first_column)
    # data.columns = data.columns.str.replace(' ', '_')
    # data.columns = data.columns.str.replace('(', '')
    # data.columns = data.columns.str.replace(')', '')

# data.columns = [col.replace("(", "").replace(")", "") for col in data.columns]

    # data.columns = data.columns.str.replace('/', '_')
    # data.columns = data.columns.str.replace(',', '_')
    # data.columns= data.columns.str.strip().str.lower()
    #data['id'] = [i for i in range (len(data))]
    #print(data['id'])
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']

    # engine = create_engine('sqlite:///db.sqlite3')
    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format( user=user,password=password,database_name=database_name,)

    engine = create_engine(database_url, echo=False)

    data.to_sql('search', if_exists='replace', con=engine, index=False)
