def send_password_reset_email(access_request, password):
    """
    Sendet eine spezielle Passwort-Reset-Mail an den Benutzer
    """
    from flask import current_app
    from flask_mail import Message

    mail = (
        current_app.extensions["mail"]
        if "mail" in current_app.extensions
        else current_app.extensions.get("mail", None)
    )
    subject = "Ihr neues Passwort für das Portfolio"
    base_url = current_app.config.get("BASE_URL", "http://localhost:5000")
    login_url = f"{base_url}/auth/portfolio-login"
    html_body = f"""
    <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            </style>
        </head>
        <body style='font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa;'>
            <div style='max-width: 600px; margin: 40px auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08);'>
                <div style='background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); padding: 40px; text-align: center;'>
                    <div style='display: inline-grid; grid-template-columns: repeat(2, 24px); gap: 4px; margin-bottom: 20px;'>
                        <div style='background: linear-gradient(135deg, #F34F1C 0%, #FF6B39 100%); width: 24px; height: 24px; border-radius: 3px;'></div>
                        <div style='background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); width: 24px; height: 24px; border-radius: 3px;'></div>
                        <div style='background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); width: 24px; height: 24px; border-radius: 3px;'></div>
                        <div style='background: linear-gradient(135deg, #01A6F0 0%, #39B4F0 100%); width: 24px; height: 24px; border-radius: 3px;'></div>
                    </div>
                    <h1 style='color: white; margin: 0; font-size: 28px; font-weight: 700;'>Passwort zurückgesetzt</h1>
                    <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;'>Ihr neues Passwort für das Portfolio</p>
                </div>
                <div style='padding: 40px;'>
                    <p style='font-size: 16px; color: #212529; margin-bottom: 10px;'>Hallo {access_request.name},</p>
                    <p style='font-size: 16px; color: #212529; margin-bottom: 30px;'>Sie haben ein neues Passwort für das Portfolio angefordert. Sie können sich jetzt mit diesen Zugangsdaten anmelden:</p>
                    <div style='background: linear-gradient(135deg, #fffbe6 0%, #fff9c4 100%); border-left: 4px solid #FFBA01; padding: 24px; border-radius: 8px; margin: 25px 0;'>
                        <h3 style='margin: 0 0 20px 0; color: #FFBA01; font-size: 16px; font-weight: 700;'>NEUES PASSWORT</h3>
                        <table style='width: 100%; border-collapse: collapse;'>
                            <tr>
                                <td style='padding: 12px 0;'>
                                    <p style='margin: 0 0 6px 0; color: #6c757d; font-size: 13px; font-weight: 600;'>E-MAIL-ADRESSE:</p>
                                    <div style='background-color: rgba(0,0,0,0.05); padding: 12px 16px; border-radius: 6px; font-family: "Courier New", monospace; font-size: 14px; color: #212529;'>
                                        {access_request.email}
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td style='padding: 12px 0;'>
                                    <p style='margin: 0 0 6px 0; color: #6c757d; font-size: 13px; font-weight: 600;'>PASSWORT:</p>
                                    <div style='background-color: rgba(0,0,0,0.05); padding: 12px 16px; border-radius: 6px; font-family: "Courier New", monospace; font-size: 14px; color: #212529; word-break: break-all;'>
                                        {password}
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div style='background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin: 20px 0;'>
                        <p style='margin: 0; color: #212529; font-size: 14px;'>
                            <strong style='color: #FFBA01;'>Hinweis:</strong> Aus Sicherheitsgründen sollten Sie Ihr Passwort nach dem Login ändern.
                        </p>
                    </div>
                    <div style='text-align: center; margin: 35px 0;'>
                        <a href='{login_url}' style='display: inline-block; background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(255, 186, 1, 0.3);'>Jetzt anmelden →</a>
                    </div>
                </div>
                <div style='background-color: #f8f9fa; padding: 24px; text-align: center; border-top: 1px solid #e9ecef;'>
                    <p style='margin: 0; color: #6c757d; font-size: 12px;'>Diese E-Mail wurde automatisch generiert. Bei Fragen antworten Sie einfach auf diese E-Mail.</p>
                </div>
            </div>
        </body>
    </html>
    """
    text_body = f"""
Portfolio Passwort zurückgesetzt
===============================

Hallo {access_request.name},

Sie haben ein neues Passwort für das Portfolio angefordert.

E-Mail-Adresse: {access_request.email}
Neues Passwort: {password}

Login-URL: {login_url}

Tipp: Ändern Sie Ihr Passwort nach dem Login über Ihr Profil.

Bei Fragen antworten Sie einfach auf diese E-Mail.
    """
    msg = Message(
        subject=subject,
        recipients=[access_request.email],
        html=html_body,
        body=text_body,
    )
    mail.send(msg)
    print(f"✓ Passwort-Reset-Mail an {access_request.email} gesendet")
    return True


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
            <head>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                </style>
            </head>
            <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa;">
                <div style="max-width: 600px; margin: 40px auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08);">
                    <!-- Microsoft-inspired Header -->
                    <div style="background: linear-gradient(135deg, #01A6F0 0%, #0078D4 100%); padding: 40px; text-align: center;">
                        <!-- Logo Grid -->
                        <div style="display: inline-grid; grid-template-columns: repeat(2, 24px); gap: 4px; margin-bottom: 20px;">
                            <div style="background: linear-gradient(135deg, #F34F1C 0%, #FF6B39 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #01A6F0 0%, #39B4F0 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        </div>
                        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Neue Zugriffsanfrage</h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">Portfolio-Projekte</p>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 40px;">
                        <p style="font-size: 16px; color: #212529; margin-bottom: 30px;">
                            Es gibt eine neue Anfrage für den Zugriff auf Ihre Portfolio-Projekte:
                        </p>
                        
                        <!-- Info Card -->
                        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-left: 4px solid #01A6F0; padding: 24px; border-radius: 8px; margin: 25px 0;">
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px 0; color: #6c757d; font-size: 14px; font-weight: 600;">Name:</td>
                                    <td style="padding: 8px 0; color: #212529; font-size: 14px;">{access_request.name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #6c757d; font-size: 14px; font-weight: 600;">E-Mail:</td>
                                    <td style="padding: 8px 0;">
                                        <a href="mailto:{access_request.email}" style="color: #01A6F0; text-decoration: none; font-size: 14px;">{access_request.email}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #6c757d; font-size: 14px; font-weight: 600;">Datum:</td>
                                    <td style="padding: 8px 0; color: #212529; font-size: 14px;">{access_request.created_at.strftime('%d.%m.%Y %H:%M')}</td>
                                </tr>
                            </table>
                            
                            {f'<div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(0,0,0,0.1);"><p style="margin: 0; color: #6c757d; font-size: 13px; font-weight: 600;">Nachricht:</p><p style="margin: 10px 0 0 0; color: #212529; font-size: 14px; line-height: 1.6;">{access_request.message}</p></div>' if access_request.message else ''}
                        </div>
                        
                        <!-- Action Button -->
                        <div style="text-align: center; margin: 35px 0;">
                            <a href="{current_app.config.get('BASE_URL', 'http://localhost:5000')}/admin/access-requests" 
                               style="display: inline-block; background: linear-gradient(135deg, #01A6F0 0%, #0078D4 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(1, 166, 240, 0.3);">
                                Token-Verwaltung öffnen
                            </a>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f8f9fa; padding: 24px; text-align: center; border-top: 1px solid #e9ecef;">
                        <p style="margin: 0; color: #6c757d; font-size: 12px;">
                            Diese E-Mail wurde automatisch von Ihrem Portfolio-System generiert.
                        </p>
                    </div>
                </div>
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
            <head>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                </style>
            </head>
            <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa;">
                <div style="max-width: 600px; margin: 40px auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08);">
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); padding: 40px; text-align: center;">
                        <div style="display: inline-grid; grid-template-columns: repeat(2, 24px); gap: 4px; margin-bottom: 20px;">
                            <div style="background: linear-gradient(135deg, #F34F1C 0%, #FF6B39 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #01A6F0 0%, #39B4F0 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        </div>
                        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Token generiert</h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">Ihr Zugriff wurde genehmigt</p>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 40px;">
                        <p style="font-size: 16px; color: #212529; margin-bottom: 10px;">
                            Hallo {access_request.name},
                        </p>
                        
                        <p style="font-size: 16px; color: #212529; margin-bottom: 30px;">
                            Ihr Zugriff auf die Portfolio-Projekte wurde genehmigt!
                        </p>
                        
                        <!-- Token Card -->
                        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 4px solid #7FBC00; padding: 24px; border-radius: 8px; margin: 25px 0;">
                            <p style="margin: 0 0 12px 0; color: #6c757d; font-size: 13px; font-weight: 600;">IHR ZUGANGSTOKEN:</p>
                            <div style="background-color: rgba(0,0,0,0.05); padding: 16px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 15px; color: #212529; word-break: break-all; letter-spacing: 0.5px;">
                                {access_request.token}
                            </div>
                        </div>
                        
                        <!-- Validity Info -->
                        <div style="background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 0; color: #212529; font-size: 14px;">
                                <strong style="color: #7FBC00;">⏰ Gültigkeit:</strong><br>
                                {f'<span style="color: #6c757d;">Gültig bis {access_request.token_expires.strftime("%d.%m.%Y")}</span>' if access_request.token_expires else '<span style="color: #7FBC00;">Unbegrenzt gültig ✓</span>'}
                            </p>
                        </div>
                        
                        <p style="font-size: 14px; color: #6c757d; line-height: 1.6; margin: 25px 0;">
                            Gehen Sie auf die Portfolio-Seite und geben Sie das Token ein, um Zugriff auf alle Projekte zu erhalten.
                        </p>
                        
                        <!-- Warning Box -->
                        <div style="background-color: #fff3cd; border-left: 4px solid #FFBA01; padding: 16px; border-radius: 6px; margin: 25px 0;">
                            <p style="margin: 0; color: #856404; font-size: 13px;">
                                <strong>⚠️ Wichtig:</strong> Teilen Sie dieses Token nicht mit anderen Personen.
                            </p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f8f9fa; padding: 24px; text-align: center; border-top: 1px solid #e9ecef;">
                        <p style="margin: 0; color: #6c757d; font-size: 12px;">
                            Bei Fragen antworten Sie einfach auf diese E-Mail.
                        </p>
                    </div>
                </div>
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
            <head>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                </style>
            </head>
            <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa;">
                <div style="max-width: 600px; margin: 40px auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08);">
                    <!-- Microsoft-inspired Header -->
                    <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); padding: 40px; text-align: center;">
                        <!-- Logo Grid -->
                        <div style="display: inline-grid; grid-template-columns: repeat(2, 24px); gap: 4px; margin-bottom: 20px;">
                            <div style="background: linear-gradient(135deg, #F34F1C 0%, #FF6B39 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                            <div style="background: linear-gradient(135deg, #01A6F0 0%, #39B4F0 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        </div>
                        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Zugang gewährt</h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">Ihre persönlichen Zugangsdaten</p>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 40px;">
                        <p style="font-size: 16px; color: #212529; margin-bottom: 10px;">
                            Hallo {access_request.name},
                        </p>
                        
                        <p style="font-size: 16px; color: #212529; margin-bottom: 30px;">
                            Ihr Zugang zu den Portfolio-Projekten wurde genehmigt! Sie können sich jetzt mit Ihren persönlichen Zugangsdaten anmelden.
                        </p>
                        
                        <!-- Credentials Card -->
                        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 4px solid #7FBC00; padding: 24px; border-radius: 8px; margin: 25px 0;">
                            <h3 style="margin: 0 0 20px 0; color: #7FBC00; font-size: 16px; font-weight: 700;">IHRE ZUGANGSDATEN</h3>
                            
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 12px 0;">
                                        <p style="margin: 0 0 6px 0; color: #6c757d; font-size: 13px; font-weight: 600;">E-MAIL-ADRESSE:</p>
                                        <div style="background-color: rgba(0,0,0,0.05); padding: 12px 16px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 14px; color: #212529;">
                                            {access_request.email}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 0;">
                                        <p style="margin: 0 0 6px 0; color: #6c757d; font-size: 13px; font-weight: 600;">PASSWORT:</p>
                                        <div style="background-color: rgba(0,0,0,0.05); padding: 12px 16px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 14px; color: #212529; word-break: break-all;">
                                            {password}
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        
                        <!-- Validity Info -->
                        <div style="background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 0; color: #212529; font-size: 14px;">
                                <strong style="color: #7FBC00;">⏰ Gültigkeit:</strong><br>
                                {f'<span style="color: #6c757d;">Gültig bis {access_request.token_expires.strftime("%d.%m.%Y")}</span>' if access_request.token_expires else '<span style="color: #7FBC00;">Unbegrenzt gültig ✓</span>'}
                            </p>
                        </div>
                        
                        <!-- Login Button -->
                        <div style="text-align: center; margin: 35px 0;">
                            <a href="{login_url}" 
                               style="display: inline-block; background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(127, 188, 0, 0.3);">
                                Jetzt anmelden →
                            </a>
                        </div>
                        
                        <!-- Warning Box -->
                        <div style="background-color: #fff3cd; border-left: 4px solid #FFBA01; padding: 16px; border-radius: 6px; margin: 25px 0;">
                            <p style="margin: 0; color: #856404; font-size: 13px;">
                                <strong>⚠️ Sicherheitshinweis:</strong> Bewahren Sie diese Zugangsdaten sicher auf und teilen Sie Ihr Passwort nicht mit anderen Personen.
                            </p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f8f9fa; padding: 24px; text-align: center; border-top: 1px solid #e9ecef;">
                        <p style="margin: 0; color: #6c757d; font-size: 12px;">
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
