def calculateFirstIntentStep(goalList):
    # 不要在函数里面转化数据 应该让函数通用
    goalList = eval(goalList)
    # 不用magic number，把99换成len(goalList)
    intent1 = goalList.index(1) + 1 if 1 in goalList else 99
    intent2 = goalList.index(2) + 1 if 2 in goalList else 99
    # 减少if 可以用python自带的min或者max简化
    if intent1 < intent2:
        firstIntentStep = intent1
    elif intent2 < intent1:
        firstIntentStep = intent2
    else:
        firstIntentStep = len(goalList)
    return firstIntentStep


def calculateFirstIntentStepRatio(goalList):
    firstIntentStepRatio = calculateFirstIntentStep(goalList) / len(eval(goalList))
    return firstIntentStepRatio


def calculateGoalCommit(goalList):
    goalList = eval(goalList)
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

# 把这个简化 不需要算最后一个goal  直接把goallist传入算第一个intend和最后一个intend是否一致（全0的情况下这种算法也可以）
def calculateFinalGoal(bean1GridX, bean1GridY, trajectory):
    trajectory = eval(trajectory)
    finalStep = trajectory[len(trajectory) - 1]
    if finalStep[0] == bean1GridX and finalStep[1] == bean1GridY:
        finalGoal = 1
    else:
        finalGoal = 2
    return finalGoal

# 同上 简化 具体做法是把goallist reverse就可以了
def calculateFirstIntentGoalAccord(finalGoal, goalList):
    firstIntentStep = calculateFirstIntentStep(goalList)
    if firstIntentStep != len(eval(goalList)):
        firstIntent = eval(goalList)[firstIntentStep - 1]
        if firstIntent == finalGoal:
            isFirstIntentGoalAccord = 1
        else:
            isFirstIntentGoalAccord = 0
    else:
        isFirstIntentGoalAccord = 1
    return isFirstIntentGoalAccord

# 不需要去和机器做比较  机器没有所谓的反应时  就是一个计算时间
# 可以把一个被试的有噪声的trial的反应时的平均值和没有的平均值做比较
def calculateIsTimeMaxNextNoisePoint(timeList, noisePoint):
    timeList = eval(timeList)
    noisePoint = eval(noisePoint)
    noisePointNextStep = [i + 1 for i in noisePoint]
    timeGap = [timeList[i + 1] - timeList[i] for i in range(len(timeList) - 1)]
    maxReactTimeStep = [i + 2 for i, x in enumerate(timeGap) if x == max(timeGap)]
    if [i for i in maxReactTimeStep if i in noisePointNextStep] != []:
        isTimeMaxNextNoisePoint = 1
    else:
        isTimeMaxNextNoisePoint = 0
    return isTimeMaxNextNoisePoint
