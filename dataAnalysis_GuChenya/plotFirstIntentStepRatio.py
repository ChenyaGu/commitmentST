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
    subNum = len(humanResultsDF['name'].unique())
    humanResultsDF['firstIntentStepRatio'] = humanResultsDF.apply(lambda x: calculateFirstIntentStepRatio(eval(x['goal'])), axis=1)
    maxResultsDF['firstIntentStepRatio'] = maxResultsDF.apply(lambda x: calculateFirstIntentStepRatio(eval(x['goal'])), axis=1)
    humanNormalTrail = humanResultsDF[humanResultsDF['noiseNumber'] != 'special']
    humanSpecialTrail = humanResultsDF[humanResultsDF['noiseNumber'] == 'special']
    maxNormalTrail = maxResultsDF[maxResultsDF['noiseNumber'] != 'special']
    maxSpecialTrail = maxResultsDF[maxResultsDF['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    humanMeanDF['firstIntentStepRatioNormal'] = humanNormalTrail.groupby("name")['firstIntentStepRatio'].mean()
    humanMeanDF['firstIntentStepRatioSpecail'] = humanSpecialTrail.groupby("name")['firstIntentStepRatio'].mean()
    maxMeanDF['firstIntentStepRatioNormal'] = maxNormalTrail.groupby("name")['firstIntentStepRatio'].mean()
    maxMeanDF['firstIntentStepRatioSpecail'] = maxSpecialTrail.groupby("name")['firstIntentStepRatio'].mean()
    humanFirstIntentStepRatioMeanNormal = np.mean(humanMeanDF['firstIntentStepRatioNormal'])
    humanFirstIntentStepRatioMeanSpecail = np.mean(humanMeanDF['firstIntentStepRatioSpecail'])
    maxFirstIntentStepRatioMeanNormal = np.mean(maxMeanDF['firstIntentStepRatioNormal'])
    maxFirstIntentStepRatioMeanSpecail = np.mean(maxMeanDF['firstIntentStepRatioSpecail'])
    # meanDF.to_csv("meandF.csv")
    print('First intent step ratio')
    print('Normal trial:', 'human:', humanFirstIntentStepRatioMeanNormal, 'maxNoise0:', maxFirstIntentStepRatioMeanNormal)
    print('Specail trial:', 'human:', humanFirstIntentStepRatioMeanSpecail, 'maxNoise0:', maxFirstIntentStepRatioMeanSpecail)

    plt.title('First intent step ratio')
    x = np.arange(2)
    y1 = [humanFirstIntentStepRatioMeanNormal, maxFirstIntentStepRatioMeanNormal]
    y2 = [humanFirstIntentStepRatioMeanSpecail, maxFirstIntentStepRatioMeanSpecail]
    width = 0.35
    std_err1 = [calculateSE(humanMeanDF['firstIntentStepRatioNormal']),
                calculateSE(maxMeanDF['firstIntentStepRatioNormal'])]
    std_err2 = [calculateSE(humanMeanDF['firstIntentStepRatioSpecail']),
                calculateSE(maxMeanDF['firstIntentStepRatioSpecail'])]
    error_attri = {'elinewidth': 1, 'ecolor': 'black', 'capsize': 3}
    plt.bar(x, y1, width, align='center', yerr=std_err1, error_kw=error_attri, label='normal trial', alpha=1)
    for a, b in zip(x, y1):
        plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    plt.bar(x + width, y2, width, align='center', yerr=std_err2, error_kw=error_attri, label='special trial', alpha=1)
    for a, b in zip(x, y2):
        plt.text(a + width, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    names = ['human', 'maxNoise0', 'maxNoise0.1']
    plt.xticks(x + width / 2, names)
    plt.ylabel('Ratio')
    plt.ylim((0, 1))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
