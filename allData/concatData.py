import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import matplotlib.patheffects as PathEffects

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

output_dir = 'allData'
os.makedirs(output_dir, exist_ok=True)
# --- PETA 1: JUMLAH PENYAKIT MENULAR ---
fig1, ax1 = plt.subplots(1, 1, figsize=(15, 10))
gdf.plot(column='Jumlah Penyakit Menular', cmap='Reds', linewidth=0.8, ax=ax1, edgecolor='0.8', legend=True)
ax1.set_title('Peta Sebaran Jumlah Penyakit Menular di Lampung', fontsize=16)
ax1.axis('off')

# Menambahkan label unik
added_labels_1 = []
for idx, row in gdf.iterrows():
    kab_kota = row['Kabupaten/Kota']
    if kab_kota not in added_labels_1:
        ax1.annotate(text=kab_kota, xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                     horizontalalignment='center', fontsize=9, color='black',
                     path_effects=[PathEffects.withStroke(linewidth=2, foreground='white')])
        added_labels_1.append(kab_kota)

# Menyimpan gambar peta 1
output_path1 = os.path.join(output_dir, 'peta_penyakit_menular.png')
plt.savefig(output_path1, dpi=300, bbox_inches='tight')

# --- PETA 2: TOTAL TENAGA KESEHATAN ---
fig2, ax2 = plt.subplots(1, 1, figsize=(15, 10))
gdf.plot(column='Total Nakes', cmap='Greens', linewidth=0.8, ax=ax2, edgecolor='0.8', legend=True)
ax2.set_title('Peta Sebaran Total Tenaga Kesehatan di Lampung', fontsize=16)
ax2.axis('off')

# Menambahkan label unik
added_labels_2 = []
for idx, row in gdf.iterrows():
    kab_kota = row['Kabupaten/Kota']
    if kab_kota not in added_labels_2:
        ax2.annotate(text=kab_kota, xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                     horizontalalignment='center', fontsize=9, color='black',
                     path_effects=[PathEffects.withStroke(linewidth=2, foreground='white')])
        added_labels_2.append(kab_kota)

# Menyimpan gambar peta 2
output_path2 = os.path.join(output_dir, 'peta_tenaga_kesehatan.png')
plt.savefig(output_path2, dpi=300, bbox_inches='tight')

# --- PETA 3: KEPADATAN PENDUDUK ---
fig3, ax3 = plt.subplots(1, 1, figsize=(15, 10))
gdf.plot(column='Kepadatan Penduduk per km persegi (Km2)', cmap='Blues', linewidth=0.8, ax=ax3, edgecolor='0.8', legend=True)
ax3.set_title('Peta Sebaran Kepadatan Penduduk di Lampung', fontsize=16)
ax3.axis('off')

# Menambahkan label unik
added_labels_3 = []
for idx, row in gdf.iterrows():
    kab_kota = row['Kabupaten/Kota']
    if kab_kota not in added_labels_3:
        ax3.annotate(text=kab_kota, xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                     horizontalalignment='center', fontsize=9, color='black',
                     path_effects=[PathEffects.withStroke(linewidth=2, foreground='white')])
        added_labels_3.append(kab_kota)

# Menyimpan gambar peta 3
output_path3 = os.path.join(output_dir, 'peta_kepadatan_penduduk.png')
plt.savefig(output_path3, dpi=300, bbox_inches='tight')

# Menampilkan semua plot
plt.show()

# Menyimpan Data yang Telah Digabungkan
output_dir = 'allData'
os.makedirs(output_dir, exist_ok=True)
gdf.to_csv(os.path.join(output_dir, 'data.csv'), index=False)