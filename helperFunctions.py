import datetime
import os
from subprocess import call
import sqlite3 as sq

# Database connection
con = sq.connect("twitterReloaded.db",
                 detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
cur = con.cursor()

def today():
    """Prettier way to call datetime function in code.

    Returns:
        datetime: today's date
    """
    return datetime.datetime.today().date()


def clear_screen():
    """Clears the terminal screen, compatibility for linux, mac and windows.
    """
    if os.name == 'posix':
        call('clear')
    else:
        os.system("cls")


def logged_telemetry(userID):
    """Saves into the database when its called, data is used for telemetry functions.

    Args:
        userID (int): Current user's ID
    """    
    curr_date = datetime.datetime.now()
    cur.execute("""
                INSERT INTO telemetry (userID, date)
                VALUES (?, ?)
                """, (userID, curr_date))
    con.commit()


def menu_op_in_range(op, range):
    """Checks if user's choise is in given menu range

    Args:
        op (str): User's menu choise
        range (list<int>): Range of menu

    Returns:
        bool: True if choise in range, False if not
    """
    if not op.isnumeric():
        return False
    
    if int(op) in range:
        return True
    else:
        return False


def find_user(userID):
    """Gets username from the database with the corresponding userID and return the username.

    Args:
        userID (int): ID of the user whose username is needed.

    Returns:
        str: username
    """    
    res = cur.execute("""
                SELECT username FROM user
                WHERE userID = ?
                """, (userID,))
    aux_db = res.fetchone()
    con.commit()
    return aux_db[0]

def database_constructor():
    """Creates all tables in database if not app directory
    """    
    if os.path.exists('twitterReloaded.db'):
        # User table
        cur.execute(
        "CREATE TABLE IF NOT EXISTS user(userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, joinDate TIMESTAMP)")

        # Telemetry table
        cur.execute(
            "CREATE TABLE IF NOT EXISTS telemetry(userID INTEGER NOT NULL, date TIMESTAMP NOT NULL, FOREIGN KEY (userID) REFERENCES user (userID))")

        # Tweet table
        cur.execute("CREATE TABLE IF NOT EXISTS tweet(tweetID INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER NOT NULL, date TIMESTAMP NOT NULL, tweet TEXT NOT NULL, FOREIGN KEY (userID) REFERENCES user (userID))")

        # Reply table
        cur.execute("CREATE TABLE IF NOT EXISTS reply(tweetID INTEGER NOT NULL, userID INTEGER NOT NULL, reply TEXT NOT NULL, date TIMESTAMP NOT NULL, FOREIGN KEY (tweetID) REFERENCES tweet (tweetID), FOREIGN KEY (userID) REFERENCES user (userID))")

        con.commit()

####################
# LOGIN FUNCTIONS  #
####################

def lookup_by_username(user_input):
    """Looks up given username in database

    Args:
        user_input (str): Username that will be looked up in database

    Returns:
        bool, tuple<int, str>: Bool : If username is in the database, tuple : (userID, username)
    """    
    res = cur.execute("""
                      SELECT userID, username FROM user
                      WHERE username = ?
                      """, (user_input,))
    # aux_db = (userID, username)
    aux_db = res.fetchone()
    con.commit()
    
    if aux_db != None:
        return True, aux_db
    else:
        return False, aux_db
    
def password_match(user_input, username):
    """Checks if password given matches the one on the database

    Args:
        user_input (str): Password that will be matched with one in the database
        username (str): Username of the user trying to log in

    Returns:
        bool, tuple<str>: bool: if passwords matched, tuple : password from the database
    """    
    res = cur.execute("""
                        SELECT password FROM user
                        WHERE username = ?
                        """, (username,))
    aux_db = res.fetchone()
    con.commit()
    if user_input == aux_db[0]:
        return True, aux_db
    else:
        return False, aux_db
