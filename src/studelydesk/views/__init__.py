from flask import Flask

from studelydesk.views.web import web_ui
from studelydesk.views.api import api_ui, spec


def create_app():
    app = Flask(__name__)

    # Charger la configuration depuis l'objet config
    app.config.from_prefixed_env(prefix="ARCHILOG")


    # Enregistrer les Blueprints qui sont un moyen d'organiser un groupes de vues et d'autres codes
    app.register_blueprint(web_ui)
    app.register_blueprint(api_ui)

    # Ajout de Spectree
    spec.register(app)


    return app

