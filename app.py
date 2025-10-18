from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

from config import Config
from models import db, User, Admin, ChatSession, ChatMessage, AnalysisResult, SurveyQuestion, SurveyAnswer
from survey_questions import get_survey_questions, get_all_surveys
from survey_analyzer import SurveyAnalyzer
from report_generator import generate_pdf_report

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# SQLite optimization for better performance and concurrency
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        """Set SQLite PRAGMAs for optimal performance"""
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
        cursor.execute("PRAGMA synchronous=NORMAL")  # Faster writes, still safe
        cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
        cursor.execute("PRAGMA temp_store=MEMORY")  # Use RAM for temp storage
        cursor.execute("PRAGMA mmap_size=268435456")  # 256MB memory-mapped I/O
        cursor.close()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login terlebih dahulu!'

# Survey system (no external API needed)
survey_analyzer = SurveyAnalyzer()

def admin_required(f):
    """Decorator to require admin access"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Silakan login terlebih dahulu!', 'error')
            return redirect(url_for('login'))
        if not isinstance(current_user, Admin):
            flash('Akses ditolak! Halaman ini hanya untuk admin.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_all_surveys():
    """Get all available surveys from survey_questions.py"""
    from survey_questions import SURVEY_QUESTIONS
    return SURVEY_QUESTIONS

@login_manager.user_loader
def load_user(user_id):
    # Try to load as admin first (admin IDs are typically higher)
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    
    # If not found, try to load as regular user
    user = User.query.get(int(user_id))
    if user:
        return user
    
    return None


# ============ AUTHENTICATION ROUTES ============

@app.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        # Redirect admin to admin dashboard
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        # Redirect admin to admin dashboard
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')
        nis = request.form.get('nis')
        tempat_lahir = request.form.get('tempat_lahir')
        tanggal_lahir = request.form.get('tanggal_lahir')
        kelas = request.form.get('kelas')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([nama_lengkap, email, nis, tempat_lahir, tanggal_lahir, kelas, password]):
            flash('Semua field wajib diisi!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Password tidak cocok!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password minimal 6 karakter!', 'error')
            return render_template('register.html')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar!', 'error')
            return render_template('register.html')
        
        # Check if NIS already exists
        if User.query.filter_by(nis=nis).first():
            flash('NIS sudah terdaftar!', 'error')
            return render_template('register.html')
        
        # Parse tanggal lahir
        from datetime import datetime
        try:
            tanggal_lahir_obj = datetime.strptime(tanggal_lahir, '%Y-%m-%d').date()
        except ValueError:
            flash('Format tanggal lahir tidak valid!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            nama_lengkap=nama_lengkap,
            email=email,
            nis=nis,
            tempat_lahir=tempat_lahir,
            tanggal_lahir=tanggal_lahir_obj,
            kelas=kelas
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Auto login after successful registration
        login_user(user)
        
        flash('Registrasi berhasil! Selamat datang!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        # Redirect admin to admin dashboard
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Selamat datang, {user.nama_lengkap}! 👋', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau password salah!', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Berhasil logout!', 'success')
    return redirect(url_for('index'))


# ============ DASHBOARD ROUTES ============

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing all analysis results"""
    # Redirect admin to admin dashboard (check if it's actually an admin)
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    modules = get_all_surveys()
    
    # Get all analysis results for current user
    results = {}
    for module_type in modules.keys():
        result = AnalysisResult.query.filter_by(
            user_id=current_user.id,
            module_type=module_type
        ).order_by(AnalysisResult.created_at.desc()).first()
        
        if result:
            results[module_type] = {
                'data': json.loads(result.result_data),
                'date': result.created_at
            }
    
    # Get recent chat sessions
    recent_sessions = ChatSession.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatSession.started_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                          modules=modules, 
                          results=results,
                          recent_sessions=recent_sessions)


@app.route('/modules')
@login_required
def modules():
    """Display all available modules"""
    # Redirect admin to admin dashboard
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    all_modules = get_all_surveys()
    
    # Check which modules are completed
    completed = {}
    for module_type in all_modules.keys():
        result = AnalysisResult.query.filter_by(
            user_id=current_user.id,
            module_type=module_type
        ).first()
        completed[module_type] = result is not None
    
    return render_template('modules.html', modules=all_modules, completed=completed)


