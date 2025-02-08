from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import About, Contact
from app.forms import AboutForm
from app.admin import admin


@admin.route("/about", methods=["GET", "POST"])
@login_required
def edit_about():
    # Wir nehmen an, dass es nur einen Datensatz gibt
    about = About.query.first()
    form = AboutForm(obj=about)

    if form.validate_on_submit():
        if about:
            # Datensatz aktualisieren
            form.populate_obj(about)
            flash("Bio wurde aktualisiert.", "success")
        else:
            # Datensatz erstellen
            about = About()
            form.populate_obj(about)
            db.session.add(about)
            flash("Bio wurde erstellt.", "success")
        db.session.commit()
        return redirect(url_for("admin.edit_about"))

    return render_template(
        "admin/edit_about.html",
        form=form,
        about=about,
        now=datetime.now(),
        contact=Contact.query.first(),
    )


@admin.route("/about/delete", methods=["POST"])
@login_required
def delete_about():
    about = About.query.first()
    if about:
        db.session.delete(about)
        db.session.commit()
        flash("Bio wurde gelöscht.", "success")
    else:
        flash("Kein Bio-Datensatz gefunden.", "error")
    return redirect(url_for("admin.edit_about"))
