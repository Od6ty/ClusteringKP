import pandas as pd
import os

data_penduduk_total = pd.read_csv('DataNumerik/rawData/jumlahPenduduk.csv')
data_nakes = pd.read_csv('DataNumerik/rawData/jumlahNakes.csv')
data_kependudukan = pd.read_csv('DataNumerik/rawData/kepadatanPenduduk.csv')
data_penyakit = pd.read_csv('DataNumerik/rawData/sebaranPenyakit.csv')
jumlah_lansia = int(data_penduduk_total['Jumlah (Ribu)'].iloc[12:16].sum() * 1000)
data_nakes_bersih = data_nakes[:15].copy()
data_kependudukan_bersih = data_kependudukan[:15].copy()
data_penyakit_bersih = data_penyakit[:15].copy()
df_master = data_kependudukan_bersih.copy()
df_master = pd.merge(df_master, data_nakes_bersih, on='Kabupaten/Kota', how='left')
df_master = pd.merge(df_master, data_penyakit_bersih, on='Kabupaten/Kota', how='left')
kolom_nakes = [
    'Tenaga Kesehatan - Perawat', 'Tenaga Kesehatan - Bidan', 'Tenaga Kesehatan - Tenaga Kefarmasian',
    'Tenaga Kesehatan - Tenaga Kesehatan Masyarakat','Tenaga Kesehatan - Tenaga Kesehatan Lingkungan','Tenaga Kesehatan - Tenaga Gizi'
]
df_master['Total Nakes'] = df_master[kolom_nakes].sum(axis=1)
df_master['Jumlah Lansia'] = (df_master['Persentase Penduduk'] / 100) * jumlah_lansia
df_master['Jumlah Penduduk (Ribu)'] = df_master['Jumlah Penduduk (Ribu)']*1000
df_master['Jumlah Kasus Penyakit Malaria'] = df_master['Jumlah Kasus Penyakit Malaria'] * df_master['Jumlah Penduduk (Ribu)'] / 1000
df_master['Jumlah Kasus Penyakit DBD'] = df_master['Jumlah Kasus Penyakit DBD'] * df_master['Jumlah Penduduk (Ribu)'] / 100000

df_master['Jumlah Penyakit Menular'] = df_master['Jumlah Kasus Penyakit Malaria'].fillna(0) + df_master['Jumlah Kasus Penyakit DBD'].fillna(0)

kolom_final = [
    'Kabupaten/Kota',
    'Total Nakes',
    'Jumlah Lansia',
    'Kepadatan Penduduk per km persegi (Km2)',
    'Jumlah Penyakit Menular'
]
df_clean = df_master[kolom_final].copy()

# Ubah tipe data menjadi integer setelah semua perhitungan selesai
df_clean['Total Nakes'] = df_clean['Total Nakes'].astype(int)
df_clean['Jumlah Lansia'] = df_clean['Jumlah Lansia'].astype(int)
df_clean['Jumlah Penyakit Menular'] = df_clean['Jumlah Penyakit Menular'].astype(int)

# Ganti spasi pada nama kabupaten/kota
df_clean['Kabupaten/Kota'] = df_clean['Kabupaten/Kota'].str.replace(' ', '_')
output_dir = 'DataNumerik/cleanData'
os.makedirs(output_dir, exist_ok=True)
df_clean.to_csv(os.path.join(output_dir, 'cleanData.csv'), index=False)

print(f"Proses EDA selesai. Jumlah lansia yang digunakan: {jumlah_lansia}")
print("File cleanData.csv berhasil disimpan.")