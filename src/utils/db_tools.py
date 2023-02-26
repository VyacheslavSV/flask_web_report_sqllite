import argparse
import os
from pathlib import Path

from peewee import SqliteDatabase
from svv_report_main.svv_report import read_file, parse_abbr_lines, parsed_start_end_lines

from src.models import Driver, StartLog, EndLog

DB_FILEPATH = '../database.db'

DRIVERS_FILENAME = 'abbreviations.txt'
START_FILENAME = 'start.log'
END_FILENAME = 'end.log'


def create_db() -> SqliteDatabase:
    """
    Create database and create tables in the database
    :return: SqliteDatabase
    """
    if os.path.exists(DB_FILEPATH):
        os.remove(DB_FILEPATH)
    db = SqliteDatabase(DB_FILEPATH)
    db.create_tables([Driver, StartLog, EndLog])
    return db


def separate_data_to_dict(drivers: list, start: list, end: list) -> (dict, dict, dict):
    """
    Separate data from correct dicts with data
    :param drivers: list
    :param start: list
    :param end: list
    :return: (dict, dict, dict)
    """
    drivers = [dict(zip(('abbr', 'name', 'team'), driver))
               for driver in drivers]
    start = [dict(zip(('driver', 'time_start'), drive_start))
             for drive_start in start]
    end = [dict(zip(('driver', 'time_finish'), drive_end))
           for drive_end in end]
    return drivers, start, end


def get_data_from_files(path: str) -> tuple[dict, dict, dict]:
    """
    Get data from files and return dicts of data
    :param path: str
    :return: tuple[dict, dict, dict]
    """
    path_dir = Path(path).resolve()
    drivers = parse_abbr_lines(read_file(path_dir / DRIVERS_FILENAME))
    start = parsed_start_end_lines(read_file(path_dir / START_FILENAME))
    end = parsed_start_end_lines(read_file(path_dir / END_FILENAME))
    return separate_data_to_dict(drivers, start, end)


def store_data_to_db(db: SqliteDatabase, data: tuple) -> None:
    """
    Store data to database
    :param db: SqliteDatabase
    :param data: dict
    :return: None
    """
    drivers, start, end = data
    with db.atomic() as transaction:
        drivers_id = {}
        for driver in drivers:
            driver_obj = Driver.create(**driver)
            drivers_id[driver_obj.abbr] = driver_obj.id
        for time in start:
            StartLog.create(**{'time_start': time.get('time_start'),
                               'driver_id': drivers_id.get(time.get('driver'))})
        for time in end:
            EndLog.create(**{'time_finish': time.get('time_finish'),
                             'driver_id': drivers_id.get(time.get('driver'))})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true', help='create db')
    parser.add_argument(
        '--path',
        nargs='?',
        type=str,
        help='get data from files for path')
    parser.add_argument(
        '--store_data',
        action='store_true',
        help='store_data_to_db')
    args = parser.parse_args()
    db = create_db() if args.create else 'Please write ARGUMENT (--create) in CLI'
    print('1. Read files')
    data = get_data_from_files(args.path) if args.path else '1'
    print('2. Store data into db')
    if args.store_data:
        store_data_to_db(db, data)
    print('Database complete')


if __name__ == '__main__':
    main()
