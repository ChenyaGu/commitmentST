﻿import os
import glob
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from dataAnalysis import *

DIRNAME = os.path.dirname(__file__)


def main():
    humanResultsPath = DIRNAME + '/human'
    maxResultsPath = DIRNAME + '/maxModel'
    humanResultsDF = pd.concat(map(pd.read_csv, glob.glob(os.path.join(humanResultsPath, '*.csv'))), sort=False)
    maxResultsDF = pd.concat(map(pd.read_csv, glob.glob(os.path.join(maxResultsPath, '*.csv'))), sort=False)
    humanResultsDF['goalCommitment'] = humanResultsDF.apply(lambda x: calculateGoalCommit(eval(x['goal'])), axis=1)
    maxResultsDF['goalCommitment'] = maxResultsDF.apply(lambda x: calculateGoalCommit(eval(x['goal'])), axis=1)
    humanNormalTrail = humanResultsDF[humanResultsDF['noiseNumber'] != 'special']
    humanSpecialTrail = humanResultsDF[humanResultsDF['noiseNumber'] == 'special']
    maxNormalTrail = maxResultsDF[maxResultsDF['noiseNumber'] != 'special']
    maxSpecialTrail = maxResultsDF[maxResultsDF['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    humanMeanDF['goalCommitNormal'] = humanNormalTrail.groupby("name")['goalCommitment'].mean()
    humanMeanDF['goalCommitSpecail'] = humanSpecialTrail.groupby("name")['goalCommitment'].mean()
    maxMeanDF['goalCommitNormal'] = maxNormalTrail.groupby("name")['goalCommitment'].mean()
    maxMeanDF['goalCommitSpecail'] = maxSpecialTrail.groupby("name")['goalCommitment'].mean()
    humanGoalCommitMeanNormal = np.mean(humanMeanDF['goalCommitNormal'])
    humanGoalCommitMeanSpecail = np.mean(humanMeanDF['goalCommitSpecail'])
    maxGoalCommitMeanNormal = np.mean(maxMeanDF['goalCommitNormal'])
    maxGoalCommitMeanSpecail = np.mean(maxMeanDF['goalCommitSpecail'])
    # humanMeanDF.to_csv("humanMeanDF.csv")
    print('Goal commitment probability')
    print('Normal trial:', 'human:', humanGoalCommitMeanNormal, 'maxModel:', maxGoalCommitMeanNormal)
    print('Specail trial:', 'human:', humanGoalCommitMeanSpecail, 'maxModel:', maxGoalCommitMeanSpecail)

    plt.title('Goal commitment probability')
    x = np.arange(2)
    y1 = [humanGoalCommitMeanNormal, maxGoalCommitMeanNormal]
    y2 = [humanGoalCommitMeanSpecail, maxGoalCommitMeanSpecail]
    width = 0.35
    std_err1 = [calculateSE(humanMeanDF['goalCommitNormal']),calculateSE(maxMeanDF['goalCommitNormal'])]
    std_err2 = [calculateSE(humanMeanDF['goalCommitSpecail']),calculateSE(maxMeanDF['goalCommitSpecail'])]
    error_attri = {'elinewidth': 1, 'ecolor': 'black', 'capsize': 3}
    plt.bar(x, y1, width, align='center', yerr=std_err1, error_kw=error_attri, label='normal', alpha=1)
    for a, b in zip(x, y1):
        plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    plt.bar(x + width, y2, width, align='center', yerr=std_err2, error_kw=error_attri, label='special', alpha=1)
    for a, b in zip(x, y2):
        plt.text(a + width, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    names = ['human', 'maxModel']
    plt.xticks(x + width / 2, names)
    plt.ylabel('Probability')
    plt.ylim((0, 1))
    plt.legend(loc='upper right')
    plt.show()


if __name__ == "__main__":
    main()
