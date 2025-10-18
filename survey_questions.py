"""
Survey Questions untuk RASA
Sistem pertanyaan survey yang sudah disiapkan untuk setiap modul
"""

SURVEY_QUESTIONS = {
    'jati_diri': {
        'name': 'Analisator Jati Diri',
        'emoji': '🧠',
        'description': 'Yuk kenali diri kamu lebih dalam! Analisis komprehensif dengan 24 pertanyaan yang mengukur 6 dimensi jati diri.',
        'intro': '''Saya akan membantu kamu mengenal lebih dalam tentang jati diri kamu melalui beberapa pertanyaan sederhana.
Tidak ada jawaban benar atau salah — cukup pilih jawaban yang paling menggambarkan diri kamu ya.

Siap mulai? 😊''',
        'meta': {
            'version': 'v3.0-24item',
            'based_on': ['Dimensi Spiritual', 'Dimensi Sosial', 'Dimensi Emosional', 'Dimensi Kognitif', 'Dimensi Moral', 'Dimensi Motivasi'],
            'total_questions': 24,
            'dimensions': ['Spiritual', 'Sosial', 'Emosional', 'Kognitif', 'Moral', 'Motivasi']
        },
        'questions': [
            # Dimensi Spiritual (Pertanyaan 1, 2, 3, 20)
            {
                'id': 1,
                'dimension': 'Spiritual',
                'question': 'Saya berusaha melaksanakan ibadah sesuai ajaran agama saya.',
                'options': {
                    'a': 'Jarang beribadah',
                    'b': 'Kadang beribadah',
                    'c': 'Selalu beribadah tepat waktu'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 2,
                'dimension': 'Spiritual',
                'question': 'Saya merasa tenang setelah berdoa atau beribadah.',
                'options': {
                    'a': 'Tidak merasa tenang',
                    'b': 'Kadang merasa tenang',
                    'c': 'Selalu merasa tenang'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 3,
                'dimension': 'Spiritual',
                'question': 'Saya menghindari perbuatan yang dilarang oleh agama.',
                'options': {
                    'a': 'Jarang menghindari',
                    'b': 'Kadang menghindari',
                    'c': 'Selalu berusaha menghindari'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            # Dimensi Sosial (Pertanyaan 4, 5, 6, 19)
            {
                'id': 4,
                'dimension': 'Sosial',
                'question': 'Saya mudah bekerja sama dengan teman sekelas.',
                'options': {
                    'a': 'Sulit bekerja sama',
                    'b': 'Kadang mudah bekerja sama',
                    'c': 'Sangat mudah bekerja sama'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 5,
                'dimension': 'Sosial',
                'question': 'Saya membantu teman yang mengalami kesulitan belajar.',
                'options': {
                    'a': 'Tidak pernah membantu',
                    'b': 'Kadang membantu',
                    'c': 'Selalu siap membantu'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 6,
                'dimension': 'Sosial',
                'question': 'Saya menghargai pendapat teman walau berbeda.',
                'options': {
                    'a': 'Jarang menghargai',
                    'b': 'Kadang menghargai',
                    'c': 'Selalu menghargai'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            # Dimensi Emosional (Pertanyaan 7, 8, 9, 21)
            {
                'id': 7,
                'dimension': 'Emosional',
                'question': 'Saya dapat mengendalikan emosi ketika menghadapi masalah.',
                'options': {
                    'a': 'Sulit mengendalikan diri',
                    'b': 'Kadang bisa mengendalikan diri',
                    'c': 'Selalu tenang dalam menghadapi masalah'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 8,
                'dimension': 'Emosional',
                'question': 'Saya cepat marah jika sesuatu tidak sesuai keinginan.',
                'options': {
                    'a': 'Sering marah',
                    'b': 'Kadang marah',
                    'c': 'Jarang marah'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 9,
                'dimension': 'Emosional',
                'question': 'Saya berusaha berpikir positif saat menghadapi kesulitan.',
                'options': {
                    'a': 'Jarang berpikir positif',
                    'b': 'Kadang berpikir positif',
                    'c': 'Selalu berpikir positif'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            # Dimensi Kognitif (Pertanyaan 10, 11, 12, 24)
            {
                'id': 10,
                'dimension': 'Kognitif',
                'question': 'Saya suka mencari tahu hal baru di luar pelajaran sekolah.',
                'options': {
                    'a': 'Tidak tertarik belajar hal baru',
                    'b': 'Kadang tertarik',
                    'c': 'Sangat suka belajar hal baru'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 11,
                'dimension': 'Kognitif',
                'question': 'Saya mampu menjelaskan kembali pelajaran dengan cara saya sendiri.',
                'options': {
                    'a': 'Belum mampu',
                    'b': 'Cukup mampu',
                    'c': 'Sangat mampu'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 12,
                'dimension': 'Kognitif',
                'question': 'Saya menggunakan logika dan alasan ketika mengambil keputusan.',
                'options': {
                    'a': 'Jarang menggunakan logika',
                    'b': 'Kadang menggunakan logika',
                    'c': 'Selalu berpikir logis'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            # Dimensi Moral (Pertanyaan 13, 14, 15, 22)
            {
                'id': 13,
                'dimension': 'Moral',
                'question': 'Saya meminta maaf jika melakukan kesalahan.',
                'options': {
                    'a': 'Jarang meminta maaf',
                    'b': 'Kadang meminta maaf',
                    'c': 'Selalu meminta maaf dengan tulus'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 14,
                'dimension': 'Moral',
                'question': 'Saya berusaha jujur meskipun dalam situasi sulit.',
                'options': {
                    'a': 'Kadang tidak jujur',
                    'b': 'Sering jujur tapi masih takut',
                    'c': 'Selalu jujur'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 15,
                'dimension': 'Moral',
                'question': 'Saya menghormati guru dan orang tua.',
                'options': {
                    'a': 'Jarang menghormati',
                    'b': 'Kadang menghormati',
                    'c': 'Selalu menghormati dan menghargai'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            # Dimensi Motivasi (Pertanyaan 16, 17, 18, 23)
            {
                'id': 16,
                'dimension': 'Motivasi',
                'question': 'Saya berusaha mencapai hasil belajar yang lebih baik setiap hari.',
                'options': {
                    'a': 'Jarang berusaha',
                    'b': 'Berusaha kadang-kadang',
                    'c': 'Selalu berusaha maksimal'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 17,
                'dimension': 'Motivasi',
                'question': 'Saya memiliki tujuan yang jelas dalam belajar di sekolah.',
                'options': {
                    'a': 'Belum punya tujuan',
                    'b': 'Ada tujuan tapi belum jelas',
                    'c': 'Tujuan belajar sangat jelas'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 18,
                'dimension': 'Motivasi',
                'question': 'Saya tetap berusaha walau pernah gagal.',
                'options': {
                    'a': 'Mudah menyerah',
                    'b': 'Kadang bertahan',
                    'c': 'Selalu berusaha bangkit'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            # Kembali ke pertanyaan dimensi lain sesuai urutan
            {
                'id': 19,
                'dimension': 'Sosial',
                'question': 'Saya menjaga sopan santun dalam berbicara dengan orang lain.',
                'options': {
                    'a': 'Sering berbicara seenaknya',
                    'b': 'Kadang menjaga sopan santun',
                    'c': 'Selalu berbicara sopan dan santun'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 20,
                'dimension': 'Spiritual',
                'question': 'Saya merasa bersyukur atas hal-hal kecil dalam hidup.',
                'options': {
                    'a': 'Jarang bersyukur',
                    'b': 'Kadang bersyukur',
                    'c': 'Selalu bersyukur'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 21,
                'dimension': 'Emosional',
                'question': 'Saya mudah memaafkan orang yang berbuat salah pada saya.',
                'options': {
                    'a': 'Sulit memaafkan',
                    'b': 'Kadang memaafkan',
                    'c': 'Mudah memaafkan'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 22,
                'dimension': 'Moral',
                'question': 'Saya berani menegur teman yang berbuat salah.',
                'options': {
                    'a': 'Tidak berani menegur',
                    'b': 'Kadang berani',
                    'c': 'Selalu berani menegur dengan sopan'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 23,
                'dimension': 'Motivasi',
                'question': 'Saya punya cita-cita yang ingin saya capai di masa depan.',
                'options': {
                    'a': 'Belum punya cita-cita',
                    'b': 'Sudah punya tapi belum jelas',
                    'c': 'Punya cita-cita jelas dan kuat'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            },
            {
                'id': 24,
                'dimension': 'Kognitif',
                'question': 'Saya suka mencari solusi dari permasalahan yang saya hadapi.',
                'options': {
                    'a': 'Jarang mencari solusi',
                    'b': 'Kadang mencari solusi',
                    'c': 'Selalu mencari solusi secara mandiri'
                },
                'score': {'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3},
                'type': 'multiple_choice'
            }
        ],
        'interpretation': {
            'total_score': {
                '60-72': 'Sangat Baik — Siswa memiliki pemahaman jati diri yang kuat, sadar akan nilai spiritual, sosial, emosional, moral, dan motivasi diri.',
                '45-59': 'Cukup Baik — Siswa sudah mengenal jati diri, namun masih perlu memperdalam aspek tertentu (misalnya pengendalian emosi atau motivasi).',
                '0-44': 'Perlu Pengembangan — Siswa masih dalam tahap pencarian jati diri dan membutuhkan pendampingan lebih lanjut.'
            },
            'dimension_average': {
                '2.6-3.0': 'Tinggi — Kesadaran dan perilaku pada dimensi tersebut sangat baik.',
                '1.8-2.5': 'Sedang — Masih perlu konsistensi dan pendalaman.',
                '1.0-1.7': 'Rendah — Perlu perhatian dan pembinaan lebih dalam.'
            }
        }
    },
    
    'eq': {
        'name': 'Kecerdasan Emosional (EQ)',
        'emoji': '💝',
        'description': 'Let\'s talk about feelings! Kita akan eksplorasi cara kamu mengelola emosi.',
        'questions': [
            {
                'id': 1,
                'question': 'Bagaimana kamu mengenali emosi yang sedang kamu rasakan? Apa tanda-tanda fisik atau mental yang kamu perhatikan?',
                'type': 'text',
                'required': True
            },
            {
                'id': 2,
                'question': 'Kapan terakhir kali kamu merasa overwhelmed atau stres? Bagaimana kamu menangani perasaan itu?',
                'type': 'text',
                'required': True
            },
            {
                'id': 3,
                'question': 'Bayangkan teman kamu curhat tentang masalah pribadi yang berat. Bagaimana kamu akan merespons dan membantu mereka?',
                'type': 'text',
                'required': True
            },
            {
                'id': 4,
                'question': 'Bagaimana kamu menenangkan diri saat marah atau kesal? Strategi apa yang paling efektif buat kamu?',
                'type': 'text',
                'required': True
            },
            {
                'id': 5,
                'question': 'Ceritakan pengalaman ketika kamu berhasil menyelesaikan konflik dengan teman atau keluarga. Bagaimana caranya?',
                'type': 'text',
                'required': True
            },
            {
                'id': 6,
                'question': 'Bagaimana kamu membangun dan menjaga pertemanan yang baik? Apa yang kamu lakukan untuk mempertahankan hubungan?',
                'type': 'text',
                'required': True
            },
            {
                'id': 7,
                'question': 'Apa yang memotivasi kamu untuk terus berkembang dan menjadi versi terbaik dari diri kamu?',
                'type': 'text',
                'required': True
            }
        ]
    },
    
    'gaya_belajar': {
        'name': 'Gaya Belajar',
        'emoji': '📚',
        'description': 'Yuk cari tau cara belajar yang paling cocok buat kamu!',
        'questions': [
            {
                'id': 1,
                'question': 'Saat belajar hal baru, kamu lebih suka cara yang mana? (baca buku, lihat video, langsung praktik, atau dijelasin orang lain)',
                'type': 'choice',
                'options': ['Baca buku/artikel', 'Lihat video/tutorial', 'Langsung praktik', 'Dijelasin orang lain'],
                'required': True
            },
            {
                'id': 2,
                'question': 'Kalau lagi belajar, kamu lebih fokus sendirian atau sambil dengerin musik/ada suara?',
                'type': 'choice',
                'options': ['Sendirian, sunyi total', 'Sambil dengerin musik', 'Ada suara latar (cafe, dll)', 'Tidak masalah'],
                'required': True
            },
            {
                'id': 3,
                'question': 'Lebih mudah ingat sesuatu kalau gimana?',
                'type': 'choice',
                'options': ['Ditulis/dicatat', 'Dijelasin ke orang lain', 'Praktik langsung', 'Bikin diagram/mindmap'],
                'required': True
            },
            {
                'id': 4,
                'question': 'Saat presentasi, kamu lebih nyaman pakai slide visual atau jelasin langsung tanpa slide?',
                'type': 'choice',
                'options': ['Pakai slide visual', 'Jelasin langsung tanpa slide', 'Kombinasi keduanya', 'Tidak masalah'],
                'required': True
            },
            {
                'id': 5,
                'question': 'Apa hobi atau aktivitas favorit kamu yang berhubungan dengan belajar atau mengembangkan skill?',
                'type': 'text',
                'required': True
            },
            {
                'id': 6,
                'question': 'Mata pelajaran apa yang paling kamu suka dan kenapa?',
                'type': 'text',
                'required': True
            },
            {
                'id': 7,
                'question': 'Bagaimana cara kamu bikin catatan? (mindmap, list, gambar, atau ga bikin catatan sama sekali)',
                'type': 'choice',
                'options': ['Mindmap/diagram', 'List/bullet points', 'Gambar/sketsa', 'Tidak bikin catatan', 'Kombinasi'],
                'required': True
            }
        ]
    },
    
    'minat_karir': {
        'name': 'Minat Karir',
        'emoji': '🎯',
        'description': 'Bingung mau pilih jurusan IPA, IPS, atau Bahasa? Yuk kita tentukan bareng!',
        'questions': [
            {
                'id': 1,
                'question': 'Mata pelajaran apa yang paling kamu suka dan kenapa?',
                'type': 'text',
                'required': True
            },
            {
                'id': 2,
                'question': 'Mata pelajaran mana yang paling gampang kamu pahami?',
                'type': 'text',
                'required': True
            },
            {
                'id': 3,
                'question': 'Kamu lebih suka yang mana?',
                'type': 'choice',
                'options': ['Ngitung dan eksperimen', 'Diskusi dan analisis sosial', 'Keduanya sama suka', 'Tidak suka keduanya'],
                'required': True
            },
            {
                'id': 4,
                'question': 'Apa cita-cita atau bidang karir yang kamu minati?',
                'type': 'text',
                'required': True
            },
            {
                'id': 5,
                'question': 'Topik apa yang sering kamu cari tau sendiri? (science, sosial, budaya, bahasa, dll)',
                'type': 'text',
                'required': True
            },
            {
                'id': 6,
                'question': 'Kegiatan ekstrakurikuler atau hobi apa yang relate dengan jurusan yang kamu minati?',
                'type': 'text',
                'required': True
            },
            {
                'id': 7,
                'question': 'Gambarkan kuliah dan karir yang kamu bayangkan 5 tahun ke depan.',
                'type': 'text',
                'required': True
            }
        ]
    },
    
    'rekomendasi_jurusan': {
        'name': 'Rekomendasi Jurusan',
        'emoji': '🎓',
        'description': 'Saatnya mikirin masa depan! Mari cari program studi yang pas buat kamu.',
        'questions': [
            {
                'id': 1,
                'question': 'Pekerjaan impian atau bidang apa yang ingin kamu tekuni?',
                'type': 'text',
                'required': True
            },
            {
                'id': 2,
                'question': 'Kamu lebih suka kerja yang mana?',
                'type': 'choice',
                'options': ['Hands-on/praktik langsung', 'Analitis/riset', 'Kreatif/desain', 'Kombinasi'],
                'required': True
            },
            {
                'id': 3,
                'question': 'Preferensi tempat kerja kamu?',
                'type': 'choice',
                'options': ['Kantoran', 'Lapangan/outdoor', 'Remote/WFH', 'Entrepreneurship/wiraswasta'],
                'required': True
            },
            {
                'id': 4,
                'question': 'Industri atau sektor apa yang menarik buat kamu? (tech, kesehatan, bisnis, pendidikan, dll)',
                'type': 'text',
                'required': True
            },
            {
                'id': 5,
                'question': 'Skill apa yang sudah kamu kuasai atau ingin kamu kembangkan?',
                'type': 'text',
                'required': True
            },
            {
                'id': 6,
                'question': 'Ada pertimbangan lain untuk kuliah? (lokasi, biaya, prospek kerja, dll)',
                'type': 'text',
                'required': True
            },
            {
                'id': 7,
                'question': '5 tahun ke depan, kamu ingin jadi apa atau seperti apa?',
                'type': 'text',
                'required': True
            }
        ]
    }
}


def get_survey_questions(module_type):
    """Get survey questions for a specific module"""
    return SURVEY_QUESTIONS.get(module_type, None)


def get_all_surveys():
    """Get all available surveys"""
    return SURVEY_QUESTIONS


def get_question_by_id(module_type, question_id):
    """Get specific question by ID"""
    survey = SURVEY_QUESTIONS.get(module_type)
    if not survey:
        return None
    
    for question in survey['questions']:
        if question['id'] == question_id:
            return question
    
    return None


def get_next_question(module_type, current_question_id):
    """Get next question in sequence"""
    survey = SURVEY_QUESTIONS.get(module_type)
    if not survey:
        return None
    
    questions = survey['questions']
    for i, question in enumerate(questions):
        if question['id'] == current_question_id and i < len(questions) - 1:
            return questions[i + 1]
    
    return None  # No more questions


def is_last_question(module_type, question_id):
    """Check if this is the last question"""
    survey = SURVEY_QUESTIONS.get(module_type)
    if not survey:
        return True
    
    questions = survey['questions']
    return questions[-1]['id'] == question_id
