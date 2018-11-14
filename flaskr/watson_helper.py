import json
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslatorV3 as LanguageTranslation
import urllib.request

def visual(picture_url):
    visual_recognition = VisualRecognitionV3(
        iam_apikey="k4okWKlo1B7hygbIO62sKTBhHmjpLmB9YubkTe51KzoM",
        version = "2018-03-19",
        # url = "https://gateway.watsonplatform.net/visual-recognition/api"
    )
    urllib.request.urlretrieve(picture_url, "local.jpg")
    with open("local.jpg",'rb') as f:
        vehicle_type = visual_recognition.classify(f)

    text = ""

    results_arr = []
    print(vehicle_type.get_result())
    vehicle = vehicle_type.get_result()
    for things in vehicle['images'][0]['classifiers'][0]['classes']:
        dict = {'class':things['class'],'accuracy':round(things['score']*100,2), 'type_hierarchy':things.get('type_hierarchy')}
        results_arr.append(dict)

    # print(results_arr)
    return results_arr

    # for things in vehicle_type.result['images'][0]['classifiers'][0]['classes']:
    #     text += '\n'
    #     text += '- ' + things['class'] + ' (Accuracy: ' + str(things['score']*100) + ' %)'

    # ws['D2'] = text
    # return text

def tone(text_to_analyze):
    tone_analyzer = ToneAnalyzerV3(
        username='2746e932-0379-4c68-93f6-2a65a976d26a',
        password='IDAujoocimV0',
        version = '2016-05-19'
    )

    tone_type = tone_analyzer.tone(tone_input = text_to_analyze, content_type = 'text/plain;charset=utf-8')
    # tone_type = tone_analyzer.tone(tone_input = text_to_analyze, content_type = 'text/plain')

    # return tone_type.result['document_tone']

    tone_results = ""

    tone_arr = []

    for things in tone_type.result['document_tone']['tone_categories'][0]['tones']:
        dict = {'tone':things['tone_name'],'accuracy':round(things['score']*100,2)}
        tone_arr.append(dict)
        # tone_results += '\n'
        # tone_results += '- ' + things['tone_name'] + ' (Accuracy: ' + str(things['score']*100) +' %)'

    # print(tone_arr)
    return tone_arr
    # return tone_results

def translate(text_to_translate):
    language_translation = LanguageTranslation(
        version = '2018-05-01',
        iam_apikey='0W0AoUw-0Yxg11L5DmNPFPbwMM7De0vT-5IeTyrES-co'
    )

    translation = language_translation.translate(
        text = text_to_translate,
        source='en',
        target='fr'
    )

    # return translation['result']
    return translation.result['translations'][0]['translation']
