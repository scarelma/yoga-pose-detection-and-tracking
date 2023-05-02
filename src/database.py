# Import PyMongo
from pymongo import MongoClient

# Create a client object with your connection string
client = MongoClient("your_connection_string")

# Get the database object
db = client["your_database_name"]

# Get the collection object
users = db["users"]

# Define a class for User
class User:

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password
        self.exercise_list = []

    # Define a method to convert the user object to a dictionary
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "exercise_list": self.exercise_list
        }

    # Define a method to create a new user document in the database
    def create(self):
        users.insert_one(self.to_dict())

    # Define a method to find a user document by username
    @staticmethod
    def find_by_username(username):
        user_dict = users.find_one({"username": username})
        if user_dict:
            return User(**user_dict)
        else:
            return None

    # Define a method to add an exercise to the user's exercise list
    def add_exercise(self, name):
        self.exercise_list.append(Exercise(name).to_dict())
        users.update_one({"username": self.username}, {"$set": {"exercise_list": self.exercise_list}})

    # Define a method to get the exercise list of the user
    def get_exercise_list_name(self):
        return [exer["name"] for exer in self.exercise_list]

    # Define a method to update the reps of an exercise by name and date
    def update_reps(self, name, date, reps):
        for exer in self.exercise_list:
            if exer["name"] == name:
                for data in exer["daily_data"]:
                    if data["date"] == date:
                        data["reps"] = reps
                        break
                break
        users.update_one({"username": self.username}, {"$set": {"exercise_list": self.exercise_list}})

# Define a class for Exercise
class Exercise:

    def __init__(self, name) -> None:
        self.name = name
        self.daily_data = []

    # Define a method to convert the exercise object to a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "daily_data": self.daily_data
        }

    # Define a method to add data to the exercise's daily data list
    def add_data(self, date, reps):
        self.daily_data.append(DailyExerciseData(date, reps).to_dict())

# Define a class for DailyExerciseData
class DailyExerciseData:

    def __init__(self, date, reps):
        self.date = date
        self.reps = reps

    # Define a method to convert the daily exercise data object to a dictionary
    def to_dict(self):
        return {
            "date": self.date,
            "reps": self.reps
        }
