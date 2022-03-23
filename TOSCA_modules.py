import sen2chain
import geopandas
import csv
import time
import numpy as np
from os import listdir
from pyrasta.raster import Raster
from multiprocessing import Process
from math import nan
SEN2CHAIN_DATA_PATH = "/home/daniel/sen2chain_data/"

"""
*****************Downloading of images*****************
"""


def download_image(start_date: str,
                   end_date: str,
                   tile_list: [str]) -> [str]:
    """
    Downloads the images of the given tiles between start_date and end_date.
    Returns a list containing  the identifiers of the downloaded images
    :param start_date: str, starting date of the time period
    :param end_date: str, ending date of the time period
    :param tile_list: [str], list of tiles to monitor
    """

    # First request that shows the number of images to download
    request = sen2chain.DataRequest(start_date, end_date).from_tiles(tile_list)
    image_names = list(request['hubs'].keys())

    # results variable where the indexes will be stored
    results = {'NDVI': [], 'NDWI': [], 'NDMI': [], 'NBR': []}

    for name in image_names:
        # Temporary request that contains only one of the images of the main request
        temp_request = {'aws': {}, 'hubs': {name: request['hubs'][name]}}

        # Image download
        sen2chain.DownloadAndProcess(temp_request)

        # Image processing
        process_l1c_to_l2a(name)

        # String manipulation to work in the right folder
        name = name[:8] + "2A" + name[10:]
        temp_tile = name.split("_")[-2][1:]
        path_to_image = SEN2CHAIN_DATA_PATH + "data/L2A/" + temp_tile + "/" + name + "/"
        print("Working on image:", path_to_image)

        # Index extraction
        results = process_index(path_to_image, results)

        # Image deletion
        # implement if user specified so

    # Database update
    with open("/home/maksimov/DATABASE_TEST.csv", 'a+', newline='') as f:
        print("Writing in file " + "/home/maksimov/DATABASE_TEST.csv")
        write = csv.writer(f)
        write.writerows(results)

    return 0


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

    return results


def process_ndvi(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R10m/"
    print("Raster BO4:", sorted(listdir(path_raster))[3])
    print("Raster B08:", sorted(listdir(path_raster))[4])
    ras4 = Raster(sorted(listdir(path_raster))[3])
    ras8 = Raster(sorted(listdir(path_raster))[4])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras4 = ras4.mask(mask)
        ras8 = ras8.mask(mask)
    except ValueError:
        print("No mask for this image")
    return (ras8 - ras4) / (ras8 + ras4)


def process_ndwi(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R10m/"
    print("Raster BO3:", sorted(listdir(path_raster))[2])
    print("Raster B08:", sorted(listdir(path_raster))[4])
    ras3 = Raster(sorted(listdir(path_raster))[2])
    ras8 = Raster(sorted(listdir(path_raster))[4])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras3 = ras3.mask(mask)
        ras8 = ras8.mask(mask)
    except ValueError:
        print("No mask for this image")
    return (ras3 - ras8) / (ras3 + ras8)


def process_nbr(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R20m/"
    print("Raster BO8A:", sorted(listdir(path_raster))[7])
    print("Raster B012:", sorted(listdir(path_raster))[9])
    ras8a = Raster(sorted(listdir(path_raster))[7])
    ras12 = Raster(sorted(listdir(path_raster))[9])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras8a = ras8a.mask(mask)
        ras12 = ras12.mask(mask)
    except ValueError:
        print("No mask for this image")
    return (ras8a - ras12) / (ras8a + ras12)


def process_ndmi(path: str):
    # Rasters
    path_raster = path + "IMG_DATA/R20m/"
    print("Raster BO8A:", sorted(listdir(path_raster))[7])
    print("Raster B011:", sorted(listdir(path_raster))[8])
    ras8a = Raster(sorted(listdir(path_raster))[7])
    ras11 = Raster(sorted(listdir(path_raster))[8])

    # Try except block to manage cases where there is no cloud mask
    try:
        path_mask = path + "QI_DATA/MSK_CLOUDS_B00.gml"
        mask = geopandas.GeoDataFrame.from_file(path_mask)
        ras8a = ras8a.mask(mask)
        ras11 = ras11.mask(mask)
    except ValueError:
        print("No mask for this image")
    return (ras8a - ras11) / (ras8a + ras11)

"""
Si %cloud trop grand, on "vire" la photo
pour ça, on peut soit 
1) enregistrer ce % qq part et comparer ensuite,
2) soit virer direct
variante 1) a l'air plus appropriée
"""