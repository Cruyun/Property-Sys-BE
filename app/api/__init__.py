#coding: utf-8
from flask import Blueprint

main = Blueprint('api', __name__)

from . import users, estate, payment, rooms, login, announcements, parking, reports
