from flask import Flask, request, jsonify
from ApiParser import parse_api
from KnowledgeBase import KnowledgeBase
from statistics import mean

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/KB', methods=['POST'])
def knowledgeBase():
    print('\n\tRUNNING....')
    jsonGrade = {'score': 0.5}
    #jsonGrade = pd.DataFrame.from_dict(jsonGrade)
    jsonPost = request.get_json()
    # print(jsonPost)
    # jsonPost = get_api_response()

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
        if len(bodyDF['text'][0]):
            column = 1
            prediction = KnowledgeBase(bodyDF).execute(column, urlSetFlag)
            if prediction[-1] == 'true':
                scores.append(1)
            else:
                scores.append(0)

        # Test article tite.
        if len(bodyDF['title'][0]):
            column = 2
            prediction = KnowledgeBase(bodyDF).execute(column, urlSetFlag)
            if prediction[-1] == 'true':
                scores.append(1)
            else:
                scores.append(0)

        # Test url.
        urlSetFlag = True
        prediction = KnowledgeBase(urlDF).execute(1, urlSetFlag)
        if prediction[0] == 1:
            scores.append(1)
        else:
            scores.append(0)

        if mean(scores) > 0.6:
            jsonGrade['score'] = 1.0
        elif mean(scores) > 0.3:
            jsonGrade['score'] = 0.5
        else:
            jsonGrade['score'] = 0.0

        print(f'\n\n\tDECISION TREE SCORES: {scores}')
        print(f'\t{jsonGrade}\n')

    return jsonify(jsonGrade)


@app.route('/')
def index():
    return "<h1>Fake News Decision Tree</h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
