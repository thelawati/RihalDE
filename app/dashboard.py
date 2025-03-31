import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os


db_url = os.getenv('DB_URL', 'postgresql://admin:admin@db:5432/rihal_de')

engine = create_engine(db_url)

st.title("Rihal Crime Records Dashboard")

#1
st.header("District with the Highest Crime Rate")

crime_rate_query = """
SELECT district_id, COUNT(*) AS crime_count
FROM crime_records
GROUP BY district_id
ORDER BY crime_count DESC;
"""

crime_rate_df = pd.read_sql(crime_rate_query, engine)
st.bar_chart(crime_rate_df.set_index('district_id'))
top_district = crime_rate_df.iloc[0]
dist = top_district['district_id']
count = top_district['crime_count']

st.write("District with the highest crime rate is: District ", dist, " with ", count, "crimes.")



# 2
st.header("Day of the Week with the Most Crimes")
day_query = """
SELECT day_of_week, COUNT(*) AS crime_count
FROM crime_records
GROUP BY day_of_week
ORDER BY crime_count DESC;
"""
day_df = pd.read_sql(day_query, engine)
st.bar_chart(day_df.set_index('day_of_week'))
day = day_df.iloc[0]['day_of_week']
st.write("Day with most crimes is: ", day, ".")


# 3
st.header("District with Highest Average Police Patrol Distance")

distance_query = """
SELECT district_id, AVG(nearest_police_patrol) AS avg_distance_km
FROM crime_records
GROUP BY district_id
ORDER BY avg_distance_km DESC;
"""
distance_df = pd.read_sql(distance_query, engine)
st.bar_chart(distance_df.set_index('district_id'))

top_avg = distance_df.iloc[0]
dist = top_avg['district_id']
km = round(top_avg['avg_distance_km'],2)
st.write(f"District with the highest avg distance is district ", dist, " with ", km, "." )
