import pandas as pd
import geopandas as gpd
import os

# Mengakses Data Shapefile Provinsi Lampung
shp_dir = 'DataSHPLampung/'
shp_files = [os.path.join(shp_dir, f) for f in os.listdir(shp_dir) if f.endswith('.shp')]
gdf_list = []
for shp in shp_files:
    temp_gdf = gpd.read_file(shp)
    nama_file_bersih = os.path.splitext(os.path.basename(shp))[0]
    temp_gdf['nama_file'] = nama_file_bersih
    gdf_list.append(temp_gdf)

# Menggabungkan Fitur Numerik dan Spasial
gdf_spasial = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
df_numerik = pd.read_csv('DataNumerik/cleanData/cleanData.csv')
gdf = pd.merge(gdf_spasial, df_numerik, left_on='nama_file', right_on='Kabupaten/Kota')
gdf.drop(columns=['nama_file'], inplace=True)

# Menyimpan Data yang Telah Digabungkan
output_dir = 'allData'
os.makedirs(output_dir, exist_ok=True)
gdf.to_csv(os.path.join(output_dir, 'data.csv'), index=False)