# ============ CHAT ROUTES ============

@app.route('/chat/<module_type>')
@login_required
def chat(module_type):
    """Chat interface for a specific module"""
    # Redirect admin to admin dashboard
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    survey = get_survey_questions(module_type)
    
    if not survey:
        flash('Survey tidak ditemukan!', 'error')
        return redirect(url_for('modules'))
    
    # Create or get active session
    active_session = ChatSession.query.filter_by(
        user_id=current_user.id,
        module_type=module_type,
        is_completed=False
    ).order_by(ChatSession.started_at.desc()).first()
    
    if not active_session:
        active_session = ChatSession(
            user_id=current_user.id,
            module_type=module_type
        )
        db.session.add(active_session)
        db.session.commit()
        
        # Add welcome message with intro
        intro_text = survey.get('intro', survey['description'])
        welcome_msg = ChatMessage(
            session_id=active_session.id,
            role='assistant',
            content=f"Halo {current_user.nama_lengkap}! 👋\n\n{intro_text}"
        )
        db.session.add(welcome_msg)
        db.session.commit()
    
    # Get all messages for this session
    messages = ChatMessage.query.filter_by(
        session_id=active_session.id
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    return render_template('chat.html', 
                          module=survey, 
                          module_type=module_type,
                          session=active_session,
                          messages=messages)


@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_message():
    """Handle sending a message in chat"""
    # Redirect admin to admin dashboard
    if isinstance(current_user, Admin):
        return jsonify({'error': 'Admin tidak bisa mengakses chat siswa'}), 403
    
    data = request.json
    session_id = data.get('session_id')
    user_message = data.get('message')
    
    if not session_id or not user_message:
        return jsonify({'error': 'Missing data'}), 400
    
    # Get session
    chat_session = ChatSession.query.get(session_id)
    if not chat_session or chat_session.user_id != current_user.id:
        return jsonify({'error': 'Invalid session'}), 403
    
    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        role='user',
        content=user_message
    )
    db.session.add(user_msg)
    db.session.commit()
    
    # Get survey questions for this module
    survey = get_survey_questions(chat_session.module_type)
    if not survey:
        return jsonify({'error': 'Survey tidak ditemukan'}), 404
    
    # Get current question number from session
    current_question = chat_session.current_question or 1
    
    # Check if this is intro phase (current_question = 1 means we're at intro)
    if current_question == 1:
        # This is response to intro, start first question
        if user_message.lower() in ['ya', 'y', 'yes', 'siap', 'mulai', 'ok', 'oke']:
            # Start first question
            chat_session.current_question = 2  # Set to 2 because we're about to show question 1
            db.session.commit()
            
            # Ask first question
            first_question = survey['questions'][0]
            ai_response = f"\nOke, kita mulai ya...\n\n**Dimensi: {first_question['dimension']}**\n\n{first_question['id']}. {first_question['question']}"
            
            # Don't add options in text - they will be shown as buttons
        else:
            ai_response = "Baik, kapan saja kamu siap, tinggal ketik 'ya' atau 'siap' untuk mulai survey! 😊"
    
    # Check if this is an answer to a question (current_question > 1 means we're answering questions)
    elif current_question > 1:
        # Save the answer for current question (current_question - 2 because current_question=2 means answering question 1)
        question = survey['questions'][current_question - 2]
        
        # Find the question in database
        db_question = SurveyQuestion.query.filter_by(
            module_type=chat_session.module_type,
            question_id=question['id']
        ).first()
        
        if db_question:
            # Save answer
            answer = SurveyAnswer(
                user_id=current_user.id,
                session_id=session_id,
                question_id=db_question.id,
                answer_text=user_message
            )
            db.session.add(answer)
        
        # Move to next question
        next_question_num = current_question + 1
        chat_session.current_question = next_question_num
        db.session.commit()
        
        # Check if survey is complete
        if next_question_num > len(survey['questions']) + 1:  # +1 because current_question starts from 2
            # Survey complete, generate analysis
            ai_response = "Terima kasih! Survey Anda sudah selesai. Sekarang saya akan menganalisis jawaban Anda dan memberikan hasil yang komprehensif. Silakan tunggu sebentar... 🎉"
            
            # Mark session as completed
            chat_session.is_completed = True
            db.session.commit()
        else:
            # Ask next question
            next_question = survey['questions'][next_question_num - 2]  # -2 because current_question starts from 2
            
            # Format question with dimension above, without options in text - they will be shown as buttons
            ai_response = f"\n**Dimensi: {next_question['dimension']}**\n\n{next_question['id']}. {next_question['question']}"
    else:
        ai_response = "Survey sudah selesai! Silakan lihat hasil analisis Anda."
    
    # Save AI response
    ai_msg = ChatMessage(
        session_id=session_id,
        role='assistant',
        content=ai_response
    )
    db.session.add(ai_msg)
    db.session.commit()
    
    return jsonify({
        'response': ai_response,
        'timestamp': ai_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/api/chat/complete/<int:session_id>', methods=['POST'])
@login_required
def complete_chat(session_id):
    """Complete a chat session and generate analysis"""
    print(f"[DEBUG] complete_chat called for session {session_id}")
    
    # Redirect admin to admin dashboard
    if isinstance(current_user, Admin):
        print(f"[DEBUG] Admin user detected, returning 403")
        return jsonify({'error': 'Admin tidak bisa mengakses chat siswa'}), 403
    
    chat_session = ChatSession.query.get(session_id)
    print(f"[DEBUG] Session found: {chat_session}")
    
    if not chat_session:
        print(f"[DEBUG] Session not found, returning 403")
        return jsonify({'error': 'Invalid session'}), 403
    
    if chat_session.user_id != current_user.id:
        print(f"[DEBUG] User mismatch: session.user_id={chat_session.user_id}, current_user.id={current_user.id}")
        return jsonify({'error': 'Invalid session'}), 403
    
    if chat_session.is_completed:
        print(f"[DEBUG] Session already completed, returning 400")
        return jsonify({'error': 'Session already completed'}), 400
    
    # Generate analysis using survey analyzer
    print(f"[DEBUG] Starting analysis for user {current_user.id}, session {session_id}, module {chat_session.module_type}")
    try:
        analysis_result_data = survey_analyzer.analyze_survey(
            current_user.id,
            session_id,
            chat_session.module_type
        )
        print(f"[DEBUG] Analysis completed successfully")
    except Exception as e:
        print(f"[DEBUG] Analysis failed: {e}")
        return jsonify({'error': f'Analisis gagal: {str(e)}'}), 500
    
    # Convert to JSON string
    analysis_json = json.dumps(analysis_result_data, ensure_ascii=False, indent=2)
    
    # Save analysis result
    analysis_result = AnalysisResult(
        user_id=current_user.id,
        session_id=session_id,
        module_type=chat_session.module_type,
        result_data=analysis_json
    )
    db.session.add(analysis_result)
    
    # Mark session as completed
    chat_session.is_completed = True
    chat_session.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Analisis berhasil disimpan!',
        'redirect': url_for('view_result', module_type=chat_session.module_type)
    })


