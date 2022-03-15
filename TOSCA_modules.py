import sen2chain
import os
import time
from multiprocessing import Process

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
    for name in image_names:
        # Temporary request that contains only one of the images of the main request
        temp_request = {'aws': {}, 'hubs': {name: request['hubs'][name]}}

        # Image download
        sen2chain.DownloadAndProcess(temp_request)

        # Image processing
        process_l1c_to_l2a(name)

        # Index extraction
        temp_tile = name.split("_")[-2][1:]
        path_to_image = SEN2CHAIN_DATA_PATH + "data/L2A/" + temp_tile + "/" + name + "/"
        print("Working on image:", path_to_image)
        results = process_index(path_to_image, ['NDVI'])

        # Database update

        # Image deletion

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
                  list_indexes: [str]):

    img_path = path + "GRANULE/"
    img_path += sorted(listdir(img_path))[0] + "/"
    img_path += "IMG_DATA/"

    results = {}
    for index in list_indexes:
        if index == 'NDVI':
            results['NDVI'] = process_ndvi(img_path)
        if index == 'NDWI':
            results['NDWI'] = process_ndwi(img_path)
        if index == 'NDMI':
            results['NDMI'] = process_ndmi(img_path)
        if index == 'NBR':
            results['NBR'] = process_nbr(img_path)
    return results


def process_ndvi(path: str):
    # Rasters
    ras4 = Raster(img4)
    ras8 = Raster(img8)

    # Try except block to manage cases where there is no cloud mask
    try:
        mask = geopandas.GeoDataFrame.from_file(mask_file)
        ras4 = ras4.mask(mask)
        ras8 = ras8.mask(mask)
    except ValueError:
        print("No mask for this image")

    # Cropland parcel
    gp_parcelle = geopandas.read_file(parcel)
    # CRS
    gp_parcelle = gp_parcelle.to_crs(crs=ras4.crs)

    # Stats
    # We use np.array() so that the + operator is element-wise addition
    red = np.array(ras4.zonal_stats(gp_parcelle, band=1, stats=["mean"])["mean"])
    pir = np.array(ras8.zonal_stats(gp_parcelle, band=1, stats=["mean"])["mean"])
    del ras4, ras8
    return (pir - red) / (pir + red)

"""
Si %cloud trop grand, on "vire" la photo
pour ça, on peut soit 
1) enregistrer ce % qq part et comparer ensuite,
2) soit virer direct
variante 1) a l'air plus appropriée
"""