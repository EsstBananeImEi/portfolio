"""
E-Mail Utilities via SMTP (Strato)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def _send_email(to, subject, html, text=None):
    """Sendet eine E-Mail über SMTP"""
    smtp_host = os.getenv("MAIL_SERVER", "smtp.strato.de")
    smtp_port = int(os.getenv("MAIL_PORT", "465"))
    smtp_user = os.getenv("MAIL_USERNAME")
    smtp_pass = os.getenv("MAIL_PASSWORD")
    from_email = os.getenv("MAIL_FROM", smtp_user)

    if not smtp_user or not smtp_pass:
        print("⚠ MAIL_USERNAME oder MAIL_PASSWORD nicht konfiguriert")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to if isinstance(to, str) else ", ".join(to)

    if text:
        msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        server.login(smtp_user, smtp_pass)
        recipients = [to] if isinstance(to, str) else to
        server.sendmail(from_email, recipients, msg.as_string())
        server.quit()
        print(f"✓ E-Mail an {to} gesendet")
        return True
    except Exception as e:
        print(f"✗ Fehler beim Senden: {e}")
        return False


def init_mail(app):
    """Kompatibilität — wird nicht mehr benötigt, aber verhindert Importfehler"""
    pass


def send_admin_notification(access_request):
    """Sendet eine E-Mail-Benachrichtigung an den Admin bei neuen Zugriffsanfragen"""
    admin_email = current_app.config.get("ADMIN_EMAIL")
    if not admin_email:
        print("⚠ ADMIN_EMAIL nicht konfiguriert")
        return False

    base_url = current_app.config.get("BASE_URL", "http://localhost:5000")
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
                <div style="background: linear-gradient(135deg, #01A6F0 0%, #0078D4 100%); padding: 40px; text-align: center;">
                    <div style="display: inline-grid; grid-template-columns: repeat(2, 24px); gap: 4px; margin-bottom: 20px;">
                        <div style="background: linear-gradient(135deg, #F34F1C 0%, #FF6B39 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        <div style="background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        <div style="background: linear-gradient(135deg, #01A6F0 0%, #39B4F0 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                    </div>
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Neue Zugriffsanfrage</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">Portfolio-Projekte</p>
                </div>
                <div style="padding: 40px;">
                    <p style="font-size: 16px; color: #212529; margin-bottom: 30px;">
                        Es gibt eine neue Anfrage für den Zugriff auf Ihre Portfolio-Projekte:
                    </p>
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
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="{base_url}/admin/access-requests"
                           style="display: inline-block; background: linear-gradient(135deg, #01A6F0 0%, #0078D4 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(1, 166, 240, 0.3);">
                            Token-Verwaltung öffnen
                        </a>
                    </div>
                </div>
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

    return _send_email(admin_email, subject, html_body, text_body)


def send_token_email(access_request):
    """Sendet das Token direkt an den Anfragenden"""
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
                <div style="padding: 40px;">
                    <p style="font-size: 16px; color: #212529; margin-bottom: 10px;">Hallo {access_request.name},</p>
                    <p style="font-size: 16px; color: #212529; margin-bottom: 30px;">Ihr Zugriff auf die Portfolio-Projekte wurde genehmigt!</p>
                    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 4px solid #7FBC00; padding: 24px; border-radius: 8px; margin: 25px 0;">
                        <p style="margin: 0 0 12px 0; color: #6c757d; font-size: 13px; font-weight: 600;">IHR ZUGANGSTOKEN:</p>
                        <div style="background-color: rgba(0,0,0,0.05); padding: 16px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 15px; color: #212529; word-break: break-all; letter-spacing: 0.5px;">
                            {access_request.token}
                        </div>
                    </div>
                    <div style="background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; color: #212529; font-size: 14px;">
                            <strong style="color: #7FBC00;">Gültigkeit:</strong><br>
                            {f'<span style="color: #6c757d;">Gültig bis {access_request.token_expires.strftime("%d.%m.%Y")}</span>' if access_request.token_expires else '<span style="color: #7FBC00;">Unbegrenzt gültig</span>'}
                        </p>
                    </div>
                    <div style="background-color: #fff3cd; border-left: 4px solid #FFBA01; padding: 16px; border-radius: 6px; margin: 25px 0;">
                        <p style="margin: 0; color: #856404; font-size: 13px;">
                            <strong>Wichtig:</strong> Teilen Sie dieses Token nicht mit anderen Personen.
                        </p>
                    </div>
                </div>
                <div style="background-color: #f8f9fa; padding: 24px; text-align: center; border-top: 1px solid #e9ecef;">
                    <p style="margin: 0; color: #6c757d; font-size: 12px;">Bei Fragen antworten Sie einfach auf diese E-Mail.</p>
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

    return _send_email(access_request.email, subject, html_body, text_body)


def send_access_credentials(access_request, password):
    """Sendet die Login-Zugangsdaten an den genehmigten Benutzer"""
    base_url = current_app.config.get("BASE_URL", "http://localhost:5000")
    login_url = f"{base_url}/auth/portfolio-login"
    subject = "Ihre Zugangsdaten für das Portfolio"

    html_body = f"""
    <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            </style>
        </head>
        <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa;">
            <div style="max-width: 600px; margin: 40px auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08);">
                <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); padding: 40px; text-align: center;">
                    <div style="display: inline-grid; grid-template-columns: repeat(2, 24px); gap: 4px; margin-bottom: 20px;">
                        <div style="background: linear-gradient(135deg, #F34F1C 0%, #FF6B39 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        <div style="background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        <div style="background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                        <div style="background: linear-gradient(135deg, #01A6F0 0%, #39B4F0 100%); width: 24px; height: 24px; border-radius: 3px;"></div>
                    </div>
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Zugang gewährt</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">Ihre persönlichen Zugangsdaten</p>
                </div>
                <div style="padding: 40px;">
                    <p style="font-size: 16px; color: #212529; margin-bottom: 10px;">Hallo {access_request.name},</p>
                    <p style="font-size: 16px; color: #212529; margin-bottom: 30px;">
                        Ihr Zugang zu den Portfolio-Projekten wurde genehmigt! Sie können sich jetzt mit Ihren persönlichen Zugangsdaten anmelden.
                    </p>
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
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="{login_url}"
                           style="display: inline-block; background: linear-gradient(135deg, #7FBC00 0%, #9FDC20 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(127, 188, 0, 0.3);">
                            Jetzt anmelden
                        </a>
                    </div>
                    <div style="background-color: #fff3cd; border-left: 4px solid #FFBA01; padding: 16px; border-radius: 6px; margin: 25px 0;">
                        <p style="margin: 0; color: #856404; font-size: 13px;">
                            <strong>Sicherheitshinweis:</strong> Bewahren Sie diese Zugangsdaten sicher auf und teilen Sie Ihr Passwort nicht mit anderen Personen.
                        </p>
                    </div>
                </div>
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

Hallo {access_request.name},

Ihr Zugang zu den Portfolio-Projekten wurde genehmigt!

E-Mail-Adresse: {access_request.email}
Passwort: {password}

{f'Gültig bis: {access_request.token_expires.strftime("%d.%m.%Y")}' if access_request.token_expires else 'Ihr Zugang ist unbegrenzt gültig.'}

Login-URL: {login_url}

WICHTIG: Bewahren Sie diese Zugangsdaten sicher auf.
    """

    return _send_email(access_request.email, subject, html_body, text_body)


def send_password_reset_email(access_request, password):
    """Sendet eine Passwort-Reset-Mail an den Benutzer"""
    base_url = current_app.config.get("BASE_URL", "http://localhost:5000")
    login_url = f"{base_url}/auth/portfolio-login"
    subject = "Ihr neues Passwort für das Portfolio"

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
                    <p style='font-size: 16px; color: #212529; margin-bottom: 30px;'>Sie haben ein neues Passwort für das Portfolio angefordert.</p>
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
                    <div style='text-align: center; margin: 35px 0;'>
                        <a href='{login_url}' style='display: inline-block; background: linear-gradient(135deg, #FFBA01 0%, #FFD54F 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(255, 186, 1, 0.3);'>Jetzt anmelden</a>
                    </div>
                </div>
                <div style='background-color: #f8f9fa; padding: 24px; text-align: center; border-top: 1px solid #e9ecef;'>
                    <p style='margin: 0; color: #6c757d; font-size: 12px;'>Diese E-Mail wurde automatisch generiert.</p>
                </div>
            </div>
        </body>
    </html>
    """

    text_body = f"""
Passwort zurückgesetzt

Hallo {access_request.name},

E-Mail-Adresse: {access_request.email}
Neues Passwort: {password}

Login-URL: {login_url}
    """

    return _send_email(access_request.email, subject, html_body, text_body)
