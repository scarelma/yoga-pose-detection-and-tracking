# Importing the required modules
from pymongo import MongoClient
from datetime import date

# Creating a client object to connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Creating a database object for your app
db = client["my_app"]

# Creating a collection object for users
users = db["users"]

# Creating a class for User
class User:

    def __init__(self, username, password, email):
        # Initializing the attributes of the user
        self.username = username
        self.password = password
        self.email = email
        self.exercise_list = []

        # Inserting the user document into the users collection
        self.user_id = users.insert_one({
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "exercise_list": self.exercise_list
        }).inserted_id

    def addExercise(self, name):
        # Creating an exercise object and appending it to the exercise list
        exercise = Exercise(name)
        self.exercise_list.append(exercise)

        # Updating the user document in the users collection with the new exercise list
        users.update_one({"_id": self.user_id}, {"$set": {"exercise_list": self.getExerciseListName()}})

    def getExerciseListName(self):
        # Returning a list of exercise names from the exercise list
        return [exer.name for exer in self.exercise_list]

# Creating a class for Exercise
class Exercise:

    def __init__(self, name):
        # Initializing the attribute of the exercise
        self.name = name

        # Creating a collection object for the exercise data
        self.exercise_data = db[self.name]

    def addData(self, date, reps):
        # Inserting a document into the exercise data collection with the date and reps
        self.exercise_data.insert_one({"date": date, "reps": reps})

    def updateTopReps(self, reps):
        # Updating the last document in the exercise data collection with the new reps
        self.exercise_data.update_one({}, {"$set": {"reps": reps}}, sort=[("date", -1)])