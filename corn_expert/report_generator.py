"""
Generator Laporan Hasil Diagnosa
Membuat laporan dalam format teks dan PDF menggunakan reportlab.
"""

import io
import datetime
from cf_engine import format_cf_steps, CF_USER_SCALE

# ── Cek ketersediaan reportlab ──────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, KeepTogether
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_text_report(hasil_diagnosa: list, gejala_dipilih: dict,
                          nama_petani: str = "", lokasi: str = "") -> str:
    """Buat laporan teks plain (fallback jika reportlab tidak tersedia)."""
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    lines = [
        "=" * 65,
        "   SISTEM PAKAR DIAGNOSA PENYAKIT TANAMAN JAGUNG",
        "   Metode: Certainty Factor (CF)",
        "=" * 65,
        f"Tanggal   : {now}",
    ]
    if nama_petani:
        lines.append(f"Petani    : {nama_petani}")
    if lokasi:
        lines.append(f"Lokasi    : {lokasi}")
    lines += ["", "GEJALA YANG DIAMATI", "-" * 40]

    from knowledge_base import GEJALA
    for gejala_id, cf_val in gejala_dipilih.items():
        label = next((k for k, v in CF_USER_SCALE.items() if abs(v - cf_val) < 0.01), str(cf_val))
        lines.append(f"  [{gejala_id}] {GEJALA.get(gejala_id, '')} — {label}")

    lines += ["", "HASIL DIAGNOSA", "-" * 40]
    if not hasil_diagnosa:
        lines.append("Tidak ditemukan penyakit yang sesuai dengan gejala yang diamati.")
    else:
        for i, h in enumerate(hasil_diagnosa[:5], 1):
            lines += [
                f"\n{i}. {h['nama']} ({h['nama_ilmiah']})",
                f"   Nilai CF   : {h['cf_total']} ({h['cf_persen']}%)",
                f"   Keyakinan  : {h['tingkat_keyakinan']}",
                f"   Bahaya     : {h['tingkat_bahaya']}",
                "",
                "   Deskripsi:",
                f"   {h['deskripsi']}",
                "",
                "   Rekomendasi Penanganan:",
            ]
            for j, p in enumerate(h["penanganan"], 1):
                lines.append(f"   {j}. {p}")

    lines += [
        "",
        "=" * 65,
        "DETAIL PERHITUNGAN CF",
        "=" * 65,
    ]
    for h in hasil_diagnosa[:3]:
        lines.append(format_cf_steps(h["detail_hitung"], h["nama"]))
        lines.append("")

    lines += ["=" * 65, "--- Laporan dibuat oleh Sistem Pakar Penyakit Jagung ---"]
    return "\n".join(lines)


