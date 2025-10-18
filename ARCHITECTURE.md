# 🏗️ RASA - Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│                     (Chrome, Firefox, etc)                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTP/HTTPS
                 │
┌────────────────▼────────────────────────────────────────────┐
│                      FLASK APPLICATION                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    app.py (Main)                      │   │
│  │  • Routes & Controllers                               │   │
│  │  • Request Handling                                   │   │
│  │  • Session Management                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   models.py  │  │  config.py   │  │ chat_modules.py  │  │
│  │  (Database)  │  │ (Settings)   │  │   (Prompts)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                               │
│  ┌──────────────────┐           ┌────────────────────────┐  │
│  │openrouter_service│◄──────────┤  report_generator.py   │  │
│  │    (AI API)      │           │    (PDF Reports)       │  │
│  └──────────────────┘           └────────────────────────┘  │
└────────────────┬─────────────────┬──────────────────────────┘
                 │                 │
                 │                 │
     ┌───────────▼─────┐     ┌────▼─────────────┐
     │  SQLite Database│     │ OpenRouter API   │
     │    (rasa.db)    │     │  (LLM Service)   │
     └─────────────────┘     └──────────────────┘
```

## Component Architecture

### 1. Frontend Layer (Templates + Static)

```
templates/
├── base.html              # Base template with navigation
├── index.html            # Landing page
├── login.html            # User login
├── register.html         # User registration
├── dashboard.html        # Main dashboard
├── modules.html          # Module selection
├── chat.html             # Interactive chat interface
├── result.html           # Analysis results display
└── results/              # Module-specific result templates
    ├── jati_diri.html
    ├── eq.html
    ├── gaya_belajar.html
    ├── jurusan_sma.html
    └── prodi_kuliah.html

static/
├── css/
│   └── style.css         # Custom styles + animations
└── js/
    └── main.js           # JavaScript functionality
```

### 2. Backend Layer (Python/Flask)

#### Core Files:

**app.py** - Main application file
```
Responsibilities:
• Route definitions
• Request/Response handling
• Authentication logic
• Session management
• API endpoints
```

**models.py** - Database models
```
Models:
• User (Authentication & Profile)
• ChatSession (Conversation tracking)
• ChatMessage (Individual messages)
• AnalysisResult (Module results storage)
```

**config.py** - Configuration
```
Settings:
• Database connection
• Secret keys
• API configurations
• Session settings
```

**openrouter_service.py** - AI Integration
```
Functions:
• chat_completion() - Send requests to LLM
• get_rasa_response() - Get AI responses
• analyze_and_generate_result() - Generate analysis
```

**chat_modules.py** - Module Configurations
```
Modules:
• jati_diri - Self-identity analysis
• eq - Emotional intelligence
• gaya_belajar - Learning style
• jurusan_sma - High school major
• prodi_kuliah - University program
```

**report_generator.py** - PDF Generation
```
Functions:
• generate_pdf_report() - Create comprehensive PDF
• Module-specific content generators
• PDF styling and formatting
```

### 3. Database Schema

```sql
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ nama_lengkap    │
│ nis (UNIQUE)    │
│ kelas           │
│ password_hash   │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼──────────┐
│   ChatSessions    │
├───────────────────┤
│ id (PK)           │
│ user_id (FK)      │
│ module_type       │
│ started_at        │
│ completed_at      │
│ is_completed      │
└────────┬──────────┘
         │
         │ 1:N
         │
┌────────▼──────────┐       ┌──────────────────┐
│   ChatMessages    │       │ AnalysisResults  │
├───────────────────┤       ├──────────────────┤
│ id (PK)           │       │ id (PK)          │
│ session_id (FK)   │       │ user_id (FK)     │
│ role              │       │ session_id (FK)  │
│ content           │       │ module_type      │
│ timestamp         │       │ result_data      │
└───────────────────┘       │ created_at       │
                            └──────────────────┘
```

## Data Flow

### User Registration Flow
```
1. User fills registration form
2. Frontend validates input
3. POST request to /register
4. Backend validates data
5. Password hashed with Werkzeug
6. User saved to database
7. Redirect to login page
```

### Chat Interaction Flow
```
1. User sends message
2. JavaScript sends POST to /api/chat/send
3. Backend saves user message to database
4. Backend builds conversation history
5. Request sent to OpenRouter API with:
   • System prompt (module-specific)
   • Conversation history
