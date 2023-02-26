import pytest
from peewee import SqliteDatabase
from svv_report_main.svv_report import parse_abbr_lines, parsed_start_end_lines
from src.models import Driver, StartLog, EndLog
from src import create_app
from src.utils.db_tools import store_data_to_db, separate_data_to_dict

TEST_DATA_ABBR = [
    'SVF_Sebastian Vettel_FERRARI\n',
    'VBM_Valtteri Bottas_MERCEDES\n',
    'SVM_Stoffel Vandoorne_MCLAREN RENAULT\n']
TEST_DATA_START = [
    'SVF2018-05-24_12:02:58.917\n',
    'SVM2018-05-24_12:18:37.735\n',
    'VBM2018-05-24_12:00:00.000']
TEST_DATA_END = [
    'SVF2018-05-24_12:13:13.883\n',
    'SVM2018-05-24_12:19:50.198\n',
    'VBM2018-05-24_12:01:12.434\n']
TEST_RESULT = [('Sebastian Vettel', 'FERRARI', '0:01:04.415000'),
               ('Valtteri Bottas', 'MERCEDES', '0:01:12.434000'),
               ('Stoffel Vandoorne', 'MCLAREN RENAULT', '0:01:12.463000')]


def temporary_path(directory_temp):
    directory_temp.mkdir(parents=True)
    with app.app_context():
        db = SqliteDatabase(directory_temp)
        db.create_tables([Driver, StartLog, EndLog])

        data = separate_data_to_dict(parse_abbr_lines(TEST_DATA_ABBR),
                                     parsed_start_end_lines(TEST_DATA_START),
                                     parsed_start_end_lines(TEST_DATA_END))
        store_data_to_db(db, data)


@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
