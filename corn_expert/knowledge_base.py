"""
Basis Pengetahuan Sistem Pakar Diagnosa Penyakit Tanaman Jagung
Menggunakan metode Certainty Factor (CF)
"""

# ============================================================
# DATABASE GEJALA
# ============================================================
GEJALA = {
    # Gejala Daun
    "G01": "Bercak kecil berbentuk oval atau persegi panjang pada daun",
    "G02": "Bercak berwarna coklat keabu-abuan dengan tepi kuning pada daun",
    "G03": "Bercak daun berwarna coklat tua dengan halo kuning",
    "G04": "Daun menguning (klorosis) dimulai dari tepi daun",
    "G05": "Daun mengering dan berwarna coklat dari ujung",
    "G06": "Bercak berair (water-soaked lesion) pada daun",
    "G07": "Daun memiliki garis-garis kuning sejajar tulang daun",
    "G08": "Permukaan daun tertutup serbuk putih seperti tepung",
    "G09": "Bercak coklat kehitaman berbentuk tidak teratur pada daun",
    "G10": "Daun menunjukkan gejala mosaik (belang-belang kuning hijau)",

    # Gejala Batang
    "G11": "Batang membusuk dan berwarna coklat kehitaman",
    "G12": "Batang mudah patah/roboh (lodging)",
    "G13": "Jaringan dalam batang berwarna pink atau merah muda",
    "G14": "Terdapat massa spora (stroma) pada batang yang sakit",
    "G15": "Batang mengeluarkan lendir berbau busuk",
    "G16": "Ruas batang membengkak atau berubah bentuk",

    # Gejala Tongkol & Biji
    "G17": "Biji jagung berwarna hitam atau coklat gelap",
    "G18": "Biji tertutup lapisan jamur berwarna putih, abu, atau merah muda",
    "G19": "Tongkol mengalami pembusukan dari ujung",
    "G20": "Biji mengkerut dan tidak berkembang sempurna",
    "G21": "Tongkol tertutup massa spora hitam (seperti arang)",
    "G22": "Biji memiliki bintik-bintik hitam kecil",

    # Gejala Akar
    "G23": "Akar berwarna coklat kehitaman dan membusuk",
    "G24": "Akar tidak berkembang sempurna (kerdil)",
    "G25": "Akar adventif tumbuh di atas permukaan tanah",

    # Gejala Umum Tanaman
    "G26": "Tanaman tumbuh kerdil (stunting)",
    "G27": "Tanaman layu meskipun cukup air (wilt)",
    "G28": "Tanaman mati mendadak (sudden death)",
    "G29": "Daun bagian bawah tanaman lebih dulu menunjukkan gejala",
    "G30": "Gejala menyebar dari tepi lahan ke dalam",
    "G31": "Tanaman menunjukkan gejala pada musim hujan/lembab",
    "G32": "Terdapat serangga vektor (wereng, kutudaun) pada tanaman",
    "G33": "Gejala muncul pada fase vegetatif muda",
    "G34": "Ujung tongkol tidak terisi biji (bare tip)",
    "G35": "Terdapat eksudat berwarna oranye atau merah pada jaringan",
}

