import os
import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from TOSCA_modules import *
from ERA5_modules import *

#abc = download_image_tile("2021-01-01", "2021-02-01", ["31TEJ"])
#get_climate_data('2010', '06', '/home/maksimov/ERA5_TOSCA_download.nc')
#this_df = process_climate_data("/home/maksimov/ERA5_download.nc")
#print(this_df)

#download_image_gdf("2021-01-01", "2021-03-01", "/home/maksimov/DF_Municipios_2021.shp", "ok")

# main_folder = "/home/maksimov/sen2chain_data/data/L2A/22LGH/"
# folder_1 = "/home/maksimov/sen2chain_data/data/L2A/22LHH/"
# folder_2 = "/home/maksimov/sen2chain_data/data/L2A/22LGH/"
#
# img_list = sorted(os.listdir(main_folder))
# gdf_m = geopandas.read_file("/home/maksimov/region_presentation.shp")
#
# data_dict = {}
#
# for img in img_list:
#     raster_list = [main_folder + img]
#     datetime = img[:19]  # Date at which the image is taken
#     date_str = img[11:19]
#     # # Gathering all the other images of the same date
#     # for img1 in sorted(os.listdir(folder_1)):
#     #     if img1[:19] == datetime:
#     #         raster_list.append(folder_1 + img1)
#     # for img2 in sorted(os.listdir(folder_2)):
#     #     if img2[:19] == datetime:
#     #         raster_list.append(folder_2 + img2)
#
#     # Now we rasterize what we need
#     raster_04 = []
#     raster_08 = []
#     for rst in raster_list:
#         path = rst + "/GRANULE/"
#         path += sorted(listdir(path))[0] + "/IMG_DATA/R10m/"
#         raster_04.append(Raster(path + sorted(listdir(path))[3]))
#         raster_08.append(Raster(path + sorted(listdir(path))[4]))
#
#     gdf_m = gdf_m.to_crs(crs=raster_04[0].crs)
#     # Now we create two large rasters with the merge function
#     #print(sys.getsizeof(raster_04[0]))
#     # raster4 = Raster.merge(raster_04)
#     # raster8 = Raster.merge(raster_08)
#
#     # Zonal stats to get mean NDVI
#     red = np.array(raster_04[0].zonal_stats(gdf_m, band=1, stats=["mean"])["mean"])
#     pir = np.array(raster_08[0].zonal_stats(gdf_m, band=1, stats=["mean"])["mean"])
#     print(red)
#     print(pir)
#     ndvi_val = (pir - red) / (pir + red)
#     data_dict[date_str] = ndvi_val
#     print(data_dict)

