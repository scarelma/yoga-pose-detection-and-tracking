class User:

    def __init__(self,username, password, email):
        self.username = username
        self.email = email
        self.password = password
        self.exercise_list = []
    
    def addExercise(self, name):
        self.exercise_list.append(Exercise(name))

    def getExerciseListName(self):
        lt = [exer.name for exer in self.exercise_list]
        return lt

class Exercise:

    def __init__(self, name) -> None:
        self.name = name
        self.daily_data = []

    def addData(self, date, reps):
        self.daily_data.append(DailyExerciseData(date, reps))

    def updateTopReps(self, reps):
        # check array is not empty
        self.daily_data[-1].updateReps(reps)
        
        # send to database call should be made here above changes only update in memory



class DailyExerciseData:

    def __init__(self, date, reps):
        self.date = date
        self.reps = reps

    def updateReps(self, reps):
        self.reps = reps 