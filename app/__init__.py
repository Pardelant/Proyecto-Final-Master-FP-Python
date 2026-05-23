from flask import Flask


def create_app(config: dict | None = None):
    """Crea y configura la aplicación Flask.

    Acepta un diccionario `config` opcional para configurar `app.config`.
    """

    app = Flask(__name__)

    if config:
        app.config.update(config)

    from app.routes import main, init_sistema

    app.register_blueprint(main)

    init_sistema()

    return app


__all__ = ["create_app"]
