import sen2chain
import geopandas
import pandas as pd
import rioxarray as rxr
from shapely.geometry import Polygon
import gistools
import csv
import time
import datetime
import numpy as np
from os import listdir
from pyrasta.raster import Raster
from multiprocessing import Process
from math import nan
SEN2CHAIN_DATA_PATH = "/home/maksimov/sen2chain_data/"


"""
*****************Downloading of images*****************
"""


def download_image_tile(start_date: str,
                        end_date: str,
                        tile_list: [str],
                        file_output: str) -> [str]:
    """
    Downloads the images of the given tiles between start_date and end_date.
    Returns a list containing  the identifiers of the downloaded images
    Creates a .hdf file containing the time series for NDVI, NDWI, NDMI and NBR

    :param start_date: str, starting date of the time period
    :param end_date: str, ending date of the time period
    :param tile_list: [str], list of tiles to monitor
    :param file_output: str, name of the file containing the output data
    """

    store = pd.HDFStore(file_output)

    for tile in tile_list:
        # First request that shows the number of images to download
        request = sen2chain.DataRequest(start_date, end_date).from_tiles(tile)
        image_names = list(request['hubs'].keys())

        # Variable storing indexes
        results = {'NDVI': [], 'NDWI': [], 'NDMI': [], 'NBR': []}
        # Variable storing dates
        dates = []

        for name in image_names:
            # Temporary request that contains only one of the images of the main request
            temp_request = {'aws': {}, 'hubs': {name: request['hubs'][name]}}

            # Image download
            try:
                sen2chain.DownloadAndProcess(temp_request)
            except:
                print("ERROR: Image " + name +" could not be downloaded")

            # Image processing
            try:
                process_l1c_to_l2a(name)
            except:
                print("ERROR: Image " + name + " could not be processed to L2A")

            # String manipulation to work in the right folder
            name_2a = name[:8] + "2A" + name[10:]
            temp_tile = name_2a.split("_")[-2][1:]
            path_to_image = SEN2CHAIN_DATA_PATH + "data/L2A/" + temp_tile + "/" + name_2a + ".SAFE/"
            print("Working on image:", path_to_image)

            try:
                # Index extraction
                process_index(path_to_image, results)

                # Date extraction
                sensing_date = name.split("_")[2][:8]
                dates.append(pd.to_datetime(sensing_date, format="%Y\%m\%d"))

            except:
                print("ERROR: Image " + name + " could not be analysed")

            # Image deletion
            # implement if user specified so

        # Database update, with each key being a tile from the input list of tiles
        df = pd.DataFrame(results, index=dates)
        store.append(temp_tile, df)

    store.close()
    return 0


def download_image_gdf(start_date: str,
                       end_date: str,
                       geodataframe: str,
                       file_output: str) -> [str]:
    """
    Downloads the images of the given geodataframes between start_date and end_date.
    Returns a list containing  the identifiers of the downloaded images
    Creates a .hdf file containing the time series for NDVI, NDWI, NDMI and NBR

    :param start_date: str, starting date of the time period
    :param end_date: str, ending date of the time period
    :param geodataframe: str, path to file containing the polygons to monitor
    :param file_output: str, name of the file containing the output data
    """

    # First request that shows the number of images to download
    request = sen2chain.DataRequest(start_date, end_date).from_file(geodataframe)
    image_names = list(request['hubs'].keys())

    # Variable storing indexes
    results = {'NDVI': [], 'NDWI': [], 'NDMI': [], 'NBR': []}
    # Variable storing dates
    dates = []

    for name in image_names:
        # Temporary request that contains only one of the images of the main request
        temp_request = {'aws': {}, 'hubs': {name: request['hubs'][name]}}

        # Image download
        try:
            sen2chain.DownloadAndProcess(temp_request)
        except:
            print("ERROR: Image " + name + " could not be downloaded")

        # Image processing
        try:
            process_l1c_to_l2a(name)
        except:
            print("ERROR: Image " + name + " could not be processed to L2A")

        # String manipulation to work in the right folder
        name_2a = name[:8] + "2A" + name[10:]
        temp_tile = name_2a.split("_")[-2][1:]
        path_to_image = SEN2CHAIN_DATA_PATH + "data/L2A/" + temp_tile + "/" + name_2a + ".SAFE/"
        print("Working on image:", path_to_image)

        try:
            # Index extraction
            gdf_municipality = geopandas.GeoDataFrame.from_file(geodataframe)
            big_raster_red = Raster.merge(list_of_rasters_red)
            big_raster_pir = Raster.merge(list_of_rasters_pir)

            red = np.array(big_raster.zonal_stats(gdf_municipality, stats=["mean"])["mean"])
            pir = np.array(big_raster.zonal_stats(gdf_municipality, stats=["mean"])["mean"])

            ndvi_val = (pir - red) / (pir + red)
            # process_index(path_to_image, results)

            # Date extraction
            sensing_date = name.split("_")[2][:8]
            dates.append(pd.to_datetime(sensing_date, format="%Y\%m\%d"))

        except:
            print("ERROR: Image " + name + " could not be analysed")

        # Image deletion
        # implement if user specified so

    # Database update
    store = pd.HDFStore(file_output)
    df = pd.DataFrame(results, index=dates)
    store.append(geodataframe, df)
    store.close()
    return 0


