import pytest
import sqlite3 as sq
from helperFunctions import find_user, lookup_by_username, password_match
import datetime

@pytest.fixture
def session():
    con = sq.connect("twitterReloaded.db",
                 detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
    cur = con.cursor()
    
    username = "testUser"
    password = "0000"
    cur.execute("""INSERT INTO user (userID, username, password, joinDate)
                        VALUES (?, ?, ?, ?)
                    """, (0, username, password, datetime.datetime.now()))
    con.commit()
    
    yield
    
    cur.execute("""DELETE FROM user
                   WHERE userID = ?
                """, (0,))
    con.commit()


#, (None, None), (1000, None)
@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("test_input, expected", [(0, "testUser")])
def test_find_user(test_input, expected):
    """For testing find_user, the parameters of this function should never be empty or higher than the biggest userID
    First case: Should pass

    Args:
        test_input (int): userID
        expected (str): username
    """
    assert find_user(test_input) == expected


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("test_input, expected", [("testUser", (True, (0, "testUser"))), (None, (False, None)), (1000, (False, None))])
def test_lookup_by_user(test_input, expected):
    """For testing lookup_by_user, input for function tested has user input

    Args:
        test_input (str): username
        expected (tuple<bool, tuple<int, str>>): (user found, (userID, username))
    """    
    assert lookup_by_username(test_input) == expected


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("test_input, expected", [(("0000", "testUser"), (True, ("0000",))), (("", "testUser"), (False, ("0000",))), (("1234", "testUser"), (False, ("0000",)))])
def test_password_match(test_input, expected):
    """for testing password_match, input for function tested has user input

    Args:
        test_input (tuple<str, str>): (password, username)
        expected (tuple<bool, tuple<str,>): (password match result, (password,))
    """    
    assert password_match(test_input[0], test_input[1]) == expected