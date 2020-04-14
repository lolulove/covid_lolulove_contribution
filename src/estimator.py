import math
from flask import Flask, jsonify, request, g
#from estimator import estimator
from data import data
import dicttoxml
import time

app = Flask(__name__)


def infectionsCalcution(periodType, timeToElapse):
    if periodType == "months":
        normalizedDays = 30 * timeToElapse

    elif periodType == "weeks":
        normalizedDays = 7 * timeToElapse

    else:
        normalizedDays = timeToElapse

    infectionFactor = normalizedDays // 3

    return 2 ** infectionFactor


def dayCalcution(periodType, timeToElapse):
    if periodType == "months":
        normalizedDays = 30 * timeToElapse

    elif periodType == "weeks":
        normalizedDays = 7 * timeToElapse

    else:
        normalizedDays = timeToElapse

    return normalizedDays


def impact_cal(data):
    impact = {
        "currentlyInfected": data["reportedCases"] * 10
    }

    impact = {
        "currentlyInfected": data["reportedCases"] * 10,
        "infectionsByRequestedTime": impact["currentlyInfected"] * infectionsCalcution(data["periodType"],
                                                                                       data["timeToElapse"])}

    impact = {
        "currentlyInfected": data["reportedCases"] * 10,
        "infectionsByRequestedTime": impact["currentlyInfected"] * infectionsCalcution(data["periodType"],
                                                                                       data["timeToElapse"]),
        "severeCasesByRequestedTime": math.floor(0.15 * impact["infectionsByRequestedTime"])
    }

    impact = {
        "currentlyInfected": data["reportedCases"] * 10,
        "infectionsByRequestedTime": impact["currentlyInfected"] * infectionsCalcution(data["periodType"],
                                                                                       data["timeToElapse"]),
        "severeCasesByRequestedTime": math.floor(0.15 * impact["infectionsByRequestedTime"]),
        "hospitalBedsByRequestedTime": math.trunc(0.35 * data["totalHospitalBeds"] - impact["severeCasesByRequestedTime"]),
        "casesForICUByRequestedTime": math.floor(0.05 * impact["infectionsByRequestedTime"]),
        "casesForVentilatorsByRequestedTime": math.floor(0.02 * impact["infectionsByRequestedTime"]),
        "dollarsInFlight": math.trunc((impact["infectionsByRequestedTime"] * data["region"]["avgDailyIncomePopulation"] * data["region"]["avgDailyIncomeInUSD"]) / dayCalcution(data["periodType"],
                                                   data["timeToElapse"]))
    }

    return impact


def severeImpact_cal(data):
    severeImpact = {
        "currentlyInfected": data["reportedCases"] * 50
    }

    severeImpact = {
        "currentlyInfected": data["reportedCases"] * 50,
        "infectionsByRequestedTime": severeImpact["currentlyInfected"] * infectionsCalcution(data["periodType"],
                                                                                             data["timeToElapse"])}

    severeImpact = {
        "currentlyInfected": data["reportedCases"] * 50,
        "infectionsByRequestedTime": severeImpact["currentlyInfected"] * infectionsCalcution(data["periodType"],
                                                                                             data["timeToElapse"]),
        "severeCasesByRequestedTime": math.floor(0.15 * severeImpact["infectionsByRequestedTime"])
    }

    severeImpact = {
        "currentlyInfected": data["reportedCases"] * 50,
        "infectionsByRequestedTime": severeImpact["currentlyInfected"] * infectionsCalcution(data["periodType"],
                                                                                             data["timeToElapse"]),
        "severeCasesByRequestedTime": math.floor(0.15 * severeImpact["infectionsByRequestedTime"]),
        "hospitalBedsByRequestedTime": math.trunc(0.35 * data["totalHospitalBeds"] - severeImpact["severeCasesByRequestedTime"]),
        "casesForICUByRequestedTime": math.floor(0.05 * severeImpact["infectionsByRequestedTime"]),
        "casesForVentilatorsByRequestedTime": math.floor(0.02 * severeImpact["infectionsByRequestedTime"]),
        "dollarsInFlight": math.trunc((severeImpact["infectionsByRequestedTime"] * data["region"]["avgDailyIncomePopulation"] * data["region"]["avgDailyIncomeInUSD"]) / dayCalcution(data["periodType"],
                                                   data["timeToElapse"]))
    }

    return severeImpact


def estimator(data):
    return {
        "data": data,
        "impact": impact_cal(data),
        "severeImpact": severeImpact_cal(data)
    }


@app.route("/api/v1/on-covid-19", methods=["GET"])
def index():
    return jsonify(estimator(data))


@app.route("/api/v1/on-covid-19/json", methods=["GET"])
def index1():
    return jsonify(estimator(data))


@app.route("/api/v1/on-covid-19/xml", methods=["GET"])
def index2():
    return dicttoxml.dicttoxml(estimator(data))


@app.route("/api/v1/on-covid-19/log", methods=["GET"])
def index3():
    dispatch = ""
    with open("syslog.txt", "r") as sys_file:
        lines = sys_file.readlines()
        for line in lines:
            dispatch = dispatch + line

    return dispatch


@app.before_request
def activate_timing():
    g.start_time = time.time()


@app.after_request
def dactivate_timing(response):
    time_elapsed = round(time.time() - g.start_time, 2)
    status = response.status_code
    method_type = request.method
    url_path = request.path
    with open("syslog.txt", "a") as sys_file:
        print("{}\t\t\t{}\t\t\t{}\t\t\t{}ms".format(method_type, url_path, status, time_elapsed), file=sys_file)
    return response


if __name__ == "__main__":
    app.run(debug=True)