#
# data_23LKC = {'20210104': np.array([       nan, 0.06318182,        nan,        nan]), '20210107': np.array([nan, nan, nan, nan]), '20210114': np.array([       nan, 0.10298464,        nan,        nan]), '20210117': np.array([nan, nan, nan, nan]), '20210124': np.array([       nan, 0.78351759,        nan,        nan]), '20210127': np.array([nan, nan, nan, nan]), '20210203': np.array([     nan, 0.488186,      nan,      nan]), '20210206': np.array([nan, nan, nan, nan]), '20210213': np.array([       nan, 0.50610906,        nan,        nan]), '20210216': np.array([nan, nan, nan, nan]), '20210226': np.array([nan, nan, nan, nan]), '20210102': np.array([nan, nan, nan, nan]), '20210109': np.array([       nan, 0.79458557,        nan,        nan]), '20210112': np.array([nan, nan, nan, nan]), '20210119': np.array([       nan, 0.68346461,        nan,        nan]), '20210122': np.array([nan, nan, nan, nan]), '20210129': np.array([      nan, 0.7335299,       nan,       nan]), '20210201': np.array([nan, nan, nan, nan]), '20210208': np.array([       nan, 0.08752182,        nan,        nan]), '20210211': np.array([nan, nan, nan, nan]), '20210218': np.array([       nan, 0.05831094,        nan,        nan]), '20210221': np.array([nan, nan, nan, nan])}
# data_22LHH = {'20210104': np.array([-0.00347569,  0.03912345, -0.01128028, -0.00994138]), '20210107': np.array([0.22573332,        nan, 0.24304981, 0.32679321]), '20210114': np.array([0.08001797, 0.10245434, 0.09260796, 0.0920282 ]), '20210117': np.array([0.06502877,        nan, 0.04498852, 0.08610686]), '20210124': np.array([0.57392376, 0.78538936, 0.37428644, 0.5598232 ]), '20210127': np.array([0.40312937,        nan, 0.32444333, 0.47231102]), '20210203': np.array([0.55880644, 0.48890985, 0.13960961, 0.41340622]), '20210206': np.array([0.0116059 ,        nan, 0.00967562, 0.01285322]), '20210213': np.array([0.13422694, 0.50676663, 0.29302269, 0.19889546]), '20210216': np.array([0.11550732,        nan, 0.06105835, 0.23820064]), '20210223': np.array([0.4769293 , 0.31148673, 0.08054929, 0.16623882]), '20210226': np.array([0.03248721,        nan, 0.0062528 , 0.03368744]), '20210102': np.array([0.15336815,        nan, 0.13836135, 0.33370326]), '20210109': np.array([0.32823167, 0.79583718, 0.18902963, 0.3913837 ]), '20210112': np.array([0.07334279,        nan, 0.06078713, 0.14836781]), '20210119': np.array([0.14232921, 0.68465278, 0.22254234, 0.4085314 ]), '20210122': np.array([0.51695551,        nan, 0.2724269 , 0.512846  ]), '20210129': np.array([0.48250469, 0.73480396, 0.33059891, 0.44998128]), '20210201': np.array([0.59095416,        nan, 0.2630367 , 0.5762425 ]), '20210208': np.array([0.17394875, 0.08810873, 0.09299007, 0.13898861]), '20210211': np.array([0.18527133,        nan, 0.05333226, 0.08652483]), '20210218': np.array([0.15468178, 0.05887434, 0.10837304, 0.25060785]), '20210221': np.array([ 0.06257637,         nan, -0.012273  , -0.00854734]), '20210228': np.array([-0.00698679, -0.01113653, -0.016956  ,  0.00808873])}
# data_22LGH = {'20210107': np.array([nan, nan, nan, nan]), '20210117': np.array([nan, nan, nan, nan]), '20210127': np.array([nan, nan, nan, nan]), '20210206': np.array([nan, nan, nan, nan]), '20210216': np.array([nan, nan, nan, nan]), '20210226': np.array([nan, nan, nan, nan]), '20210102': np.array([nan, nan, nan, nan]), '20210112': np.array([nan, nan, nan, nan]), '20210122': np.array([nan, nan, nan, nan]), '20210201': np.array([nan, nan, nan, nan]), '20210211': np.array([nan, nan, nan, nan]), '20210221': np.array([nan, nan, nan, nan])}
# #data_global = {'20210104': array([       nan, 0.05115264,        nan,        nan]), '20210107': array([nan, nan, nan, nan]), '20210114': array([       nan, 0.10271949,        nan,        nan]), '20210117': array([nan, nan, nan, nan]), '20210124': array([       nan, 0.78445348,        nan,        nan]), '20210127': array([nan, nan, nan, nan]), '20210203': array([       nan, 0.48854792,        nan,        nan]), '20210206': array([nan, nan, nan, nan]), '20210213': array([       nan, 0.50643784,        nan,        nan]), '20210216': array([nan, nan, nan, nan]), '20210226': array([nan, nan, nan, nan]), '20210102': array([nan, nan, nan, nan]), '20210109': array([       nan, 0.79521138,        nan,        nan]), '20210112': array([nan, nan, nan, nan]), '20210119': array([      nan, 0.6840587,       nan,       nan]), '20210122': array([nan, nan, nan, nan]), '20210129': array([       nan, 0.73416693,        nan,        nan]), '20210201': array([nan, nan, nan, nan]), '20210208': array([       nan, 0.08781527,        nan,        nan]), '20210211': array([nan, nan, nan, nan]), '20210218': array([       nan, 0.05859264,        nan,        nan]), '20210221': array([nan, nan, nan, nan]), '20210223': array([0.4769293 , 0.31148673, 0.08054929, 0.16623882]), '20210228': array([-0.00698679, -0.01113653, -0.016956  ,  0.00808873])}
# data_global = {'20210104': np.array([-0.00347569,  0.05115264, -0.01128028, -0.00994138]), '20210107': np.array([0.22573332,        nan, 0.24304981, 0.32679321]), '20210114': np.array([0.08001797, 0.10271949, 0.09260796, 0.0920282 ]), '20210117': np.array([0.06502877,        nan, 0.04498852, 0.08610686]), '20210124': np.array([0.57392376, 0.78445348, 0.37428644, 0.5598232 ]), '20210127': np.array([0.40312937,        nan, 0.32444333, 0.47231102]), '20210203': np.array([0.55880644, 0.48854792, 0.13960961, 0.41340622]), '20210206': np.array([0.0116059 ,        nan, 0.00967562, 0.01285322]), '20210213': np.array([0.13422694, 0.50643784, 0.29302269, 0.19889546]), '20210216': np.array([0.11550732,        nan, 0.06105835, 0.23820064]), '20210226': np.array([0.03248721,        nan, 0.0062528 , 0.03368744]), '20210102': np.array([0.15336815,        nan, 0.13836135, 0.33370326]), '20210109': np.array([0.32823167, 0.79521138, 0.18902963, 0.3913837 ]), '20210112': np.array([0.07334279,        nan, 0.06078713, 0.14836781]), '20210119': np.array([0.14232921, 0.6840587 , 0.22254234, 0.4085314 ]), '20210122': np.array([0.51695551,        nan, 0.2724269 , 0.512846  ]), '20210129': np.array([0.48250469, 0.73416693, 0.33059891, 0.44998128]), '20210201': np.array([0.59095416,        nan, 0.2630367 , 0.5762425 ]), '20210208': np.array([0.17394875, 0.08781527, 0.09299007, 0.13898861]), '20210211': np.array([0.18527133,        nan, 0.05333226, 0.08652483]), '20210218': np.array([0.15468178, 0.05859264, 0.10837304, 0.25060785]), '20210221': np.array([ 0.06257637,         nan, -0.012273  , -0.00854734]), '20210223': np.array([0.4769293 , 0.31148673, 0.08054929, 0.16623882]), '20210228': np.array([-0.00698679, -0.01113653, -0.016956  ,  0.00808873])}
#
# df_global = pd.DataFrame(data_global)
# df_global = df_global.reindex(sorted(df_global.columns), axis=1)
# #X=[i for i in range ]
# plt.plot(df_global.iloc[[0]].T, 'b')
# plt.plot(df_global.iloc[[1]].T.ffill(), 'g')
# plt.plot(df_global.iloc[[2]].T, 'r')
# plt.plot(df_global.iloc[[3]].T, 'k')
# plt.xticks(fontsize=20, rotation = 45)
# plt.yticks(fontsize=20)
#
# # df_global.plot(df_global)
# plt.show()