# ============================================================
# DATABASE PENYAKIT
# ============================================================
PENYAKIT = {
    "P01": {
        "nama": "Hawar Daun Utara (Northern Leaf Blight)",
        "nama_ilmiah": "Exserohilum turcicum",
        "deskripsi": "Penyakit jamur yang menyebabkan bercak panjang berbentuk cerutu pada daun. Salah satu penyakit daun jagung yang paling umum dan merusak di daerah beriklim sedang hingga tropis.",
        "penanganan": [
            "Gunakan varietas jagung tahan penyakit (benih bersertifikat)",
            "Lakukan rotasi tanaman dengan tanaman bukan inang selama 1-2 musim",
            "Aplikasikan fungisida berbahan aktif mankozeb atau propikonazol",
            "Atur jarak tanam agar sirkulasi udara baik (75 x 20 cm)",
            "Musnahkan sisa tanaman sakit setelah panen",
            "Hindari penanaman saat kelembaban tinggi berkepanjangan",
        ],
        "tingkat_bahaya": "Tinggi",
        "kondisi_favorit": "Suhu 18-27°C, kelembaban > 90%, angin kencang",
    },
    "P02": {
        "nama": "Hawar Daun Selatan (Southern Leaf Blight)",
        "nama_ilmiah": "Bipolaris maydis",
        "deskripsi": "Penyakit jamur yang berkembang pesat pada kondisi panas dan lembab. Menyebabkan bercak daun yang lebih kecil dibanding hawar utara dan dapat menyerang tongkol.",
        "penanganan": [
            "Tanam varietas resisten ras O (bukan Texas Male Sterile Cytoplasm)",
            "Aplikasikan fungisida propikonazol atau azoksistrobin",
            "Kurangi kelembaban dengan pengaturan irigasi yang tepat",
            "Lakukan sanitasi lahan dari sisa tanaman terinfeksi",
            "Penanaman lebih awal untuk menghindari kondisi panas-lembab",
        ],
        "tingkat_bahaya": "Tinggi",
        "kondisi_favorit": "Suhu > 30°C, kelembaban tinggi, malam hari hangat",
    },
    "P03": {
        "nama": "Karat Jagung (Corn Rust)",
        "nama_ilmiah": "Puccinia sorghi",
        "deskripsi": "Penyakit jamur yang ditandai pustul berwarna oranye kecoklatan pada permukaan daun. Spora menyebar melalui angin dan dapat mengurangi hasil panen secara signifikan.",
        "penanganan": [
            "Gunakan fungisida berbahan aktif triazol (propikonazol, tebukonazol)",
            "Aplikasikan fungisida preventif saat tanaman fase V6-V8",
            "Pilih varietas jagung dengan gen resistensi Rp1",
            "Monitor tanaman secara rutin terutama saat musim hujan",
            "Hindari irigasi di atas tajuk tanaman",
        ],
        "tingkat_bahaya": "Sedang",
        "kondisi_favorit": "Suhu 16-23°C, embun pagi, angin",
    },
    "P04": {
        "nama": "Busuk Batang Fusarium (Fusarium Stalk Rot)",
        "nama_ilmiah": "Fusarium verticillioides / F. graminearum",
        "deskripsi": "Penyakit jamur pada batang yang menyebabkan pembusukan jaringan dalam batang berwarna pink. Menyebabkan tanaman mudah roboh dan kehilangan hasil panen yang signifikan.",
        "penanganan": [
            "Pertahankan keseimbangan nutrisi N-P-K, hindari kelebihan nitrogen",
            "Lakukan irigasi yang cukup terutama saat pengisian biji",
            "Kendalikan serangga penggerek batang (Ostrinia furnacalis)",
            "Gunakan seed treatment fungisida berbahan aktif tiabendazol",
            "Panen tepat waktu untuk mengurangi paparan penyakit",
            "Rotasi tanaman dengan kedelai atau kacang-kacangan",
        ],
        "tingkat_bahaya": "Tinggi",
        "kondisi_favorit": "Stres kekeringan + periode panas, luka mekanis",
    },
    "P05": {
        "nama": "Busuk Batang Diplodia (Diplodia Stalk Rot)",
        "nama_ilmiah": "Stenocarpella maydis",
        "deskripsi": "Penyakit jamur yang menyebabkan busuk batang dengan adanya piknidia (titik hitam kecil) pada jaringan yang terinfeksi. Sering menyerang menjelang panen.",
        "penanganan": [
            "Hindari stres tanaman (kekeringan, kelebihan N, kerapatan tinggi)",
            "Gunakan varietas dengan ketahanan terhadap busuk batang",
            "Kendalikan penggerek batang sebagai pintu masuk infeksi",
            "Lakukan panen lebih awal jika gejala terdeteksi",
            "Sanitasi lahan dari sisa tanaman terinfeksi",
        ],
        "tingkat_bahaya": "Sedang-Tinggi",
        "kondisi_favorit": "Stres pasca-silking, suhu hangat dan lembab",
    },
    "P06": {
        "nama": "Busuk Tongkol Fusarium (Fusarium Ear Rot)",
        "nama_ilmiah": "Fusarium verticillioides",
        "deskripsi": "Penyakit yang menyerang tongkol jagung menyebabkan biji berwarna merah muda atau putih. Menghasilkan mikotoksin fumonisin yang berbahaya bagi kesehatan manusia dan hewan.",
        "penanganan": [
            "Kendalikan serangga pada tongkol (Helicoverpa armigera)",
            "Panen segera saat kadar air biji ≤ 25%",
            "Keringkan jagung secepatnya hingga kadar air < 14%",
            "Simpan di tempat kering dengan aerasi baik",
            "Gunakan fungisida saat pemasakan susu (R3)",
            "Hindari kerusakan mekanis pada tongkol",
        ],
        "tingkat_bahaya": "Tinggi (ancaman keamanan pangan)",
        "kondisi_favorit": "Luka serangga pada tongkol, kelembaban saat panen",
    },
    "P07": {
        "nama": "Gosong Jagung (Corn Smut / Common Smut)",
        "nama_ilmiah": "Ustilago maydis",
        "deskripsi": "Penyakit jamur unik yang membentuk tumor/gal berisi spora hitam pada bagian tanaman yang diserang. Di beberapa negara (huitlacoche) dianggap sebagai bahan makanan.",
        "penanganan": [
            "Buang dan musnahkan gal sebelum pecah dan menyebarkan spora",
            "Hindari luka mekanis pada tanaman saat budidaya",
            "Jangan gunakan pupuk nitrogen berlebihan",
            "Gunakan seed treatment fungisida sebelum tanam",
            "Rotasi tanaman minimal 2 tahun",
            "Hindari irigasi di atas tajuk",
        ],
        "tingkat_bahaya": "Sedang",
        "kondisi_favorit": "Suhu hangat, luka pada jaringan tanaman",
    },
    "P08": {
        "nama": "Layu Stewart (Stewart's Wilt)",
        "nama_ilmiah": "Pantoea stewartii",
        "deskripsi": "Penyakit bakteri yang ditularkan oleh kutudaun jagung (Cicadulina mbila). Menyebabkan garis-garis kuning pada daun dan layu pada tanaman muda yang dapat mematikan.",
        "penanganan": [
            "Kendalikan serangga vektor (kutudaun) dengan insektisida sistemik",
            "Gunakan seed treatment insektisida (imidakloprid, tiametoksam)",
            "Tanam varietas tahan penyakit layu stewart",
            "Lakukan penanaman serempak untuk mengurangi sumber inokulum",
            "Monitor populasi serangga vektor di lapangan",
        ],
        "tingkat_bahaya": "Tinggi (terutama fase seedling)",
        "kondisi_favorit": "Musim panas kering, populasi kutudaun tinggi",
    },
    "P09": {
        "nama": "Busuk Akar Pythium (Pythium Root Rot)",
        "nama_ilmiah": "Pythium spp.",
        "deskripsi": "Penyakit yang disebabkan oleh oomycete yang menyerang akar dan pangkal batang jagung muda. Sangat merusak pada kondisi tanah tergenang dan suhu rendah.",
        "penanganan": [
            "Perbaiki drainase lahan untuk mencegah genangan air",
            "Hindari penanaman di tanah terlalu basah",
            "Gunakan seed treatment dengan metalaksil atau mefenoksam",
            "Tanam saat suhu tanah > 15°C",
            "Kurangi kepadatan populasi tanaman",
            "Hindari pemupukan nitrogen berlebihan pada lahan basah",
        ],
        "tingkat_bahaya": "Sedang",
        "kondisi_favorit": "Tanah tergenang, suhu dingin, drainase buruk",
    },
    "P10": {
        "nama": "Virus Mosaik Jagung (Maize Dwarf Mosaic Virus - MDMV)",
        "nama_ilmiah": "Maize dwarf mosaic virus",
        "deskripsi": "Penyakit virus yang ditularkan oleh kutudaun dalam cara non-persisten. Menyebabkan mosaik kuning-hijau pada daun, kerdil, dan penurunan hasil panen yang drastis.",
        "penanganan": [
            "Kendalikan kutudaun vektor dengan insektisida kontak",
            "Gunakan mulsa reflektif untuk mengusir kutudaun",
            "Eradikasi tanaman sakit segera setelah terdeteksi",
            "Jauhkan pertanaman dari gulma inang virus",
            "Tidak ada obat untuk tanaman yang terinfeksi virus",
            "Gunakan benih bersertifikat bebas virus",
        ],
        "tingkat_bahaya": "Tinggi (tidak dapat disembuhkan)",
        "kondisi_favorit": "Musim kemarau, populasi kutudaun tinggi",
    },
    "P11": {
        "nama": "Blight Daun Kabur (Gray Leaf Spot)",
        "nama_ilmiah": "Cercospora zeae-maydis",
        "deskripsi": "Penyakit jamur yang menyebabkan lesi abu-abu panjang sejajar dengan tulang daun. Berkembang pesat pada kondisi lembab dan hangat, terutama di dataran tinggi.",
        "penanganan": [
            "Aplikasikan fungisida strobilurin (azoksistrobin, piraklostrobin)",
            "Gunakan varietas dengan ketahanan parsial",
            "Tingkatkan sirkulasi udara dengan jarak tanam yang tepat",
            "Kurangi irigasi berlebihan yang meningkatkan kelembaban",
            "Rotasi tanaman untuk mengurangi sumber inokulum",
        ],
        "tingkat_bahaya": "Sedang-Tinggi",
        "kondisi_favorit": "Suhu 25-30°C, kelembaban > 95%, embun pagi",
    },
    "P12": {
        "nama": "Embun Tepung (Powdery Mildew)",
        "nama_ilmiah": "Peronosclerospora spp.",
        "deskripsi": "Penyakit yang menyebabkan lapisan serbuk putih pada permukaan daun. Pada jagung lebih sering terjadi di daerah dengan kelembaban tinggi dan suhu sedang.",
        "penanganan": [
            "Aplikasikan fungisida berbahan sulfur atau triazol",
            "Gunakan varietas tahan embun tepung",
            "Tingkatkan sirkulasi udara di pertanaman",
            "Hindari pemupukan nitrogen berlebihan",
            "Lakukan sanitasi lahan secara rutin",
        ],
        "tingkat_bahaya": "Rendah-Sedang",
        "kondisi_favorit": "Kelembaban tinggi, suhu 20-25°C, teduh",
    },
}

