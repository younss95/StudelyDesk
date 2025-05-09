from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, StringField
import logging

from wtforms.validators import DataRequired, Optional

import studelydesk.models as models
from studelydesk.models import *
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

app = Flask(__name__)


# Création du Blueprint
web_ui = Blueprint("web_ui", __name__, url_prefix="/")

# Page d'accueil : liste des tickets
@web_ui.route("/")
def home():
    entries = models.get_all_entries()
    return render_template("home.html", entries=entries)

# Page de création d’un ticket
@web_ui.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        name = request.form["name"]
        status = request.form["status"]
        priority = request.form["priority"]
        date = datetime.now()

        models.create_entry(title, description, name, date, status, priority)
        return redirect(url_for("web_ui.home"))

    return render_template("create.html")


class DeleteTicketForm(FlaskForm):
    tickets_id = SelectField("Sélectionnez un produit à supprimer", coerce=int)
    submit = SubmitField("Supprimer")



@web_ui.route("/delete_ticket", methods=["GET", "POST"])
def delete_ticket():
    form = DeleteTicketForm()
    tickets = models.get_all_entries()
    form.tickets_id.choices = [(p.id, p.title) for p in tickets]

    if form.validate_on_submit():
        tickets_id = form.tickets_id.data
        ticket = models.get_entry(tickets_id)

        if ticket is None:
            flash("Ticket non trouvé.", "error")
            return redirect(url_for("web_ui.delete_product"))

        models.delete_entry(tickets_id)
        flash("Ticket supprimé avec succès.", "success")
        return redirect(url_for("web_ui.delete_ticket"))

    return render_template("delete_ticket.html", form=form)




class UpdateTicketForm(FlaskForm):
    ticket_id = IntegerField("ID du ticket", validators=[DataRequired()])
    title = StringField("Titre", validators=[DataRequired()])
    description = StringField("Description", validators=[Optional()])
    name = StringField("Nom du demandeur", validators=[DataRequired()])
    status = SelectField("Statut", choices=[
        ("open", "Ouvert"),
        ("in progress", "En cours"),
        ("closed", "Fermé")
    ], validators=[DataRequired()])

    priority = SelectField("Priorité", choices=[
        ("low", "Basse"),
        ("medium", "Moyenne"),
        ("high", "Haute")
    ], validators=[DataRequired()])
    submit = SubmitField("Mettre à jour")

@web_ui.route("/update_ticket", methods=["GET", "POST"])
def update_ticket():
    form = UpdateTicketForm()
    ticket = None

    if request.method == "POST" and form.validate_on_submit():

        ticket_id = form.ticket_id.data
        title = form.title.data
        description = form.description.data
        name = form.name.data
        status = form.status.data
        priority = form.priority.data

        ticket = models.get_entry(ticket_id)
        if ticket is None:
            flash("Ticket non trouvé.", "error")
            return redirect(url_for("web_ui.update_ticket"))

        models.update_entry(ticket_id, title, description, name, status, priority)
        flash(f"Ticket '{title}' mis à jour avec succès !", "success")
        return redirect(url_for("web_ui.home"))

    return render_template("update.html", form=form, ticket=ticket)

@web_ui.route("/get_ticket", methods=["GET", "POST"])
def get_ticket():
    ticket = None
    if request.method == "POST":
        ticket_id = request.form["id"]
        ticket = models.get_entry(int(ticket_id))  # ou get_entry si c'est la bonne fonction
        if ticket is None:
            flash("Ticket non trouvé.", "error")

    return render_template("get_ticket.html", ticket=ticket)



@web_ui.route("/getall_ticket")
def getall_ticket():
    entries = models.get_all_entries()
    return render_template("getall_ticket.html", entries=entries)


# Enregistrement du blueprint
app.register_blueprint(web_ui)

init_db()

if __name__ == "__main__":
    app.run(debug=True)
