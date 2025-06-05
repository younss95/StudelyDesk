import os

from flask import Flask

from studelydesk.views.web import web_ui
from studelydesk.views.api import api_ui, spec


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("ARCHILOG_FLASK_SECRET_KEY")

    # Charger la configuration depuis l'objet config
    app.config.from_prefixed_env(prefix="ARCHILOG")


    # Enregistrer les Blueprints qui sont un moyen d'organiser un groupes de vues et d'autres codes
    app.register_blueprint(web_ui)
    app.register_blueprint(api_ui)

    # Ajout de Spectree
    spec.register(app)


    return app

