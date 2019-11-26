import os
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
    humanResultsDF['firstIntentGoalAccord'] = humanResultsDF.apply(
        lambda x: calculateFirstIntentGoalAccord(eval(x['goal'])), axis=1)
    maxResultsDF['firstIntentGoalAccord'] = maxResultsDF.apply(
        lambda x: calculateFirstIntentGoalAccord(eval(x['goal'])), axis=1)
    humanNormalTrail = humanResultsDF[humanResultsDF['noiseNumber'] != 'special']
    humanSpecialTrail = humanResultsDF[humanResultsDF['noiseNumber'] == 'special']
    maxNormalTrail = maxResultsDF[maxResultsDF['noiseNumber'] != 'special']
    maxSpecialTrail = maxResultsDF[maxResultsDF['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    humanMeanDF['firstIntentGoalAccordNormal'] = humanNormalTrail.groupby("name")['firstIntentGoalAccord'].mean()
    humanMeanDF['firstIntentGoalAccordSpecail'] = humanSpecialTrail.groupby("name")['firstIntentGoalAccord'].mean()
    maxMeanDF['firstIntentGoalAccordNormal'] = maxNormalTrail.groupby("name")['firstIntentGoalAccord'].mean()
    maxMeanDF['firstIntentGoalAccordSpecail'] = maxSpecialTrail.groupby("name")['firstIntentGoalAccord'].mean()
    humanFirstIntentGoalAccordMeanNormal = np.mean(humanMeanDF['firstIntentGoalAccordNormal'])
    humanFirstIntentGoalAccordMeanSpecail = np.mean(humanMeanDF['firstIntentGoalAccordSpecail'])
    maxFirstIntentGoalAccordMeanNormal = np.mean(maxMeanDF['firstIntentGoalAccordNormal'])
    maxFirstIntentGoalAccordMeanSpecail = np.mean(maxMeanDF['firstIntentGoalAccordSpecail'])
    # humanMeanDF.to_csv("humanMeanDF.csv")
    print('First intent goal accord probability')
    print('Normal trial:', 'human:', humanFirstIntentGoalAccordMeanNormal, 'maxModel:', maxFirstIntentGoalAccordMeanNormal)
    print('Specail trial:', 'human:', humanFirstIntentGoalAccordMeanSpecail, 'maxModel:', maxFirstIntentGoalAccordMeanSpecail)

    plt.title('First intent goal accord probability')
    x = np.arange(2)
    y1 = [humanFirstIntentGoalAccordMeanNormal, maxFirstIntentGoalAccordMeanNormal]
    y2 = [humanFirstIntentGoalAccordMeanSpecail, maxFirstIntentGoalAccordMeanSpecail]
    width = 0.35
    std_err1 = [calculateSE(humanMeanDF['firstIntentGoalAccordNormal']), calculateSE(maxMeanDF['firstIntentGoalAccordNormal'])]
    std_err2 = [calculateSE(humanMeanDF['firstIntentGoalAccordSpecail']), calculateSE(maxMeanDF['firstIntentGoalAccordSpecail'])]
    error_attri = {'elinewidth': 1, 'ecolor': 'black', 'capsize': 3}
    plt.bar(x, y1, width, align='center', yerr=std_err1, error_kw=error_attri, label='normal trial', alpha=1)
    for a, b in zip(x, y1):
        plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    plt.bar(x + width, y2, width, align='center', yerr=std_err2, error_kw=error_attri, label='special trial', alpha=1)
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
