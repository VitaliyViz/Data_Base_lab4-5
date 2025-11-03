import os
import yaml
from flask import Flask
from my_project import create_app
from my_project.auth.controller.general_controller import (
    general_controller, animator_controller,
    noname_animator_controller, mmas_controller,
    animator_distribute_controller
)
from flasgger import Swagger
from aws_secrets import get_secret_dict, build_sqlalchemy_url_from_secret

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"

flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()

config_yaml_path = os.path.join(os.getcwd(), 'config', 'app.yml')
with open(config_yaml_path, "r", encoding='utf-8') as yaml_file:
    config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
    additional_config = config_data_dict[ADDITIONAL_CONFIG]

    if flask_env == DEVELOPMENT:
        config_data = config_data_dict[DEVELOPMENT]
    elif flask_env == PRODUCTION:
        config_data = config_data_dict[PRODUCTION]
    else:
        raise ValueError(f"Check OS environment variable '{FLASK_ENV}'")

if "SECRETS_MANAGER" in config_data:
    secret_info = config_data["SECRETS_MANAGER"]
    secret_dict = get_secret_dict(secret_info["NAME"], secret_info["REGION"])
    sqlalchemy_uri = build_sqlalchemy_url_from_secret(secret_dict)
    config_data["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_uri

app = create_app(config_data, additional_config)

def register_blueprints(app):
    app.register_blueprint(general_controller)
    app.register_blueprint(animator_controller)
    app.register_blueprint(noname_animator_controller)
    app.register_blueprint(mmas_controller)
    app.register_blueprint(animator_distribute_controller)

register_blueprints(app)
Swagger(app)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    if flask_env == DEVELOPMENT:
        app.run(host=HOST, port=DEVELOPMENT_PORT, debug=True)
    elif flask_env == PRODUCTION:
        from waitress import serve
        import logging
        logging.basicConfig(level=logging.INFO)
        serve(app, host=HOST, port=PRODUCTION_PORT)

