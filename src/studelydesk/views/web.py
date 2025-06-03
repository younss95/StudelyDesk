import sqlite3
from datetime import datetime
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_httpauth import HTTPBasicAuth
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import SelectField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, Optional

# Redondant: `from studelydesk.db import get_db_connection` supprimé ici
import studelydesk.models as models
from studelydesk.models import *

# Initialisation de l'application
app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Nécessaire pour les sessions/CSRF

auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("admin"),
    "kassandra": generate_password_hash("kassandra")

}


def get_roles(username):
    roles = {
        "admin": ["admin", "chef"],
        "kassandra": ["chef", "customer"],
        "marc": ["chef", "treso", "conformite", "engagement"],
        "sarah": ["chef", "product"],
        "brice": ["chef", "support"],
        "jerdy": ["test"]
    }
    return roles.get(username, [])


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@auth.get_user_roles
def get_user_roles(username):
    return get_roles(username)



web_ui = Blueprint("web_ui", __name__, url_prefix="/")
conn = get_db_connection()


@web_ui.route('/')
def index():
    return render_template('index.html')

@web_ui.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()  # ta fonction qui crée la connexion psycopg2
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['user'] = dict(user)
        return redirect('/home')

    flash("Identifiants incorrects.", "error")
    return redirect('/')


@web_ui.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    password_hash = generate_password_hash(password)
    departement = request.form['departement']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, departement, password_hash) VALUES (%s, %s, %s, %s)",
            (name, email, departement, password_hash)
        )
        conn.commit()
    except Exception as e:
        print("Erreur d'inscription :", e)
        flash("Erreur lors de l'inscription : " + str(e), "error")
        return redirect('/')
    finally:
        cursor.close()
        conn.close()

    flash("Inscription réussie. Connecte-toi maintenant.", "success")
    return redirect('/')


@web_ui.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')

    user_email = session['user']['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
    user_tickets = cursor.fetchall()
    conn.close()

    return render_template('home.html', tickets=user_tickets, user=session['user'])



@web_ui.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@web_ui.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        if 'user_id' not in session:
            flash("Vous devez être connecté pour créer un ticket.", "error")
            return redirect(url_for("web_ui.index"))

        data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "name": request.form["name"],
            "status": request.form["status"],
            "souscategorie" : request.form["souscategorie"],
            "priority": request.form["priority"],
            "departement": request.form["departement"],
            "categorie": request.form["categorie"],
            "assigne_a": request.form.get("assigne_a", ""),
            "email": request.form["email"],
            "pays": request.form["pays"],
            "date": datetime.now(),
            "user_id": session["user_id"]
        }

        models.create_entry(**data)
        return redirect(url_for("web_ui.home"))

    return render_template("create.html")



@web_ui.route("/delete_ticket", methods=["GET", "POST"])
@auth.login_required(role="admin")
def delete_ticket():
    form = DeleteTicketForm()
    tickets = models.get_all_entries()
    form.tickets_id.choices = [(p.id, p.title) for p in tickets]

    if form.validate_on_submit():
        tickets_id = form.tickets_id.data
        ticket = models.get_entry(tickets_id)

        if ticket is None:
            flash("Ticket non trouvé.", "error")
            return redirect(url_for("web_ui.delete_ticket"))

        models.delete_entry(tickets_id)
        flash("Ticket supprimé avec succès.", "success")
        return redirect(url_for("web_ui.delete_ticket"))

    return render_template("delete_ticket.html", form=form)



