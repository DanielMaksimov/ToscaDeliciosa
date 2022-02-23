import sen2chain
import os
import time
from multiprocessing import Process
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
    request = sen2chain.DataRequest(start_date, end_date)
    req = request.from_tiles(tile_list)

    image_names = list(req['hubs'].keys())
    print(image_names)
    # Check the directory to see which files are already there
    old_file_dict = {}
    for t in tile_list:
        path = "/home/maksimov/sen2chain_data/data/L1C/" + t
        old_file_dict[path] = os.listdir(path)
    # Download the new files
    # # New thread created here so the function .join() can be called later
    # thread_dl = threading.Thread(target=sen2chain.DownloadAndProcess,
    #                              kwargs={'identifiers': req, 'hubs_limit': {"scihub": 0, "peps": 8}})
    # thread_dl.start()
    # thread_dl.join()

    proc = Process(target=sen2chain.DownloadAndProcess,
                   kwargs={'identifiers': req, 'hubs_limit': {"scihub": 0, "peps": 8}})
    proc.start()
    proc.join()

    #sen2chain.DownloadAndProcess(identifiers=req, hubs_limit={"scihub": 0, "peps": 8})

    #time.sleep(3)
    # Once the download has finished, we can check the given tiles folders to see which files have been added
    added_files_list = []
    for t in tile_list:
        path = "/home/maksimov/sen2chain_data/data/L1C/" + t
        file_list = os.listdir(path)
        for f in file_list:
            if f not in old_file_dict[path]:
                added_files_list.append(f)
    return added_files_list



"""
*****************L1C to L2A*****************
"""


"""
def process_L1C_to_L2A(tile):
    t = sen2chain.Tile(tile)
    l1c = sen2chain.L1cProduct(p.identifier, t.name)
        try:
            l1c.process_l2a()
        except:
            print("FAILED:", p.identifier)
        print("PASSED:", p.identifier)
"""

