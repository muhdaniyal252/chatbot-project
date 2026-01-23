import os
import pytest

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_db.sqlite3')

@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
    # Set environment variables before Django setup
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
    os.environ['USE_SQLITE_FOR_TESTS'] = '1'
    # Now import Django and run setup
    import django
    django.setup()
    from django.core.management import call_command
    call_command('migrate', verbosity=0)
    yield
    # Remove test DB after tests
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
