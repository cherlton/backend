from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, jwt
from flask_cors import CORS  # ← NEW
from flasgger import Swagger
import webbrowser
from app.api.auth.routes import auth_bp
from app.api.users.routes import users_bp
from app.api.skills.routes import skills_bp
from app.api.opinions.routes import opinions_bp
from app.api.health.routes import health_bp
from app.api.trends.routes import trends_bp
from app.api.dashboard.routes import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})  # ← NEW


    # Swagger configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }

    swagger_template = {
        "info": {
            "title": "Insight Sphere API",
            "description": "API documentation for Insight Sphere backend",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header. Example: 'Bearer {token}'"
            }
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # JWT Error Handlers for debugging
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "invalid_token",
            "message": f"Signature verification failed: {error}"
        }), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "token_expired",
            "message": "The token has expired"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "error": "authorization_required",
            "message": "Request does not contain an access token (Bearer prefix might be missing)"
        }), 401

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(skills_bp, url_prefix="/skills")
    app.register_blueprint(opinions_bp, url_prefix="/opinions")
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(trends_bp, url_prefix="/trends")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # Create database tables
    with app.app_context():
        # Import all models so they're registered with SQLAlchemy
        from app.models.sql import user, trend_analysis, skill_path, opinion_analysis
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    # Open Swagger UI in browser
    # webbrowser.open("http://127.0.0.1:5000/docs")
    app.run(debug=True, port=5000)