def get_all_previous_results(user_id):
    """Get all previous analysis results for a user"""
    results = {}
    module_types = ['jati_diri', 'eq', 'gaya_belajar', 'jurusan_sma']
    
    for module_type in module_types:
        result = AnalysisResult.query.filter_by(
            user_id=user_id,
            module_type=module_type
        ).order_by(AnalysisResult.created_at.desc()).first()
        
        if result:
            try:
                results[module_type] = json.loads(result.result_data)
            except:
                results[module_type] = None
    
    return results


@app.route('/result/<module_type>')
@login_required
def view_result(module_type):
    """View analysis result for a specific module"""
    # Redirect admin to admin dashboard
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    survey = get_survey_questions(module_type)
    
    if not survey:
        flash('Survey tidak ditemukan!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get latest result
    result = AnalysisResult.query.filter_by(
        user_id=current_user.id,
        module_type=module_type
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not result:
        flash('Belum ada hasil analisis. Silakan mulai chat terlebih dahulu!', 'info')
        return redirect(url_for('chat', module_type=module_type))
    
    try:
        result_data = json.loads(result.result_data)
    except:
        result_data = {}
    
    return render_template('result.html',
                          module=survey,
                          module_type=module_type,
                          result_data=result_data,
                          date=result.created_at)


# ============ REPORT ROUTES ============

@app.route('/download-report')
@login_required
def download_report():
    """Download complete RASA report as PDF"""
    # Redirect admin to admin dashboard
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    # Get all results
    all_results = {}
    modules = get_all_surveys()
    
    for module_type, module_config in modules.items():
        result = AnalysisResult.query.filter_by(
            user_id=current_user.id,
            module_type=module_type
        ).order_by(AnalysisResult.created_at.desc()).first()
        
        if result:
            try:
                all_results[module_type] = {
                    'config': module_config,
                    'data': json.loads(result.result_data),
                    'date': result.created_at
                }
            except:
                pass
    
    if not all_results:
        flash('Belum ada hasil analisis untuk diunduh!', 'warning')
        return redirect(url_for('dashboard'))
    
    # Generate PDF
    pdf_path = generate_pdf_report(current_user, all_results)
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f'Laporan_RASA_{current_user.nama_lengkap.replace(" ", "_")}.pdf',
        mimetype='application/pdf'
    )


# ============ DATABASE INITIALIZATION ============

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')


# ============ ADMIN ROUTES ============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            admin.last_login = datetime.utcnow()
            db.session.commit()
            flash(f'Selamat datang, {admin.nama_lengkap}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    if isinstance(current_user, Admin):
        logout_user()
        flash('Berhasil logout!', 'success')
        return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('index'))


@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    
    # Get statistics
    total_students = User.query.count()
    total_sessions = ChatSession.query.count()
    completed_sessions = ChatSession.query.filter_by(is_completed=True).count()
    total_results = AnalysisResult.query.count()
    
    # Get recent activities
    recent_sessions = ChatSession.query.order_by(ChatSession.started_at.desc()).limit(10).all()
    recent_results = AnalysisResult.query.order_by(AnalysisResult.created_at.desc()).limit(10).all()
    
    # Get module statistics
    module_stats = {}
    modules = get_all_surveys()
    for module_type in modules.keys():
        count = AnalysisResult.query.filter_by(module_type=module_type).count()
        module_stats[module_type] = {
            'name': modules[module_type]['name'],
            'count': count
        }
    
    # Get class statistics
    class_stats = db.session.query(
        User.kelas, 
        db.func.count(User.id).label('count')
    ).group_by(User.kelas).all()
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_sessions=total_sessions,
                         completed_sessions=completed_sessions,
                         total_results=total_results,
                         recent_sessions=recent_sessions,
                         recent_results=recent_results,
                         module_stats=module_stats,
                         class_stats=class_stats)


