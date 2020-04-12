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

    return impact


def severeImpact_cal(data={}):
    severeImpact = {
        'currentlyInfected': data['reportedCases'] * 50
    }

    severeImpact = {
        'currentlyInfected': data['reportedCases'] * 50,
        'infectionsByRequestedTime': severeImpact['currentlyInfected'] * infectionsCalcution(data['periodType'],
                                                                                             data['timeToElapse'])}
    return severeImpact


def estimator(data):
    return {
        'data': data,
        'impact': impact_cal(data),
        'severeImpact': severeImpact_cal(data)
    }
