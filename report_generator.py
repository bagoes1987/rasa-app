from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
import json


def generate_pdf_report(user, all_results):
    """
    Generate comprehensive PDF report for user
    
    Args:
        user: User object
        all_results: Dictionary of all analysis results
        
    Returns:
        Path to generated PDF file
    """
    # Create reports directory if not exists
    os.makedirs('reports', exist_ok=True)
    
    filename = f'reports/RASA_Report_{user.nis}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY
    )
    
    # ========== COVER PAGE ==========
    elements.append(Spacer(1, 3*cm))
    elements.append(Paragraph('LAPORAN RASA', title_style))
    elements.append(Paragraph('Refleksi dan Asistensi Sosial Emosional Siswa', 
                             ParagraphStyle('subtitle', parent=normal_style, alignment=TA_CENTER, fontSize=12)))
    elements.append(Spacer(1, 2*cm))
    
    # User info table
    user_data = [
        ['Nama', ':', user.nama_lengkap],
        ['NIS', ':', user.nis],
        ['Kelas', ':', user.kelas],
        ['Tanggal', ':', datetime.now().strftime('%d %B %Y')]
    ]
    
    user_table = Table(user_data, colWidths=[4*cm, 0.5*cm, 8*cm])
    user_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(user_table)
    elements.append(Spacer(1, 2*cm))
    
    elements.append(Paragraph('SMA Negeri 1 Belitang', 
                             ParagraphStyle('school', parent=normal_style, alignment=TA_CENTER, 
                                          fontName='Helvetica-Bold', fontSize=14)))
    
    elements.append(PageBreak())
    
    # ========== INTRODUCTION ==========
    elements.append(Paragraph('Tentang Laporan Ini', heading_style))
    intro_text = """
    Laporan ini merupakan hasil analisis komprehensif yang dilakukan melalui sistem RASA 
    (Refleksi dan Asistensi Sosial Emosional Siswa). Analisis mencakup berbagai aspek penting 
    dalam perkembangan siswa, termasuk jati diri, kecerdasan emosional, gaya belajar, 
    dan rekomendasi pendidikan yang disesuaikan dengan karakteristik individual.
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 1*cm))
    
    # ========== MODULE RESULTS ==========
    module_order = ['jati_diri', 'eq', 'gaya_belajar', 'jurusan_sma', 'prodi_kuliah']
    
    for module_type in module_order:
        if module_type in all_results:
            module_info = all_results[module_type]
            config = module_info['config']
            data = module_info['data']
            
            elements.append(PageBreak())
            elements.append(Paragraph(f"{config['emoji']} {config['name']}", heading_style))
            
            # Module-specific content
            if module_type == 'jati_diri':
                elements.extend(generate_jati_diri_content(data, subheading_style, normal_style))
            elif module_type == 'eq':
                elements.extend(generate_eq_content(data, subheading_style, normal_style))
            elif module_type == 'gaya_belajar':
                elements.extend(generate_gaya_belajar_content(data, subheading_style, normal_style))
            elif module_type == 'jurusan_sma':
                elements.extend(generate_jurusan_sma_content(data, subheading_style, normal_style))
            elif module_type == 'prodi_kuliah':
                elements.extend(generate_prodi_kuliah_content(data, subheading_style, normal_style))
    
    # ========== CLOSING ==========
    elements.append(PageBreak())
    elements.append(Paragraph('Penutup', heading_style))
    closing_text = """
    Laporan ini merupakan panduan untuk membantu Anda mengenali potensi diri dan merencanakan 
    masa depan dengan lebih baik. Ingatlah bahwa hasil analisis ini bersifat dinamis dan dapat 
    berkembang seiring waktu. Teruslah eksplorasi diri, belajar, dan berkembang!
    <br/><br/>
    Jika ada pertanyaan atau membutuhkan bimbingan lebih lanjut, jangan ragu untuk 
    berkonsultasi dengan guru BK atau konselor sekolah.
    <br/><br/>
    <b>Semangat untuk masa depan yang cerah! 🌟</b>
    """
    elements.append(Paragraph(closing_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    return filename


def generate_jati_diri_content(data, subheading_style, normal_style):
    """Generate content for Jati Diri module"""
    elements = []
    
    elements.append(Paragraph('Ringkasan Jati Diri', subheading_style))
    elements.append(Paragraph(data.get('ringkasan_jati_diri', 'Tidak tersedia'), normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph('Kekuatan Inti', subheading_style))
    for i, kekuatan in enumerate(data.get('kekuatan_inti', []), 1):
        elements.append(Paragraph(f"{i}. {kekuatan}", normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph('Area Pengembangan Diri', subheading_style))
    for i, area in enumerate(data.get('area_pengembangan', []), 1):
        elements.append(Paragraph(f"{i}. {area}", normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    if 'nilai_utama' in data:
        elements.append(Paragraph('Nilai-nilai Utama', subheading_style))
        nilai_text = ', '.join(data['nilai_utama'])
        elements.append(Paragraph(nilai_text, normal_style))
    
    return elements


def generate_eq_content(data, subheading_style, normal_style):
    """Generate content for EQ module"""
    elements = []
    
    elements.append(Paragraph('Ringkasan Kecerdasan Emosional', subheading_style))
    elements.append(Paragraph(data.get('ringkasan_eq', 'Tidak tersedia'), normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    if 'skor_eq' in data:
        elements.append(Paragraph('Skor EQ', subheading_style))
        skor_data = []
        for aspek, nilai in data['skor_eq'].items():
            aspek_name = aspek.replace('_', ' ').title()
            skor_data.append([aspek_name, f'{nilai}/10'])
        
        skor_table = Table(skor_data, colWidths=[8*cm, 3*cm])
        skor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(skor_table)
        elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph('Saran Peningkatan EQ', subheading_style))
    for i, saran in enumerate(data.get('saran_peningkatan', []), 1):
        elements.append(Paragraph(f"{i}. {saran}", normal_style))
    
    return elements


def generate_gaya_belajar_content(data, subheading_style, normal_style):
    """Generate content for Gaya Belajar module"""
    elements = []
    
    elements.append(Paragraph('Gaya Belajar Dominan', subheading_style))
    gaya_text = f"<b>Utama:</b> {data.get('gaya_belajar_utama', 'Tidak tersedia')}"
    if 'gaya_belajar_sekunder' in data:
        gaya_text += f"<br/><b>Sekunder:</b> {data['gaya_belajar_sekunder']}"
    elements.append(Paragraph(gaya_text, normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph('Ringkasan', subheading_style))
    elements.append(Paragraph(data.get('ringkasan', 'Tidak tersedia'), normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph('Tips Belajar Efektif', subheading_style))
    for i, tip in enumerate(data.get('tips_belajar', []), 1):
        elements.append(Paragraph(f"{i}. {tip}", normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    if 'rekomendasi_tools' in data:
        elements.append(Paragraph('Rekomendasi Tools & Metode', subheading_style))
        for i, tool in enumerate(data['rekomendasi_tools'], 1):
            elements.append(Paragraph(f"{i}. {tool}", normal_style))
    
    return elements


def generate_jurusan_sma_content(data, subheading_style, normal_style):
    """Generate content for Jurusan SMA module"""
    elements = []
    
    if 'rekomendasi_prioritas_1' in data:
        elements.append(Paragraph('Rekomendasi Prioritas 1', subheading_style))
        prio1 = data['rekomendasi_prioritas_1']
        elements.append(Paragraph(f"<b>{prio1.get('jurusan', 'N/A')}</b> (Confidence: {prio1.get('confidence', 0)}%)", normal_style))
        
        for i, alasan in enumerate(prio1.get('alasan', []), 1):
            elements.append(Paragraph(f"{i}. {alasan}", normal_style))
        elements.append(Spacer(1, 0.5*cm))
    
    if 'rekomendasi_prioritas_2' in data:
        elements.append(Paragraph('Rekomendasi Prioritas 2 (Alternatif)', subheading_style))
        prio2 = data['rekomendasi_prioritas_2']
        elements.append(Paragraph(f"<b>{prio2.get('jurusan', 'N/A')}</b> (Confidence: {prio2.get('confidence', 0)}%)", normal_style))
        
        for i, alasan in enumerate(prio2.get('alasan', []), 1):
            elements.append(Paragraph(f"{i}. {alasan}", normal_style))
        elements.append(Spacer(1, 0.5*cm))
    
    if 'ringkasan' in data:
        elements.append(Paragraph('Ringkasan', subheading_style))
        elements.append(Paragraph(data['ringkasan'], normal_style))
    
    return elements


def generate_prodi_kuliah_content(data, subheading_style, normal_style):
    """Generate content for Program Studi Kuliah module"""
    elements = []
    
    if 'ringkasan_holistik' in data:
        elements.append(Paragraph('Ringkasan Holistik', subheading_style))
        elements.append(Paragraph(data['ringkasan_holistik'], normal_style))
        elements.append(Spacer(1, 0.5*cm))
    
    if 'rekomendasi' in data:
        for i, prodi in enumerate(data['rekomendasi'], 1):
            elements.append(Paragraph(f"Rekomendasi {i}: {prodi.get('program_studi', 'N/A')}", subheading_style))
            elements.append(Paragraph(f"<b>Kesesuaian:</b> {prodi.get('kesesuaian', 0)}%", normal_style))
            
            elements.append(Paragraph('<b>Alasan:</b>', normal_style))
            for alasan in prodi.get('alasan', []):
                elements.append(Paragraph(f"• {alasan}", normal_style))
            
            elements.append(Paragraph('<b>Prospek Karir:</b>', normal_style))
            for karir in prodi.get('prospek_karir', []):
                elements.append(Paragraph(f"• {karir}", normal_style))
            
            if 'universitas_contoh' in prodi:
                univ_text = ', '.join(prodi['universitas_contoh'])
                elements.append(Paragraph(f'<b>Contoh Universitas:</b> {univ_text}', normal_style))
            
            elements.append(Spacer(1, 0.5*cm))
    
    if 'saran_persiapan' in data:
        elements.append(Paragraph('Saran Persiapan', subheading_style))
        for i, saran in enumerate(data['saran_persiapan'], 1):
            elements.append(Paragraph(f"{i}. {saran}", normal_style))
    
    return elements