@app.route('/admin/students')
@login_required
@admin_required
def admin_students():
    """View all students and their activities"""
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Validate per_page to prevent abuse
    if per_page not in [10, 25, 50]:
        per_page = 20
    
    students = User.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/students.html', students=students)


@app.route('/admin/student/<int:student_id>')
@login_required
def admin_student_detail(student_id):
    """View detailed student information"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    student = User.query.get_or_404(student_id)
    
    # Get student's sessions
    sessions = ChatSession.query.filter_by(user_id=student_id).order_by(ChatSession.started_at.desc()).all()
    
    # Get student's results
    results = AnalysisResult.query.filter_by(user_id=student_id).order_by(AnalysisResult.created_at.desc()).all()
    
    # Parse results data
    parsed_results = {}
    for result in results:
        try:
            parsed_results[result.module_type] = {
                'data': json.loads(result.result_data),
                'date': result.created_at
            }
        except:
            parsed_results[result.module_type] = {
                'data': {},
                'date': result.created_at
            }
    
    return render_template('admin/student_detail.html',
                         student=student,
                         sessions=sessions,
                         results=parsed_results)


@app.route('/admin/reports')
@login_required
def admin_reports():
    """Generate and view system reports"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    # Get comprehensive statistics
    total_students = User.query.count()
    total_sessions = ChatSession.query.count()
    completed_sessions = ChatSession.query.filter_by(is_completed=True).count()
    
    # Module completion rates
    modules = get_all_surveys()
    module_completion = {}
    for module_type in modules.keys():
        total_attempts = ChatSession.query.filter_by(module_type=module_type).count()
        completed_attempts = ChatSession.query.filter_by(module_type=module_type, is_completed=True).count()
        completion_rate = (completed_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        module_completion[module_type] = {
            'name': modules[module_type]['name'],
            'total_attempts': total_attempts,
            'completed_attempts': completed_attempts,
            'completion_rate': round(completion_rate, 1)
        }
    
    # Class-wise statistics
    class_stats = []
    for kelas in ['X', 'XI', 'XII']:
        students_in_class = User.query.filter_by(kelas=kelas).count()
        sessions_in_class = db.session.query(ChatSession).join(User).filter(User.kelas == kelas).count()
        completed_in_class = db.session.query(ChatSession).join(User).filter(
            User.kelas == kelas, ChatSession.is_completed == True
        ).count()
        
        class_stats.append({
            'kelas': kelas,
            'total_students': students_in_class,
            'total_sessions': sessions_in_class,
            'completed_sessions': completed_in_class,
            'completion_rate': round((completed_in_class / sessions_in_class * 100) if sessions_in_class > 0 else 0, 1)
        })
    
    # Recent activity (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_activity = {
        'new_students': User.query.filter(User.created_at >= thirty_days_ago).count(),
        'new_sessions': ChatSession.query.filter(ChatSession.started_at >= thirty_days_ago).count(),
        'completed_sessions': ChatSession.query.filter(
            ChatSession.completed_at >= thirty_days_ago
        ).count()
    }
    
    # Get students for top students list
    students = User.query.paginate(page=1, per_page=1000, error_out=False)
    
    return render_template('admin/reports.html',
                         students=students,
                         total_students=total_students,
                         total_sessions=total_sessions,
                         completed_sessions=completed_sessions,
                         module_completion=module_completion,
                         class_stats=class_stats,
                         recent_activity=recent_activity)


