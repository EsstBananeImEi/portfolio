"""
E-Mail Benachrichtigungen für Zugriffsanfragen
Optionale Erweiterung für automatische E-Mail-Benachrichtigungen
"""

from flask import current_app, render_template_string
from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    """Initialisiert Flask-Mail mit der App"""
    mail.init_app(app)

def send_admin_notification(access_request):
    """
    Sendet eine E-Mail-Benachrichtigung an den Admin bei neuen Zugriffsanfragen
    
    Voraussetzungen:
    1. Flask-Mail installiert: pip install Flask-Mail
    2. In config.py konfiguriert:
       - MAIL_SERVER
       - MAIL_PORT
       - MAIL_USE_TLS
       - MAIL_USERNAME
       - MAIL_PASSWORD
       - ADMIN_EMAIL
    3. In app/__init__.py initialisiert:
       from app.email_utils import init_mail
       init_mail(app)
    4. In app/main/routes.py import und aufrufen:
       from app.email_utils import send_admin_notification
       send_admin_notification(access_request)
    """
    try:
        admin_email = current_app.config.get('ADMIN_EMAIL')
        if not admin_email:
            print("⚠ ADMIN_EMAIL nicht in config.py konfiguriert")
            return False
        
        subject = f"Neue Zugriffsanfrage von {access_request.name}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #2563eb;">Neue Zugriffsanfrage für Portfolio-Projekte</h2>
                
                <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Name:</strong> {access_request.name}</p>
                    <p><strong>E-Mail:</strong> <a href="mailto:{access_request.email}">{access_request.email}</a></p>
                    <p><strong>Datum:</strong> {access_request.created_at.strftime('%d.%m.%Y %H:%M')}</p>
                    
                    {f'<p><strong>Nachricht:</strong><br>{access_request.message}</p>' if access_request.message else ''}
                </div>
                
                <p>Bitte loggen Sie sich ein, um ein Token zu generieren:</p>
                <p>
                    <a href="{current_app.config.get('BASE_URL', 'http://localhost:5000')}/admin/access-requests" 
                       style="background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Zur Token-Verwaltung
                    </a>
                </p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280; font-size: 12px;">
                    Diese E-Mail wurde automatisch von Ihrem Portfolio-System generiert.
                </p>
            </body>
        </html>
        """
        
        text_body = f"""
        Neue Zugriffsanfrage für Portfolio-Projekte
        
        Name: {access_request.name}
        E-Mail: {access_request.email}
        Datum: {access_request.created_at.strftime('%d.%m.%Y %H:%M')}
        
        {f'Nachricht: {access_request.message}' if access_request.message else ''}
        
        Bitte loggen Sie sich ein, um ein Token zu generieren.
        """
        
        msg = Message(
            subject=subject,
            recipients=[admin_email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        print(f"✓ E-Mail-Benachrichtigung an {admin_email} gesendet")
        return True
        
    except Exception as e:
        print(f"✗ Fehler beim Senden der E-Mail-Benachrichtigung: {e}")
        return False


def send_token_email(access_request):
    """
    Optional: Sendet das Token direkt an den Anfragenden
    (Nur verwenden, wenn Sie keine manuelle Prüfung wünschen)
    """
    try:
        subject = "Ihr Zugangstoken für das Portfolio"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #16a34a;">Ihr Zugangstoken wurde generiert</h2>
                
                <p>Hallo {access_request.name},</p>
                
                <p>Ihr Zugriff auf die Portfolio-Projekte wurde genehmigt!</p>
                
                <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Ihr Token:</strong></p>
                    <code style="background-color: #e5e7eb; padding: 10px; display: block; font-size: 14px; word-break: break-all;">
                        {access_request.token}
                    </code>
                </div>
                
                {f'<p><strong>Gültig bis:</strong> {access_request.token_expires.strftime("%d.%m.%Y")}</p>' if access_request.token_expires else '<p>Dieses Token ist <strong>unbegrenzt</strong> gültig.</p>'}
                
                <p>Gehen Sie auf die Portfolio-Seite und geben Sie das Token ein, um Zugriff auf alle Projekte zu erhalten.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280; font-size: 12px;">
                    Teilen Sie dieses Token nicht mit anderen. Bei Fragen antworten Sie einfach auf diese E-Mail.
                </p>
            </body>
        </html>
        """
        
        text_body = f"""
        Ihr Zugangstoken wurde generiert
        
        Hallo {access_request.name},
        
        Ihr Zugriff auf die Portfolio-Projekte wurde genehmigt!
        
        Ihr Token: {access_request.token}
        
        {f'Gültig bis: {access_request.token_expires.strftime("%d.%m.%Y")}' if access_request.token_expires else 'Dieses Token ist unbegrenzt gültig.'}
        
        Gehen Sie auf die Portfolio-Seite und geben Sie das Token ein.
        """
        
        msg = Message(
            subject=subject,
            recipients=[access_request.email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        print(f"✓ Token an {access_request.email} gesendet")
        return True
        
    except Exception as e:
        print(f"✗ Fehler beim Senden des Tokens: {e}")
        return False
