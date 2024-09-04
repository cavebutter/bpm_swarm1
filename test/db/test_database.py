import pytest
from db.database import Database

@pytest.fixture
def database():
    return Database("athena.eagle-mimosa.ts.net", "jay", "d0ghouse", "sandbox")
# Test Database class


def create_test_table_w_data(database):
    database.connect()
    query = "CREATE TABLE IF NOT EXISTS test_table(id INT)"
    database.create_table(query)
    database.execute_query("INSERT INTO test_table VALUES (1)")


def test_connect(database):
    db = database
    db.connect()
    assert db.connection is not None


def test_close(database):
    db = database
    db.connect()
    db.close()
    assert db.connection is None


# Positive unit test case for drop_table
def test_drop_table_positive(database):
    table_name = "test_table"
    database.connect()
    database.create_table(f"CREATE TABLE IF NOT EXISTS {table_name}(id INT)")
    database.drop_table(table_name)
    # Add assertion to check if the table was dropped successfully
    assert True  # Add your assertion here

# Negative unit test case for drop_table
# def test_drop_table_negative(database):
#     database.connect()
#     table_name = "non_existing_table"
#     # Add assertion to check if dropping a non-existing table raises an exception
#     with pytest.raises(Exception):
#         database.drop_table(table_name)


# Positive unit test case for create_table
def test_create_table_positive(database):
    database.connect()
    query = "CREATE TABLE IF NOT EXISTS test_table(id INT)"
    database.create_table(query)
    # Add assertion to check if the table was created successfully
    assert True  # Add your assertion here


# Negative unit test case for create_table
def test_create_table_negative(database):
    database.connect()
    query = "CREATE TABLE test_table(id INT)"
    # Add assertion to check if creating a table with incorrect query raises an exception
    with pytest.raises(Exception):
        database.create_table(query)


def test_execute_query_positive(database):
    database.connect()
    database.drop_table("test_table")
    query = "CREATE TABLE IF NOT EXISTS test_table(id INT)"
    assert database.execute_query(query) is True


def test_execute_query_w_params_positive(database):
    database.connect()
    database.drop_table("test_table")
    database.execute_query("CREATE TABLE IF NOT EXISTS test_table(id INT)")
    test_query = "INSERT INTO test_table VALUES (%s)"
    params = (1,)
    assert database.execute_query(test_query, params) is True


def test_execute_query_negative(database):
    database.connect()
    query = "CREAT TABLE test_table(id INT)" # wrong query
    assert database.execute_query(query) is False


def test_execute_select_query_positive(database):
    database.connect()
    database.drop_table("test_table")
    create_test_table_w_data(database)
    query = "SELECT * FROM test_table"
    assert database.execute_select_query(query) == [(1,)]


def test_execute_select_query_negative(database):
    database.connect()
    query = "SELECT * FROM non_existing_table"
    with pytest.raises(Exception):
        database.execute_select_query(query)