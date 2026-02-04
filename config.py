import os

class Config:
    DEBUG = True
    
    # Session-Konfiguration (für Token-Speicherung)
    SECRET_KEY = os.getenv("SECRET_KEY", "123")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Für HTTPS auf True setzen
    SESSION_TYPE = 'sqlalchemy'  # Sessions in der Datenbank statt im Dateisystem
    PERMANENT_SESSION_LIFETIME = 86400  # Session läuft nach 24 Stunden ab
    
    # E-Mail-Konfiguration für automatische Benachrichtigungen
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_PORT', '587') == '587'  # TLS für Port 587
    MAIL_USE_SSL = os.getenv('MAIL_PORT', '587') == '465'  # SSL für Port 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
