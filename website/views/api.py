# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, jsonify, request, render_template
from ..model import Reservation
from ..utils import is_valid_email

app = Blueprint('api', __name__)


@app.route('/new')
def new():
    jid = request.values.get('jid', None)
    start=None
    end=None
    if is_valid_email(jid):
        data = {"error": False}
        data.update(Reservation.new(jid=jid).serialized)     
	start=data["start"]
        end=data["end"]
        data = check()      
        page = "validReserve.html"
    else:
        data = {"error": True, "error_message": "invalid jid"}
	page = "errorReserve.html"
    #return jsonify(data)
    return render_template(page,start=start,end=end)


@app.route('/check')
def check():
    key = request.values.get('key', None)
    if key:
        r = Reservation.query.filter_by(key=key).first()
        if r is not None:
            return jsonify(dict(r.serialized.items() + [("valid", True)]))
    return jsonify(valid=False)
