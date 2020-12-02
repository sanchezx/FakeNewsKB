# FakeNewsKB
Fake News Detector.

Modules included(?):
    
    API Reader
    API Parser
    Knowledge Base (Decision Tree Model)

In order to build and deploy:

    1. Launch flask app via command line to begin local server on port 5000.
    2. Simulate POST via ApiParser.sendPost()
    3. Return values shown in Python Console which is the dictionary/JSON package that would be returned to the webservice.
    
Dependencies:
    
    nltk, sklearn, flask, pandas