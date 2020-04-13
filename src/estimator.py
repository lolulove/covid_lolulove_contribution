import math

def infectionsCalcution(periodType, timeToElapse):
    if periodType == 'months':
        normalizedDays = 30 * timeToElapse

    elif periodType == 'weeks':
        normalizedDays = 7 * timeToElapse

    else:
        normalizedDays = timeToElapse

    infectionFactor = normalizedDays // 3

    return 2 ** infectionFactor


def impact_cal(data={}):
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
        'hospitalBedsByRequestedTime': math.trunc(0.35 * data['totalHospitalBeds'] - impact['severeCasesByRequestedTime'])
    }

    return impact


def severeImpact_cal(data={}):
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
        'hospitalBedsByRequestedTime': math.trunc(0.35 * data['totalHospitalBeds'] - severeImpact['severeCasesByRequestedTime'])
    }

    return severeImpact


def estimator(data):
    return {
        'data': data,
        'impact': impact_cal(data),
        'severeImpact': severeImpact_cal(data)
    }

