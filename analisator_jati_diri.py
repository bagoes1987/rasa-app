#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 ANALISATOR JATI DIRI SISWA SMA
================================
Sistem analisis jati diri berdasarkan teori James Marcia (1966)
dengan 4 dimensi identitas dan 24 pertanyaan komprehensif.

Author: RASA System
Version: 2.1
Date: October 2025
"""

import time
import json
from datetime import datetime

# ==============================
# 📊 DATA PERTANYAAN LENGKAP
# ==============================

ANALISATOR_DATA = {
    "meta": {
        "title": "Analisator Jati Diri Siswa SMA",
        "version": "v2.1-24item",
        "based_on": [
            "James Marcia (1966)",
            "Crocetti et al. (2008)", 
            "Luyckx et al. (2006)",
            "Berzonsky (2011)"
        ],
        "scoring": {
            "A": 1,
            "B": 2, 
            "C": 3
        },
        "interpretation": {
            "24-36": "Identity Diffusion — belum memiliki arah hidup atau kesadaran nilai diri.",
            "37-48": "Foreclosure — mengikuti nilai luar tanpa eksplorasi mendalam.",
            "49-60": "Moratorium — sedang mencari dan bereksperimen dengan identitas diri.",
            "61-72": "Identity Achievement — sudah mengenal, mengeksplorasi, dan menetapkan jati diri."
        }
    },
    "questions": [
        {
            "id": 1,
            "dimension": "Eksplorasi Diri",
            "question": "Saya mencoba berbagai kegiatan di sekolah untuk mengetahui apa yang cocok bagi saya.",
            "options": {
                "A": "Tidak pernah mencoba hal baru",
                "B": "Kadang mencoba hal baru", 
                "C": "Sering mencoba hal baru untuk mengenal diri"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang aktif mengeksplorasi diri, cenderung pasif terhadap pengalaman baru.",
                "B": "Mulai membuka diri terhadap hal baru namun belum konsisten.",
                "C": "Memiliki sikap terbuka dan eksploratif dalam memahami diri sendiri."
            }
        },
        {
            "id": 2,
            "dimension": "Eksplorasi Diri",
            "question": "Saya suka mencari tahu tentang jurusan kuliah dan pekerjaan yang mungkin sesuai dengan minat saya.",
            "options": {
                "A": "Tidak pernah mencari tahu",
                "B": "Kadang mencari tahu",
                "C": "Sering mencari tahu dan membandingkan"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang memiliki orientasi masa depan.",
                "B": "Sedang mencari arah tetapi belum mendalam.",
                "C": "Proaktif dalam mengenal minat dan arah karier pribadi."
            }
        },
        {
            "id": 3,
            "dimension": "Eksplorasi Diri",
            "question": "Saya berusaha mengenal kelebihan dan kelemahan diri saya.",
            "options": {
                "A": "Tidak terlalu memikirkannya",
                "B": "Kadang memikirkannya",
                "C": "Sering merenung untuk mengenal diri sendiri"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Belum sadar akan potensi diri.",
                "B": "Mulai memahami diri namun belum mendalam.",
                "C": "Sudah melakukan refleksi diri secara aktif."
            }
        },
        {
            "id": 4,
            "dimension": "Eksplorasi Diri",
            "question": "Saya mencari informasi dari guru, orang tua, atau internet untuk memahami pilihan masa depan.",
            "options": {
                "A": "Jarang mencari informasi",
                "B": "Kadang mencari informasi",
                "C": "Aktif mencari berbagai sumber"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Cenderung pasif dalam menentukan arah hidup.",
                "B": "Mulai mencari informasi secara terbatas.",
                "C": "Aktif mencari wawasan untuk pengembangan diri."
            }
        },
        {
            "id": 5,
            "dimension": "Eksplorasi Diri",
            "question": "Saya mempertanyakan nilai-nilai hidup yang saya anut agar lebih memahami diri saya.",
            "options": {
                "A": "Tidak pernah mempertanyakan",
                "B": "Kadang berpikir begitu",
                "C": "Sering merefleksi nilai hidup saya"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Belum melakukan refleksi nilai pribadi.",
                "B": "Sedikit reflektif terhadap nilai diri.",
                "C": "Reflektif dan kritis terhadap makna hidup pribadi."
            }
        },
        {
            "id": 6,
            "dimension": "Eksplorasi Diri",
            "question": "Saya tertarik mengenal pengalaman hidup orang lain untuk belajar tentang diri sendiri.",
            "options": {
                "A": "Tidak tertarik",
                "B": "Kadang membaca/mendengar",
                "C": "Sering mencari inspirasi dari orang lain"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang terbuka terhadap pengalaman sosial.",
                "B": "Cukup terbuka namun belum aktif belajar dari orang lain.",
                "C": "Mampu belajar dari pengalaman sosial dan lingkungan."
            }
        },
        {
            "id": 7,
            "dimension": "Komitmen Diri",
            "question": "Saya memiliki cita-cita atau tujuan hidup yang jelas.",
            "options": {
                "A": "Belum punya",
                "B": "Ada tapi belum yakin",
                "C": "Sudah jelas dan saya perjuangkan"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Belum memiliki arah hidup yang pasti.",
                "B": "Sedang mencari kejelasan arah.",
                "C": "Memiliki tujuan hidup yang kuat dan konsisten."
            }
        },
        {
            "id": 8,
            "dimension": "Komitmen Diri",
            "question": "Saya yakin dengan keputusan saya tentang jurusan atau karier masa depan.",
            "options": {
                "A": "Belum yakin",
                "B": "Kadang yakin",
                "C": "Sudah yakin dan mantap"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Masih ragu menentukan arah masa depan.",
                "B": "Mulai yakin namun belum stabil.",
                "C": "Memiliki keyakinan kuat dan arah karier yang jelas."
            }
        },
        {
            "id": 9,
            "dimension": "Komitmen Diri",
            "question": "Saya menjadikan nilai-nilai pribadi saya sebagai pedoman dalam bertindak.",
            "options": {
                "A": "Tidak punya pedoman jelas",
                "B": "Kadang mengikuti nilai pribadi",
                "C": "Selalu berpegang pada nilai saya sendiri"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Belum menginternalisasi nilai pribadi.",
                "B": "Mulai mengenal nilai namun belum konsisten.",
                "C": "Konsisten dalam berpegang pada nilai pribadi."
            }
        },
        {
            "id": 10,
            "dimension": "Komitmen Diri",
            "question": "Saya tetap pada keputusan saya meskipun orang lain tidak setuju.",
            "options": {
                "A": "Mudah berubah",
                "B": "Kadang goyah",
                "C": "Tetap berpegang pada pilihan"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Cenderung mudah terpengaruh.",
                "B": "Memiliki pendirian, namun belum kuat.",
                "C": "Kuat dan tegas dalam mempertahankan keputusan."
            }
        },
        {
            "id": 11,
            "dimension": "Komitmen Diri",
            "question": "Saya merasa hidup saya memiliki arah dan makna yang jelas.",
            "options": {
                "A": "Belum terasa",
                "B": "Mulai terasa",
                "C": "Jelas dan saya tahu ke mana ingin menuju"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Belum memiliki makna hidup yang kuat.",
                "B": "Mulai menemukan arah hidup.",
                "C": "Sudah memahami arah dan makna hidup secara mendalam."
            }
        },
        {
            "id": 12,
            "dimension": "Komitmen Diri",
            "question": "Saya berkomitmen untuk menjadi pribadi yang sesuai dengan nilai yang saya yakini.",
            "options": {
                "A": "Tidak yakin",
                "B": "Cukup yakin",
                "C": "Sangat yakin dan konsisten"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Masih ragu terhadap komitmen diri.",
                "B": "Sedang menguatkan komitmen.",
                "C": "Berkomitmen penuh pada nilai diri."
            }
        },
        {
            "id": 13,
            "dimension": "Reconsideration",
            "question": "Saya sering meninjau ulang apakah keputusan saya benar-benar cocok untuk saya.",
            "options": {
                "A": "Tidak pernah",
                "B": "Kadang",
                "C": "Sering melakukan refleksi"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Tidak reflektif terhadap keputusan.",
                "B": "Kadang meninjau ulang.",
                "C": "Reflektif dan terbuka memperbaiki keputusan."
            }
        },
        {
            "id": 14,
            "dimension": "Reconsideration",
            "question": "Saya memikirkan kemungkinan untuk mengubah keputusan jika ada pilihan yang lebih baik.",
            "options": {
                "A": "Tidak pernah",
                "B": "Kadang",
                "C": "Sering mempertimbangkan perubahan"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Tidak fleksibel dalam berpikir.",
                "B": "Cukup terbuka dengan perubahan.",
                "C": "Adaptif dan terbuka terhadap alternatif yang lebih baik."
            }
        },
        {
            "id": 15,
            "dimension": "Reconsideration",
            "question": "Saya membandingkan pengalaman saya dengan orang lain untuk memperbaiki diri.",
            "options": {
                "A": "Tidak pernah",
                "B": "Kadang",
                "C": "Sering membandingkan untuk belajar"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang reflektif terhadap pengalaman.",
                "B": "Mulai belajar dari orang lain.",
                "C": "Aktif menggunakan perbandingan untuk berkembang."
            }
        },
        {
            "id": 16,
            "dimension": "Reconsideration",
            "question": "Saya mencoba memahami konsekuensi dari keputusan yang sudah saya ambil.",
            "options": {
                "A": "Tidak memikirkan",
                "B": "Kadang memikirkan",
                "C": "Sering meninjau konsekuensinya"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang mempertimbangkan dampak keputusan.",
                "B": "Cukup sadar terhadap konsekuensi.",
                "C": "Reflektif dan bijak dalam mengambil keputusan."
            }
        },
        {
            "id": 17,
            "dimension": "Reconsideration",
            "question": "Saya merasa ragu apakah jalan hidup yang saya pilih sudah tepat.",
            "options": {
                "A": "Tidak pernah ragu",
                "B": "Kadang ragu",
                "C": "Sering merasa ragu dan berpikir ulang"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Cukup yakin dengan pilihan hidup.",
                "B": "Sedang dalam fase eksplorasi identitas.",
                "C": "Aktif meninjau ulang arah hidup secara reflektif."
            }
        },
        {
            "id": 18,
            "dimension": "Reconsideration",
            "question": "Saya ingin memperdalam pemahaman tentang nilai-nilai yang saya pilih.",
            "options": {
                "A": "Tidak tertarik",
                "B": "Kadang tertarik",
                "C": "Sering memperdalam makna nilai yang saya yakini"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang tertarik memperkuat nilai diri.",
                "B": "Sedang mencari makna nilai pribadi.",
                "C": "Reflektif dan mendalam terhadap keyakinan diri."
            }
        },
        {
            "id": 19,
            "dimension": "Gaya Identitas",
            "question": "Sebelum mengambil keputusan penting, saya mencari informasi sebanyak mungkin.",
            "options": {
                "A": "Tidak pernah mencari informasi",
                "B": "Kadang mencari informasi",
                "C": "Selalu mencari tahu dulu"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Impulsif, kurang analisis sebelum bertindak.",
                "B": "Cukup hati-hati namun belum konsisten.",
                "C": "Analitis dan rasional dalam mengambil keputusan."
            }
        },
        {
            "id": 20,
            "dimension": "Gaya Identitas",
            "question": "Saya mengikuti nilai-nilai keluarga dan guru dalam menentukan arah hidup.",
            "options": {
                "A": "Jarang mengikuti",
                "B": "Kadang mengikuti",
                "C": "Selalu mengikuti"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Mandiri menentukan arah hidup.",
                "B": "Seimbang antara nilai pribadi dan sosial.",
                "C": "Cenderung mengikuti norma luar tanpa eksplorasi."
            }
        },
        {
            "id": 21,
            "dimension": "Gaya Identitas",
            "question": "Saya sering menunda mengambil keputusan karena takut salah.",
            "options": {
                "A": "Tidak pernah menunda",
                "B": "Kadang menunda",
                "C": "Sering menunda keputusan"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Cepat bertindak, kadang kurang pertimbangan.",
                "B": "Hati-hati namun bisa ragu.",
                "C": "Cenderung menghindari keputusan sulit."
            }
        },
        {
            "id": 22,
            "dimension": "Gaya Identitas",
            "question": "Saya mempertimbangkan pendapat orang lain sebelum menentukan keputusan akhir.",
            "options": {
                "A": "Tidak pernah mempertimbangkan",
                "B": "Kadang mempertimbangkan",
                "C": "Selalu mendengar dan menimbang"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang sosial dalam berpikir.",
                "B": "Seimbang antara diri dan orang lain.",
                "C": "Sosial dan terbuka terhadap masukan."
            }
        },
        {
            "id": 23,
            "dimension": "Gaya Identitas",
            "question": "Jika saya ragu, saya lebih memilih menunggu sampai keadaan memaksa saya memilih.",
            "options": {
                "A": "Tidak pernah seperti itu",
                "B": "Kadang begitu",
                "C": "Sering menunda sampai terpaksa"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Proaktif dan percaya diri dalam keputusan.",
                "B": "Kadang pasif dalam situasi sulit.",
                "C": "Cenderung menghindar dari tanggung jawab keputusan."
            }
        },
        {
            "id": 24,
            "dimension": "Gaya Identitas",
            "question": "Saya percaya setiap orang harus menentukan jalan hidupnya sendiri meskipun berbeda dengan lingkungan.",
            "options": {
                "A": "Tidak setuju",
                "B": "Setuju sebagian",
                "C": "Sangat setuju dan melakukannya"
            },
            "score": {"A": 1, "B": 2, "C": 3},
            "analysis": {
                "A": "Kurang mandiri dalam menentukan arah hidup.",
                "B": "Mulai mengembangkan otonomi diri.",
                "C": "Mandiri dan yakin pada keputusan pribadi."
            }
        }
    ]
}

# ==============================
# 🧮 FUNGSI UTAMA ANALISATOR
# ==============================

def print_intro():
    """Tampilkan intro yang menarik"""
    print("=" * 60)
    print("ANALISATOR JATI DIRI SISWA SMA")
    print("=" * 60)
    print("- Berdasarkan teori James Marcia (1966)")
    print("- 24 pertanyaan untuk mengenal diri lebih dalam")
    print("- Tidak ada jawaban benar/salah - pilih yang paling menggambarkan diri kamu")
    print("=" * 60)

def get_user_info():
    """Dapatkan informasi user"""
    print("\nHalo! Mari kita mulai perjalanan mengenal diri kamu.")
    time.sleep(1)
    
    name = input("Siapa nama kamu? ").strip()
    if not name:
        name = "Sahabat"
    
    print(f"\nHalo {name}!")
    time.sleep(1)
    
    print("\nSaya akan membantu kamu mengenal lebih dalam tentang jati diri kamu")
    print("melalui beberapa pertanyaan sederhana.")
    print("Tidak ada jawaban benar atau salah — cukup pilih jawaban yang")
    print("paling menggambarkan diri kamu ya.")
    
    while True:
        ready = input("\nSiap mulai? (ya/tidak): ").lower().strip()
        if ready in ['ya', 'y', 'yes']:
            return name
        elif ready in ['tidak', 't', 'no']:
            print("\nBaik, kamu bisa kembali lagi kapan saja 😊")
            return None
        else:
            print("Jawab dengan 'ya' atau 'tidak' saja ya")

def ask_questions(questions):
    """Tanyakan pertanyaan dan kumpulkan jawaban"""
    answers = []
    total_score = 0
    dimension_scores = {}
    
    print("\nOke, kita mulai ya...")
    print("=" * 60)
    
    for i, q in enumerate(questions, 1):
        print(f"\nPERTANYAAN {i}/24")
        print(f"Kategori: {q['dimension']}")
        print(f"\n{q['question']}")
        print()
        
        # Tampilkan opsi
        for key, option in q['options'].items():
            print(f"   {key}. {option}")
        
        # Minta jawaban
        while True:
            answer = input("\nJawaban (A/B/C): ").upper().strip()
            if answer in ['A', 'B', 'C']:
                break
            print("Masukkan hanya A, B, atau C")
        
        # Hitung skor
        score = q['score'][answer]
        total_score += score
        
        # Hitung skor per dimensi
        dim = q['dimension']
        dimension_scores[dim] = dimension_scores.get(dim, 0) + score
        
        # Simpan jawaban
        answers.append({
            'question_id': q['id'],
            'dimension': dim,
            'answer': answer,
            'score': score,
            'analysis': q['analysis'][answer]
        })
        
        # Tampilkan analisis singkat
        print(f"\nAnalisis: {q['analysis'][answer]}")
        print(f"Skor: +{score}")
        
        if i < len(questions):
            input("\nTekan Enter untuk lanjut...")
    
    return answers, total_score, dimension_scores

def analyze_results(total_score, dimension_scores, questions):
    """Analisis hasil dan berikan interpretasi"""
    print("\n" + "=" * 60)
    print("HASIL ANALISIS JATI DIRI")
    print("=" * 60)
    
    # Interpretasi umum
    interpretation_ranges = ANALISATOR_DATA['meta']['interpretation']
    if total_score <= 36:
        status = interpretation_ranges['24-36']
    elif total_score <= 48:
        status = interpretation_ranges['37-48']
    elif total_score <= 60:
        status = interpretation_ranges['49-60']
    else:
        status = interpretation_ranges['61-72']
    
    print(f"\nTotal Skor: {total_score} dari {len(questions) * 3}")
    print(f"Status Jati Diri: {status}")
    
    # Analisis per dimensi
    print(f"\nANALISIS PER DIMENSI:")
    print("-" * 40)
    
    for dim, score in dimension_scores.items():
        # Hitung rata-rata per dimensi
        questions_in_dim = [q for q in questions if q['dimension'] == dim]
        avg_score = score / len(questions_in_dim)
        
        if avg_score >= 2.5:
            level = "[TINGGI]"
            desc = "Sangat kuat"
        elif avg_score >= 2.0:
            level = "[SEDANG-TINGGI]"
            desc = "Cukup kuat"
        elif avg_score >= 1.5:
            level = "[SEDANG]"
            desc = "Mulai berkembang"
        else:
            level = "[RENDAH]"
            desc = "Perlu pengembangan"
        
        print(f"{dim}: {level} ({avg_score:.2f}) - {desc}")
    
    # Rekomendasi
    print(f"\nREKOMENDASI PENGEMBANGAN:")
    print("-" * 40)
    
    for dim, score in dimension_scores.items():
        questions_in_dim = [q for q in questions if q['dimension'] == dim]
        avg_score = score / len(questions_in_dim)
        
        if avg_score < 2.0:
            if dim == "Eksplorasi Diri":
                print(f"* {dim}: Coba aktivitas baru, eksplorasi minat dan bakat")
            elif dim == "Komitmen Diri":
                print(f"* {dim}: Buat tujuan jangka pendek dan panjang, latih konsistensi")
            elif dim == "Reconsideration":
                print(f"* {dim}: Lakukan refleksi diri rutin, evaluasi keputusan")
            elif dim == "Gaya Identitas":
                print(f"* {dim}: Kembangkan kemandirian, percayai intuisi diri")
    
    return status

def save_results(name, answers, total_score, dimension_scores, status):
    """Simpan hasil ke file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"hasil_jati_diri_{name.replace(' ', '_')}_{timestamp}.json"
    
    results = {
        "user_info": {
            "name": name,
            "timestamp": timestamp,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "scores": {
            "total": total_score,
            "max_possible": len(answers) * 3,
            "dimension_scores": dimension_scores,
            "status": status
        },
        "answers": answers
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nHasil tersimpan di: {filename}")
    except Exception as e:
        print(f"\nGagal menyimpan hasil: {e}")

def start_chat():
    """Fungsi utama untuk memulai chatbot"""
    print_intro()
    
    name = get_user_info()
    if not name:
        return
    
    print(f"\n{'='*60}")
    print(f"MULAI ANALISIS UNTUK {name.upper()}")
    print(f"{'='*60}")
    
    questions = ANALISATOR_DATA['questions']
    answers, total_score, dimension_scores = ask_questions(questions)
    
    status = analyze_results(total_score, dimension_scores, questions)
    
    save_results(name, answers, total_score, dimension_scores, status)
    
    print(f"\n{'='*60}")
    print("ANALISIS SELESAI!")
    print("=" * 60)
    print(f"Terima kasih {name} telah mengikuti tes ini!")
    print("Semoga hasilnya bermanfaat untuk pengembangan diri kamu!")
    print("\nTips: Lakukan tes ini lagi setelah 6 bulan untuk melihat perkembangan diri kamu.")
    print("=" * 60)

# ==============================
# 🎯 EKSEKUSI PROGRAM
# ==============================

if __name__ == "__main__":
    try:
        start_chat()
    except KeyboardInterrupt:
        print("\n\nTerima kasih! Sampai jumpa lagi!")
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")
        print("Silakan coba lagi nanti.")