# ============================================================
# ATURAN PRODUKSI (Rules) dengan Nilai CF Pakar
# Format: {penyakit_id: {gejala_id: CF_pakar}}
# CF Pakar: 0.0 - 1.0 (keyakinan pakar terhadap hubungan gejala-penyakit)
# ============================================================
RULES = {
    "P01": {  # Hawar Daun Utara
        "G01": 0.8,   # Bercak oval/persegi panjang - sangat khas
        "G02": 0.9,   # Bercak abu-abu dengan halo kuning - sangat khas
        "G05": 0.5,   # Daun mengering
        "G31": 0.4,   # Musim hujan/lembab
        "G29": 0.6,   # Daun bawah dulu
    },
    "P02": {  # Hawar Daun Selatan
        "G01": 0.6,   # Bercak oval (lebih kecil dari P01)
        "G03": 0.8,   # Bercak coklat tua dengan halo kuning
        "G17": 0.5,   # Biji berwarna gelap (jika menyerang tongkol)
        "G31": 0.5,   # Musim hujan
        "G29": 0.4,   # Daun bawah dulu
    },
    "P03": {  # Karat Jagung
        "G35": 0.9,   # Eksudat oranye/merah (pustul karat)
        "G09": 0.7,   # Bercak coklat kehitaman
        "G31": 0.5,   # Musim lembab
        "G30": 0.4,   # Menyebar dari tepi
    },
    "P04": {  # Busuk Batang Fusarium
        "G11": 0.8,   # Batang membusuk
        "G12": 0.9,   # Batang mudah patah (lodging)
        "G13": 0.9,   # Jaringan dalam berwarna pink/merah muda - sangat khas
        "G27": 0.7,   # Tanaman layu
        "G23": 0.5,   # Akar membusuk
    },
    "P05": {  # Busuk Batang Diplodia
        "G11": 0.8,   # Batang membusuk
        "G12": 0.8,   # Batang mudah patah
        "G14": 0.9,   # Massa spora/stroma pada batang - sangat khas
        "G27": 0.6,   # Tanaman layu
        "G05": 0.4,   # Daun mengering
    },
    "P06": {  # Busuk Tongkol Fusarium
        "G18": 0.9,   # Biji tertutup jamur pink/putih - sangat khas
        "G17": 0.7,   # Biji berwarna gelap
        "G19": 0.8,   # Tongkol membusuk dari ujung
        "G20": 0.6,   # Biji mengkerut
        "G34": 0.5,   # Bare tip
    },
    "P07": {  # Gosong Jagung
        "G21": 1.0,   # Massa spora hitam - SANGAT KHAS (diagnostik)
        "G16": 0.8,   # Batang/bagian membengkak
        "G20": 0.6,   # Biji tidak berkembang sempurna
    },
    "P08": {  # Layu Stewart
        "G07": 0.9,   # Garis kuning sejajar tulang daun - sangat khas
        "G27": 0.8,   # Tanaman layu
        "G26": 0.7,   # Tanaman kerdil
        "G32": 0.8,   # Serangga vektor
        "G33": 0.7,   # Gejala fase vegetatif muda
        "G06": 0.6,   # Bercak berair
    },
    "P09": {  # Busuk Akar Pythium
        "G23": 0.9,   # Akar membusuk - sangat khas
        "G24": 0.7,   # Akar tidak berkembang
        "G26": 0.7,   # Tanaman kerdil
        "G27": 0.6,   # Tanaman layu
        "G28": 0.5,   # Mati mendadak
        "G33": 0.6,   # Fase vegetatif muda
    },
    "P10": {  # Virus Mosaik
        "G10": 0.9,   # Mosaik kuning-hijau - sangat khas
        "G07": 0.7,   # Garis kuning sejajar tulang daun
        "G26": 0.8,   # Tanaman kerdil
        "G32": 0.7,   # Serangga vektor (kutudaun)
        "G20": 0.5,   # Biji tidak berkembang
    },
    "P11": {  # Gray Leaf Spot
        "G02": 0.7,   # Bercak abu-abu dengan tepi kuning
        "G04": 0.6,   # Daun menguning
        "G31": 0.6,   # Musim hujan/lembab
        "G05": 0.5,   # Daun mengering
        "G29": 0.5,   # Daun bawah dulu
    },
    "P12": {  # Embun Tepung
        "G08": 1.0,   # Serbuk putih - SANGAT KHAS (diagnostik)
        "G04": 0.5,   # Daun menguning
        "G26": 0.3,   # Kerdil (jika parah)
    },
}

# ============================================================
# HELPER: Gejala yang relevan per penyakit
# ============================================================
def get_gejala_untuk_penyakit(penyakit_id: str) -> dict:
    """Mengembalikan dict {gejala_id: keterangan} untuk suatu penyakit"""
    result = {}
    if penyakit_id in RULES:
        for gejala_id in RULES[penyakit_id]:
            if gejala_id in GEJALA:
                result[gejala_id] = GEJALA[gejala_id]
    return result

def get_all_gejala_sorted() -> list:
    """Mengembalikan semua gejala diurutkan berdasarkan ID"""
    return [(k, v) for k, v in sorted(GEJALA.items())]