# "/home/maksimov/HDFStore_Sentinel2_Brasilia_Mun.hdf5"

"""
*****************L1C to L2A*****************
"""


def process_l1c_to_l2a(name):
    l1c = sen2chain.L1cProduct(name)
    try:
        l1c.process_l2a()
    except:
        print("FAILED:", name)
    print("PASSED:", name)
    return 0


"""
*****************Index processing*****************
"""


def process_index(path: str,
                  results: dict):

    img_path = path + "GRANULE/"
    img_path += sorted(listdir(img_path))[0] + "/"

    results['NDVI'].append(process_ndvi(img_path))
    results['NDWI'].append(process_ndwi(img_path))
    results['NDMI'].append(process_ndmi(img_path))
    results['NBR'].append(process_nbr(img_path))

    return 0


def process_ndvi(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R10m/"
    print("Raster BO4:", sorted(listdir(path_raster))[3])
    print("Raster B08:", sorted(listdir(path_raster))[4])
    ras4 = Raster(path_raster + sorted(listdir(path_raster))[3])
    ras8 = Raster(path_raster + sorted(listdir(path_raster))[4])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras4 = ras4.mask(mask)
        ras8 = ras8.mask(mask)
    except ValueError:
        print("No mask for this image")
    ras = (ras8 - ras4) / (ras8 + ras4)
    return ras.mean[0]


def process_ndwi(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R10m/"
    print("Raster BO3:", sorted(listdir(path_raster))[2])
    print("Raster B08:", sorted(listdir(path_raster))[4])
    ras3 = Raster(path_raster + sorted(listdir(path_raster))[2])
    ras8 = Raster(path_raster + sorted(listdir(path_raster))[4])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras3 = ras3.mask(mask)
        ras8 = ras8.mask(mask)
    except ValueError:
        print("No mask for this image")
    ras = (ras3 - ras8) / (ras3 + ras8)
    return ras.mean[0]


def process_nbr(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R20m/"
    print("Raster BO8A:", sorted(listdir(path_raster))[7])
    print("Raster B012:", sorted(listdir(path_raster))[9])
    ras8a = Raster(path_raster + sorted(listdir(path_raster))[7])
    ras12 = Raster(path_raster + sorted(listdir(path_raster))[9])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras8a = ras8a.mask(mask)
        ras12 = ras12.mask(mask)
    except ValueError:
        print("No mask for this image")
    ras = (ras8a - ras12) / (ras8a + ras12)
    return ras.mean[0]


def process_ndmi(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R20m/"
    print("Raster BO8A:", sorted(listdir(path_raster))[7])
    print("Raster B011:", sorted(listdir(path_raster))[8])
    ras8a = Raster(path_raster + sorted(listdir(path_raster))[7])
    ras11 = Raster(path_raster + sorted(listdir(path_raster))[8])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras8a = ras8a.mask(mask)
        ras11 = ras11.mask(mask)
    except ValueError:
        print("No mask for this image")
    ras = (ras8a - ras11) / (ras8a + ras11)
    return ras.mean[0]


"""
*****************Raster processing*****************
"""


def majority_count(zone):
    return np.argmax([np.sum(zone == n) for n in np.arange(1, 7)]) + 1


def create_grid(name, xmin, xmax, ymin, ymax, grid_size=0.001):
    rows = int(np.ceil((ymax-ymin) / grid_size))
    cols = int(np.ceil((xmax-xmin) / grid_size))
    XleftOrigin = xmin
    XrightOrigin = xmin + grid_size
    YtopOrigin = ymax
    YbottomOrigin = ymax - grid_size
    polygons = []
    for i in range(cols):
       Ytop = YtopOrigin
       Ybottom =YbottomOrigin
       for j in range(rows):
           polygons.append(Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)]))
           Ytop = Ytop - grid_size
           Ybottom = Ybottom - grid_size
       XleftOrigin = XleftOrigin + grid_size
       XrightOrigin = XrightOrigin + grid_size
    grid = geopandas.GeoDataFrame(columns=['building_d'], geometry=polygons, crs="EPSG:4326")
    grid.to_file(name)
    return 0

def create_one_column_grid(name, xmin, xmax, ymin, ymax, grid_size=0.001):
    rows = int(np.ceil((ymax-ymin) / grid_size))
    XleftOrigin = xmin
    XrightOrigin = xmax
    YtopOrigin = ymax
    YbottomOrigin = ymax - grid_size
    polygons = []
    Ytop = YtopOrigin
    Ybottom =YbottomOrigin
    for j in range(rows):
        polygons.append(Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)]))
        Ytop = Ytop - grid_size
        Ybottom = Ybottom - grid_size
    grid = geopandas.GeoDataFrame(columns=['building_d'], data=[0.00 for i in polygons], geometry=polygons, crs="EPSG:4326")
    grid.to_file(name)
    return 0

"""
Si %cloud trop grand, on "vire" la photo
pour ça, on peut soit 
1) enregistrer ce % qq part et comparer ensuite,
2) soit virer direct
variante 1) a l'air plus appropriée

débat sur stockage raster ou raster.mean[0]

API pour les données climatiques complexes ;
Soit API openWeatherData (pas complètement opne source)
soit dl de ERA5 tous les 5/10 jours
"""