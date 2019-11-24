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
    humanResultsDF['firstIntentStepRatio'] = humanResultsDF.apply(lambda x: calculateFirstIntentStepRatio(x['goal']),
                                                                  axis=1)
    maxResultsDF['firstIntentStepRatio'] = maxResultsDF.apply(lambda x: calculateFirstIntentStepRatio(x['goal']),
                                                              axis=1)
    softmaxResultsDF['firstIntentStepRatio'] = softmaxResultsDF.apply(
        lambda x: calculateFirstIntentStepRatio(x['goal']), axis=1)
    humanNormalTrail = humanResultsDF[humanResultsDF['noiseNumber'] != 'special']
    humanSpecialTrail = humanResultsDF[humanResultsDF['noiseNumber'] == 'special']
    maxNormalTrail = maxResultsDF[maxResultsDF['noiseNumber'] != 'special']
    maxSpecialTrail = maxResultsDF[maxResultsDF['noiseNumber'] == 'special']
    softmaxNormalTrail = softmaxResultsDF[softmaxResultsDF['noiseNumber'] != 'special']
    softmaxSpecialTrail = softmaxResultsDF[softmaxResultsDF['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    softmaxMeanDF = pd.DataFrame()
    humanMeanDF['firstIntentStepRatioNormal'] = humanNormalTrail.groupby("name")['firstIntentStepRatio'].mean()
    humanMeanDF['firstIntentStepRatioSpecail'] = humanSpecialTrail.groupby("name")['firstIntentStepRatio'].mean()
    maxMeanDF['firstIntentStepRatioNormal'] = maxNormalTrail.groupby("name")['firstIntentStepRatio'].mean()
    maxMeanDF['firstIntentStepRatioSpecail'] = maxSpecialTrail.groupby("name")['firstIntentStepRatio'].mean()
    softmaxMeanDF['firstIntentStepRatioNormal'] = softmaxNormalTrail.groupby("name")['firstIntentStepRatio'].mean()
    softmaxMeanDF['firstIntentStepRatioSpecail'] = softmaxSpecialTrail.groupby("name")['firstIntentStepRatio'].mean()
    humanFirstIntentStepRatioMeanNormal = np.mean(humanMeanDF['firstIntentStepRatioNormal'])
    humanFirstIntentStepRatioMeanSpecail = np.mean(humanMeanDF['firstIntentStepRatioSpecail'])
    maxFirstIntentStepRatioMeanNormal = np.mean(maxMeanDF['firstIntentStepRatioNormal'])
    maxFirstIntentStepRatioMeanSpecail = np.mean(maxMeanDF['firstIntentStepRatioSpecail'])
    softmaxFirstIntentStepRatioMeanNormal = np.mean(softmaxMeanDF['firstIntentStepRatioNormal'])
    softmaxFirstIntentStepRatioMeanSpecail = np.mean(softmaxMeanDF['firstIntentStepRatioSpecail'])
    # meanDF.to_csv("meandF.csv")
    print('First intent step ratio')
    print('Normal trial:', 'human:', humanFirstIntentStepRatioMeanNormal, 'maxNoise0:', maxFirstIntentStepRatioMeanNormal,
          'maxNoise0.1:', softmaxFirstIntentStepRatioMeanNormal)
    print('Specail trial:', 'human:', humanFirstIntentStepRatioMeanSpecail, 'maxNoise0:', maxFirstIntentStepRatioMeanSpecail,
          'maxNoise0.1:', softmaxFirstIntentStepRatioMeanSpecail)

    plt.title('First intent step ratio')
    x = np.arange(3)
    y1 = [humanFirstIntentStepRatioMeanNormal, maxFirstIntentStepRatioMeanNormal, softmaxFirstIntentStepRatioMeanNormal]
    y2 = [humanFirstIntentStepRatioMeanSpecail, maxFirstIntentStepRatioMeanSpecail,
          softmaxFirstIntentStepRatioMeanSpecail]
    width = 0.2
    std_err1 = [np.std(humanMeanDF['firstIntentStepRatioNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['firstIntentStepRatioNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['firstIntentStepRatioNormal'], ddof=1) / math.sqrt(subNum - 1)]
    std_err2 = [np.std(humanMeanDF['firstIntentStepRatioSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['firstIntentStepRatioSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['firstIntentStepRatioSpecail'], ddof=1) / math.sqrt(subNum - 1)]
    error_attri = {'elinewidth': 1, 'ecolor': 'black', 'capsize': 3}
    plt.bar(x, y1, width, align='center', yerr=std_err1, error_kw=error_attri, label='normal trial', alpha=1)
    for a, b in zip(x, y1):
        plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    plt.bar(x + width, y2, width, align='center', yerr=std_err2, error_kw=error_attri, label='special trial', alpha=1)
    for a, b in zip(x, y2):
        plt.text(a+width, b + 0.01, '%.3f' % b, ha='center', va='bottom')
    names = ['huamn', 'maxNoise0', 'maxNoise0.1']
    plt.xticks(x + width / 2, names)
    plt.ylabel('Ratio')
    plt.ylim((0, 1))
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
