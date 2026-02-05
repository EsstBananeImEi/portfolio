"""
Passwort-Hash Generator für Admin-Login

Verwendung:
    python generate_password_hash.py

Das Skript fragt nach einem Passwort, generiert einen sicheren Hash
und zeigt den Wert an, der in die Umgebungsvariable ADMIN_PASSWORD_HASH
eingetragen werden muss.
"""

from werkzeug.security import generate_password_hash
import getpass


def main():
    print("=" * 60)
    print("Admin Passwort-Hash Generator")
    print("=" * 60)
    print()

    # Passwort sicher eingeben (wird nicht angezeigt)
    password = getpass.getpass("Geben Sie das Admin-Passwort ein: ")
    password_confirm = getpass.getpass("Bestätigen Sie das Passwort: ")

    if password != password_confirm:
        print("\n❌ Fehler: Passwörter stimmen nicht überein!")
        return

    if len(password) < 8:
        print("\n⚠️  Warnung: Passwort sollte mindestens 8 Zeichen lang sein!")
        confirm = input("Trotzdem fortfahren? (j/n): ")
        if confirm.lower() != "j":
            return

    # Hash generieren
    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    print("\n" + "=" * 60)
    print("✅ Passwort-Hash erfolgreich generiert!")
    print("=" * 60)
    print("\nFügen Sie folgende Zeile in Ihre .env Datei ein:\n")
    print(f"ADMIN_PASSWORD_HASH={password_hash}")
    print("\nOder setzen Sie die Umgebungsvariable in PowerShell:\n")
    print(f'$env:ADMIN_PASSWORD_HASH="{password_hash}"')
    print("\nOder in Bash/Linux:\n")
    print(f'export ADMIN_PASSWORD_HASH="{password_hash}"')
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
