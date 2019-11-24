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
    humanNoiseTrail = humanResultsDF[humanResultsDF['noisePoint'] != '[]']
    maxNoiseTrail = maxResultsDF[maxResultsDF['noisePoint'] != '[]']
    softmaxNoiseTrail = softmaxResultsDF[softmaxResultsDF['noisePoint'] != '[]']
    humanNoiseTrail['isTimeMaxNextNoisePoint'] = humanNoiseTrail.apply(
        lambda x: calculateIsTimeMaxNextNoisePoint(x['reactionTime'], x['noisePoint']), axis=1)
    maxNoiseTrail['isTimeMaxNextNoisePoint'] = maxNoiseTrail.apply(
        lambda x: calculateIsTimeMaxNextNoisePoint(x['reactionTime'], x['noisePoint']), axis=1)
    softmaxNoiseTrail['isTimeMaxNextNoisePoint'] = softmaxNoiseTrail.apply(
        lambda x: calculateIsTimeMaxNextNoisePoint(x['reactionTime'], x['noisePoint']), axis=1)
    humanNormalTrail = humanNoiseTrail[humanNoiseTrail['noiseNumber'] != 'special']
    humanSpecialTrail = humanNoiseTrail[humanNoiseTrail['noiseNumber'] == 'special']
    maxNormalTrail = maxNoiseTrail[maxNoiseTrail['noiseNumber'] != 'special']
    maxSpecialTrail = maxNoiseTrail[maxNoiseTrail['noiseNumber'] == 'special']
    softmaxNormalTrail = softmaxNoiseTrail[softmaxNoiseTrail['noiseNumber'] != 'special']
    softmaxSpecialTrail = softmaxNoiseTrail[softmaxNoiseTrail['noiseNumber'] == 'special']
    humanMeanDF = pd.DataFrame()
    maxMeanDF = pd.DataFrame()
    softmaxMeanDF = pd.DataFrame()
    humanMeanDF['isTimeMaxNextNoisePointNormal'] = humanNormalTrail.groupby("name")['isTimeMaxNextNoisePoint'].mean()
    humanMeanDF['isTimeMaxNextNoisePointSpecail'] = humanSpecialTrail.groupby("name")['isTimeMaxNextNoisePoint'].mean()
    maxMeanDF['isTimeMaxNextNoisePointNormal'] = maxNormalTrail.groupby("name")['isTimeMaxNextNoisePoint'].mean()
    maxMeanDF['isTimeMaxNextNoisePointSpecail'] = maxSpecialTrail.groupby("name")['isTimeMaxNextNoisePoint'].mean()
    softmaxMeanDF['isTimeMaxNextNoisePointNormal'] = softmaxNormalTrail.groupby("name")['isTimeMaxNextNoisePoint'].mean()
    softmaxMeanDF['isTimeMaxNextNoisePointSpecail'] = softmaxSpecialTrail.groupby("name")['isTimeMaxNextNoisePoint'].mean()
    humanIsTimeMaxNextNoisePointMeanNormal = np.mean(humanMeanDF['isTimeMaxNextNoisePointNormal'])
    humanIsTimeMaxNextNoisePointMeanSpecail = np.mean(humanMeanDF['isTimeMaxNextNoisePointSpecail'])
    maxIsTimeMaxNextNoisePointMeanNormal = np.mean(maxMeanDF['isTimeMaxNextNoisePointNormal'])
    maxIsTimeMaxNextNoisePointMeanSpecail = np.mean(maxMeanDF['isTimeMaxNextNoisePointSpecail'])
    softmaxIsTimeMaxNextNoisePointMeanNormal = np.mean(softmaxMeanDF['isTimeMaxNextNoisePointNormal'])
    softmaxIsTimeMaxNextNoisePointMeanSpecail = np.mean(softmaxMeanDF['isTimeMaxNextNoisePointSpecail'])
    # humanMeanDF.to_csv("humanMeanDF.csv")
    print('If time is maximal next to noise point')
    print(
        'Normal trial:', 'human:', humanIsTimeMaxNextNoisePointMeanNormal, 'maxNoise0:', maxIsTimeMaxNextNoisePointMeanNormal,
        'maxNoise0.1:', softmaxIsTimeMaxNextNoisePointMeanNormal)
    print(
        'Specail trial:', 'human:', humanIsTimeMaxNextNoisePointMeanSpecail, 'maxNoise0:', maxIsTimeMaxNextNoisePointMeanSpecail,
        'maxNoise0.1:', softmaxIsTimeMaxNextNoisePointMeanSpecail)

    plt.title('If time is maximal next to noise point')
    x = np.arange(3)
    y1 = [humanIsTimeMaxNextNoisePointMeanNormal, maxIsTimeMaxNextNoisePointMeanNormal, softmaxIsTimeMaxNextNoisePointMeanNormal]
    y2 = [humanIsTimeMaxNextNoisePointMeanSpecail, maxIsTimeMaxNextNoisePointMeanSpecail, softmaxIsTimeMaxNextNoisePointMeanSpecail]
    width = 0.2
    std_err1 = [np.std(humanMeanDF['isTimeMaxNextNoisePointNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['isTimeMaxNextNoisePointNormal'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['isTimeMaxNextNoisePointNormal'], ddof=1) / math.sqrt(subNum - 1)]
    std_err2 = [np.std(humanMeanDF['isTimeMaxNextNoisePointSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(maxMeanDF['isTimeMaxNextNoisePointSpecail'], ddof=1) / math.sqrt(subNum - 1),
                np.std(softmaxMeanDF['isTimeMaxNextNoisePointSpecail'], ddof=1) / math.sqrt(subNum - 1)]
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
