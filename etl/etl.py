import pandas as pd
import re
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import numpy as np
from sqlalchemy import create_engine, text
import os



pdf_path = 'district_info.pdf'
images = convert_from_path(pdf_path)

# Extracting text from image using OCR
pdf_text = ''
for page_num, image in enumerate(images):
    text = pytesseract.image_to_string(image)
    pdf_text += text



lines = pdf_text.strip().split('\n')
cleaned_lines = []
buffer = ""

for line in lines:
    if re.match(r'^\d+\s', line):  
        if buffer:
            cleaned_lines.append(buffer.strip())
        buffer = line
    else:
        buffer += " " + line  
if buffer:
    cleaned_lines.append(buffer.strip())


data = []
for line in cleaned_lines:
    line = line.replace('|', '')
    match = re.match(r"(\d+)\s+(.*)\s+([\d,]+)\s+(.*)", line)
    if match:
        district_id = int(match.group(1))
        district_name = match.group(2).strip()
        population = int(match.group(3).replace(',', ''))
        governor = match.group(4).strip()
        data.append([district_id, district_name, population, governor])
district_df = pd.DataFrame(data, columns=["district_id", "district_name", "Population", "governor"])
#This is correctly named with no spellind mistakes in district_name


df = pd.read_json('crime_records.json')
df = df[df['crime_type'].notnull() & (df['crime_type'].str.strip() != "")]

df['crime_type'] = df['crime_type'].str.lower()

corrections = {
    'assult': 'assault',
    'frued': 'fraud'
}
df['crime_type'] = df['crime_type'].replace(corrections)

def convert_to_km(value):
    if not isinstance(value, str):
        return None  # or np.nan

    if 'km' in value:
        distance = float(value.split(' ')[0])
    elif 'miles' in value:
        distance = float(value.split(' ')[0]) * 1.60934
    else:
        print(value)
        return None  # unrecognized format

    return round(distance, 2)
    

df['nearest_police_patrol_km'] = df['nearest_police_patrol'].apply(convert_to_km)
df = df.drop(columns=['nearest_police_patrol'])
df = df.rename(columns={'nearest_police_patrol_km': 'nearest_police_patrol'})

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['day_of_week'] = df['timestamp'].dt.day_name()
df['date'] = df['timestamp'].dt.date
df['time'] = df['timestamp'].dt.time



#left join
merged_df = pd.merge(df, district_df, on='district_id', how='left')

merged_df[['district_id', 'district_name', 'crime_type', 'nearest_police_patrol', 'Population', 'governor', 'day_of_week', 'date', 'time']]
merged_df.rename(columns={'Population': 'population'})


engine = create_engine("postgresql://admin:admin@db:5432/rihal_de")

db_url = os.getenv('DB_URL', 'postgresql://admin:admin@db:5432/rihal_de')
engine = create_engine(db_url)


#Create or replace
df.to_sql('crime_records', engine, if_exists='replace', index=False)


print("Data written to PostgreSQL DB.")






