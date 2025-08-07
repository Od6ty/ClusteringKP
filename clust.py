import geopandas as gpd
import numpy as np
import matplotlib.patheffects as path_effects
from sklearn.preprocessing import StandardScaler
from sklearn_extra.cluster import KMedoids
import matplotlib.pyplot as plt
import folium
from allData import concatData # <-- Menggunakan file dependensi sesuai permintaan
from sklearn.metrics import silhouette_score

# --- 1. Memuat dan Mempersiapkan Data ---

# Memuat data dari file dependensi sesuai permintaan
df = concatData.gdf 

# Membuat GeoDataFrame dari DataFrame pandas
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# Menetapkan Sistem Referensi Koordinat (CRS) awal ke WGS84 (EPSG:4326)
gdf.crs = "EPSG:4326"

print("Memproyeksikan CRS untuk perhitungan centroid yang akurat...")
projected_crs = "EPSG:32748" # UTM Zone 48S cocok untuk Lampung
original_crs = gdf.crs

# Hitung centroid dalam CRS yang diproyeksikan (dalam satuan meter)
centroids_projected = gdf.to_crs(projected_crs).geometry.centroid

# Konversi titik centroid kembali ke CRS geografis asli (derajat lintang/bujur)
centroids_geographic = centroids_projected.to_crs(original_crs)

# Tetapkan koordinat lon/lat dari centroid yang telah dikonversi dengan benar
gdf['lon'] = centroids_geographic.x
gdf['lat'] = centroids_geographic.y
# --------------------------------------------------------------------

print("Data berhasil dimuat dan diproses menjadi GeoDataFrame.")
print(gdf.head())
print("\n")

# --- 2. Rekayasa dan Standardisasi Fitur ---

# Membuat fitur baru: rasio tenaga kesehatan per 1000 lansia
epsilon = 1e-6
gdf['rasio_layanan_kesehatan'] = (gdf['Total Nakes'] / (gdf['Jumlah Lansia'] + epsilon)) * 1000

# Memilih fitur numerik dan spasial yang akan digunakan untuk clustering
features = [
    'Kepadatan Penduduk per km persegi (Km2)',
    'Jumlah Penyakit Menular',
    'rasio_layanan_kesehatan',
    'lon',
    'lat'
]

X = gdf[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Fitur telah dipilih dan distandarisasi.")
print("Shape dari data yang distandarisasi:", X_scaled.shape)
print("\n")

# --- 3. Melakukan Clustering dan Evaluasi ---

print("Memulai clustering PAM...")
kmedoids = KMedoids(n_clusters=3, method='pam', random_state=42)
clusters = kmedoids.fit_predict(X_scaled)
gdf['cluster'] = clusters
print("Clustering PAM selesai.")

# --- EVALUASI DENGAN SILHOUETTE SCORE ---
silhouette_avg = silhouette_score(X_scaled, clusters)
print(f"Evaluasi Klaster Selesai.")
print(f"--> Silhouette Score untuk k=3 adalah: {silhouette_avg:.4f}")
# ----------------------------------------

print("Persebaran wilayah per klaster:")
print(gdf['cluster'].value_counts())
print("\n")

# --- 4. Menampilkan Medoid (Pusat Klaster) ---

medoid_indices = kmedoids.medoid_indices_
medoids = gdf.loc[medoid_indices]

print("--- Medoid untuk Setiap Klaster ---")
print(medoids[['Kabupaten/Kota', 'cluster'] + features])
print("\n")


# --- 5. Visualisasi Peta Statis dengan Matplotlib ---

print("Membuat peta statis...")
fig, ax = plt.subplots(1, 1, figsize=(15, 12))

gdf.plot(column='cluster',
         ax=ax,
         legend=True,
         categorical=True,
         cmap='tab10',
         legend_kwds={'title': "Klaster Risiko", 'loc': 'upper left'})

try:
    label_gdf = gdf.dissolve(by='Kabupaten/Kota', aggfunc='first')
except Exception as e:
    print(f"Tidak dapat melakukan dissolve, mungkin karena versi geopandas. Melanjutkan tanpa dissolve: {e}")
    label_gdf = gdf.drop_duplicates(subset='Kabupaten/Kota').set_index('Kabupaten/Kota')


for kabupaten, row in label_gdf.iterrows():
    representative_point = row.geometry.representative_point()
    plt.annotate(
        text=kabupaten,
        xy=(representative_point.x, representative_point.y),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=8,
        color='white',
        fontweight='bold',
        path_effects=[path_effects.withStroke(linewidth=2, foreground='black')]
    )

ax.set_title('Hasil Clustering Spasial Risiko Penyakit (n=3)', fontsize=16, pad=20)
ax.set_axis_off()
plt.tight_layout()
plt.show()


# --- 6. Visualisasi Peta Interaktif dengan Folium ---

print("Membuat peta interaktif...")
map_center = [gdf['lat'].mean(), gdf['lon'].mean()]
m = folium.Map(location=map_center, zoom_start=8, tiles='CartoDB positron')

max_cluster_val = gdf['cluster'].max()
threshold_scale = list(np.linspace(0, max_cluster_val + 1, 4))


choropleth = folium.Choropleth(
    geo_data=gdf.to_json(),
    data=gdf,
    columns=['Kabupaten/Kota', 'cluster'],
    key_on='feature.properties.Kabupaten/Kota',
    fill_color='Set1',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='ID Klaster Risiko',
    threshold_scale=threshold_scale,
    nan_fill_color="white"
).add_to(m)

tooltip_fields = [
    'Kabupaten/Kota',
    'cluster',
    'Kepadatan Penduduk per km persegi (Km2)',
    'Jumlah Penyakit Menular',
    'rasio_layanan_kesehatan'
]

tooltip = folium.features.GeoJsonTooltip(
    fields=tooltip_fields,
    aliases=[
        'Kabupaten/Kota:',
        'Klaster:',
        'Kepadatan Penduduk:',
        'Jumlah Penyakit Menular:',
        'Rasio Nakes/1000 Lansia:'
    ],
    sticky=True,
    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
)

tooltip.add_to(choropleth.geojson)
folium.LayerControl().add_to(m)

output_filename = 'cluster_pam_interaktif.html'
m.save(output_filename)