from datetime import datetime
import studelydesk.models as models
from flask import Flask, Blueprint, render_template, request, redirect, url_for


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

# Enregistrement du blueprint
app.register_blueprint(web_ui)

if __name__ == "__main__":
    app.run(debug=True)
