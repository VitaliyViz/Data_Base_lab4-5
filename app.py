import os
import yaml
from flask import Flask
from flasgger import Swagger

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"

flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()


def load_config():
    """Завантаження конфігурації та AWS секретів, fallback на SQLite для локальної розробки"""
    config_yaml_path = os.path.join(os.getcwd(), 'config', 'app.yml')
    if not os.path.exists(config_yaml_path):
        print(f"Warning: Config file not found at {config_yaml_path}, using empty config")
        config_data, additional_config = {}, {}
    else:
        with open(config_yaml_path, "r", encoding='utf-8') as yaml_file:
            config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
            additional_config = config_data_dict.get(ADDITIONAL_CONFIG, {})

            if flask_env == DEVELOPMENT:
                config_data = config_data_dict.get(DEVELOPMENT, {})
            elif flask_env == PRODUCTION:
                config_data = config_data_dict.get(PRODUCTION, {})
            else:
                raise ValueError(f"Check OS environment variable '{FLASK_ENV}'")

    # Спроба завантажити AWS Secrets
    if "SECRETS_MANAGER" in config_data:
        try:
            from aws_secrets import get_secret_dict, build_sqlalchemy_url_from_secret
            secret_info = config_data["SECRETS_MANAGER"]
            secret_dict = get_secret_dict(secret_info["NAME"], secret_info["REGION"])
            sqlalchemy_uri = build_sqlalchemy_url_from_secret(secret_dict)
            config_data["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_uri
        except Exception as e:
            print(f"Warning: Cannot load AWS secrets: {e}")

    # Якщо ключ не створився, fallback на SQLite для локальної розробки
    if "SQLALCHEMY_DATABASE_URI" not in config_data:
        config_data["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        print("Warning: Using local SQLite database for development")

    return config_data, additional_config


def create_app_safe():
    """Створення Flask app з безпечним завантаженням конфігів"""
    from my_project import create_app
    config_data, additional_config = load_config()
    app = create_app(config_data, additional_config)
    return app


def register_blueprints(app):
    """Реєстрація всіх blueprints з обробкою помилок"""
    try:
        from my_project.auth.controller.general_controller import (
            general_controller, animator_controller,
            noname_animator_controller, mmas_controller,
            animator_distribute_controller
        )
        app.register_blueprint(general_controller)
        app.register_blueprint(animator_controller)
        app.register_blueprint(noname_animator_controller)
        app.register_blueprint(mmas_controller)
        app.register_blueprint(animator_distribute_controller)
    except Exception as e:
        print(f"Warning: Cannot register blueprints: {e}")


# --- Старт додатку ---
app = create_app_safe()
register_blueprints(app)

# Swagger UI
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
