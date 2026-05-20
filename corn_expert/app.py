"""
Aplikasi Streamlit: Sistem Pakar Diagnosa Penyakit Tanaman Jagung
Menggunakan metode Certainty Factor (CF)

Jalankan dengan: streamlit run app.py
"""

import streamlit as st
import json
import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from knowledge_base import GEJALA, PENYAKIT, RULES, get_all_gejala_sorted
from cf_engine import run_inference, CF_USER_SCALE, format_cf_steps
from report_generator import generate_text_report, REPORTLAB_AVAILABLE

try:
    from report_generator import generate_pdf_report
except Exception:
    REPORTLAB_AVAILABLE = False

# ─────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="SiPakar Jagung 🌽",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS KUSTOM
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* Tema Hijau Pertanian */
    :root {
        --hijau-tua: #14532d;
        --hijau-med: #16a34a;
        --hijau-muda: #dcfce7;
        --kuning: #ca8a04;
    }

    .main-header {
        background: linear-gradient(135deg, #14532d 0%, #15803d 50%, #16a34a 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(20,83,45,0.3);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #bbf7d0 !important;
        font-size: 1rem;
    }

    .card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .result-card-1 {
        border-left: 5px solid #16a34a;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }
    .result-card-2 {
        border-left: 5px solid #65a30d;
        background: linear-gradient(135deg, #f7fee7 0%, #ecfccb 100%);
    }
    .result-card-3 {
        border-left: 5px solid #ca8a04;
        background: linear-gradient(135deg, #fffbeb 0%, #fef9c3 100%);
    }

    .cf-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .gejala-tag {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        font-size: 0.78rem;
        margin: 0.15rem;
        border: 1px solid #86efac;
    }

    /* ✅ FIX #2: Step-box dengan background gelap agar teks terlihat jelas */
    .step-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.82rem;
        color: #e2e8f0;
        white-space: pre-wrap;
        overflow-x: auto;
    }

    .sidebar-info {
        background: #f0fdf4;
        border-radius: 8px;
        padding: 0.8rem;
        border: 1px solid #86efac;
        margin-top: 1rem;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #16a34a, #4ade80);
    }
    .metric-card {
        background: linear-gradient(135deg, #f0fdf4, white);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #86efac;
    }

    /* ✅ FIX #4: Skala keyakinan CF di sidebar — background gelap, teks putih */
    .skala-cf-box {
        background: #14532d;
        border-radius: 8px;
        padding: 0.8rem;
        border: 1px solid #16a34a;
        margin-top: 1rem;
        color: #f0fdf4;
    }
    .skala-cf-box b {
        color: #bbf7d0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# STATE MANAGEMENT
# ─────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "gejala_dipilih" not in st.session_state:
    st.session_state.gejala_dipilih = {}
if "hasil_diagnosa" not in st.session_state:
    st.session_state.hasil_diagnosa = []
if "nama_petani" not in st.session_state:
    st.session_state.nama_petani = ""
if "lokasi" not in st.session_state:
    st.session_state.lokasi = ""


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌽 SiPakar — Sistem Pakar Penyakit Tanaman Jagung</h1>
    <p>Diagnosa berbasis Metode Certainty Factor (CF) | 12 Penyakit · 35 Gejala</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# SIDEBAR — Navigasi & Info
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗂 Menu Navigasi")
    halaman = st.radio(
        "",
        ["🔍 Diagnosa Penyakit", "📊 Basis Pengetahuan",
         "📜 History Konsultasi", "ℹ️ Tentang Sistem"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 👤 Data Pengguna")
    st.session_state.nama_petani = st.text_input(
        "Nama Petani/Pengguna", value=st.session_state.nama_petani,
        placeholder="Opsional..."
    )
    st.session_state.lokasi = st.text_input(
        "Lokasi Lahan", value=st.session_state.lokasi,
        placeholder="Contoh: Brebes, Jawa Tengah"
    )

    # ✅ FIX #4: Pakai class skala-cf-box (background hijau tua, teks putih)
    st.markdown("""
    <div class="skala-cf-box">
        <b>📌 Skala Keyakinan CF:</b><br>
        🔵 Tidak Yakin &nbsp;→ 0.2<br>
        🟡 Agak Yakin &nbsp;&nbsp;→ 0.4<br>
        🟢 Yakin &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 0.6<br>
        💚 Sangat Yakin → 0.8<br>
        ✅ Pasti &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1.0
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption(f"🕐 {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("v1.0.0 | Mata Kuliah Sistem Pakar")


# ═══════════════════════════════════════════════
# HALAMAN: DIAGNOSA PENYAKIT
# ═══════════════════════════════════════════════
if halaman == "🔍 Diagnosa Penyakit":

    col_left, col_right = st.columns([1, 1.4], gap="large")

    # ── PANEL KIRI: Input Gejala ──────────────────
    with col_left:
        st.subheader("📋 Pilih Gejala yang Diamati")
        st.caption("Pilih gejala yang sesuai dan tentukan tingkat keyakinan Anda.")

        # Filter kategori
        kategori_map = {
            "🍃 Semua Gejala": None,
            "🍃 Gejala Daun": ["G01","G02","G03","G04","G05","G06","G07","G08","G09","G10"],
            "🌿 Gejala Batang": ["G11","G12","G13","G14","G15","G16"],
            "🌽 Gejala Tongkol/Biji": ["G17","G18","G19","G20","G21","G22"],
            "🌱 Gejala Akar": ["G23","G24","G25"],
            "🌾 Gejala Umum": ["G26","G27","G28","G29","G30","G31","G32","G33","G34","G35"],
        }
        filter_kat = st.selectbox("Filter Kategori Gejala:", list(kategori_map.keys()))
        gejala_filter = kategori_map[filter_kat]

        # Tampilkan daftar gejala
        gejala_baru = {}
        semua_gejala = get_all_gejala_sorted()

        with st.form("form_gejala"):
            for gejala_id, keterangan in semua_gejala:
                if gejala_filter and gejala_id not in gejala_filter:
                    continue

                col_chk, col_sel = st.columns([0.08, 0.92])
                with col_chk:
                    checked = st.checkbox(
                        "", key=f"chk_{gejala_id}",
                        value=gejala_id in st.session_state.gejala_dipilih
                    )
                with col_sel:
                    if checked:
                        keyakinan = st.selectbox(
                            f"**[{gejala_id}]** {keterangan}",
                            options=list(CF_USER_SCALE.keys()),
                            index=list(CF_USER_SCALE.keys()).index("Yakin"),
                            key=f"sel_{gejala_id}"
                        )
                        gejala_baru[gejala_id] = CF_USER_SCALE[keyakinan]
                    else:
                        st.markdown(f"<small style='color:#6b7280'>[{gejala_id}] {keterangan}</small>",
                                    unsafe_allow_html=True)

            st.markdown("---")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("🔬 Diagnosa Sekarang",
                                               use_container_width=True, type="primary")
            with col_btn2:
                reset = st.form_submit_button("🔄 Reset",
                                              use_container_width=True)

        if reset:
            st.session_state.gejala_dipilih = {}
            st.session_state.hasil_diagnosa = []
            st.rerun()

        if submit:
            if not gejala_baru:
                st.warning("⚠️ Pilih minimal 1 gejala untuk melakukan diagnosa.")
            else:
                st.session_state.gejala_dipilih = gejala_baru
                with st.spinner("Menjalankan inferensi Certainty Factor..."):
                    hasil = run_inference(gejala_baru)
                st.session_state.hasil_diagnosa = hasil

                # Simpan ke history
                st.session_state.history.append({
                    "waktu": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "nama_petani": st.session_state.nama_petani,
                    "lokasi": st.session_state.lokasi,
                    "jumlah_gejala": len(gejala_baru),
                    "gejala": dict(gejala_baru),
                    "hasil": [{"nama": h["nama"], "cf": h["cf_total"],
                                "keyakinan": h["tingkat_keyakinan"]}
                               for h in hasil[:3]],
                })
                st.rerun()

    # ── PANEL KANAN: Hasil Diagnosa ───────────────
    with col_right:
        hasil = st.session_state.hasil_diagnosa
        gejala_dipilih = st.session_state.gejala_dipilih

        if not gejala_dipilih:
            st.info("👈 Pilih gejala di panel kiri, lalu klik **Diagnosa Sekarang**.")

            # Tips penggunaan
            with st.expander("💡 Cara Penggunaan"):
                st.markdown("""
                1. **Pilih kategori** gejala yang ingin dilihat
                2. **Centang gejala** yang sesuai dengan kondisi tanaman
                3. **Tentukan keyakinan** Anda terhadap setiap gejala
                4. Klik **Diagnosa Sekarang** untuk mendapatkan hasil
                5. Lihat **laporan lengkap** dan unduh jika diperlukan
                """)
        else:
            # Ringkasan gejala dipilih
            st.markdown(f"**✅ {len(gejala_dipilih)} gejala dipilih:**")
            tag_html = "".join(
                f'<span class="gejala-tag">{gid}</span>'
                for gid in gejala_dipilih
            )
            st.markdown(tag_html, unsafe_allow_html=True)
            st.markdown("---")

            if not hasil:
                st.warning("⚠️ Tidak ada penyakit yang terdeteksi dengan gejala tersebut. "
                           "Coba tambah lebih banyak gejala.")
            else:
                st.subheader(f"🎯 Ditemukan {len(hasil)} kemungkinan penyakit")

                # Tab utama
                tab_hasil, tab_grafik, tab_hitung, tab_laporan = st.tabs(
                    ["📋 Hasil Diagnosa", "📊 Visualisasi CF",
                     "🧮 Detail Perhitungan", "📄 Laporan"]
                )

                # ── Tab Hasil ──────────────────────────────
                with tab_hasil:
                    for i, h in enumerate(hasil[:5]):
                        kelas = f"result-card-{min(i+1, 3)}"
                        rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]

                        with st.container():
                            st.markdown(f"""
                            <div class="card {kelas}">
                                <div style="display:flex; justify-content:space-between; align-items:center">
                                    <h4 style="margin:0; color:#14532d">
                                        {rank_emoji} {h['nama']}
                                    </h4>
                                    <span class="cf-badge" style="background:{h['warna_cf']}22;
                                          color:{h['warna_cf']}; border:1px solid {h['warna_cf']}">
                                        CF = {h['cf_total']} &nbsp;|&nbsp; {h['cf_persen']}%
                                    </span>
                                </div>
                                <small style="color:#6b7280"><i>{h['nama_ilmiah']}</i></small>
                            </div>
                            """, unsafe_allow_html=True)

                            st.progress(h["cf_total"])

                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("Keyakinan", h["tingkat_keyakinan"])
                            with col_b:
                                st.metric("Tingkat Bahaya", h["tingkat_bahaya"])

                            with st.expander(f"📖 Detail & Penanganan — {h['nama']}"):
                                st.markdown(f"**Kondisi Favorit Penyakit:**  \n{h['kondisi_favorit']}")
                                st.markdown(f"**Deskripsi:**  \n{h['deskripsi']}")
                                st.markdown("**🌿 Rekomendasi Penanganan:**")
                                for j, p in enumerate(h["penanganan"], 1):
                                    st.markdown(f"{j}. {p}")

                            st.markdown("---")

                # ── Tab Grafik ─────────────────────────────
                # ✅ FIX #1: Ganti background menjadi coklat tua / gelap agar tulisan & bar terlihat
                with tab_grafik:
                    if len(hasil) >= 1:
                        # Bar chart horizontal
                        df = pd.DataFrame([
                            {"Penyakit": f"{['🥇','🥈','🥉','4️⃣','5️⃣'][i]} {h['nama'][:35]}",
                             "CF (%)": h["cf_persen"],
                             "Keyakinan": h["tingkat_keyakinan"]}
                            for i, h in enumerate(hasil[:8])
                        ])

                        warna_map = {
                            "Sangat Tinggi": "#4ade80",
                            "Tinggi": "#86efac",
                            "Sedang": "#fde68a",
                            "Rendah": "#fb923c",
                            "Sangat Rendah": "#f87171",
                        }
                        warna_bars = [
                            warna_map.get(h["tingkat_keyakinan"], "#94a3b8")
                            for h in hasil[:8]
                        ]

                        fig_bar = go.Figure(go.Bar(
                            x=df["CF (%)"],
                            y=df["Penyakit"],
                            orientation='h',
                            marker_color=warna_bars,
                            marker_line_color='rgba(255,255,255,0.3)',
                            marker_line_width=1,
                            text=[f"{v}%" for v in df["CF (%)"]],
                            textposition='outside',
                            textfont=dict(color='#f1f5f9', size=12),
                        ))
                        fig_bar.update_layout(
                            title=dict(
                                text="Perbandingan Nilai CF Penyakit",
                                font=dict(color="#f1f5f9", size=14)
                            ),
                            xaxis=dict(
                                title="Nilai CF (%)",
                                title_font=dict(color="#94a3b8"),
                                tickfont=dict(color="#94a3b8"),
                                gridcolor="#334155",
                                range=[0, 120],
                            ),
                            yaxis=dict(
                                title="",
                                tickfont=dict(color="#e2e8f0", size=11),
                                gridcolor="#334155",
                            ),
                            height=380,
                            plot_bgcolor="#1e293b",
                            paper_bgcolor="#0f172a",
                            font=dict(color="#e2e8f0"),
                            margin=dict(l=20, r=20, t=50, b=40),
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)

                        # Radar chart — top 3
                        if len(hasil) >= 3:
                            st.markdown("**Radar Chart — Gejala Cocok Top 3 Penyakit:**")
                            semua_gejala_ids = sorted(set(
                                g for h in hasil[:3] for g in h["gejala_cocok"]
                            ))
                            fig_radar = go.Figure()
                            warna_radar = ["#4ade80", "#60a5fa", "#f472b6"]
                            for idx_r, h in enumerate(hasil[:3]):
                                nilai = []
                                for gid in semua_gejala_ids:
                                    val = next(
                                        (d["cf_gejala"] for d in h["detail_hitung"]
                                         if d["gejala_id"] == gid), 0
                                    )
                                    nilai.append(val)
                                fig_radar.add_trace(go.Scatterpolar(
                                    r=nilai + [nilai[0]],
                                    theta=semua_gejala_ids + [semua_gejala_ids[0]],
                                    fill='toself',
                                    name=h["nama"][:25],
                                    opacity=0.7,
                                    line=dict(color=warna_radar[idx_r], width=2),
                                    fillcolor=warna_radar[idx_r].replace(")", ",0.3)").replace("rgb", "rgba") if warna_radar[idx_r].startswith("rgb") else warna_radar[idx_r],
                                ))
                            fig_radar.update_layout(
                                polar=dict(
                                    bgcolor="#1e293b",
                                    radialaxis=dict(
                                        visible=True,
                                        range=[0, 1],
                                        tickfont=dict(color="#94a3b8"),
                                        gridcolor="#334155",
                                        linecolor="#334155",
                                    ),
                                    angularaxis=dict(
                                        tickfont=dict(color="#e2e8f0"),
                                        gridcolor="#334155",
                                        linecolor="#475569",
                                    ),
                                ),
                                showlegend=True,
                                legend=dict(
                                    font=dict(color="#e2e8f0"),
                                    bgcolor="#1e293b",
                                    bordercolor="#334155",
                                ),
                                height=380,
                                title=dict(
                                    text="Kontribusi Gejala per Penyakit",
                                    font=dict(color="#f1f5f9", size=14)
                                ),
                                paper_bgcolor="#0f172a",
                                font=dict(color="#e2e8f0"),
                            )
                            st.plotly_chart(fig_radar, use_container_width=True)

                        # Pie chart distribusi keyakinan
                        keyakinan_count = {}
                        for h in hasil:
                            k = h["tingkat_keyakinan"]
                            keyakinan_count[k] = keyakinan_count.get(k, 0) + 1
                        fig_pie = px.pie(
                            values=list(keyakinan_count.values()),
                            names=list(keyakinan_count.keys()),
                            title="Distribusi Tingkat Keyakinan",
                            color_discrete_sequence=["#4ade80","#86efac","#fde68a","#fb923c","#f87171"],
                            hole=0.4,
                        )
                        fig_pie.update_layout(
                            paper_bgcolor="#0f172a",
                            plot_bgcolor="#1e293b",
                            font=dict(color="#e2e8f0"),
                            title=dict(font=dict(color="#f1f5f9")),
                            legend=dict(
                                font=dict(color="#e2e8f0"),
                                bgcolor="#1e293b",
                            ),
                        )
                        fig_pie.update_traces(textfont=dict(color="#0f172a"))
                        st.plotly_chart(fig_pie, use_container_width=True)

                # ── Tab Perhitungan ────────────────────────
                # ✅ FIX #2: step-box sudah diubah di CSS jadi background gelap
                with tab_hitung:
                    st.markdown("**Rumus CF:**")
                    st.latex(r"CF_{gejala} = CF_{pakar} \times CF_{user}")
                    st.latex(r"CF_{kombinasi} = CF_1 + CF_2 \times (1 - CF_1)")

                    st.markdown("---")
                    penyakit_options = [h["nama"] for h in hasil[:5]]
                    pilih_p = st.selectbox("Pilih penyakit untuk lihat detail:", penyakit_options)
                    h_detail = next((h for h in hasil if h["nama"] == pilih_p), None)

                    if h_detail and h_detail["detail_hitung"]:
                        # Tabel detail
                        rows = []
                        for step in h_detail["detail_hitung"]:
                            rows.append({
                                "Gejala": f"[{step['gejala_id']}] {step['gejala_nama'][:45]}",
                                "CF Pakar": step["cf_pakar"],
                                "CF User": step["cf_user"],
                                "CF Gejala": step["cf_gejala"],
                                "CF Sesudah": step["cf_sesudah"],
                            })
                        df_detail = pd.DataFrame(rows)
                        st.dataframe(df_detail, use_container_width=True, hide_index=True)

                        st.markdown("**Langkah-langkah perhitungan:**")
                        teks_step = format_cf_steps(h_detail["detail_hitung"], h_detail["nama"])
                        st.markdown(f'<div class="step-box">{teks_step}</div>',
                                    unsafe_allow_html=True)

                # ── Tab Laporan ────────────────────────────
                # ✅ FIX #3: Tambah tombol Download PDF yang lebih robust
                with tab_laporan:
                    st.markdown("### 📄 Unduh Laporan Hasil Diagnosa")

                    # Generate laporan teks dulu (selalu tersedia)
                    laporan_teks = generate_text_report(
                        hasil,
                        gejala_dipilih,
                        st.session_state.nama_petani,
                        st.session_state.lokasi,
                    )

                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.download_button(
                            "⬇️ Unduh Laporan (.txt)",
                            data=laporan_teks,
                            file_name=f"diagnosa_jagung_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )

                    with col_r2:
                        if REPORTLAB_AVAILABLE:
                            try:
                                pdf_bytes = generate_pdf_report(
                                    hasil,
                                    gejala_dipilih,
                                    st.session_state.nama_petani,
                                    st.session_state.lokasi,
                                )
                                st.download_button(
                                    "⬇️ Unduh Laporan (.pdf)",
                                    data=pdf_bytes,
                                    file_name=f"diagnosa_jagung_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                )
                            except Exception as e:
                                st.error(f"Gagal generate PDF: {e}")
                        else:
                            st.warning(
                                "⚠️ **Fitur PDF belum aktif.**\n\n"
                                "Install `reportlab` terlebih dahulu:\n"
                                "```\npip install reportlab\n```\n"
                                "Kemudian restart aplikasi."
                            )
                            # Tombol PDF disabled visual
                            st.button("⬇️ Unduh Laporan (.pdf)", disabled=True,
                                      use_container_width=True,
                                      help="Install reportlab untuk mengaktifkan fitur ini")

                    st.markdown("---")
                    st.markdown("**ℹ️ Catatan:**")
                    st.markdown(
                        "- File `.txt` selalu tersedia tanpa instalasi tambahan\n"
                        "- File `.pdf` memerlukan library `reportlab` (`pip install reportlab`)\n"
                        "- Laporan berisi detail gejala, hasil diagnosa, dan langkah perhitungan CF"
                    )

                    # Preview laporan teks
                    with st.expander("👁 Preview Laporan"):
                        st.text(laporan_teks)


# ═══════════════════════════════════════════════
# HALAMAN: BASIS PENGETAHUAN
# ═══════════════════════════════════════════════
elif halaman == "📊 Basis Pengetahuan":
    st.subheader("📊 Basis Pengetahuan Sistem Pakar")

    tab_p, tab_g, tab_r = st.tabs(
        ["🦠 Daftar Penyakit", "🍃 Daftar Gejala", "🔗 Matriks Aturan"]
    )

    with tab_p:
        for pid, info in PENYAKIT.items():
            with st.expander(f"**[{pid}]** {info['nama']} — *{info['nama_ilmiah']}*"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Deskripsi:** {info['deskripsi']}")
                    st.markdown("**Penanganan:**")
                    for p in info["penanganan"]:
                        st.markdown(f"- {p}")
                with col2:
                    st.metric("Tingkat Bahaya", info["tingkat_bahaya"])
                    st.markdown(f"**Kondisi Favorit:**  \n{info['kondisi_favorit']}")
                    jumlah_gejala = len(RULES.get(pid, {}))
                    st.metric("Jumlah Aturan Gejala", jumlah_gejala)

    with tab_g:
        df_gejala = pd.DataFrame([
            {"ID": k, "Keterangan": v,
             "Jumlah Penyakit Terkait": sum(1 for r in RULES.values() if k in r)}
            for k, v in sorted(GEJALA.items())
        ])
        st.dataframe(df_gejala, use_container_width=True, hide_index=True)

    with tab_r:
        st.markdown("**Matriks Nilai CF Pakar (baris = penyakit, kolom = gejala):**")
        gejala_ids = sorted(GEJALA.keys())
        penyakit_ids = sorted(PENYAKIT.keys())
        matrix_data = {}
        for pid in penyakit_ids:
            matrix_data[PENYAKIT[pid]["nama"][:30]] = {
                gid: RULES.get(pid, {}).get(gid, "") for gid in gejala_ids
            }
        df_matrix = pd.DataFrame(matrix_data).T
        df_matrix.columns = gejala_ids
        st.dataframe(df_matrix, use_container_width=True)


# ═══════════════════════════════════════════════
# HALAMAN: HISTORY KONSULTASI
# ═══════════════════════════════════════════════
elif halaman == "📜 History Konsultasi":
    st.subheader("📜 History Konsultasi")

    if not st.session_state.history:
        st.info("Belum ada riwayat konsultasi. Lakukan diagnosa terlebih dahulu.")
    else:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Konsultasi", len(st.session_state.history))
        with col_b:
            avg_gejala = sum(h["jumlah_gejala"] for h in st.session_state.history) / len(st.session_state.history)
            st.metric("Rata-rata Gejala", f"{avg_gejala:.1f}")
        with col_c:
            if st.button("🗑️ Hapus Semua History", type="secondary"):
                st.session_state.history = []
                st.rerun()

        st.markdown("---")
        for i, h in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"#{len(st.session_state.history)-i+1} | {h['waktu']} "
                             f"— {h.get('nama_petani') or 'Anonim'} | {h['jumlah_gejala']} gejala"):
                if h.get("lokasi"):
                    st.caption(f"📍 {h['lokasi']}")

                st.markdown("**Hasil Diagnosa:**")
                for r in h["hasil"]:
                    st.markdown(
                        f"- **{r['nama']}** — CF: `{r['cf']}` ({r['keyakinan']})"
                    )

        # Export history JSON
        history_json = json.dumps(st.session_state.history, ensure_ascii=False, indent=2)
        st.download_button(
            "⬇️ Export History (JSON)",
            data=history_json,
            file_name=f"history_diagnosa_{datetime.datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
        )


# ═══════════════════════════════════════════════
# HALAMAN: TENTANG SISTEM
# ═══════════════════════════════════════════════
elif halaman == "ℹ️ Tentang Sistem":
    st.subheader("ℹ️ Tentang Sistem Pakar Ini")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🌽 SiPakar — Sistem Pakar Diagnosa Penyakit Tanaman Jagung

        Sistem pakar ini menggunakan metode **Certainty Factor (CF)** untuk
        mendiagnosa penyakit pada tanaman jagung berdasarkan gejala yang diamati
        di lapangan.

        #### 📐 Metode: Certainty Factor
        Certainty Factor (CF) adalah metode yang digunakan untuk mewakili tingkat
        kepercayaan/keyakinan dalam sistem pakar. Diperkenalkan oleh **Shortliffe
        dan Buchanan** (1975) dalam sistem MYCIN.

        **Rumus:**
         CF(H, E) = CF_pakar × CF_user
    CF_kombinasi = CF1 + CF2 × (1 - CF1)
        """)

    with col2:
        st.markdown("""
        #### 📦 Spesifikasi Sistem
        | Komponen | Detail |
        |----------|--------|
        | Jumlah Penyakit | 12 penyakit |
        | Jumlah Gejala | 35 gejala |
        | Metode Inferensi | Certainty Factor |
        | Framework | Streamlit |
        | Bahasa | Python 3.x |

        #### 📚 Referensi Basis Pengetahuan
        - Jurnal Fitopatologi Indonesia
        - CIMMYT Maize Disease Guide
        - Balai Penelitian Tanaman Serealia
        - Direktur Perlindungan Tanaman Pangan, Kementan RI
        """)

    st.markdown("---")
    st.markdown("""
    #### 🔗 Cara Menjalankan
```bash
    # Install dependencies
    pip install streamlit plotly pandas reportlab

    # Jalankan aplikasi
    streamlit run app.py
```
    """)