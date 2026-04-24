from flask import Flask
from config import Config
from app.database import close_db
from app.init_db import init_db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

   
    jwt = JWTManager(app)

    with app.app_context():
        from app.init_db import init_db
        init_db()

    from app.database import close_db
    app.teardown_appcontext(close_db)

    # Blueprints
    from app.auth.routes.auth_routes import auth_bp
    from app.gear.routes.gear_routes import gear_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(gear_bp, url_prefix="/gear")

    return app