from flask import Flask
from app.forms import csrf
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    register_error_handlers(app)

    return app

def register_error_handlers(app):
    from flask import render_template

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
