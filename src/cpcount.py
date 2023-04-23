import time
class CustomRepetitionCounter:

    def __init__(self, holdThreshold=0.5, jitterThreshold=0.2, forModel=None):
        self.holdThreshold = holdThreshold
        self.jitterThreshold = jitterThreshold
        self.repetitionsCount = 0
        self.lastPose = None
        self.lastPoseStart = 0
        self.forModel = forModel
        self.jitterPass = True

    def countRepetitions(self, pose):
        if self.lastPose is None:
            self.lastPose = pose
            self.lastPoseStart = time.time()
        elif pose != self.lastPose:
            poseDuration = time.time() - self.lastPoseStart
            if poseDuration > self.holdThreshold and self.jitterPass:
                self.repetitionsCount += 0.5
                self.lastPose = pose
                self.lastPoseStart = time.time()
            # elif poseDuration < self.jitterThreshold:
            #     # pose has been held for less than holdThreshold, but longer than jitterThreshold
            #     # don't update lastPose, but reset lastPoseStart to current time to ignore this jitter
            #     self.jitterPass = False
            #     # self.lastPoseStart = time.time()
            # elif poseDuration >= self.jitterThreshold:
            #     self.jitterPass = True
