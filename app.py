import streamlit as st
import pyodbc
import pandas as pd
import re
from io import StringIO
from datetime import datetime


server = 'DESKTOP-I348G7M69\\SQLEXPRESS'
database = 'MeasurementDB'
table_name = 'BladeMeasurementDeviations'
driver = 'ODBC Driver 17 for SQL Server'
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def extract_data(file, nc_file):
    data = []
    blade_number = None
    file_content = StringIO(file.read().decode("utf-8"))
    timestamp = datetime.now()  # Capture current time for each file processed
    
    # Use a dictionary to store all data for a single blade in one entry
    blade_data = {
        "BladeNumber": None,
        "NCFile": nc_file,
        "Timestamp": timestamp,
        "MeasurementDeviations": []  # List to hold all measurement deviation data
    }
    
    for line in file_content:
        line = line.strip()
        if 'blade number' in line:
            blade_number = int(re.search(r'\d+', line).group())
            blade_data["BladeNumber"] = blade_number
        elif 'MEA_DEVI' in line:
            measurement_deviation = float(line.split(':')[1].strip())
            
            # Append the extracted deviation to the list
            blade_data["MeasurementDeviations"].append(measurement_deviation)
    
    # append measurmentdeviation to bladedata
    while len(blade_data["MeasurementDeviations"]) < 24:
        blade_data["MeasurementDeviations"].append(0.0)

    return blade_data

def transform_data(blade_data):
    
    row_data = [
        blade_data["BladeNumber"],
        blade_data["Timestamp"],
        blade_data["NCFile"]  # Update to match FileName if needed
    ]
    
    # Add all measurement deviations
    row_data.extend(blade_data["MeasurementDeviations"])
    
    columns = ['BladeNumber', 'Timestamp', 'FileName'] + \
              [f'MeasurementDeviation{i+1}' for i in range(24)]
    
    # Create DataFrame
    df = pd.DataFrame([row_data], columns=columns)
    return df


def load_data(df):
    try:
        with pyodbc.connect(connection_string, autocommit=True) as conn:
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                # Create the insert query dynamically
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['?' for _ in df.columns])
                
                insert_query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders});
                """
                cursor.execute(insert_query, tuple(row))
                
        st.success("Data loaded successfully into the database.")
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")



def main():
    st.title("NC program Praser")

    # File uploader for the 02080.nc and 02400.nc files
    uploaded_file_02080 = st.file_uploader("Choose the 02080.ASC file", type="asc")
    uploaded_file_02400 = st.file_uploader("Choose the 02400.ASC file", type="asc")
    
    if uploaded_file_02080 and uploaded_file_02400:
        with st.spinner("Processing..."):
            extracted_data_02080 = extract_data(uploaded_file_02080, "02080.nc")
            extracted_data_02400 = extract_data(uploaded_file_02400, "02400.nc")
            
            transformed_data_02080 = transform_data(extracted_data_02080)
            transformed_data_02400 = transform_data(extracted_data_02400)
            
            st.write("Extracted and Transformed Data for 02080.nc:")
            st.dataframe(transformed_data_02080)
            
            st.write("Extracted and Transformed Data for 02400.nc:")
            st.dataframe(transformed_data_02400)

            # Button to load data into the SQL Server
            if st.button("Load Data into SQL Server"):
                load_data(transformed_data_02080)
                load_data(transformed_data_02400)

if __name__ == "__main__":
    main()
