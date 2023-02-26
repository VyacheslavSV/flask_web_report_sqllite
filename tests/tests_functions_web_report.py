import pytest
from peewee import SqliteDatabase

from src.models import Driver, StartLog, EndLog
from src.web_report_app import get_drivers, get_time, get_driver_by_id

result_get_drivers = [{'abbr': 'SVF',
                       'name': 'Sebastian Vettel',
                       'team': 'FERRARI',
                       'time': '0:01:04.415000'},
                      {'abbr': 'VBM',
                       'name': 'Valtteri Bottas',
                       'team': 'MERCEDES',
                       'time': '0:01:12.434000'},
                      {'abbr': 'SVM',
                       'name': 'Stoffel Vandoorne',
                       'team': 'MCLAREN RENAULT',
                       'time': '0:01:12.463000'}]

result_get_driver_by_id = {'abbr': 'SVF',
                           'name': 'Sebastian Vettel',
                           'team': 'FERRARI',
                           'time': '0:01:04.415000'}


@pytest.fixture
def db(tmpdir):
    db_path = str(tmpdir.join('test.db'))
    test_db = SqliteDatabase(db_path)
    test_db.create_tables([Driver, StartLog, EndLog])
    yield test_db
    test_db.close()


def test_get_drivers(db):
    drivers = get_drivers()
    assert drivers == result_get_drivers


def test_get_driver_by_id():
    assert get_driver_by_id(
        'SVF', result_get_drivers) == result_get_driver_by_id


def test_get_time():
    assert get_time('12:02:58.917', '12:13:13.883') == '0:10:14.966000'


if __name__ == "__main__":
    pytest.main()
