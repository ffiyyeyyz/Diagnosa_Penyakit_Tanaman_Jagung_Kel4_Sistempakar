# 🌽 SiPakar — Sistem Pakar Diagnosa Penyakit Tanaman Jagung

> Proyek Akhir Mata Kuliah Sistem Pakar  
> Metode: **Certainty Factor (CF)**

---

## 📦 Struktur Proyek

```
corn_expert/
├── app.py               # Aplikasi Streamlit (entry point)
├── knowledge_base.py    # Basis pengetahuan (gejala, penyakit, aturan CF)
├── cf_engine.py         # Mesin inferensi Certainty Factor
├── report_generator.py  # Generator laporan (TXT & PDF)
├── requirements.txt     # Daftar dependencies
└── README.md            # Dokumentasi ini
```

---

## ⚙️ Instalasi & Menjalankan

```bash
# 1. Clone / salin folder proyek
cd corn_expert

# 2. Install semua dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

---

## 🧠 Metode Certainty Factor

### Rumus Dasar
```
CF(H, E) = CF_pakar × CF_user
```

### Rumus Kombinasi (beberapa gejala)
```
CF_kombinasi(H, E1∧E2) = CF(H,E1) + CF(H,E2) × (1 - CF(H,E1))
```

### Skala Keyakinan Pengguna
| Label         | Nilai CF |
|---------------|----------|
| Tidak Yakin   | 0.2      |
| Agak Yakin    | 0.4      |
| Yakin         | 0.6      |
| Sangat Yakin  | 0.8      |
| Pasti         | 1.0      |

---

## 🗂 Basis Pengetahuan

### Penyakit (12)
| ID  | Nama Penyakit                        | Patogen                          |
|-----|--------------------------------------|----------------------------------|
| P01 | Hawar Daun Utara                     | Exserohilum turcicum             |
| P02 | Hawar Daun Selatan                   | Bipolaris maydis                 |
| P03 | Karat Jagung                         | Puccinia sorghi                  |
| P04 | Busuk Batang Fusarium                | Fusarium verticillioides         |
| P05 | Busuk Batang Diplodia                | Stenocarpella maydis             |
| P06 | Busuk Tongkol Fusarium               | Fusarium verticillioides         |
| P07 | Gosong Jagung                        | Ustilago maydis                  |
| P08 | Layu Stewart                         | Pantoea stewartii                |
| P09 | Busuk Akar Pythium                   | Pythium spp.                     |
| P10 | Virus Mosaik Jagung (MDMV)           | Maize dwarf mosaic virus         |
| P11 | Gray Leaf Spot                       | Cercospora zeae-maydis           |
| P12 | Embun Tepung                         | Peronosclerospora spp.           |

### Gejala (35)
Gejala dikelompokkan menjadi 5 kategori:
- **G01–G10**: Gejala Daun
- **G11–G16**: Gejala Batang
- **G17–G22**: Gejala Tongkol & Biji
- **G23–G25**: Gejala Akar
- **G26–G35**: Gejala Umum Tanaman

---

## ✨ Fitur Aplikasi

| Fitur | Deskripsi |
|-------|-----------|
| 🔍 Diagnosa Penyakit | Input gejala dengan skala keyakinan, inferensi CF otomatis |
| 📊 Visualisasi CF | Bar chart, radar chart, pie chart hasil diagnosa |
| 🧮 Detail Perhitungan | Langkah-langkah perhitungan CF step-by-step |
| 📄 Laporan | Export hasil diagnosa ke TXT dan PDF |
| 📜 History Konsultasi | Riwayat semua sesi konsultasi + export JSON |
| 📊 Basis Pengetahuan | Tampilan daftar penyakit, gejala, dan matriks aturan |

---

## 📖 Referensi

- Shortliffe, E.H. & Buchanan, B.G. (1975). *A model of inexact reasoning in medicine*
- CIMMYT (2004). *Maize Diseases: A Guide for Field Identification*
- Direktorat Perlindungan Tanaman Pangan, Kementerian Pertanian RI
- Jurnal Fitopatologi Indonesia, Vol. 13-18

---

*Sistem Pakar Penyakit Tanaman Jagung — Mata Kuliah Sistem Pakar*
