import nltk
import string
import pandas as pd
from sklearn.utils import shuffle

from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split


class KnowledgeBase:
    def __init__(self, data):
        self.fake = None
        self.true = None
        self.urls = None
        self.data = None
        self.pred = data

    @staticmethod
    def punctuation_removal(text):
        all_list = [char for char in text if char not in string.punctuation]
        clean_str = ''.join(all_list)
        return clean_str

    def prep_data(self, column, urlSetFlag):
        if not urlSetFlag:
            # os.get_cwd() didn't work properly, hardcoded location to avoid issues.
            file = 'https://raw.githubusercontent.com/sanchezx/FakeNewsKB/master/Fake.csv'
            self.fake = pd.read_csv(file, sep=',')

            file = 'https://raw.githubusercontent.com/sanchezx/FakeNewsKB/master/True.csv'
            self.true = pd.read_csv(file, sep=',')

            self.fake['target'] = 'fake'
            self.true['target'] = 'true'

            self.data = pd.concat([self.fake, self.true]).reset_index(drop=True)
            self.data = shuffle(self.data)
            self.data = self.data.reset_index(drop=True)
            self.data.drop(["date"], axis=1, inplace=True)

            if column == 'text':
                self.data.drop(["title"], axis=1, inplace=True)
            else:
                self.data.drop(["text"], axis=1, inplace=True)

            self.data[column] = self.data[column].apply(lambda x: x.lower())
            self.data[column] = self.data[column].apply(self.punctuation_removal)

            #Only need to run this line on initial run.
            nltk.download('stopwords')
            stop = stopwords.words('english')
            self.data[column] = self.data[column].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))
        else:
            file = 'https://raw.githubusercontent.com/sanchezx/FakeNewsKB/master/urlSet.csv'
            self.urls = pd.read_csv(file, sep=',')

    def runModel(self, column, urlSetFlag):
        features = ["domain_type", "protocol"]

        if not urlSetFlag:
            X_train, X_test, y_train, y_test = train_test_split(self.data[column], self.data.target,
                                                                test_size=0.25, random_state=42)
            pipe = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('model', DecisionTreeClassifier(criterion='entropy', max_depth=20,
                                                              splitter='best', random_state=42))])
            model = pipe.fit(X_train, y_train)
            prediction = model.predict(self.pred)
            # accuracy = 0 round(accuracy_score(y_test, prediction) * 100)
        else:
            X_train, X_test, y_train, y_test = train_test_split(self.urls[features], self.urls.label,
                                                                test_size=0.01, random_state=42)

            model = DecisionTreeClassifier(criterion='entropy', max_depth=20, splitter='best', random_state=42)
            model = model.fit(X_train, y_train)
            prediction = model.predict(self.pred)
            # accuracy = 0 round(accuracy_score(y_test, prediction) * 100)

        return prediction

    def execute(self, columnType, urlSetFlag):
        # Decision tree can use title or text to determine real or fake.
        if columnType == 1:
            column = 'title'
        else:
            column = 'text'

        self.prep_data(column, urlSetFlag)
        return self.runModel(column, urlSetFlag)

        # print(f'MODEL RUNNING PRED: {prediction}')
        # print("accuracy: {}%".format(accuracy, 2))
