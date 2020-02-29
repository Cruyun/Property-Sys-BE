#coding: utf-8
from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, estate, payment, rooms, login, announcements, parking, reports
