"""
Mesin Inferensi Certainty Factor (CF)
Implementasi metode CF untuk sistem pakar diagnosa penyakit jagung.

Rumus CF yang digunakan:
- CF kombinasi (berurutan): CF(H,E1,E2) = CF(H,E1) + CF(H,E2) * (1 - CF(H,E1))
- CF dengan evidence user: CF_final = CF_pakar * CF_user
- CF_user: 0.2 (tidak yakin), 0.4 (agak yakin), 0.6 (yakin), 0.8 (sangat yakin), 1.0 (pasti)
"""

from knowledge_base import RULES, PENYAKIT, GEJALA

# Skala keyakinan pengguna
CF_USER_SCALE = {
    "Tidak Yakin":   0.2,
    "Agak Yakin":    0.4,
    "Yakin":         0.6,
    "Sangat Yakin":  0.8,
    "Pasti":         1.0,
}

# Label untuk interpretasi hasil CF
CF_INTERPRETATION = [
    (0.8, 1.01, "Sangat Tinggi",  "#16a34a", "✅"),
    (0.6, 0.8,  "Tinggi",         "#65a30d", "🟢"),
    (0.4, 0.6,  "Sedang",         "#ca8a04", "🟡"),
    (0.2, 0.4,  "Rendah",         "#ea580c", "🟠"),
    (0.0, 0.2,  "Sangat Rendah",  "#dc2626", "🔴"),
]


def combine_cf(cf1: float, cf2: float) -> float:
    """
    Menggabungkan dua nilai CF menggunakan rumus kombinasi CF.
    CF_combine = CF1 + CF2 * (1 - CF1)
    """
    return cf1 + cf2 * (1 - cf1)


def calculate_cf_for_disease(penyakit_id: str, gejala_cf_user: dict) -> dict:
    """
    Menghitung CF total untuk satu penyakit berdasarkan gejala yang dipilih.
    
    Args:
        penyakit_id: ID penyakit yang dihitung
        gejala_cf_user: dict {gejala_id: cf_user_value} - gejala yg dipilih user
    
    Returns:
        dict berisi:
            - cf_total: nilai CF akhir
            - gejala_cocok: list gejala yang cocok dengan aturan
            - detail_hitung: list detail perhitungan untuk tiap gejala
    """
    if penyakit_id not in RULES:
        return {"cf_total": 0.0, "gejala_cocok": [], "detail_hitung": []}

    rules_penyakit = RULES[penyakit_id]
    cf_combined = 0.0
    gejala_cocok = []
    detail_hitung = []

    for gejala_id, cf_user in gejala_cf_user.items():
        if gejala_id in rules_penyakit:
            cf_pakar = rules_penyakit[gejala_id]
            
            # CF per gejala = CF_pakar * CF_user
            cf_gejala = cf_pakar * cf_user
            
            # Simpan detail sebelum kombinasi
            cf_sebelum = cf_combined
            
            # Kombinasikan dengan CF sebelumnya
            if cf_combined == 0.0:
                cf_combined = cf_gejala
            else:
                cf_combined = combine_cf(cf_combined, cf_gejala)
            
            gejala_cocok.append(gejala_id)
            detail_hitung.append({
                "gejala_id": gejala_id,
                "gejala_nama": GEJALA.get(gejala_id, ""),
                "cf_pakar": cf_pakar,
                "cf_user": cf_user,
                "cf_gejala": round(cf_gejala, 4),
                "cf_sebelum": round(cf_sebelum, 4),
                "cf_sesudah": round(cf_combined, 4),
            })

    return {
        "cf_total": round(cf_combined, 4),
        "gejala_cocok": gejala_cocok,
        "detail_hitung": detail_hitung,
    }


def run_inference(gejala_cf_user: dict, threshold: float = 0.1) -> list:
    """
    Menjalankan inferensi CF untuk semua penyakit.
    
    Args:
        gejala_cf_user: dict {gejala_id: cf_user_value}
        threshold: nilai CF minimum untuk ditampilkan (default 0.1)
    
    Returns:
        List hasil diagnosis diurutkan dari CF tertinggi.
        Setiap item adalah dict berisi info penyakit + CF.
    """
    hasil = []

    for penyakit_id, info_penyakit in PENYAKIT.items():
        result = calculate_cf_for_disease(penyakit_id, gejala_cf_user)
        
        if result["cf_total"] >= threshold and result["gejala_cocok"]:
            tingkat, warna, emoji = get_cf_interpretation(result["cf_total"])
            
            hasil.append({
                "penyakit_id": penyakit_id,
                "nama": info_penyakit["nama"],
                "nama_ilmiah": info_penyakit["nama_ilmiah"],
                "deskripsi": info_penyakit["deskripsi"],
                "penanganan": info_penyakit["penanganan"],
                "tingkat_bahaya": info_penyakit["tingkat_bahaya"],
                "kondisi_favorit": info_penyakit["kondisi_favorit"],
                "cf_total": result["cf_total"],
                "cf_persen": round(result["cf_total"] * 100, 2),
                "gejala_cocok": result["gejala_cocok"],
                "detail_hitung": result["detail_hitung"],
                "tingkat_keyakinan": tingkat,
                "warna_cf": warna,
                "emoji_cf": emoji,
            })

    # Urutkan dari CF tertinggi
    hasil.sort(key=lambda x: x["cf_total"], reverse=True)
    return hasil


def get_cf_interpretation(cf_value: float) -> tuple:
    """
    Mengembalikan (label, warna_hex, emoji) berdasarkan nilai CF.
    """
    for cf_min, cf_max, label, warna, emoji in CF_INTERPRETATION:
        if cf_min <= cf_value < cf_max:
            return label, warna, emoji
    return "Tidak Diketahui", "#6b7280", "❓"


def format_cf_steps(detail_hitung: list, penyakit_nama: str) -> str:
    """
    Memformat langkah-langkah perhitungan CF menjadi teks yang mudah dibaca.
    Berguna untuk laporan / tampilan perhitungan manual.
    """
    if not detail_hitung:
        return "Tidak ada gejala yang cocok."

    lines = [f"Perhitungan CF untuk: {penyakit_nama}", "=" * 50]

    for i, step in enumerate(detail_hitung):
        lines.append(f"\nGejala ke-{i+1}: [{step['gejala_id']}] {step['gejala_nama']}")
        lines.append(f"  CF Pakar   : {step['cf_pakar']}")
        lines.append(f"  CF User    : {step['cf_user']}")
        lines.append(f"  CF Gejala  : CF_pakar × CF_user = {step['cf_pakar']} × {step['cf_user']} = {step['cf_gejala']}")

        if i == 0:
            lines.append(f"  CF Awal    : {step['cf_sesudah']} (gejala pertama)")
        else:
            lines.append(f"  CF Kombinasi: CF_lama + CF_baru × (1 - CF_lama)")
            lines.append(f"              = {step['cf_sebelum']} + {step['cf_gejala']} × (1 - {step['cf_sebelum']})")
            lines.append(f"              = {step['cf_sesudah']}")

    lines.append(f"\n{'=' * 50}")
    lines.append(f"CF TOTAL: {detail_hitung[-1]['cf_sesudah']}")
    return "\n".join(lines)
