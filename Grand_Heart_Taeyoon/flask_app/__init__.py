from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)

    if app.config["ENV"] == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    if config is not None:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app,db)

    from flask_app.routes import (main_route)
    app.register_blueprint(main_route.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)