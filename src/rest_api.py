from flask import Flask, jsonify, request, g
from data3 import estimator
import dicttoxml
import time

app = Flask(__name__)


@app.route('/api/v1/on-covid-19', methods=['GET'])
def index(data={}):
    return jsonify(estimator(data))


@app.route('/api/v1/on-covid-19/json', methods=['GET'])
def index1(data={}):
    return jsonify(estimator(data))


@app.route('/api/v1/on-covid-19/xml', methods=['GET'])
def index2(data={}):
    return dicttoxml.dicttoxml(estimator(data))


@app.route('/api/v1/on-covid-19/log', methods=['GET'])
def index3():
    dispatch = ""
    with open('syslog.txt', 'r') as sys_file:
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


if __name__ == '__main__':
    app.run(debug=True)
