数据：
human
maxModel

数据分析：
dataAnalysis
包含四个主要函数
1.calculateGoalCommit
在整个游戏过程中是否始终坚持同一目标（坚持1，不坚持0）。\*goal为全0时视为坚持*\
2.calculateFirstIntentGoalAccord
第一次做出选择的目标和最后到达的目标是否一致（一致1，不一致0）。\*goal为全0时视为一致*\
3.calculateFirstIntentStepRatio
第一次做出选择的步数占总步数的比例。\*goal为全0时视为直至最后也没有做出选择，比例为1*\
4.calculateIsTimeMaxNextNoisePoint
最长反应时是否对应于某个噪声点产生的那一步(i)的下一步(i+1)的按键反应时（是为1，不是为0）。\*剔除无噪声点的trial*\
testDataAnalysis
包含所有unittest

数据分析可视化：
plotGoalCommitment
plotFirstIntentGoalAccord
plotFirstIntentStepRatio
plotIsTimeMaxNextNoisePoint
分别对应上述四个函数，误差线使用标准误SE