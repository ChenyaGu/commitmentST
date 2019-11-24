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
    humanResultsDF['goalCommitment'] = humanResultsDF.apply(lambda x: calculateGoalCommit(x['goal']), axis=1)
    maxResultsDF['goalCommitment'] = maxResultsDF.apply(lambda x: calculateGoalCommit(x['goal']), axis=1)
    softmaxResultsDF['goalCommitment'] = softmaxResultsDF.apply(lambda x: calculateGoalCommit(x['goal']), axis=1)
    humanNormalTrail = humanResultsDF[humanResultsDF['noiseNumber'] != 'special']
    humanSpecialTrail = humanResultsDF[humanResultsDF['noiseNumber'] == 'special']
    maxNormalTrail = maxResultsDF[maxResultsDF['noiseNumber'] != 'special']
    maxSpecialTrail = maxResultsDF[maxResultsDF['noiseNumber'] == 'special']
    softmaxNormalTrail = softmaxResultsDF[softmaxResultsDF['noiseNumber'] != 'special']
    softmaxSpecialTrail = softmaxResultsDF[softmaxResultsDF['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    softmaxMeanDF = pd.DataFrame()
    humanMeanDF['goalCommitNormal'] = humanNormalTrail.groupby("name")['goalCommitment'].mean()
    humanMeanDF['goalCommitSpecail'] = humanSpecialTrail.groupby("name")['goalCommitment'].mean()
    maxMeanDF['goalCommitNormal'] = maxNormalTrail.groupby("name")['goalCommitment'].mean()
    maxMeanDF['goalCommitSpecail'] = maxSpecialTrail.groupby("name")['goalCommitment'].mean()
    softmaxMeanDF['goalCommitNormal'] = softmaxNormalTrail.groupby("name")['goalCommitment'].mean()
    softmaxMeanDF['goalCommitSpecail'] = softmaxSpecialTrail.groupby("name")['goalCommitment'].mean()
    humanGoalCommitMeanNormal = np.mean(humanMeanDF['goalCommitNormal'])
    humanGoalCommitMeanSpecail = np.mean(humanMeanDF['goalCommitSpecail'])
    maxGoalCommitMeanNormal = np.mean(maxMeanDF['goalCommitNormal'])
    maxGoalCommitMeanSpecail = np.mean(maxMeanDF['goalCommitSpecail'])
    softmaxGoalCommitMeanNormal = np.mean(softmaxMeanDF['goalCommitNormal'])
    softmaxGoalCommitMeanSpecail = np.mean(softmaxMeanDF['goalCommitSpecail'])
    # humanMeanDF.to_csv("humanMeanDF.csv")
    print('Goal commitment probability')
    print('Normal trial:', 'human:', humanGoalCommitMeanNormal, 'maxNoise0:', maxGoalCommitMeanNormal, 'maxNoise0.1:',
          softmaxGoalCommitMeanNormal)
    print('Specail trial:', 'human:', humanGoalCommitMeanSpecail, 'maxNoise0:', maxGoalCommitMeanSpecail, 'maxNoise0.1:',
          softmaxGoalCommitMeanSpecail)

    plt.title('Goal commitment probability')
    x = np.arange(3)
    y1 = [humanGoalCommitMeanNormal, maxGoalCommitMeanNormal, softmaxGoalCommitMeanNormal]
    y2 = [humanGoalCommitMeanSpecail, maxGoalCommitMeanSpecail, softmaxGoalCommitMeanSpecail]
    width = 0.2
    std_err1 = [np.std(humanMeanDF['goalCommitNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['goalCommitNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['goalCommitNormal'], ddof=1) / math.sqrt(subNum - 1)]
    std_err2 = [np.std(humanMeanDF['goalCommitSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['goalCommitSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['goalCommitSpecail'], ddof=1) / math.sqrt(subNum - 1)]
    error_attri = {'elinewidth': 1, 'ecolor': 'black', 'capsize': 3}
    plt.bar(x, y1, width, align='center', yerr=std_err1, error_kw=error_attri, label='normal trial', alpha=1)
    for a, b in zip(x, y1):
        plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    plt.bar(x + width, y2, width, align='center', yerr=std_err2, error_kw=error_attri, label='special trial', alpha=1)
    for a, b in zip(x, y2):
        plt.text(a + width, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    names = ['huamn', 'maxNoise0', 'maxNoise0.1']
    plt.xticks(x + width / 2, names)
    plt.ylabel('Probability')
    plt.ylim((0, 1))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
