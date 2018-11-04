import os
import json
import ast
from flask_cors import CORS
from flask import Flask, jsonify, request, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES
from . import watson_helper

def create_app(test_config = None):
    app = Flask(__name__,instance_relative_config=True)
    CORS(app)

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

    @app.route('/api/watson_helper', methods = ['POST','GET'])
    def get_watson_details():
        if request.method == "POST":
            print(request.data)
            data = request.data
            dataDict = json.loads(data)
            print(dataDict["chat_body"])
            json_chat = dataDict["chat_body"]
            visual_analysis = watson_helper.visual(dataDict["image_url"])

            # condense chat body and provide that to the watson helper - just join up everything in the array
            condensed_chat = ' '.join([json_chat[i]['message'] for i in range(len(json_chat)) if json_chat[i]['user'] == 'client'])
            tone_analysis = watson_helper.tone(condensed_chat)
            # move through array of chat body from user and bot - condense these
            translation_arr = []

            for chat in json_chat:
                translation_dict = {}
                if chat['user'] == 'bot':
                    bot_translation = watson_helper.translate(chat['message'])
                    translation_dict = {'user':'bot','message':bot_translation}
                else:
                    user_translation = watson_helper.translate(chat['message'])
                    translation_dict = {'user':'client','message':user_translation}
                # bot_translation = watson_helper.translate(request.form['chat_body'])
                translation_arr = translation_arr + [translation_dict]

            results = {}
            results['visual'] = visual_analysis
            results['tone_sentiment'] = tone_analysis
            results['translation'] = translation_arr
            print(results)
            rawJSON = json.dumps(results,ensure_ascii=False)
            return rawJSON

    from . import db
    db.init_app(app)

    from . import file_claim
    app.register_blueprint(file_claim.bp)
    app.add_url_rule('/',endpoint='index')


        # rawJSON = json.dumps(results,ensure_ascii=False)
        # return rawJSON # placeholder

    return app
