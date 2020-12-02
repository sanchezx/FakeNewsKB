import pandas as pd
from flask import Flask, request, jsonify
from ApiParser import get_api_response, parse_api
from KnowledgeBase import KnowledgeBase
from statistics import mean

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/KB', methods=['POST'])
def knowledgeBase():
    jsonGrade = pd.DataFrame.from_dict({'score': 0.5})
    # jsonPost = request.get_json()
    jsonPost = get_api_response()

    if jsonPost is None:
        return {"response": "400 Bad Request"}

    # df = pd.DataFrame.from_dict(jsonPost)
    bodyDF, urlDF = parse_api(jsonPost)

    if jsonPost['url'] is None:
        print('No URL')
    else:
        # Check column type.
        urlSetFlag = False
        scores = []

        # Test article body
        if jsonPost['page_data']['body'] is not None:
            column = 1
            prediction, accuracy = KnowledgeBase(bodyDF).execute(column, urlSetFlag)
            if prediction:
                scores.append(1)
            else:
                scores.append(0)

        # Test article tite.
        if jsonPost['page_data']['title'] is not None:
            column = 2
            prediction, accuracy = KnowledgeBase(bodyDF).execute(column, urlSetFlag)
            if prediction:
                scores.append(1)
            else:
                scores.append(0)

        # Test url.
        prediction, accuracy = KnowledgeBase(urlDF).execute(1, urlSetFlag)
        if prediction:
            scores.append(1)
        else:
            scores.append(0)

        if mean(scores) >= 0.5:
            jsonGrade['score'] = 1.0
        else:
            jsonGrade['score'] = 0.0

    return jsonify(jsonGrade)


@app.route('/')
def index():
    return "<h1>Fake News Decision Tree</h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)