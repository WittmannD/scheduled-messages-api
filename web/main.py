import os
import web.api.common.constants as constants

from dotenv import load_dotenv
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api

from web.api.models.BaseModel import db
from web.api.resources.ScheduleApi import ScheduleApi


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()


def init_routes(api):
    api.add_resource(ScheduleApi, constants.SCHEDULE_API_ROUTE)


def create_app():
    load_dotenv(f'../.env.{os.environ.get("ENV", "development")}')

    app = Flask(__name__)

    app.config.from_object(os.environ.get('FLASK_APP_SETTINGS'))
    init_db(app)

    api_blueprint = Blueprint('api', __name__)

    api = Api(api_blueprint, catch_all_404s=True)
    CORS(api_blueprint)

    init_routes(api)

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(port=os.environ.get('FLASK_PORT'), threaded=True)
