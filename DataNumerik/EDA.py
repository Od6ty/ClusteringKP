import pandas as pd
import os

#EDA
data1 = pd.read_csv('DataNumerik/rawData/jumlahPenduduk.csv')
jumlah_lansia = int(data1['Jumlah (Ribu)'].iloc[12:16].sum() * 1000)
jumlahPenduduk = int(data1['Jumlah (Ribu)'][16]*1000)
data2 = pd.read_csv('DataNumerik/rawData/jumlahNakes.csv')
data2['Total Nakes'] = data2[['Tenaga Kesehatan - Perawat', 'Tenaga Kesehatan - Bidan', 'Tenaga Kesehatan - Tenaga Kefarmasian','Tenaga Kesehatan - Tenaga Kesehatan Masyarakat','Tenaga Kesehatan - Tenaga Kesehatan Lingkungan','Tenaga Kesehatan - Tenaga Gizi']].sum(axis=1)
data3 = pd.read_csv('DataNumerik/rawData/kepadatanPenduduk.csv')
data3['Jumlah Lansia'] = (data3['Persentase Penduduk'] / 100) * jumlah_lansia
data3['Jumlah Lansia'] = data3['Jumlah Lansia'].astype(int)
jumlahPenduduk = int(data1['Jumlah (Ribu)'][16]*1000)
data5 = pd.read_csv('DataNumerik/rawData/sebaranPenyakit.csv')
data5 = data5.fillna(0)
data5['Jumlah Kasus Penyakit Kusta'] = data5['Jumlah Kasus Penyakit Kusta']*jumlahPenduduk/100000
data5['Jumlah Kasus Penyakit Kusta'] = data5['Jumlah Kasus Penyakit Kusta'].astype(int)
data5['Jumlah Kasus Penyakit Malaria'] = data5['Jumlah Kasus Penyakit Malaria']*jumlahPenduduk/1000
data5['Jumlah Kasus Penyakit Malaria'] = data5['Jumlah Kasus Penyakit Malaria'].astype(int)
data5['Jumlah Kasus Penyakit DBD'] = data5['Jumlah Kasus Penyakit DBD']*jumlahPenduduk/100000
data5['Jumlah Kasus Penyakit DBD'] = data5['Jumlah Kasus Penyakit DBD'].astype(int)
data5['Jumlah Penyakit Menular'] = data5['Jumlah Kasus Penyakit Malaria']+data5['Jumlah Kasus Penyakit DBD']
data5['Jumlah Penyakit Menular'] = data5['Jumlah Penyakit Menular'].astype(int)
kolom= [
    data2['Kabupaten/Kota'],
    data2['Total Nakes'],
    data3['Jumlah Lansia'],
    data3['Kepadatan Penduduk per km persegi (Km2)'],
    data5['Jumlah Penyakit Menular']
]
data = pd.concat(kolom,axis=1)
data = data[:15]
data['Kabupaten/Kota'] = data['Kabupaten/Kota'].str.replace(' ', '_')

#Simpan Data Hasil EDA
output_dir = 'DataNumerik/cleanData'
os.makedirs(output_dir, exist_ok=True)
data.to_csv(os.path.join(output_dir, 'cleanData.csv'), index=False)