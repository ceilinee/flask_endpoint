from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
from werkzeug.exceptions import abort
from flask_uploads import UploadSet, configure_uploads, IMAGES

# from flaskr.auth import login_required
from flaskr.db import get_db

import os

from . import watson_helper
import json


photos = UploadSet('photos', IMAGES)


bp = Blueprint('file_claim',__name__)

@bp.route('/',methods=('GET','POST'))
def index():
    if request.method == 'POST' and 'photo' in request.files:
        chat_body = request.form['chatlog']
        filename = photos.save(request.files['photo'])
        print(filename)
        filename = os.path.join('static','img',filename)
        error = None
        if not chat_body:
            error = 'Chat Body is required'
        if error is not None:
            flash(error)
        else:
            # send to watson api and return results

            visual_analysis = watson_helper.visual(filename)
            tone_analysis = watson_helper.tone(chat_body)
            translation = watson_helper.translate(chat_body)

            results = {}

            results['tone_sentiment'] = tone_analysis
            results['translation'] = translation
            results['visual'] = visual_analysis

            rawJSON = json.dumps(results,ensure_ascii=False)

            # return redirect(url_for('file_claim/ai_results.html'))
            return render_template('file_claim/ai_results.html', results=results,rawJSON=rawJSON)

    # if 'photo' not in request.FILES:
    #     flash('Photo required to move forward')

    return render_template('file_claim/claim_form.html')

# @bp.route('/create_request',methods=('GET','POST'))
# def create_request():
#     if request.METHOD == 'POST' and 'photo' in request.files:
#         filename = photos.save()
#     return render_template('file_claim/claim_form.html')
#
# @bp.route('/send_request',methods=('GET','POST'))
# def send_request():
#     if request.method == 'POST' and 'photo' in request.FILES:
#         chat_body = request.form['chatlog']
#         filename = photos.save()
#         print(filename)
#         error = None
#
#         if not chat_body:
#             error = 'Chat Body is required'
#
#         if error is not None:
#             flash(error)
#         else:
#             # send to watson api and return results
#
#             visual_analysis = watson_helper.visual(filename)
#             tone_analysis = watson_helper.tone(chat_body)
#             translation = watson_helper.translate(chat_body)
#
#             results = {}
#
#             results['tone_sentiment'] = tone_analysis
#             results['translation'] = translation
#             results['visual'] = visual_analysis
#
#             # return redirect(url_for('file_claim/ai_results.html'))
#             return render_template('file_claim/ai_results.html', results=results)
#
#         return render_template('file_claim/claim_form.html')
