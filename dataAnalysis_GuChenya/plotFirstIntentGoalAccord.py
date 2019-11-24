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
    softmaxResultsPath = DIRNAME + '/maxNoise0.1'
    humanResultsDF = pd.concat(map(pd.read_csv, glob.glob(os.path.join(humanResultsPath, '*.csv'))), sort=False)
    maxResultsDF = pd.concat(map(pd.read_csv, glob.glob(os.path.join(maxResultsPath, '*.csv'))), sort=False)
    softmaxResultsDF = pd.concat(map(pd.read_csv, glob.glob(os.path.join(softmaxResultsPath, '*.csv'))), sort=False)
    subNum = len(humanResultsDF['name'].unique())
    humanResultsDF['finalGoal'] = humanResultsDF.apply(lambda x: calculateFinalGoal(x['bean1GridX'],x['bean1GridY'],x['trajectory']), axis=1)
    maxResultsDF['finalGoal'] = maxResultsDF.apply(lambda x: calculateFinalGoal(x['bean1GridX'],x['bean1GridY'],x['trajectory']), axis=1)
    softmaxResultsDF['finalGoal'] = softmaxResultsDF.apply(lambda x: calculateFinalGoal(x['bean1GridX'],x['bean1GridY'],x['trajectory']), axis=1)
    humanResultsDF['firstIntentGoalAccord'] = humanResultsDF.apply(lambda x: calculateFirstIntentGoalAccord(x['finalGoal'],x['goal']), axis=1)
    maxResultsDF['firstIntentGoalAccord'] = maxResultsDF.apply(lambda x: calculateFirstIntentGoalAccord(x['finalGoal'],x['goal']), axis=1)
    softmaxResultsDF['firstIntentGoalAccord'] = softmaxResultsDF.apply(lambda x: calculateFirstIntentGoalAccord(x['finalGoal'],x['goal']), axis=1)
    humanNormalTrail = humanResultsDF[humanResultsDF['noiseNumber'] != 'special']
    humanSpecialTrail = humanResultsDF[humanResultsDF['noiseNumber'] == 'special']
    maxNormalTrail = maxResultsDF[maxResultsDF['noiseNumber'] != 'special']
    maxSpecialTrail = maxResultsDF[maxResultsDF['noiseNumber'] == 'special']
    softmaxNormalTrail = softmaxResultsDF[softmaxResultsDF['noiseNumber'] != 'special']
    softmaxSpecialTrail = softmaxResultsDF[softmaxResultsDF['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    softmaxMeanDF = pd.DataFrame()
    humanMeanDF['firstIntentGoalAccordNormal'] = humanNormalTrail.groupby("name")['firstIntentGoalAccord'].mean()
    humanMeanDF['firstIntentGoalAccordSpecail'] = humanSpecialTrail.groupby("name")['firstIntentGoalAccord'].mean()
    maxMeanDF['firstIntentGoalAccordNormal'] = maxNormalTrail.groupby("name")['firstIntentGoalAccord'].mean()
    maxMeanDF['firstIntentGoalAccordSpecail'] = maxSpecialTrail.groupby("name")['firstIntentGoalAccord'].mean()
    softmaxMeanDF['firstIntentGoalAccordNormal'] = softmaxNormalTrail.groupby("name")['firstIntentGoalAccord'].mean()
    softmaxMeanDF['firstIntentGoalAccordSpecail'] = softmaxSpecialTrail.groupby("name")['firstIntentGoalAccord'].mean()
    humanFirstIntentGoalAccordMeanNormal = np.mean(humanMeanDF['firstIntentGoalAccordNormal'])
    humanFirstIntentGoalAccordMeanSpecail = np.mean(humanMeanDF['firstIntentGoalAccordSpecail'])
    maxFirstIntentGoalAccordMeanNormal = np.mean(maxMeanDF['firstIntentGoalAccordNormal'])
    maxFirstIntentGoalAccordMeanSpecail = np.mean(maxMeanDF['firstIntentGoalAccordSpecail'])
    softmaxFirstIntentGoalAccordMeanNormal = np.mean(softmaxMeanDF['firstIntentGoalAccordNormal'])
    softmaxFirstIntentGoalAccordMeanSpecail = np.mean(softmaxMeanDF['firstIntentGoalAccordSpecail'])
    # humanMeanDF.to_csv("humanMeanDF.csv")
    print('First intent goal accord probability')
    print('Normal trial:', 'human:', humanFirstIntentGoalAccordMeanNormal, 'maxNoise0:', maxFirstIntentGoalAccordMeanNormal, 'maxNoise0.1:',
          softmaxFirstIntentGoalAccordMeanNormal)
    print('Specail trial:', 'human:', humanFirstIntentGoalAccordMeanSpecail, 'maxNoise0:', maxFirstIntentGoalAccordMeanSpecail, 'maxNoise0.1:',
          softmaxFirstIntentGoalAccordMeanSpecail)

    plt.title('First intent goal accord probability')
    x = np.arange(3)
    y1 = [humanFirstIntentGoalAccordMeanNormal, maxFirstIntentGoalAccordMeanNormal, softmaxFirstIntentGoalAccordMeanNormal]
    y2 = [humanFirstIntentGoalAccordMeanSpecail, maxFirstIntentGoalAccordMeanSpecail, softmaxFirstIntentGoalAccordMeanSpecail]
    width = 0.2
    std_err1 = [np.std(humanMeanDF['firstIntentGoalAccordNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['firstIntentGoalAccordNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['firstIntentGoalAccordNormal'], ddof=1) / math.sqrt(subNum - 1)]
    std_err2 = [np.std(humanMeanDF['firstIntentGoalAccordSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['firstIntentGoalAccordSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['firstIntentGoalAccordSpecail'], ddof=1) / math.sqrt(subNum - 1)]
    error_attri = {'elinewidth': 1, 'ecolor': 'black', 'capsize': 3}
    plt.bar(x, y1, width, align='center', yerr=std_err1, error_kw=error_attri, label='normal trial', alpha=1)
    for a, b in zip(x, y1):
        plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    plt.bar(x + width, y2, width, align='center', yerr=std_err2, error_kw=error_attri, label='special trial', alpha=1)
    for a, b in zip(x, y2):
        plt.text(a+width, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    names = ['huamn', 'maxNoise0', 'maxNoise0.1']
    plt.xticks(x + width / 2, names)
    plt.ylabel('Probability')
    plt.ylim((0, 1))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
