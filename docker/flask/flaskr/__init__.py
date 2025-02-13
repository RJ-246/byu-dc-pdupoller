from flask import Flask
import os
import json

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200


    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .devices import bp as devices_bp
    app.register_blueprint(devices_bp)
    
    return app