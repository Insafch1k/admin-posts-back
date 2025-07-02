from flask import Flask
from flask_cors import CORS

from .channels import channels_bp
from .posts import posts_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(channels_bp)
app.register_blueprint(posts_bp)




