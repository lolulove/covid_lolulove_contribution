import math
from data import data

def infectionsCalcution(periodType, timeToElapse):
    if periodType == 'months':
        normalizedDays = 30 * timeToElapse

    elif periodType == 'weeks':
        normalizedDays = 7 * timeToElapse

    else:
        normalizedDays = timeToElapse

    infectionFactor = normalizedDays // 3

    return 2 ** infectionFactor


def dayCalcution(periodType, timeToElapse):
    if periodType == 'months':
        normalizedDays = 30 * timeToElapse

    elif periodType == 'weeks':
        normalizedDays = 7 * timeToElapse

    else:
        normalizedDays = timeToElapse

    return normalizedDays


def impact_cal(data):
    impact = {
        'currentlyInfected': data['reportedCases'] * 10
    }

    impact = {
        'currentlyInfected': data['reportedCases'] * 10,
        'infectionsByRequestedTime': impact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                       data['timeToElapse'])}

    impact = {
        'currentlyInfected': data['reportedCases'] * 10,
        'infectionsByRequestedTime': impact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                       data['timeToElapse']),
        'severeCasesByRequestedTime': math.floor(0.15 * impact['infectionsByRequestedTime'])
    }

    impact = {
        'currentlyInfected': data['reportedCases'] * 10,
        'infectionsByRequestedTime': impact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                       data['timeToElapse']),
        'severeCasesByRequestedTime': math.floor(0.15 * impact['infectionsByRequestedTime']),
        'hospitalBedsByRequestedTime': math.trunc(0.35 * data['totalHospitalBeds'] - impact['severeCasesByRequestedTime']),
        'casesForICUByRequestedTime': math.floor(0.05 * impact['infectionsByRequestedTime']),
        'casesForVentilatorsByRequestedTime': math.floor(0.02 * impact['infectionsByRequestedTime']),
        'dollarsInFlight': math.trunc((impact['infectionsByRequestedTime'] * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD']) / dayCalcution(data['periodType'],
                                                   data['timeToElapse']))
    }

    return impact


def severeImpact_cal(data):
    severeImpact = {
        'currentlyInfected': data['reportedCases'] * 50
    }

    severeImpact = {
        'currentlyInfected': data['reportedCases'] * 50,
        'infectionsByRequestedTime': severeImpact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                             data['timeToElapse'])}

    severeImpact = {
        'currentlyInfected': data['reportedCases'] * 50,
        'infectionsByRequestedTime': severeImpact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                             data['timeToElapse']),
        'severeCasesByRequestedTime': math.floor(0.15 * severeImpact['infectionsByRequestedTime'])
    }

    severeImpact = {
        'currentlyInfected': data['reportedCases'] * 50,
        'infectionsByRequestedTime': severeImpact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                             data['timeToElapse']),
        'severeCasesByRequestedTime': math.floor(0.15 * severeImpact['infectionsByRequestedTime']),
        'hospitalBedsByRequestedTime': math.trunc(0.35 * data['totalHospitalBeds'] - severeImpact['severeCasesByRequestedTime']),
        'casesForICUByRequestedTime': math.floor(0.05 * severeImpact['infectionsByRequestedTime']),
        'casesForVentilatorsByRequestedTime': math.floor(0.02 * severeImpact['infectionsByRequestedTime']),
        'dollarsInFlight': math.trunc((severeImpact['infectionsByRequestedTime'] * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD']) / dayCalcution(data['periodType'],
                                                   data['timeToElapse']))
    }

    return severeImpact


def estimator(data):
    return {
        'data': data,
        'impact': impact_cal(data),
        'severeImpact': severeImpact_cal(data)
    }

