import os
import pandas as pd
import numpy as np
from datetime import datetime
from libcomcat.search import search
from libcomcat.dataframes import get_summary_data_frame, get_detail_data_frame
from tqdm import tqdm


# Constants
R_earth = 6378.1 # km | Equatorial radius (source: NASA's Earth Fact Sheet)

def saving_data(df, filename, folder="B_eq_raw"):

    script_dir = os.path.dirname(os.path.abspath(__file__))  # Script path
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))  # Project root path

    eq_dir = os.path.join(project_root, f"A00_data/{folder}") # Eq. data folder

    if not os.path.exists(eq_dir):
        os.makedirs(eq_dir)

    filepath = os.path.join(eq_dir, filename) # File path to save the data

    df.to_csv(filepath, index=False)
       
    print(f"Data saved to {filepath}")

def date_format(date):
    date = date.replace("-", ",")
    date = date.replace(" ", ",")
    date = date.replace(":", ",")
    date = date.replace("/", ",")
    return date

def limit_region_coords(lat_cent, lon_cent, region_rad):

    #Differential of the angle and then the lat and long
    d_theta = region_rad / R_earth
    d_lat = np.degrees(d_theta)  
    d_lon = np.degrees(d_theta) / np.cos(np.radians(lat_cent))

    #Creating the square interval
    lat_min = lat_cent - d_lat
    lat_max = lat_cent + d_lat
    lon_min = lon_cent - d_lon
    lon_max = lon_cent + d_lon
    
    return lat_min, lat_max, lon_min, lon_max

def mw_to_mo(mw):
     return 10**(3/2 * mw + 16.1)


# Esto está todavía en proceso de desarrollo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def magnitude_of_completeness(date_i, date_f, center_coords, reg_rad):
       
    lat_cent, lon_cent = center_coords
    lat_min, lat_max, lon_min, lon_max = limit_region_coords(lat_cent, lon_cent, reg_rad)

    date_i = datetime.strptime(date_format(date_i), "%Y,%m,%d,%H,%M")
    date_f = datetime.strptime(date_format(date_f), "%Y,%m,%d,%H,%M")
     
    events = search(
        starttime= date_i,
        endtime= date_f,
        minlatitude= lat_min,
        maxlatitude= lat_max,
        minlongitude= lon_min,
        maxlongitude= lon_max,
        minmagnitude= -10,
        eventtype= "earthquake",
        orderby= "time"
    )
    
    detail_events_df = get_detail_data_frame(events, get_all_magnitudes= True)

    return detail_events_df

def get_lat_lot_from_file(file="wrk_df.csv"):
    path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(path, "..", ".."))

    file_path = os.path.join(project_root, f"A00_data/B_eq_raw/{file}")

    df = pd.read_csv(file_path)

    id = df['id'].values
    lat = df['latitude'].values
    lon = df['longitude'].values

    return id, lat, lon



# This is a future function, for now we consider that the magnitude is already in Mw
def magnitude_conversion(magnitude, mag_type, target_type="Mw"):
    return print("Conversion not implemented yet")