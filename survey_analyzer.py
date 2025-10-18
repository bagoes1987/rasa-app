"""
Survey Analyzer
Sistem analisis survey yang menggantikan AI untuk menghasilkan hasil analisis
"""

import json
from datetime import datetime
from models import SurveyAnswer, SurveyQuestion

class SurveyAnalyzer:
    """Analyzer untuk survey responses"""
    
    def __init__(self):
        self.analysis_templates = {
            'jati_diri': self._analyze_jati_diri,
            'eq': self._analyze_eq,
            'gaya_belajar': self._analyze_gaya_belajar,
            'minat_karir': self._analyze_minat_karir,
            'rekomendasi_jurusan': self._analyze_rekomendasi_jurusan
        }
    
    def analyze_survey(self, user_id, session_id, module_type):
        """Analyze survey responses for a specific module"""
        try:
            # Get all answers for this user and session
            answers = SurveyAnswer.query.filter_by(
                user_id=user_id,
                session_id=session_id
            ).join(SurveyQuestion).filter(
                SurveyQuestion.module_type == module_type
            ).all()
            
            if not answers:
                return self._get_default_result(module_type, "Tidak ada jawaban survey yang ditemukan.")
            
            # Parse answers into structured data
            survey_data = {}
            for answer in answers:
                question = answer.question
                survey_data[question.question_id] = {
                    'question': question.question_text,
                    'answer': answer.answer_text,
                    'type': question.question_type
                }
            
            # Analyze based on module type
            if module_type in self.analysis_templates:
                result = self.analysis_templates[module_type](survey_data)
            else:
                result = self._get_default_result(module_type, "Modul tidak dikenali.")
            
            return result
            
        except Exception as e:
            return self._get_default_result(module_type, f"Error dalam analisis: {str(e)}")
    
    def _analyze_jati_diri(self, survey_data):
        """Analyze jati diri survey responses - Updated for 6 dimensions (v3.0)"""
        total_questions = len(survey_data)
        if total_questions == 0:
            return self._get_default_result('jati_diri', "Tidak ada jawaban untuk dianalisis.")
        
        # Calculate scores for each dimension (6 dimensions baru)
        dimension_scores = {
            'Spiritual': 0,
            'Sosial': 0,
            'Emosional': 0,
            'Kognitif': 0,
            'Moral': 0,
            'Motivasi': 0
        }
        
        dimension_count = {
            'Spiritual': 0,
            'Sosial': 0,
            'Emosional': 0,
            'Kognitif': 0,
            'Moral': 0,
            'Motivasi': 0
        }
        
        total_score = 0
        
        # Analyze each response
        for q_id, data in survey_data.items():
            answer = data['answer'].lower().strip()
            
            # Skip if answer is not a, b, or c (case insensitive)
            if answer not in ['a', 'b', 'c', 'A', 'B', 'C']:
                continue
                
            # Get question info from survey_questions
            from survey_questions import SURVEY_QUESTIONS
            jati_diri_questions = SURVEY_QUESTIONS['jati_diri']['questions']
            
            # Find the question by ID
            question_info = None
            for q in jati_diri_questions:
                if q['id'] == int(q_id):
                    question_info = q
                    break
            
            if not question_info:
                continue
                
            # Calculate score (A/a=1, B/b=2, C/c=3)
            score = question_info['score'][answer]
            total_score += score
            
            # Add to dimension score
            dimension = question_info['dimension']
            if dimension in dimension_scores:
                dimension_scores[dimension] += score
                dimension_count[dimension] += 1
        
        # Determine overall category based on total score
        if total_score >= 60:
            overall_category = "Sangat Baik"
            overall_desc = "Siswa memiliki pemahaman jati diri yang kuat, sadar akan nilai spiritual, sosial, emosional, moral, dan motivasi diri."
        elif total_score >= 45:
            overall_category = "Cukup Baik"
            overall_desc = "Siswa sudah mengenal jati diri, namun masih perlu memperdalam aspek tertentu (misalnya pengendalian emosi atau motivasi)."
        else:
            overall_category = "Perlu Pengembangan"
            overall_desc = "Siswa masih dalam tahap pencarian jati diri dan membutuhkan pendampingan lebih lanjut."
        
        # Analyze dimension strengths and weaknesses
        dimension_analysis = {}
        dimension_insights = {}
        
        for dimension, score in dimension_scores.items():
            questions_in_dim = dimension_count[dimension]
            if questions_in_dim == 0:
                continue
                
            avg_score = score / questions_in_dim
            
            # Kategorisasi berdasarkan rata-rata dimensi
            if avg_score >= 2.6:
                level = "Tinggi"
                desc = "Kesadaran dan perilaku pada dimensi tersebut sangat baik."
            elif avg_score >= 1.8:
                level = "Sedang"
                desc = "Masih perlu konsistensi dan pendalaman."
            else:
                level = "Rendah"
                desc = "Perlu perhatian dan pembinaan lebih dalam."
            
            dimension_analysis[dimension] = {
                'score': score,
                'average': round(avg_score, 2),
                'level': level,
                'description': desc,
                'max_score': questions_in_dim * 3
            }
            
            # Generate insights per dimension
            if dimension == "Spiritual":
                if level == "Tinggi":
                    dimension_insights[dimension] = "Kamu memiliki kesadaran spiritual yang baik dan mampu menjalankan nilai keagamaan dalam kehidupan sehari-hari."
                elif level == "Sedang":
                    dimension_insights[dimension] = "Kamu sudah memiliki dasar spiritual yang cukup baik, namun perlu lebih konsisten dalam menjalankan ibadah dan bersyukur."
                else:
                    dimension_insights[dimension] = "Kamu perlu meningkatkan kesadaran spiritual dengan lebih rutin beribadah dan merenungkan nilai-nilai keagamaan."
            
            elif dimension == "Sosial":
                if level == "Tinggi":
                    dimension_insights[dimension] = "Kamu sangat baik dalam berinteraksi dengan orang lain dan memiliki empati yang tinggi."
                elif level == "Sedang":
                    dimension_insights[dimension] = "Kamu cukup baik dalam berinteraksi dengan orang lain, namun masih bisa lebih aktif dalam membantu dan menghargai teman."
                else:
                    dimension_insights[dimension] = "Kamu perlu meningkatkan kemampuan bersosialisasi dan lebih peduli dengan orang di sekitar."
            
            elif dimension == "Emosional":
                if level == "Tinggi":
                    dimension_insights[dimension] = "Kamu memiliki kecerdasan emosional yang baik dan mampu mengendalikan diri dengan baik."
                elif level == "Sedang":
                    dimension_insights[dimension] = "Kamu cukup mampu mengelola emosi, namun masih perlu melatih pengendalian diri saat menghadapi masalah."
                else:
                    dimension_insights[dimension] = "Kamu masih perlu melatih pengendalian emosi dan berpikir positif saat menghadapi masalah."
            
            elif dimension == "Kognitif":
                if level == "Tinggi":
                    dimension_insights[dimension] = "Kamu memiliki rasa ingin tahu yang tinggi dan suka memecahkan masalah secara logis."
                elif level == "Sedang":
                    dimension_insights[dimension] = "Kamu memiliki kemampuan berpikir yang cukup baik, namun bisa lebih aktif dalam mencari pengetahuan baru."
                else:
                    dimension_insights[dimension] = "Kamu perlu meningkatkan kemampuan berpikir kritis dan rasa ingin tahu terhadap hal-hal baru."
            
            elif dimension == "Moral":
                if level == "Tinggi":
                    dimension_insights[dimension] = "Kamu memiliki integritas moral yang kuat dan selalu berpegang pada nilai-nilai kejujuran."
                elif level == "Sedang":
                    dimension_insights[dimension] = "Kamu memahami nilai-nilai moral, namun perlu meningkatkan keberanian dan kejujuran dalam tindakan nyata."
                else:
                    dimension_insights[dimension] = "Kamu perlu memperkuat nilai-nilai moral seperti kejujuran, tanggung jawab, dan keberanian."
            
            elif dimension == "Motivasi":
                if level == "Tinggi":
                    dimension_insights[dimension] = "Kamu punya cita-cita yang jelas dan semangat belajar yang tinggi untuk mencapainya."
                elif level == "Sedang":
                    dimension_insights[dimension] = "Kamu memiliki motivasi yang cukup baik, namun perlu lebih konsisten dalam usaha mencapai tujuan."
                else:
                    dimension_insights[dimension] = "Kamu perlu menetapkan tujuan yang lebih jelas dan meningkatkan motivasi untuk mencapainya."
        
        # Generate recommendations based on low dimensions
        recommendations = []
        for dimension, analysis in dimension_analysis.items():
            if analysis['average'] < 2.0:
                if dimension == "Spiritual":
                    recommendations.append("Tingkatkan rutinitas ibadah dan refleksi spiritual")
                elif dimension == "Sosial":
                    recommendations.append("Lebih aktif berinteraksi dan membantu teman")
                elif dimension == "Emosional":
                    recommendations.append("Latih pengendalian emosi dan berpikir positif")
                elif dimension == "Kognitif":
                    recommendations.append("Tingkatkan rasa ingin tahu dan berpikir kritis")
                elif dimension == "Moral":
                    recommendations.append("Perkuat nilai kejujuran dan tanggung jawab")
                elif dimension == "Motivasi":
                    recommendations.append("Tetapkan tujuan jelas dan tingkatkan semangat belajar")
        
        if not recommendations:
            recommendations.append("Pertahankan semangat dan terus kembangkan semua aspek jati diri")
        
        # Get top 3 strengths
        kekuatan_inti = []
        sorted_dimensions = sorted(dimension_analysis.items(), key=lambda x: x[1]['average'], reverse=True)
        for dimension, analysis in sorted_dimensions[:3]:
            if analysis['average'] >= 2.0:
                kekuatan_inti.append(f"{dimension}: {dimension_insights.get(dimension, 'Baik')}")
        
        if not kekuatan_inti:
            kekuatan_inti.append("Memiliki potensi untuk berkembang di semua aspek jati diri")
        
        # Format result for compatibility with existing system
        result = {
            "ringkasan_jati_diri": f"Berdasarkan analisis {total_questions} pertanyaan, skor total kamu adalah {total_score}/72 ({overall_category}). {overall_desc}",
            
            "kekuatan_inti": kekuatan_inti[:3],
            
            "area_pengembangan": recommendations,
            
            "nilai_utama": [dim for dim, analysis in sorted_dimensions[:4] if analysis['average'] >= 2.0],
            
            "kesimpulan": f"Secara keseluruhan ({overall_category}), kamu memiliki potensi diri yang baik. {self._get_kesimpulan_jati_diri(dimension_analysis)}",
            
            # Additional detailed analysis
            "total_score": total_score,
            "max_total_score": 72,
            "overall_category": overall_category,
            "overall_description": overall_desc,
            "dimension_analysis": dimension_analysis,
            "dimension_insights": dimension_insights,
            "persentase": round((total_score / 72) * 100, 1)
        }
        
        return result
    
    def _get_kesimpulan_jati_diri(self, dimension_analysis):
        """Generate conclusion based on dimension analysis"""
        high_dims = []
        low_dims = []
        
        for dimension, analysis in dimension_analysis.items():
            if analysis['average'] >= 2.6:
                high_dims.append(dimension)
            elif analysis['average'] < 1.8:
                low_dims.append(dimension)
        
        if len(high_dims) >= 4:
            return "Pertahankan semangat belajar dan terus kembangkan semua aspek kepribadian."
        elif len(low_dims) >= 3:
            return "Fokus pada pengembangan aspek-aspek yang masih perlu ditingkatkan dengan pendampingan yang tepat."
        else:
            return "Pertahankan kekuatan yang sudah ada dan tingkatkan aspek-aspek yang masih perlu dikembangkan."
    
    
    def _analyze_eq(self, survey_data):
        """Analyze EQ responses"""
        # Analyze emotional intelligence aspects
        self_awareness = 7.0
        emotion_regulation = 7.0
        empathy = 7.0
        social_skills = 7.0
        motivation = 7.0
        
        # Analyze answers for EQ indicators
        for q_id, data in survey_data.items():
            answer = data['answer'].lower()
            
            if q_id == 1:  # Self-awareness
                if any(word in answer for word in ['sadari', 'perhatikan', 'rasa', 'merasa']):
                    self_awareness += 1.5
                if any(word in answer for word in ['bingung', 'tidak tahu', 'sulit']):
                    self_awareness -= 1.0
            
            elif q_id == 2:  # Stress management
                if any(word in answer for word in ['tarik napas', 'tenang', 'relaks', 'meditasi']):
                    emotion_regulation += 1.5
                if any(word in answer for word in ['marah', 'panik', 'stres']):
                    emotion_regulation -= 1.0
            
            elif q_id == 3:  # Empathy
                if any(word in answer for word in ['dengarkan', 'pahami', 'empati', 'dukung']):
                    empathy += 1.5
                if any(word in answer for word in ['saran', 'solusi', 'langsung']):
                    empathy += 0.5
            
            elif q_id == 5:  # Conflict resolution
                if any(word in answer for word in ['bicara', 'komunikasi', 'diskusi', 'kompromi']):
                    social_skills += 1.5
                if any(word in answer for word in ['hindari', 'abaikan', 'diam']):
                    social_skills -= 1.0
        
        # Normalize scores
        scores = {
            'kesadaran_diri': min(10, max(1, self_awareness)),
            'pengaturan_emosi': min(10, max(1, emotion_regulation)),
            'empati': min(10, max(1, empathy)),
            'keterampilan_sosial': min(10, max(1, social_skills)),
            'motivasi_diri': min(10, max(1, motivation))
        }
        
        avg_score = sum(scores.values()) / len(scores)
        
        if avg_score >= 8:
            level = "Tinggi"
        elif avg_score >= 6:
            level = "Sedang"
        else:
            level = "Berkembang"
        
        result = {
            "skor_eq": scores,
            "ringkasan_eq": f"Kecerdasan emosional Anda berada pada level {level} dengan skor rata-rata {avg_score:.1f}/10. Anda menunjukkan kemampuan yang baik dalam {max(scores, key=scores.get).replace('_', ' ')}.",
            "kekuatan_eq": [
                f"Kesadaran diri yang baik (skor: {scores['kesadaran_diri']:.1f})",
                f"Empati yang tinggi (skor: {scores['empati']:.1f})"
            ],
            "saran_peningkatan": [
                "Praktikkan mindfulness untuk meningkatkan kesadaran diri",
                "Belajar teknik relaksasi untuk mengelola emosi",
                "Latih kemampuan mendengarkan aktif untuk meningkatkan empati"
            ],
            "level_eq": level
        }
        
        return result
    
    def _analyze_gaya_belajar(self, survey_data):
        """Analyze learning style responses"""
        # Count preferences
        visual_score = 0
        auditory_score = 0
        kinesthetic_score = 0
        reading_score = 0
        
        for q_id, data in survey_data.items():
            answer = data['answer'].lower()
            
            if q_id == 1:  # Learning preference
                if 'video' in answer or 'gambar' in answer or 'visual' in answer:
                    visual_score += 2
                if 'dengar' in answer or 'audio' in answer or 'suara' in answer:
                    auditory_score += 2
                if 'praktik' in answer or 'langsung' in answer or 'hands-on' in answer:
                    kinesthetic_score += 2
                if 'baca' in answer or 'tulisan' in answer:
                    reading_score += 2
            
            elif q_id == 2:  # Study environment
                if 'sunyi' in answer or 'sendirian' in answer:
                    reading_score += 1
                if 'musik' in answer or 'suara' in answer:
                    auditory_score += 1
            
            elif q_id == 3:  # Memory preference
                if 'tulis' in answer or 'catat' in answer:
                    reading_score += 1
                if 'jelasin' in answer or 'cerita' in answer:
                    auditory_score += 1
                if 'praktik' in answer or 'langsung' in answer:
                    kinesthetic_score += 1
                if 'diagram' in answer or 'mindmap' in answer:
                    visual_score += 1
        
        # Calculate percentages
        total = visual_score + auditory_score + kinesthetic_score + reading_score
        if total == 0:
            total = 1  # Avoid division by zero
        
        percentages = {
            'visual': round((visual_score / total) * 100),
            'auditorik': round((auditory_score / total) * 100),
            'kinestetik': round((kinesthetic_score / total) * 100),
            'reading_writing': round((reading_score / total) * 100)
        }
        
        # Determine primary and secondary styles
        primary = max(percentages, key=percentages.get)
        secondary = max([k for k in percentages.keys() if k != primary], key=percentages.get)
        
        style_names = {
            'visual': 'Visual',
            'auditorik': 'Auditorik',
            'kinestetik': 'Kinestetik',
            'reading_writing': 'Reading/Writing'
        }
        
        result = {
            "gaya_belajar_utama": style_names[primary],
            "gaya_belajar_sekunder": style_names[secondary],
            "persentase": percentages,
            "ringkasan": f"Gaya belajar utama Anda adalah {style_names[primary]} ({percentages[primary]}%), diikuti oleh {style_names[secondary]} ({percentages[secondary]}%). Ini berarti Anda belajar paling efektif dengan {self._get_learning_description(primary)}.",
            "tips_belajar": self._get_learning_tips(primary),
            "rekomendasi_tools": self._get_learning_tools(primary)
        }
        
        return result
    
    def _analyze_minat_karir(self, survey_data):
        """Analyze career interest responses"""
        # Analyze subject preferences and career interests
        subjects = []
        career_interest = ""
        work_style = ""
        
        for q_id, data in survey_data.items():
            answer = data['answer'].lower()
            
            if q_id == 1:  # Favorite subject
                if any(word in answer for word in ['matematika', 'fisika', 'kimia', 'biologi']):
                    subjects.append('Sains')
                if any(word in answer for word in ['sejarah', 'geografi', 'sosiologi', 'ekonomi']):
                    subjects.append('Sosial')
                if any(word in answer for word in ['bahasa', 'sastra', 'komunikasi']):
                    subjects.append('Bahasa')
                if any(word in answer for word in ['seni', 'musik', 'gambar', 'desain']):
                    subjects.append('Seni')
            
            elif q_id == 4:  # Career interest
                career_interest = data['answer']
            
            elif q_id == 2:  # Easy subject
                if any(word in answer for word in ['matematika', 'logika', 'angka']):
                    subjects.append('Matematika')
                if any(word in answer for word in ['bahasa', 'komunikasi', 'menulis']):
                    subjects.append('Komunikasi')
        
        # Determine recommended major
        if 'Sains' in subjects or 'Matematika' in subjects:
            recommended = 'IPA'
            confidence = 85
            reasons = [
                "Minat yang kuat pada mata pelajaran sains dan matematika",
                "Kemampuan analitis dan logis yang baik",
                "Potensi untuk berkembang di bidang teknologi dan penelitian"
            ]
        elif 'Sosial' in subjects:
            recommended = 'IPS'
            confidence = 80
            reasons = [
                "Minat pada ilmu sosial dan humaniora",
                "Kemampuan memahami dinamika masyarakat",
                "Potensi untuk berkontribusi di bidang sosial dan ekonomi"
            ]
        elif 'Bahasa' in subjects or 'Seni' in subjects:
            recommended = 'Bahasa'
            confidence = 75
            reasons = [
                "Minat yang tinggi pada bahasa dan seni",
                "Kemampuan komunikasi dan kreativitas",
                "Potensi untuk berkembang di bidang komunikasi dan budaya"
            ]
        else:
            recommended = 'IPA'
            confidence = 70
            reasons = [
                "Fleksibilitas tinggi untuk berbagai bidang",
                "Potensi untuk berkembang di berbagai jurusan",
                "Dasar yang kuat untuk melanjutkan ke perguruan tinggi"
            ]
        
        result = {
            "rekomendasi_prioritas_1": {
                "jurusan": recommended,
                "confidence": confidence,
                "alasan": reasons
            },
            "rekomendasi_prioritas_2": {
                "jurusan": "IPS" if recommended != "IPS" else "IPA",
                "confidence": confidence - 15,
                "alasan": [
                    "Alternatif yang baik berdasarkan minat umum",
                    "Memberikan perspektif yang berbeda"
                ]
            },
            "ringkasan": f"Berdasarkan analisis minat dan kemampuan, rekomendasi utama adalah jurusan {recommended} dengan tingkat kepercayaan {confidence}%. {career_interest}",
            "mata_pelajaran_kunci": [
                f"Mata pelajaran utama untuk jurusan {recommended}",
                "Mata pelajaran pendukung untuk pengembangan diri"
            ],
            "persiapan": [
                "Fokus pada mata pelajaran kunci",
                "Ikuti kegiatan ekstrakurikuler yang relevan",
                "Eksplorasi lebih dalam tentang bidang yang diminati"
            ]
        }
        
        return result
    
    def _analyze_rekomendasi_jurusan(self, survey_data):
        """Analyze university major recommendations"""
        # Analyze career aspirations and preferences
        career_goals = []
        work_preferences = []
        industries = []
        
        for q_id, data in survey_data.items():
            answer = data['answer'].lower()
            
            if q_id == 1:  # Dream job
                career_goals.append(data['answer'])
            
            elif q_id == 2:  # Work style preference
                if 'hands-on' in answer or 'praktik' in answer:
                    work_preferences.append('Praktis')
                if 'analitis' in answer or 'riset' in answer:
                    work_preferences.append('Analitis')
                if 'kreatif' in answer or 'desain' in answer:
                    work_preferences.append('Kreatif')
            
            elif q_id == 4:  # Industry interest
                if any(word in answer for word in ['tech', 'teknologi', 'komputer', 'software']):
                    industries.append('Teknologi')
                if any(word in answer for word in ['kesehatan', 'medis', 'dokter', 'perawat']):
                    industries.append('Kesehatan')
                if any(word in answer for word in ['bisnis', 'ekonomi', 'manajemen', 'marketing']):
                    industries.append('Bisnis')
                if any(word in answer for word in ['pendidikan', 'guru', 'mengajar', 'sekolah']):
                    industries.append('Pendidikan')
        
        # Generate recommendations based on analysis
        recommendations = []
        
        if 'Teknologi' in industries or 'Praktis' in work_preferences:
            recommendations.append({
                "program_studi": "Teknik Informatika",
                "universitas_contoh": ["Universitas Indonesia", "Institut Teknologi Bandung", "Universitas Gadjah Mada"],
                "kesesuaian": 90,
                "alasan": [
                    "Minat yang kuat pada teknologi dan komputer",
                    "Kemampuan analitis dan problem solving",
                    "Prospek karir yang sangat baik di era digital"
                ],
                "prospek_karir": [
                    "Software Developer dengan gaji 8-15 juta",
                    "Data Scientist dengan gaji 10-20 juta",
                    "Cybersecurity Specialist dengan gaji 12-25 juta"
                ],
                "skill_yang_dikembangkan": ["Programming", "Database Management", "System Analysis"]
            })
        
        if 'Kesehatan' in industries:
            recommendations.append({
                "program_studi": "Kedokteran",
                "universitas_contoh": ["Universitas Indonesia", "Universitas Gadjah Mada", "Universitas Airlangga"],
                "kesesuaian": 85,
                "alasan": [
                    "Minat yang tinggi pada bidang kesehatan",
                    "Kemampuan analitis dan empati",
                    "Kontribusi langsung untuk masyarakat"
                ],
                "prospek_karir": [
                    "Dokter Umum dengan gaji 15-30 juta",
                    "Dokter Spesialis dengan gaji 25-50 juta",
                    "Peneliti Medis dengan gaji 12-25 juta"
                ],
                "skill_yang_dikembangkan": ["Medical Knowledge", "Patient Care", "Research Skills"]
            })
        
        if 'Bisnis' in industries or 'Analitis' in work_preferences:
            recommendations.append({
                "program_studi": "Manajemen Bisnis",
                "universitas_contoh": ["Universitas Indonesia", "Universitas Gadjah Mada", "Institut Teknologi Bandung"],
                "kesesuaian": 80,
                "alasan": [
                    "Minat pada dunia bisnis dan manajemen",
                    "Kemampuan analitis dan strategis",
                    "Fleksibilitas karir di berbagai industri"
                ],
                "prospek_karir": [
                    "Business Analyst dengan gaji 8-15 juta",
                    "Marketing Manager dengan gaji 10-20 juta",
                    "Entrepreneur dengan potensi unlimited"
                ],
                "skill_yang_dikembangkan": ["Business Strategy", "Leadership", "Financial Analysis"]
            })
        
        # If no specific recommendations, provide general ones
        if not recommendations:
            recommendations.append({
                "program_studi": "Psikologi",
                "universitas_contoh": ["Universitas Indonesia", "Universitas Gadjah Mada", "Universitas Airlangga"],
                "kesesuaian": 75,
                "alasan": [
                    "Minat pada pemahaman manusia dan perilaku",
                    "Kemampuan komunikasi dan empati",
                    "Aplikasi luas di berbagai bidang"
                ],
                "prospek_karir": [
                    "Psikolog Klinis dengan gaji 8-15 juta",
                    "HR Specialist dengan gaji 7-12 juta",
                    "Counselor dengan gaji 6-10 juta"
                ],
                "skill_yang_dikembangkan": ["Counseling", "Research", "Communication"]
            })
        
        result = {
            "rekomendasi": recommendations[:3],  # Top 3 recommendations
            "ringkasan_holistik": f"Berdasarkan analisis komprehensif, Anda memiliki potensi yang kuat di bidang {', '.join(industries[:2]) if industries else 'berbagai bidang'}. Rekomendasi utama adalah {recommendations[0]['program_studi']} dengan tingkat kesesuaian {recommendations[0]['kesesuaian']}%.",
            "path_pengembangan": [
                "Fokus pada mata pelajaran yang relevan di SMA",
                "Ikuti kegiatan ekstrakurikuler yang mendukung minat",
                "Eksplorasi lebih dalam tentang program studi yang diminati"
            ],
            "saran_persiapan": [
                "Persiapkan diri untuk ujian masuk perguruan tinggi",
                "Bangun portfolio dan pengalaman yang relevan",
                "Jalin networking dengan profesional di bidang yang diminati"
            ]
        }
        
        return result
    
    def _get_default_result(self, module_type, message):
        """Get default result when analysis fails"""
        return {
            "error": True,
            "message": message,
            "ringkasan": f"Maaf, terjadi kesalahan dalam analisis {module_type}. {message}",
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_learning_description(self, style):
        """Get learning style description"""
        descriptions = {
            'visual': 'menggunakan gambar, diagram, dan visualisasi',
            'auditorik': 'mendengarkan penjelasan dan diskusi',
            'kinestetik': 'melakukan praktik langsung dan hands-on',
            'reading_writing': 'membaca dan menulis catatan'
        }
        return descriptions.get(style, 'berbagai metode')
    
    def _get_learning_tips(self, style):
        """Get learning tips based on style"""
        tips = {
            'visual': [
                "Gunakan mindmap dan diagram untuk memahami konsep",
                "Buat flashcards dengan gambar dan warna",
                "Tonton video tutorial dan presentasi visual"
            ],
            'auditorik': [
                "Rekam penjelasan dan dengarkan berulang kali",
                "Diskusikan materi dengan teman atau kelompok",
                "Gunakan podcast dan audio book untuk belajar"
            ],
            'kinestetik': [
                "Lakukan eksperimen dan praktik langsung",
                "Gunakan model dan simulasi untuk memahami konsep",
                "Belajar sambil bergerak atau dalam posisi yang nyaman"
            ],
            'reading_writing': [
                "Buat catatan detail dan ringkasan",
                "Tulis ulang materi dengan kata-kata sendiri",
                "Gunakan bullet points dan outline untuk organisasi"
            ]
        }
        return tips.get(style, [
            "Kombinasikan berbagai metode belajar",
            "Eksperimen dengan teknik yang berbeda",
            "Temukan cara yang paling efektif untuk Anda"
        ])
    
    def _get_learning_tools(self, style):
        """Get recommended learning tools"""
        tools = {
            'visual': [
                "MindMeister untuk mind mapping",
                "Canva untuk membuat visual notes",
                "YouTube untuk video pembelajaran"
            ],
            'auditorik': [
                "Audacity untuk merekam audio",
                "Spotify untuk podcast edukatif",
                "Voice recorder apps"
            ],
            'kinestetik': [
                "Simulasi online dan virtual labs",
                "Model dan prototype building tools",
                "Interactive learning platforms"
            ],
            'reading_writing': [
                "Notion untuk note-taking",
                "Google Docs untuk kolaborasi",
                "Anki untuk spaced repetition"
            ]
        }
        return tools.get(style, [
            "Google Classroom untuk organisasi",
            "Quizlet untuk flashcards",
            "Khan Academy untuk pembelajaran online"
        ])