def merge_dicts(d1,d2):
    d3 = {}
    for key, value in d1.items():
        if key in d1 and key in d2:
            d3[key] = merge_lists(d1[key], d2[key])
        else:
            d3[key] = d1[key]
    for key, value in d2.items():
        if key in d2 and not (key in d1):
            d3[key] = d2[key]
    return d3


def merge_lists(l1, l2):
    l3 = []
    for i in range(len(l1)):
        if np.isnan(l1[i]):
            l3.append(l2[i])
        elif np.isnan(l2[i]):
            l3.append(l1[i])
        else:
            l3.append((l1[i]+l2[i])/2)
    return np.array(l3)


#
# fn = "/home/maksimov/ERA5_download.nc"
# ds = nc.Dataset(fn)
# lats = ds.variables['latitude'][:]
# lons = ds.variables['longitude'][:]
# skt  = ds.variables['skt'][:]
# time = ds.variables['time'][:]
#
# p0_lat, p0_lon = nearest_era_centroid(ds, -15.680, -47.989)
#
# p1_lat, p1_lon = nearest_era_centroid(ds, -15.812, -47.515)
#
# p2_lat, p2_lon = nearest_era_centroid(ds, -15.843, -47.058)
#
# p3_lat, p3_lon = nearest_era_centroid(ds, -15.887, -47.757)
#
# print(p0_lat,p0_lon)
# print(p1_lat,p1_lon)
# print(p2_lat,p2_lon)
# print(p3_lat,p3_lon)
#
# print(ds['skt'][0][p0_lat][0][p0_lon][0]-273.15)
# print(ds['skt'][0][p1_lat][0][p1_lon][0]-273.15)
# print(ds['skt'][0][p2_lat][0][p2_lon][0]-273.15)
# print(ds['skt'][0][p3_lat][0][p3_lon][0]-273.15)
# # data_global = merge_dicts(data_23LKC, data_22LHH)
# # print(data_global)

#create_grid(-48.189, -47.227, -16.053, -15.505)
first_raster = Raster("/home/maksimov/Downloads/occupation_sol_S2/Classifications_fusion.tif").to_crs()
print(first_raster.crs)
# dataframe_brazil = geopandas.GeoDataFrame.from_file("/home/maksimov/TEST_grid.shp").to_crs(first_raster.crs)
#
# abc = first_raster.zonal_stats(layer=dataframe_brazil, customized_stats={'majority_count': majority_count})
# print(abc)