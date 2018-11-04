import os

from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES

def create_app(test_config = None):
    app = Flask(__name__,instance_relative_config=True)

    photos = UploadSet('photos',IMAGES)
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
    configure_uploads(app, photos)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import file_claim
    app.register_blueprint(file_claim.bp)
    app.add_url_rule('/',endpoint='index')

    return app
