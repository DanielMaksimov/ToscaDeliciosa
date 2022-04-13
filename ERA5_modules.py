import netCDF4 as nc
import cdsapi

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
