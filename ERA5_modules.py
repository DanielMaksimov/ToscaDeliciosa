import netCDF4 as nc
import cdsapi
import pandas as pd


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
    precipitation = dataset.variables['tp']
    new_times = nc.num2date(times[:], times.units)
    pd_skt = pd.Series(skin_temp[:, 0], index=new_times)
    pd_tp = pd.Series(precipitation[:, 0], index=new_times)
    pd_df = pd.DataFrame({'skin_temperature': pd_skt, 'total_precipitation': pd_tp})
    return pd_df


#get_climate_data('2010', '06', '/home/maksimov/ERA5_TOSCA_download.nc')
#process_climate_data('/home/maksimov/ERA5_download.nc')