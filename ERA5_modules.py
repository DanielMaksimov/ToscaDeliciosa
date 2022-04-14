import netCDF4 as nc
import cdsapi
import pandas as pd

def get_climate_data(year: [str],
                     month: [str],
                     path: str) -> object:
    """
    Downloads the climate data and returns a panda DataFrame
    """
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-land-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': 'skin_temperature',
            'year': '2021',
            'month': '12',
            'time': '00:00',
            'area': [
                8, -75, -34,
                -30,
            ],
            'format': 'netcdf',
        },
        '/home/maksimov/ERA5_download.nc')
    return 0


def process_climate_data(path: str) -> pd.DataFrame:
    dataset = nc.Dataset(path)
    times = dataset.variables['time']
    skin_temp = dataset.variables['skt']
    new_times = nc.num2date(times[:], times.units)
    pd_df = pd.Series(skin_temp[:, 0], index=new_times)
    return pd_df

process_climate_data('/home/maksimov/ERA5_download.nc')