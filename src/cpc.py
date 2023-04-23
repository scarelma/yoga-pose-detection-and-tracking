import pickle
import pandas as pd
from sklearn.svm import SVC
import os


from sklearn.model_selection import train_test_split

class CustomPoseClassification:

    def __init__(self, dataLocation = "", posename = 'default', df = pd.DataFrame(), testsize = 0.2, random_state=42):
        if dataLocation != "":
            self.dataLocation = dataLocation
            self.df = pd.read_csv(self.dataLocation)
        else:
            self.df = df 
        if posename == 'default':
            self.posename = dataLocation.split('/')[-1].split('.')[0]
        self.posename = posename
        self.modelLocation = 'models/' + self.posename + '.pkl'
        self.model = None
        self._testsize = testsize
        self._random_state = random_state

    def train(self):
        # Load the CSV files into Pandas dataframes
        

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.df.iloc[:, :-1], self.df.iloc[:, -1], test_size=self._testsize, random_state=self._random_state)
        self.model = SVC(kernel='linear', C=1)
        self.model.fit(X_train, y_train)
        
        # Evaluate the model on the testing set
        accuracy = self.model.score(X_test, y_test)
        print('Accuracy:', accuracy)

        # Save the model to disk
        with open(self.modelLocation, 'wb') as f:
            pickle.dump(self.model, f)


    def predict(self, df):
        # Use the trained SVM model to predict the output
        prediction = self.model.predict(df)

        return prediction[0]

    def loadModel(self):
        # self.model = tf.keras.models.load_model(f'models/{self.posename}.pkl')
        with open(self.modelLocation, 'rb') as f:

            self.model = pickle.load(f)

    def loadOrTrain(self):
        print(self.modelLocation)
        if os.path.exists(self.modelLocation):
            self.loadModel()
        else:
            self.train()