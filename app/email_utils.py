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
        admin_email = current_app.config.get("ADMIN_EMAIL")
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
            subject=subject, recipients=[admin_email], html=html_body, body=text_body
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
            body=text_body,
        )

        mail.send(msg)
        print(f"✓ Token an {access_request.email} gesendet")
        return True

    except Exception as e:
        print(f"✗ Fehler beim Senden des Tokens: {e}")
        return False


def send_access_credentials(access_request, password):
    """
    Sendet die Login-Zugangsdaten (E-Mail und Passwort) an den genehmigten Benutzer
    """
    try:
        subject = "Ihre Zugangsdaten für das Portfolio"

        base_url = current_app.config.get("BASE_URL", "http://localhost:5000")
        login_url = f"{base_url}/auth/portfolio-login"

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9fafb;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <!-- Header mit Gradient -->
                    <div style="background: linear-gradient(135deg, #16a34a 0%, #8fcc14 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 24px;">Portfolio-Zugang gewährt</h1>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 30px;">
                        <p style="font-size: 16px; color: #374151;">Hallo {access_request.name},</p>
                        
                        <p style="font-size: 16px; color: #374151;">
                            Ihr Zugang zu den Portfolio-Projekten wurde genehmigt! Sie können sich jetzt mit Ihren persönlichen Zugangsdaten anmelden.
                        </p>
                        
                        <!-- Zugangsdaten Box -->
                        <div style="background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%); border-left: 4px solid #16a34a; padding: 20px; border-radius: 8px; margin: 25px 0;">
                            <h3 style="margin-top: 0; color: #16a34a;">Ihre Zugangsdaten</h3>
                            
                            <p style="margin: 10px 0;">
                                <strong style="color: #374151;">E-Mail-Adresse:</strong><br>
                                <code style="background-color: rgba(0,0,0,0.05); padding: 8px 12px; display: inline-block; border-radius: 4px; font-size: 14px; margin-top: 5px;">
                                    {access_request.email}
                                </code>
                            </p>
                            
                            <p style="margin: 10px 0;">
                                <strong style="color: #374151;">Passwort:</strong><br>
                                <code style="background-color: rgba(0,0,0,0.05); padding: 8px 12px; display: inline-block; border-radius: 4px; font-size: 14px; margin-top: 5px; word-break: break-all;">
                                    {password}
                                </code>
                            </p>
                        </div>
                        
                        {f'<p style="color: #6b7280;"><strong>Gültig bis:</strong> {access_request.token_expires.strftime("%d.%m.%Y")}</p>' if access_request.token_expires else '<p style="color: #16a34a;"><strong>Ihr Zugang ist unbegrenzt gültig.</strong></p>'}
                        
                        <!-- Login Button -->
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{login_url}" 
                               style="background: linear-gradient(135deg, #16a34a 0%, #8fcc14 100%); color: white; padding: 14px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600; box-shadow: 0 4px 6px rgba(22,163,74,0.2);">
                                Jetzt anmelden →
                            </a>
                        </div>
                        
                        <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 8px; margin-top: 25px;">
                            <p style="margin: 0; font-size: 14px; color: #92400e;">
                                <strong>⚠️ Wichtig:</strong> Bewahren Sie diese Zugangsdaten sicher auf. Teilen Sie Ihr Passwort nicht mit anderen Personen.
                            </p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                        <p style="color: #6b7280; font-size: 12px; margin: 0;">
                            Diese E-Mail wurde automatisch generiert. Bei Fragen antworten Sie einfach auf diese E-Mail.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

        text_body = f"""
Portfolio-Zugang gewährt
========================

Hallo {access_request.name},

Ihr Zugang zu den Portfolio-Projekten wurde genehmigt!

ZUGANGSDATEN:
-------------
E-Mail-Adresse: {access_request.email}
Passwort: {password}

{f'Gültig bis: {access_request.token_expires.strftime("%d.%m.%Y")}' if access_request.token_expires else 'Ihr Zugang ist unbegrenzt gültig.'}

Login-URL: {login_url}

WICHTIG: Bewahren Sie diese Zugangsdaten sicher auf. Teilen Sie Ihr Passwort nicht mit anderen Personen.

Bei Fragen antworten Sie einfach auf diese E-Mail.
        """

        msg = Message(
            subject=subject,
            recipients=[access_request.email],
            html=html_body,
            body=text_body,
        )

        mail.send(msg)
        print(f"✓ Zugangsdaten an {access_request.email} gesendet")
        return True

    except Exception as e:
        print(f"✗ Fehler beim Senden der Zugangsdaten: {e}")
        return False