@app.route('/admin/student/<int:student_id>/delete', methods=['POST'])
@login_required
def admin_delete_student(student_id):
    """Delete a student and all their data"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get student
        student = User.query.get_or_404(student_id)
        student_name = student.nama_lengkap
        student_nis = student.nis
        
        # Delete the student (cascade will handle related data)
        # The relationships in models.py have cascade='all, delete-orphan'
        # So deleting the user will automatically delete:
        # - chat_sessions (and their messages via cascade)
        # - analysis_results
        db.session.delete(student)
        
        # Commit all changes
        db.session.commit()
        
        flash(f'Siswa {student_name} (NIS: {student_nis}) berhasil dihapus beserta semua datanya.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error menghapus siswa: {str(e)}', 'error')
    
    return redirect(url_for('admin_students'))


# ============ SURVEY MANAGEMENT ROUTES ============

@app.route('/admin/survey')
@login_required
def admin_survey_management():
    """Survey management dashboard"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    return render_template('admin/survey_management.html')


@app.route('/admin/survey/<module_type>')
@login_required
def admin_survey_questions(module_type):
    """Manage questions for specific module"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    # Get module info
    surveys = get_all_surveys()
    module_info = surveys.get(module_type)
    
    if not module_info:
        flash('Modul tidak ditemukan!', 'error')
        return redirect(url_for('admin_survey_management'))
    
    # Get questions from database
    questions = SurveyQuestion.query.filter_by(module_type=module_type).order_by(SurveyQuestion.question_id).all()
    
    # Parse options for each question
    for question in questions:
        if question.options:
            try:
                question.options = json.loads(question.options)
            except:
                question.options = []
    
    return render_template('admin/survey_questions.html', 
                         module_type=module_type,
                         module_name=module_info['name'],
                         module_emoji=module_info['emoji'],
                         questions=questions)


@app.route('/admin/survey/question/create', methods=['POST'])
@login_required
def admin_create_question():
    """Create new survey question"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        data = request.get_json()
        
        # Get next question ID for this module
        last_question = SurveyQuestion.query.filter_by(module_type=data['module_type']).order_by(SurveyQuestion.question_id.desc()).first()
        next_id = (last_question.question_id + 1) if last_question else 1
        
        # Convert checkbox values to boolean
        is_required = data.get('is_required', True)
        if isinstance(is_required, str):
            is_required = is_required.lower() in ['true', 'on', '1', 'yes']
        else:
            is_required = bool(is_required)
            
        is_active = data.get('is_active', True)
        if isinstance(is_active, str):
            is_active = is_active.lower() in ['true', 'on', '1', 'yes']
        else:
            is_active = bool(is_active)
        
        question = SurveyQuestion(
            module_type=data['module_type'],
            question_id=next_id,
            question_text=data['question_text'],
            question_type=data['question_type'],
            options=json.dumps(data.get('options', [])) if data.get('options') else None,
            is_required=is_required,
            is_active=is_active
        )
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Pertanyaan berhasil dibuat!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/question/<int:question_id>')
@login_required
def admin_get_question(question_id):
    """Get question data for editing"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        question = SurveyQuestion.query.get_or_404(question_id)
        
        question_data = {
            'id': question.id,
            'module_type': question.module_type,
            'question_id': question.question_id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'options': json.loads(question.options) if question.options else [],
            'is_required': question.is_required,
            'is_active': question.is_active
        }
        
        return jsonify({'success': True, 'question': question_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/question/<int:question_id>/update', methods=['PUT'])
@login_required
def admin_update_question(question_id):
    """Update survey question"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        question = SurveyQuestion.query.get_or_404(question_id)
        data = request.get_json()
        
        question.question_text = data['question_text']
        question.question_type = data['question_type']
        question.options = json.dumps(data.get('options', [])) if data.get('options') else None
        
        # Convert checkbox values to boolean
        is_required = data.get('is_required', True)
        if isinstance(is_required, str):
            question.is_required = is_required.lower() in ['true', 'on', '1', 'yes']
        else:
            question.is_required = bool(is_required)
            
        is_active = data.get('is_active', True)
        if isinstance(is_active, str):
            question.is_active = is_active.lower() in ['true', 'on', '1', 'yes']
        else:
            question.is_active = bool(is_active)
        question.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Pertanyaan berhasil diupdate!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/question/<int:question_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_question_status(question_id):
    """Toggle question active status"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        question = SurveyQuestion.query.get_or_404(question_id)
        question.is_active = not question.is_active
        question.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Status pertanyaan berhasil diubah!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/question/<int:question_id>/delete', methods=['POST'])
@login_required
def admin_delete_question(question_id):
    """Delete survey question"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        question = SurveyQuestion.query.get_or_404(question_id)
        
        # Delete related answers first
        SurveyAnswer.query.filter_by(question_id=question_id).delete()
        
        # Delete the question
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Pertanyaan berhasil dihapus!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/init-default', methods=['POST'])
@login_required
def admin_init_default_questions():
    """Initialize default survey questions"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        # Clear existing questions
        SurveyQuestion.query.delete()
        SurveyAnswer.query.delete()
        
        # Initialize from survey_questions.py
        surveys = get_all_surveys()
        
        for module_type, survey_data in surveys.items():
            for question_data in survey_data['questions']:
                question = SurveyQuestion(
                    module_type=module_type,
                    question_id=question_data['id'],
                    question_text=question_data['question'],
                    question_type=question_data['type'],
                    options=json.dumps(question_data.get('options', [])) if question_data.get('options') else None,
                    is_required=question_data.get('required', True),
                    is_active=True
                )
                db.session.add(question)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Pertanyaan default berhasil diinisialisasi!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/clear-all', methods=['POST'])
@login_required
def admin_clear_all_questions():
    """Clear all survey questions"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Akses ditolak!'})
    
    try:
        # Delete all questions and answers
        SurveyAnswer.query.delete()
        SurveyQuestion.query.delete()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Semua pertanyaan berhasil dihapus!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/admin/survey/export')
