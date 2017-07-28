import json

from flask import url_for, jsonify, abort, request
from sqlalchemy.exc import IntegrityError

from . import api
from .. import db
from ..models import Sensor, Data
from ..queries import all_sensors, all_datas

@api.route('/data', methods=['POST'])
def add_data():
    dat = Data.from_dict(json.loads(request.data))
    db.session.add(dat)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400)
    sensor_name = all_sensors().filter(Sensor.id==dat.sensor_id).first().name
    resp = jsonify(dat.to_dict())
    resp.status_code = 201
    resp.headers['Location'] = url_for('api.get_data', id=dat.id)
    return resp

@api.route('/data/<id>', methods=['GET'])
def get_data(id):
    dat = all_datas().filter(Data.id==id).first()
    if dat is None:
        abort(400)
    return jsonify(dat.to_dict())