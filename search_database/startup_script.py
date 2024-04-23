# search_database/startup_script.py
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

def run():
    print("Loading data from Excel into the database...")

    # Path to your Excel file
    excel_file = 'filtered_data2.xlsx'
    data = pd.read_excel(excel_file)

    # Fill NA/NaN values
    data.fillna('Data Not Available', inplace=True)

    # Database settings from Django settings
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']

    # Create engine for PostgreSQL database
    database_url = f'postgresql://{user}:{password}@{host}:{port}/{database_name}'
    engine = create_engine(database_url, echo=False)

    # Write DataFrame to SQL
    data.to_sql('search_table', con=engine, index=False, if_exists='replace')

    print("Data has been successfully loaded to the database.")
