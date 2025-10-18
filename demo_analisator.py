#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Analisator Jati Diri - Menampilkan struktur dan contoh penggunaan
"""

from analisator_jati_diri import ANALISATOR_DATA

def demo_structure():
    """Demo struktur data dan pertanyaan"""
    print("=" * 60)
    print("DEMO ANALISATOR JATI DIRI SISWA SMA")
    print("=" * 60)
    
    print(f"\nJudul: {ANALISATOR_DATA['meta']['title']}")
    print(f"Versi: {ANALISATOR_DATA['meta']['version']}")
    print(f"Berdasarkan: {', '.join(ANALISATOR_DATA['meta']['based_on'])}")
    
    print(f"\nTotal Pertanyaan: {len(ANALISATOR_DATA['questions'])}")
    
    print(f"\nDimensi yang Dikaji:")
    dimensions = set(q['dimension'] for q in ANALISATOR_DATA['questions'])
    for dim in sorted(dimensions):
        count = sum(1 for q in ANALISATOR_DATA['questions'] if q['dimension'] == dim)
        print(f"- {dim}: {count} pertanyaan")
    
    print(f"\nContoh Pertanyaan:")
    print("-" * 40)
    for i, q in enumerate(ANALISATOR_DATA['questions'][:3], 1):
        print(f"\n{i}. [{q['dimension']}]")
        print(f"   {q['question']}")
        print("   Opsi:")
        for key, option in q['options'].items():
            print(f"   {key}. {option}")
    
    print(f"\nInterpretasi Skor:")
    print("-" * 40)
    for range_key, interpretation in ANALISATOR_DATA['meta']['interpretation'].items():
        print(f"{range_key}: {interpretation}")
    
    print(f"\nFitur Chatbot:")
    print("-" * 40)
    print("+ Intro yang menarik dan informatif")
    print("+ 24 pertanyaan komprehensif")
    print("+ Analisis real-time per pertanyaan")
    print("+ Interpretasi berdasarkan teori James Marcia")
    print("+ Analisis per dimensi")
    print("+ Rekomendasi pengembangan")
    print("+ Penyimpanan hasil ke file JSON")
    print("+ Interface yang user-friendly")

def demo_scoring():
    """Demo sistem scoring"""
    print(f"\nSISTEM SCORING:")
    print("-" * 40)
    print("A = 1 poin (Rendah)")
    print("B = 2 poin (Sedang)")  
    print("C = 3 poin (Tinggi)")
    print(f"\nTotal maksimal: {len(ANALISATOR_DATA['questions']) * 3} poin")
    
    print(f"\nContoh Analisis:")
    print("-" * 40)
    
    # Contoh jawaban
    sample_answers = ['C', 'B', 'A', 'C', 'B']
    total_score = 0
    
    for i, answer in enumerate(sample_answers, 1):
        score = ANALISATOR_DATA['questions'][i-1]['score'][answer]
        total_score += score
        analysis = ANALISATOR_DATA['questions'][i-1]['analysis'][answer]
        
        print(f"Pertanyaan {i}: Jawaban {answer} (+{score})")
        print(f"Analisis: {analysis}")
        print()
    
    print(f"Total skor contoh: {total_score} dari {len(sample_answers) * 3}")

if __name__ == "__main__":
    demo_structure()
    demo_scoring()
    
    print(f"\n{'='*60}")
    print("CARA MENGGUNAKAN:")
    print("=" * 60)
    print("1. Jalankan: python analisator_jati_diri.py")
    print("2. Masukkan nama kamu")
    print("3. Jawab 24 pertanyaan dengan jujur")
    print("4. Dapatkan analisis komprehensif")
    print("5. Simpan hasil untuk referensi")
    print("=" * 60)
