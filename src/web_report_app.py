from datetime import datetime
from pathlib import Path
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flasgger import swag_from
from flask import Blueprint, request, jsonify, render_template, abort
from flask_restful import Api, Resource

from src.models import Driver

ROOT = Path(__file__).resolve().parent
FILES = ROOT / 'files'

bp = Blueprint('web_report_app', __name__)
api = Api(bp)


def get_time(start_logs: str, end_logs: str) -> str:
    """
    Gets the time difference between two timestamps
    :param start_logs: str
    :param end_logs: str
    :return: str
    """
    time_start = datetime.strptime(start_logs, '%H:%M:%S') if len(
        start_logs) < 9 else datetime.strptime(start_logs, '%H:%M:%S.%f')
    time_finish = datetime.strptime(end_logs, '%H:%M:%S') if len(
        end_logs) < 9 else datetime.strptime(end_logs, '%H:%M:%S.%f')
    time = time_finish - time_start if time_finish > time_start else time_start - time_finish
    return str(time)


def get_drivers(desc: bool = False) -> list:
    """
    Gets the list of drivers from the database and sorts them based on their time
    :param desc: bool = False
    :return: list
    """
    drivers = Driver.select()
    result = {}
    for driver in drivers:
        result[driver.id] = {
            'name': driver.name,
            'abbr': driver.abbr,
            'team': driver.team,
            'time': get_time(str(*[s.time_start for s in driver.start_logs]),
                             str(*[f.time_finish for f in driver.end_logs])),
        }
    changed_result = [*result.values()]
    return sorted(changed_result, key=lambda x: x['time']) if not desc else \
        sorted(changed_result, key=lambda x: x['time'], reverse=True)


def get_driver_by_id(driver_id: str, take_data: list) -> list:
    """
    Gets the list of drivers from the database and find required driver
    :param driver_id: str
    :param take_data: list
    :return: list
    """
    return list(
        filter(
            lambda item: item['abbr'] == str(driver_id),
            take_data))[0]


def prepare_responce(format_: str, data: list):
    """ Prepares a response for the given format and data.
    :param format_ (str): The format of the response, either json or xml.
    :param data (list): The data to be included in the response.
    :return: json response, or xml response, or a 404 error.
    """
    if format_ == 'json':
        return jsonify(data)
    elif format_ == 'xml':
        return parseString(
            dicttoxml(
                data, custom_root='report')).toprettyxml(), 200
    return abort(404, description="Please input correct format: json or xml")


@bp.route('/report/')
def report():
    """
    This route return list data from database - names, teams, time lupe for all drivers
    """
    order = request.args.get('order')
    result = get_drivers(order)
    return render_template('report.html', result=result)


@bp.route('/drivers/')
def drivers():
    """
    This route return list data from database - abbreviations, names all drivers
    Route return list data - abbreviations, names
    Element abbreviations is link which sent
    to page with data about specify driver(name, team, time lupe)
    """
    order = request.args.get('order')
    driver_id = request.args.get('driver_id')
    result = get_drivers(order)
    if not driver_id:
        return render_template('drivers.html', driver_data=result)
    filtered_data = get_driver_by_id(driver_id, result)
    return render_template('driver.html', driver_data=filtered_data)


class ApiReport(Resource):
    @swag_from('report.yml')
    def get(self):
        """
        Return api data route(/report/) in the format json or xml
        """
        order = request.args.get('order')
        format_ = request.args.get('format')
        result = get_drivers(order)
        current_dict_drivers = [{'driver_id': id_number,
                                 'name': data['name'],
                                 'team': data['team'],
                                 'time': data['time']} for id_number,
                                data in enumerate(result,
                                                  1)]
        return prepare_responce(format_, current_dict_drivers)


class ApiDrivers(Resource):
    @swag_from('driver.yml')
    def get(self):
        """
        Return api data route(/drivers/, if to go to link abbreviate /driver/) in the format json or xml
        """
        order = request.args.get('order')
        driver_id = request.args.get('driver_id')
        format_ = request.args.get('format')
        result = get_drivers(order)
        current_dict_drivers = [{'serial number': id_number,
                                 'abbr': data['abbr'],
                                 'name': data['name'],
                                 'team': data['team']} for id_number,
                                data in enumerate(result,
                                                  1)]
        if not driver_id:
            return prepare_responce(format_, current_dict_drivers)
        driver_data = get_driver_by_id(driver_id, result)
        current_dict_driver = [{'name': driver_data['name'],
                                'team': driver_data['team'], 'time': driver_data['time']}]
        return prepare_responce(format_, current_dict_driver)


api.add_resource(ApiReport, '/api/v1/report/')
api.add_resource(ApiDrivers, '/api/v1/drivers/')
