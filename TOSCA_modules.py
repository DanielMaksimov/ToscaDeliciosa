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

    #First request that shows the number of images to download
    request = sen2chain.DataRequest(start_date, end_date).from_tiles(tile_list)

    image_names = list(request['hubs'].keys())
    for name in image_names:
        #Temporary request that contains only one of the images of the main request
        temp_request = {'aws': {}, 'hubs': {name: request['hubs'][name]}}

        #Image download
        sen2chain.DownloadAndProcess(temp_request)

        #Image processing
        process_l1c_to_l2a(name)

        #Index extraction
        path_to_image = SEN2CHAIN_DATA_PATH + "data/L2A/" + name
        process_index(path_to_image, ['NDVI','NDWI'])

    return 0




    # # Check the directory to see which files are already there
    # old_file_dict = {}
    # for t in tile_list:
    #     path = "/home/maksimov/sen2chain_data/data/L1C/" + t
    #     old_file_dict[path] = os.listdir(path)
    # # Download the new files
    # # # New thread created here so the function .join() can be called later
    # # thread_dl = threading.Thread(target=sen2chain.DownloadAndProcess,
    # #                              kwargs={'identifiers': req, 'hubs_limit': {"scihub": 0, "peps": 8}})
    # # thread_dl.start()
    # # thread_dl.join()
    #
    # proc = Process(target=sen2chain.DownloadAndProcess,
    #                kwargs={'identifiers': req, 'hubs_limit': {"scihub": 0, "peps": 8}})
    # proc.start()
    # proc.join()

    #sen2chain.DownloadAndProcess(identifiers=req, hubs_limit={"scihub": 0, "peps": 8})

    #time.sleep(3)
    # Once the download has finished, we can check the given tiles folders to see which files have been added

    # added_files_list = []
    # for t in tile_list:
    #     path = "/home/maksimov/sen2chain_data/data/L1C/" + t
    #     file_list = os.listdir(path)
    #     for f in file_list:
    #         if f not in old_file_dict[path]:
    #             added_files_list.append(f)



    # return added_files_list
    #



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


def process_index(path, list_indexes):
    return 0
