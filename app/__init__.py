from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from app.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
redis_client = Redis.from_url(Config.REDIS_URL)
migrate = Migrate()


def create_app():
    app = Flask('test_api')
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import bp
    app.register_blueprint(bp)

    return app




