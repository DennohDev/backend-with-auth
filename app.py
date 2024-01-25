from datetime import timedelta
from models import db, User, TokenBlocklist
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from views import *
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"


CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager()
app.config["JWT_SECRET_KEY"] = "2ab4c28f-a24d-4b78-a416-1b01d87cdb9c"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt.init_app(app)

app.register_blueprint(user_bp)
# app.register_blueprint(question_bp)
# app.register_blueprint(answer_bp)
# app.register_blueprint(vote_bp)
app.register_blueprint(auth_bp)

# Operations CRUD
@app.route('/')
def hello():
    return "Welcome to the API"
# JWT LOADER
@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    if token:
        return token 
    else:
        return None


if __name__ == '__main__':
    app.run(port=5000, debug=True)