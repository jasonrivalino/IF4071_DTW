# Tugas 2 Pemrosesan Ucapan - IF4071
> Tugas 2.1: Eksplorasi Pemrosesan Suara dengan Dynamic Time Warping (DTW)

> Tugas 2.2: Sistem Pengenal Suara Generalized Template

## Anggota Kelompok
<table>
    <tr>
        <td>No.</td>
        <td>Nama</td>
        <td>NIM</td>
    </tr>
    <tr>
        <td>1.</td>
        <td>Jason Rivalino</td>
        <td>13521008</td>
    </tr>
    <tr>
        <td>2.</td>
        <td>Louis Caesa Kesuma</td>
        <td>13521069</td>
    </tr>
    </tr>
    <tr>
        <td>1.</td>
        <td>Satria Octavianus Nababan</td>
        <td>13521168</td>
    </tr>
    <tr>
        <td>2.</td>
        <td>Faris Fadhilah</td>
        <td>13518026</td>
    </tr>
</table>

## Table of Contents
* [Spesifikasi Tugas](#spesifikasi-tugas)
* [Struktur File](#struktur-file)
* [Requirements](#requirements)
* [Cara Menjalankan Program](#cara-menjalankan-program)
* [Acknowledgements](#acknowledgements)

## Spesifikasi Tugas
### Tugas 2.1
- Membuat sebuah sistem pengenal ucapan menggunakan DTW menggunakan bahasa pemrograman Python
- Ekstraksi fitur menggunakan MFCC 39 dimensi (https://python-speech-features.readthedocs.io/en/latest/)
- Dictionary berisi 5 vowel (a, i, u, e, o template direkam dari tiga orang anggota kelompok, data uji direkam dari 3 orang anggota kelompok)
- Lakukan perhitungan akurasi untuk skenario pengujian:
- Setiap template satu orang diuji dengan menggunakan suara dari 3 orang (1 suara yang sama dengan template dan dua suara yang berbeda dengan template)
- Lakukan analisis hasil eksperimen

### Tugas 2.2
- Membuat sebuah sistem pengenal ucapan menggunakan Average Template untuk mengenali bunyi a, i, u e, o
- Ekstraksi fitur menggunakan MFCC 39 dimensi
- Dictionary berisi 5 vowel (a, i, u, e, o)
- Template setiap vowel berasal dari perhitungan rata-rata audio yang direkam dari seluruh anggota kelas (diambil dari tugas sebelumya)
- Data uji: direkam dari 3 orang anggota kelompok (bisa diambil dari tugas sebelumnya), dan 3 suara lain di luar kelas ini.
- Lakukan perhitungan akurasi untuk skenario pengujian. Setiap average template satu vowel diuji dengan menggunakan suara dari:
  - 3 orang anggota kelompok (seen speakers)
  - 3 orang suara di luar kelas ini (unseen speakers)
- Lakukan analisis hasil eksperimen

## Struktur File
```
📦IF4071_DTW
 ┣ 📂ppt
 ┃ ┣ 📜Tugas 2_Eksperimen Pemrosesan Suara DTW_13521008_13521069_13521168_13518026.pdf
 ┃ ┗ 📜Tugas 2_Eksperimen Pemrosesan Suara DTW_13521008_13521069_13521168_13518026.pptx
 ┣ 📂src
 ┃ ┣ 📜dtw.py
 ┃ ┣ 📜main.py
 ┃ ┗ 📜mfcc.py
 ┣ 📂template
 ┃ ┣ 📂Faris (Template)
 ┃ ┣ 📂Jason (Template)
 ┃ ┣ 📂Louis (Template)
 ┃ ┗ 📂Satria (Template)
 ┣ 📂test
 ┃ ┣ 📂Faris (Test)
 ┃ ┣ 📂Jason (Test)
 ┃ ┣ 📂Louis (Test)
 ┃ ┗ 📂Satria (Test)
 ┣ 📜.gitignore
 ┗ 📜README.md
```

## Requirements
1. Visual Studio Code
2. Python (default version: 3.10.11)

## Cara Menjalankan Program
Langkah-langkah proses setup program adalah sebagai berikut:
1. Clone repository ini
2. Membuka folder root dari hasil clone, kemudian mengetikkan `py ./src/main.py` pada terminal untuk menjalankan file main
3. Program juga dapat dijalankan dengan membuka `main.py` yang terdapat pada folder src kemudian menekan tombol run pada Visual Studio Code

## Acknowledgements
- Tuhan Yang Maha Esa
- Ibu Dessi Puji Lestari sebagai Dosen Pemrosesan Ucapan IF4071
