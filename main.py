from TOSCA_modules import *
from ERA5_modules import *

#abc = download_image("2021-01-01", "2021-02-01", ["31TEJ"])
#get_climate_data('2010', '06', '/home/maksimov/ERA5_TOSCA_download.nc')
this_df = process_climate_data("/home/maksimov/Downloads/brasilia_era5.nc")
print(this_df)