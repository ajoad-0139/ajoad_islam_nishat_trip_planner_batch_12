from flask import Blueprint, jsonify
from setup_sqlalchemy import sqlalchemy_db as db
from sqlalchemy import text

blueprint = Blueprint("health", __name__) 

@blueprint.get('/health')
def health():
    db.session.execute(text("SELECT 1"))
    return jsonify({"status":"ok"}),200