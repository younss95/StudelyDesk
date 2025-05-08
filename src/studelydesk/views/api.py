from spectree import SpecTree, SecurityScheme
from flask import Blueprint

api_ui = Blueprint("api_ui", __name__, url_prefix="/")


# Spectree pour validation et Swagger
spec = SpecTree(
    "flask",
    security_schemes=[
        SecurityScheme(name="bearer_token", data={"type": "http", "scheme": "bearer"})
    ],
    security=[{"bearer_token": []}]
)
spec.register(api_ui)