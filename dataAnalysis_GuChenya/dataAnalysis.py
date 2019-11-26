import numpy as np


def calculateSE(data):
    standardError = np.std(data, ddof=1) / np.sqrt(len(data) - 1)
    return standardError


def calculateFirstIntentStep(goalList):
    intent1 = goalList.index(1) + 1 if 1 in goalList else len(goalList)
    intent2 = goalList.index(2) + 1 if 2 in goalList else len(goalList)
    firstIntentStep = min(intent1, intent2)
    return firstIntentStep


def calculateFirstIntentStepRatio(goalList):
    firstIntentStepRatio = calculateFirstIntentStep(goalList) / len(goalList)
    return firstIntentStepRatio


def calculateGoalCommit(goalList):
    goal1Step = [goalList.index(goalList[i]) + 1 for i in range(len(goalList)) if goalList[i] == 1]
    goal2Step = [goalList.index(goalList[i]) + 1 for i in range(len(goalList)) if goalList[i] == 2]
    numGoal1 = len(goal1Step)
    numGoal2 = len(goal2Step)
    if (numGoal1 != 0 and numGoal2 == 0) or (numGoal2 != 0 and numGoal1 == 0):
        isGoalCommit = 1
    elif numGoal1 != 0 and numGoal2 != 0:
        isGoalCommit = 0
    else:
        isGoalCommit = 1
    return isGoalCommit


def calculateFinalGoal(bean1GridX, bean1GridY, trajectory):
    finalStep = trajectory[len(trajectory) - 1]
    if finalStep[0] == bean1GridX and finalStep[1] == bean1GridY:
        finalGoal = 1
    else:
        finalGoal = 2
    return finalGoal


def calculateFirstIntentGoalAccord(goalList):
    firstIntentStep = calculateFirstIntentStep(goalList)
    firstIntent = goalList[firstIntentStep - 1]
    finalGoalStep = calculateFirstIntentStep(list(reversed(goalList)))
    finalGoal = list(reversed(goalList))[finalGoalStep - 1]
    isFirstIntentGoalAccord = 1 if firstIntent == finalGoal else 0
    return isFirstIntentGoalAccord


# 不需要去和机器做比较  机器没有所谓的反应时  就是一个计算时间
# 可以把一个被试的有噪声的trial的反应时的平均值和没有的平均值做比较
def calculateIsTimeMaxNextNoisePoint(timeList, noisePoint):
    noisePointNextStep = [i + 1 for i in noisePoint]
    timeGap = [timeList[i + 1] - timeList[i] for i in range(len(timeList) - 1)]
    maxReactTimeStep = [i + 2 for i, x in enumerate(timeGap) if x == max(timeGap)]
    if [i for i in maxReactTimeStep if i in noisePointNextStep] != []:
        isTimeMaxNextNoisePoint = 1
    else:
        isTimeMaxNextNoisePoint = 0
    return isTimeMaxNextNoisePoint