def generate_pdf_report(hasil_diagnosa: list, gejala_dipilih: dict,
                        nama_petani: str = "", lokasi: str = "") -> bytes:
    """Buat laporan PDF profesional. Memerlukan reportlab."""
    if not REPORTLAB_AVAILABLE:
        raise ImportError("Modul reportlab belum terinstall. Jalankan: pip install reportlab")

    from knowledge_base import GEJALA

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    # ── Warna tema ──────────────────────────────────────────
    HIJAU_TUA   = colors.HexColor("#166534")
    HIJAU_MUDA  = colors.HexColor("#dcfce7")
    HIJAU_MED   = colors.HexColor("#16a34a")
    ABU         = colors.HexColor("#6b7280")
    ABU_MUDA    = colors.HexColor("#f3f4f6")
    KUNING      = colors.HexColor("#fef9c3")
    ORANGE      = colors.HexColor("#fff7ed")

    styles = getSampleStyleSheet()

    def style(name, **kw):
        return ParagraphStyle(name, parent=styles["Normal"], **kw)

    s_title   = style("Title",   fontSize=16, textColor=HIJAU_TUA,
                       alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica-Bold")
    s_sub     = style("Sub",     fontSize=10, textColor=ABU,
                       alignment=TA_CENTER, spaceAfter=2)
    s_h2      = style("H2",      fontSize=12, textColor=HIJAU_TUA,
                       fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
    s_body    = style("Body",    fontSize=9,  leading=14, alignment=TA_JUSTIFY)
    s_small   = style("Small",   fontSize=8,  textColor=ABU)
    s_bold    = style("Bold",    fontSize=9,  fontName="Helvetica-Bold")
    s_step    = style("Step",    fontSize=8,  fontName="Courier", leading=12,
                       backColor=ABU_MUDA, leftIndent=6, rightIndent=6)

    story = []
    now = datetime.datetime.now().strftime("%d %B %Y, %H:%M WIB")

    # ── Header ─────────────────────────────────────────────
    story.append(Paragraph("🌽 SISTEM PAKAR PENYAKIT TANAMAN JAGUNG", s_title))
    story.append(Paragraph("Laporan Hasil Diagnosa — Metode Certainty Factor", s_sub))
    story.append(HRFlowable(width="100%", thickness=2, color=HIJAU_MED, spaceAfter=8))

    # Info laporan
    info_data = [["Tanggal", f": {now}"]]
    if nama_petani: info_data.append(["Nama Petani", f": {nama_petani}"])
    if lokasi:      info_data.append(["Lokasi Lahan", f": {lokasi}"])
    info_data.append(["Jumlah Gejala", f": {len(gejala_dipilih)} gejala diamati"])

    info_table = Table(info_data, colWidths=[3.5*cm, 13*cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), HIJAU_TUA),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # ── Gejala yang diamati ─────────────────────────────────
    story.append(Paragraph("Gejala yang Diamati", s_h2))
    gejala_data = [["No", "Kode", "Keterangan Gejala", "Keyakinan"]]
    for idx, (gejala_id, cf_val) in enumerate(gejala_dipilih.items(), 1):
        label = next((k for k, v in CF_USER_SCALE.items() if abs(v - cf_val) < 0.01), f"{cf_val}")
        gejala_data.append([
            str(idx), gejala_id,
            GEJALA.get(gejala_id, ""),
            f"{label} ({cf_val})"
        ])

    gt = Table(gejala_data, colWidths=[0.8*cm, 1.2*cm, 11*cm, 3.5*cm])
    gt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HIJAU_TUA),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HIJAU_MUDA]),
        ("GRID",       (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ]))
    story.append(gt)
    story.append(Spacer(1, 12))

    # ── Hasil Diagnosa ──────────────────────────────────────
    story.append(Paragraph("Hasil Diagnosa", s_h2))

    if not hasil_diagnosa:
        story.append(Paragraph(
            "Tidak ditemukan penyakit yang sesuai dengan gejala yang diamati. "
            "Coba tambahkan lebih banyak gejala atau konsultasikan ke ahli pertanian.",
            s_body
        ))
    else:
        # Top 3 hasil
        for rank, h in enumerate(hasil_diagnosa[:5], 1):
            # Warna baris
            if rank == 1:    bg = HIJAU_MUDA
            elif rank == 2:  bg = KUNING
            else:            bg = ORANGE

            # Bar CF visual
            bar_pct = int(h["cf_persen"])
            bar_char = "█" * (bar_pct // 5) + "░" * (20 - bar_pct // 5)

            blok = [
                [Paragraph(f"#{rank}  {h['nama']}", style(f"ph{rank}",
                    fontSize=11, fontName="Helvetica-Bold", textColor=HIJAU_TUA)),
                 Paragraph(f"CF = {h['cf_total']}  ({h['cf_persen']}%)",
                    style("cfval", fontSize=11, fontName="Helvetica-Bold",
                          textColor=HIJAU_MED, alignment=1))],
                [Paragraph(f"<i>{h['nama_ilmiah']}</i>  |  "
                           f"Tingkat Keyakinan: <b>{h['tingkat_keyakinan']}</b>  |  "
                           f"Bahaya: <b>{h['tingkat_bahaya']}</b>",
                           style("meta", fontSize=8, textColor=ABU)), ""],
                [Paragraph(f"<font name='Courier' size='8'>[{bar_char}] {bar_pct}%</font>",
                           style("bar", fontSize=8, textColor=HIJAU_MED)), ""],
            ]

            bt = Table(blok, colWidths=[12*cm, 4.5*cm])
            bt.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX",       (0, 0), (-1, -1), 1, HIJAU_MED),
                ("SPAN",      (0, 1), (1, 1)),
                ("SPAN",      (0, 2), (1, 2)),
                ("TOPPADDING",    (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ]))
            story.append(KeepTogether(bt))

            # Deskripsi
            story.append(Paragraph(h["deskripsi"], style("desc", fontSize=9,
                leading=13, leftIndent=10, alignment=TA_JUSTIFY, spaceAfter=4,
                spaceBefore=4)))

            # Penanganan
            story.append(Paragraph("<b>Rekomendasi Penanganan:</b>",
                style("ph", fontSize=9, fontName="Helvetica-Bold",
                      textColor=HIJAU_TUA, leftIndent=10)))
            for p_idx, p in enumerate(h["penanganan"], 1):
                story.append(Paragraph(f"{p_idx}. {p}",
                    style("pi", fontSize=8, leading=13, leftIndent=20, spaceAfter=1)))

            story.append(Spacer(1, 8))

    # ── Detail Perhitungan CF ───────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=HIJAU_MED, spaceBefore=8))
    story.append(Paragraph("Detail Perhitungan Certainty Factor", s_h2))
    story.append(Paragraph(
        "Rumus: CF(H,E) = CF_pakar × CF_user  |  "
        "CF kombinasi = CF1 + CF2 × (1 − CF1)",
        style("formula", fontSize=8, textColor=ABU, spaceAfter=6)
    ))

    for h in hasil_diagnosa[:3]:
        story.append(Paragraph(f"▶ {h['nama']}", s_bold))
        calc_text = format_cf_steps(h["detail_hitung"], h["nama"])
        story.append(Paragraph(
            calc_text.replace("\n", "<br/>").replace(" ", "&nbsp;"),
            s_step
        ))
        story.append(Spacer(1, 6))

    # ── Footer ──────────────────────────────────────────────
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=ABU))
    story.append(Paragraph(
        "Laporan ini dibuat secara otomatis oleh Sistem Pakar Diagnosa Penyakit Tanaman Jagung. "
        "Hasil diagnosa bersifat prediktif dan tidak menggantikan konsultasi ahli agronomis.",
        style("footer", fontSize=7, textColor=ABU, alignment=TA_CENTER, spaceBefore=4)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