@login_required
def admin_export_questions():
    """Export all survey questions to JSON"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    try:
        questions = SurveyQuestion.query.order_by(SurveyQuestion.module_type, SurveyQuestion.question_id).all()
        
        export_data = {}
        for question in questions:
            if question.module_type not in export_data:
                export_data[question.module_type] = []
            
            question_data = {
                'id': question.question_id,
                'question': question.question_text,
                'type': question.question_type,
                'options': json.loads(question.options) if question.options else None,
                'required': question.is_required,
                'active': question.is_active
            }
            export_data[question.module_type].append(question_data)
        
        from flask import Response
        from datetime import datetime
        filename = f'survey_questions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return Response(
            json.dumps(export_data, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
        
    except Exception as e:
        flash(f'Error export: {str(e)}', 'error')
        return redirect(url_for('admin_survey_management'))


@app.route('/admin/export/students')
@login_required
def admin_export_students():
    """Export student data to Excel with all analysis results"""
    if not isinstance(current_user, Admin):
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    import csv
    import io
    import json
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header dengan semua kolom analisis
    writer.writerow([
        'NIS', 'Email (Username)', 'Password', 'Nama Lengkap', 'Tempat Lahir', 'Tanggal Lahir', 'Kelas', 'Tanggal Daftar',
        'Total Sesi', 'Sesi Selesai',
        'Jati Diri', 'EQ (Kecerdasan Emosional)', 'Gaya Belajar',
        'Minat Karir', 'Rekomendasi Jurusan'
    ])
    
    module_mapping = {
        'jati_diri': 'Jati Diri',
        'eq': 'EQ (Kecerdasan Emosional)',
        'gaya_belajar': 'Gaya Belajar',
        'minat_karir': 'Minat Karir',
        'rekomendasi_jurusan': 'Rekomendasi Jurusan'
    }
    
    # Write data
    students = User.query.order_by(User.kelas, User.nama_lengkap).all()
    for student in students:
        total_sessions = ChatSession.query.filter_by(user_id=student.id).count()
        completed_sessions = ChatSession.query.filter_by(user_id=student.id, is_completed=True).count()
        
        # Get analysis results
        results = {}
        for module_type in module_mapping.keys():
            result = AnalysisResult.query.filter_by(
                user_id=student.id,
                module_type=module_type
            ).order_by(AnalysisResult.created_at.desc()).first()
            
            if result:
                try:
                    data = json.loads(result.analysis_result)
                    if isinstance(data, dict):
                        summary = data.get('summary', '')
                        if not summary and 'recommendations' in data:
                            # Get recommendations if available
                            recs = data.get('recommendations', [])
                            if isinstance(recs, list) and len(recs) > 0:
                                summary = ', '.join([str(r) for r in recs[:3]])
                        if not summary:
                            # Get any available data
                            summary = str(data)[:200]
                        results[module_type] = summary
                    else:
                        results[module_type] = str(data)[:200]
                except Exception as e:
                    results[module_type] = result.analysis_result[:200] if result.analysis_result else '-'
            else:
                results[module_type] = '-'
        
        writer.writerow([
            student.nis,
            student.email,  # Email sebagai username
            student.password_plain,  # Password asli yang diinput saat pendaftaran
            student.nama_lengkap,
            student.tempat_lahir,
            student.tanggal_lahir.strftime('%Y-%m-%d'),
            student.kelas,
            student.created_at.strftime('%Y-%m-%d'),
            total_sessions,
            completed_sessions,
            results.get('jati_diri', '-'),
            results.get('eq', '-'),
            results.get('gaya_belajar', '-'),
            results.get('minat_karir', '-'),
            results.get('rekomendasi_jurusan', '-')
        ])
    
    output.seek(0)
    
    from flask import Response
    from datetime import datetime
    filename = f'data_siswa_rasa_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    import traceback
    print(f"[ERROR 500] {error}")
    print(f"[ERROR 500] Traceback: {traceback.format_exc()}")
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Initialize database tables
    with app.app_context():
        db.create_all()
        print("[INIT] Database initialized!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