6. AI generates response
7. Backend saves AI message to database
8. Response sent back to frontend
9. JavaScript displays message in chat
```

### Analysis Generation Flow
```
1. User clicks "Selesai & Analisis"
2. POST request to /api/chat/complete/{session_id}
3. Backend retrieves all messages from session
4. Backend sends to OpenRouter with analysis prompt
5. AI generates structured JSON result
6. Result saved to AnalysisResult table
7. Session marked as completed
8. User redirected to result page
```

### Report Download Flow
```
1. User clicks "Unduh Laporan"
2. GET request to /download-report
3. Backend retrieves all analysis results
4. report_generator.py creates PDF with:
   • Cover page
   • All module results
   • Charts and formatting
5. PDF saved to reports/ directory
6. File sent to user as download
```

## Security Architecture

### Authentication
```
• Flask-Login for session management
• Werkzeug for password hashing (PBKDF2)
• Session cookies with HTTPOnly flag
• CSRF protection (Flask built-in)
```

### Data Protection
```
• Passwords: Hashed with salt
• API Keys: Stored in environment variables
• Database: No sensitive data in plain text
• Sessions: Secure cookie configuration
```

### Input Validation
```
• Frontend: HTML5 validation
• Backend: Flask form validation
• Database: SQLAlchemy ORM (SQL injection protection)
```

## API Integration

### OpenRouter API
```
Endpoint: https://openrouter.ai/api/v1/chat/completions

Request Format:
{
  "model": "openai/gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}

Response Format:
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "AI response here..."
      }
    }
  ]
}
```

## Scalability Considerations

### Current Architecture (Single Server)
```
Suitable for:
• Up to 1000 concurrent users
• Small to medium school deployment
• Limited resources
```

### Future Improvements
```
1. Database:
   • Migrate to PostgreSQL for better concurrency
   • Implement connection pooling
   • Add database replication

2. Caching:
   • Redis for session storage
   • Cache frequently accessed data
   • Rate limiting

3. Load Balancing:
   • Multiple Gunicorn workers
   • Nginx load balancer
   • Horizontal scaling

4. Microservices:
   • Separate AI service
   • Separate report generation service
   • Message queue (Celery + RabbitMQ)
```

## Performance Optimization

### Current Optimizations
```
• Static file caching (30 days)
• Gzip compression
• Lazy loading for images
• Debounced form submissions
• Connection pooling
```

### Recommended Production Settings
```
• Gunicorn workers: (2 × CPU cores) + 1
• Worker timeout: 120 seconds (for AI responses)
• Max requests per worker: 1000
• Nginx caching for static files
```

## Monitoring & Logging

### Application Logs
```python
# Location: journalctl -u rasa
# Content:
• Request/Response logs
• Error traces
• AI API calls
• Database queries
```

### Nginx Logs
```
# Access log: /var/log/nginx/access.log
# Error log: /var/log/nginx/error.log
```

### Database Monitoring
```sql
-- Check active sessions
SELECT COUNT(*) FROM chat_sessions WHERE is_completed = 0;

-- Check user growth
SELECT DATE(created_at), COUNT(*) 
FROM users 
GROUP BY DATE(created_at);
```

## Technology Stack Summary

```
Frontend:
├── HTML5
├── Tailwind CSS
├── JavaScript (Vanilla)
└── Font Awesome Icons

Backend:
├── Python 3.8+
├── Flask 3.0
├── SQLAlchemy (ORM)
├── Flask-Login (Auth)
└── Gunicorn (WSGI)

Database:
└── SQLite3 (Development/Small Scale)

External Services:
├── OpenRouter API (AI/LLM)
└── ReportLab (PDF Generation)

Deployment:
├── Nginx (Web Server)
├── Systemd (Process Management)
└── Let's Encrypt (SSL/TLS)
```

## Development vs Production

| Aspect | Development | Production |
|--------|-------------|------------|
| Debug Mode | Enabled | Disabled |
| Database | SQLite | SQLite/PostgreSQL |
| Server | Flask dev server | Gunicorn + Nginx |
| HTTPS | Optional | Required |
| Logging | Console | File + Syslog |
| Error Display | Full traceback | Generic message |

---

**Last Updated:** 2025
**Version:** 1.0

