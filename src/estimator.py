import json
from data import data
from flask import Flask, g, jsonify, request
from dicttoxml import dicttoxml
from math import trunc
import logging
import time
app = Flask(__name__)
out_data = {
    "data":data,
    "impact":{},
    "severeImpact":{}
}

def dayCalcution(periodType, timeToElapse):
    if periodType == 'months':
        normalizedDays = 30 * timeToElapse

    elif periodType == 'weeks':
        normalizedDays = 7 * timeToElapse

    else:
        normalizedDays = timeToElapse

    return normalizedDays


def challenge1_fix(data):
    impact_currently_infected = data["reportedCases"] * 10
    severe_Impact_currently_infected: data["reportedCases"] * 50
    out_data["impact"]["currentlyInfected"] = impact_currently_infected
    out_data["severeImpact"]["currentlyInfected"] = severe_Impact_currently_infected

    impact_infections_by_requested_time = impact_currently_infected * (2 **(dayCalcution(data)//3))
    severe_Impact_infections_by_requested_time = severe_Impact_currently_infected * (2 ** (dayCalcution(data) // 3))
    out_data["impact"]["infectionsByRequestedTime"] = impact_infections_by_requested_time
    out_data["severeImpact"]["infectionsByRequestedTime"] = severe_Impact_infections_by_requested_time

    return out_data


def challenge2_fix(data):
    after_challenge1 = challenge1_fix(data)
    impact_severe_cases_requested_time = trunc(after_challenge1["impact"]["infectionsByRequestedTime"]*0.15)
    severe_Impact_severe_cases_requested_time = trunc(after_challenge1["severeImpact"]["infectionsByRequestedTime"] * 0.15)
    after_challenge1["impact"]["severeCasesByRequestedTime"] = impact_severe_cases_requested_time
    after_challenge1["severeImpact"]["severeCasesByRequestedTime"] = severe_Impact_severe_cases_requested_time

    impact_hospital_beds_by_requested_time = trunc(data["totalHospitalBeds"] * 0.35 - impact_severe_cases_requested_time )
    severe_Impact_hospital_beds_by_requested_time = trunc(data["totalHospitalBeds"] * 0.35 - severe_Impact_severe_cases_requested_time)
    after_challenge1["impact"]["hospitalBedsByRequestedTime"] = impact_hospital_beds_by_requested_time
    after_challenge1["severeImpact"]["hospitalBedsByRequestedTime"] = severe_Impact_hospital_beds_by_requested_time
    out_data = after_challenge1

    return out_data


def challenge3_fix(data):
    after_challenge2 = challenge2_fix(data)
    impact_cases_for_icu_by_reuested_time = trunc(after_challenge2["impact"]["infectionsByRequestedTime"])
    severe_Impact_cases_for_icu_by_reuested_time = trunc(after_challenge2["severeImpact"]["infectionsByRequestedTime"])
    after_challenge2["impact"]["severeCasesByRequestedTime"] = impact_cases_for_icu_by_reuested_time
    after_challenge2["severeImpact"]["severeCasesByRequestedTime"] = severe_Impact_cases_for_icu_by_reuested_time

    impact_cases_for_ventilators_by_requested_time = trunc(after_challenge2["impact"]["infectionsByRequestedTime"] * 0.02)
    severe_Impact_cases_for_ventilators_by_requested_time = trunc(
        after_challenge2["severeImpact"]["infectionsByRequestedTime"] * 0.02)

    after_challenge2["impact"]["casesForVentilatorsByRequestedTime"] = impact_cases_for_ventilators_by_requested_time
    after_challenge2["severeImpact"]["casesForVentilatorsByRequestedTime"] = severe_Impact_cases_for_ventilators_by_requested_time
    out_data = after_challenge2

    return out_data

def estimator(data):
    challenge1_fix(data)
    challenge2_fix(data)
    challenge3_fix(data)

    return out_data


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
    with open('syslog.txt', 'a') as sys_file:
        print("{}\t\t\t{}\t\t\t{}\t\t\t{}ms".format(method_type, url_path, status, time_elapsed), file=sys_file)
    return response


if __name__ == "__main__":
    app.run(debug=True)
