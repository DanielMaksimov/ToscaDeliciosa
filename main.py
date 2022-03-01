from TOSCA_modules import *

abc = download_image("2022-01-07", "2022-01-10", ["31TEJ"])
#print("The result is:", abc)
# request = sen2chain.DataRequest("2022-01-01","2022-01-07")
# requests = request.from_tiles(["31TEJ"])
#
# print(requests["hubs"].keys())

# sen2chain.DownloadAndProcess(identifiers=requests, hubs_limit={"scihub": 0, "peps": 8})

download_image("2022-01-01","2022-01-10", ["31TEJ"])
