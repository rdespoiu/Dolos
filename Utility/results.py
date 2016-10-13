from flask import jsonify
from timestamp import timestamp

def results(data):
    return jsonify(**{
        'time': timestamp(),
        'results': data
    })
