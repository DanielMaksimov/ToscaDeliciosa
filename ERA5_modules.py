import netCDF4 as nc
import cdsapi
import pandas as pd
import numpy as np

def get_climate_data(year: str,
                     month: [str],
                     path: str) -> object:
    """
    Downloads the climate data and saves it to specified file
    """
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-land-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': [
                'skin_temperature', 'total_precipitation',
                ],
            'year': year,
            'month': month,
            'time': '00:00',
            'area': [
                -14, -49, -17,
                -45,
            ],
            'format': 'netcdf',
        },
        path)
    return 0


def process_climate_data(path: str) -> pd.DataFrame:
    dataset = nc.Dataset(path)
    times = dataset.variables['time']
    skin_temp = dataset.variables['skt']
    #precipitation = dataset.variables['tp']
    new_times = nc.num2date(times[:], times.units)
    pd_skt = pd.Series(skin_temp[:, 0], index=new_times)
    #pd_tp = pd.Series(precipitation[:, 0], index=new_times)
    #pd_df = pd.DataFrame({'skin_temperature': pd_skt, 'total_precipitation': pd_tp})
    #return pd_df
    return pd.DataFrame({'skin_temperature': pd_skt})

def nearest_era_centroid(dataset, parcel_lat, parcel_lon):
    #Lists
    lats = dataset.variables['latitude'][:]
    lons = dataset.variables['longitude'][:]
    #Finding the closest centroid with lat and lon
    closest_lat = min(lats, key=lambda x:abs(x-parcel_lat))
    closest_lon = min(lons, key=lambda x:abs(x-parcel_lon))
    #Finding the indexes of that centroid in the matrix
    closest_lat_index = np.where(lats == closest_lat)
    closest_lon_index = np.where(lons == closest_lon)
    return closest_lat_index, closest_lon_index


#get_climate_data('2010', '06', '/home/maksimov/ERA5_TOSCA_download.nc')
#process_climate_data('/home/maksimov/ERA5_download.nc')