@web_ui.route("/update_ticket/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    ticket = models.get_entry(ticket_id)

    if not ticket or ticket["user_id"] != session.get("user_id"):
        flash("Accès non autorisé ou ticket introuvable.", "error")
        return redirect(url_for("web_ui.mes_tickets"))

    form = UpdateTicketForm(data=ticket)

    if request.method == "POST" and form.validate_on_submit():
        models.update_entry(
            ticket_id,
            form.title.data, form.description.data, form.name.data,
            form.status.data, form.priority.data,
            form.departement.data, form.categorie.data,
            form.assigne_a.data, form.email.data, form.pays.data
        )
        flash(f"Ticket '{form.title.data}' mis à jour avec succès !", "success")
        return redirect(url_for("web_ui.mes_tickets"))

    return render_template("update.html", form=form)



@web_ui.route('/mes_tickets')
def mes_tickets():
    if 'user_id' not in session:
        return redirect(url_for('web_ui.index'))

    user_id = session['user_id']
    tickets = models.get_tickets_by_user_id(user_id)
    return render_template("mes_tickets.html", tickets=tickets)



@web_ui.route('/ticket/<int:ticket_id>')
def get_ticket_id(ticket_id):
    ticket = models.get_entry(ticket_id)
    if not ticket:
        flash("Ticket introuvable.", "error")
        return redirect(url_for("web_ui.mes_tickets"))

    # Récupérer les réponses liées
    conn = get_db_connection()
    reponses = conn.execute(
        """
        SELECT r.*, u.name AS auteur_nom
        FROM reponses r
                 JOIN users u ON r.user_id = u.id
        WHERE r.ticket_id = ?
        ORDER BY r.date ASC
        """,
        (ticket_id,)
    ).fetchall()

    conn.close()

    return render_template(
        'get_ticket.html',
        ticket=ticket,
        reponses=reponses,
        user_name=session.get('user_name')
    )



@web_ui.route('/ticket/<int:ticket_id>/repondre', methods=['POST'])
def repondre_ticket(ticket_id):

    if 'user_id' not in session:
        return redirect(url_for('web_ui.index'))

    reponse = request.form.get('reponse')

    if not reponse or reponse.strip() == "":
        flash("La réponse ne peut pas être vide.", "error")
        return redirect(url_for('web_ui.get_ticket_id', ticket_id=ticket_id))

    # Appel à ta fonction pour ajouter la réponse
    user_id = session['user_id']
    models.ajouter_reponse(ticket_id, reponse.strip(), user_id)

    flash("Réponse envoyée avec succès !", "success")
    return redirect(url_for('web_ui.get_ticket_id', ticket_id=ticket_id))




@web_ui.route("/getall_ticket")
def getall_ticket():
    entries = models.get_all_entries()
    return render_template("getall_ticket.html", entries=entries)



def get_percentage(counter: Counter) -> dict:
    total = sum(counter.values())
    return {k: (v / total * 100 if total > 0 else 0) for k, v in counter.items()}



@web_ui.route("/getstats", methods=["GET", "POST"])
def getstats():
    stats_statut = models.get_stats_par_statut()
    stats_priority = models.get_stats_par_priority()

    stats_statut_percent = get_percentage(stats_statut)
    stats_priority_percent = get_percentage(stats_priority)

    return render_template(
        "getstats.html",
        stats_statut=stats_statut,
        stats_priority=stats_priority,
        stats_statut_percent=stats_statut_percent,
        stats_priority_percent=stats_priority_percent,
    )


 #CLASSES POUR DEFINIR LA STRUCTURE DES FORMULAIRES HTML
class DeleteTicketForm(FlaskForm):
    tickets_id = SelectField("Sélectionnez un ticket à supprimer", coerce=int)
    submit = SubmitField("Supprimer")

class UpdateTicketForm(FlaskForm):
    ticket_id = IntegerField("ID du ticket", validators=[DataRequired()])
    title = StringField("Titre", validators=[DataRequired()])
    description = StringField("Description", validators=[Optional()])
    name = StringField("Nom du demandeur", validators=[DataRequired()])
    status = SelectField("Statut", choices=[
        ("ouvert", "Ouvert"),
        ("en cours", "En cours"),
        ("résolu", "Fermé")
    ], validators=[DataRequired()])
    priority = SelectField("Priorité", choices=[
        ("basse", "Basse"),
        ("moyenne", "Moyenne"),
        ("haute", "Haute")
    ], validators=[DataRequired()])
    departement = StringField("Département", validators=[Optional()])
    categorie = StringField("Catégorie", validators=[Optional()])
    assigne_a = StringField("Assigné à", validators=[Optional()])
    email = StringField("Email", validators=[Optional()])
    pays = StringField("Pays", validators=[Optional()])
    submit = SubmitField("Mettre à jour")



# Enregistrement du blueprint
app.register_blueprint(web_ui)

# Initialisation de la base de données
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
