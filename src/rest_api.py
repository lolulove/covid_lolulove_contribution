from flask import Flask, jsonify, request, g
from estimator import estimator
import dicttoxml
from logging import FileHandler, INFO, WARNING, DEBUG
import time

app = Flask(__name__)

file_handler = FileHandler('log.txt')
file_handler.setLevel(DEBUG)

app.logger.addHandler(file_handler)

@app.route('/api/v1/on-covid-19', methods=['POST'])
def index():
    #g.request_start_time = time.time()
    data = request.get_json()
    #print(data)
    data1 = estimator(data)
    # logging.basicConfig(filename='post_request.log')
    # g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    # print(g.request_time())
    return jsonify({'result': data1}), 200

@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def index1():
    #g.request_start_time = time.time()
    data = request.get_json()
    #print(data)
    data1 = estimator(data)
    # logging.basicConfig(filename='post_request.log')
    # g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    # print(g.request_time())
    return jsonify({'result': data1}), 200


@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def index2():
    #g.request_start_time = time.time()
    data = request.get_json()
    #print(data)
    data1 = dicttoxml.dicttoxml(estimator(data))
    # logging.basicConfig(filename='post_request.log')
    # g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    # print(g.request_time())
    return data1


if __name__ == '__main__':
    app.run(debug=True)
