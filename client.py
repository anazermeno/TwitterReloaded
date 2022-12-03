import sqlite3 as sq
import datetime
from colorama import Fore, Style
from helperFunctions import *
from telemetryFunctions import *


# Globals
logged = None

# Database connection
con = sq.connect("twitterReloaded.db",
                 detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
cur = con.cursor()


def change_password(username):
    """Asks the user for a new password and updates the database.

    Args:
        username (str): username of the user changing passwords
    """    
    print(Fore.LIGHTBLUE_EX, end="")
    print("---Change password---" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX, end="")
    print("New password: " + Style.RESET_ALL)
    user_input = input()

    cur.execute("""
                UPDATE user SET password = ?
                WHERE username = ?
                """, (user_input, username))
    con.commit()


def login():
    """Asks user to give his username and password, checks for both.
    If username not found user is asked for it again.
    If password is not found gives the user 5 chances to get it right,
    then asks user if they want to change password or return to login screen.

    Returns:
        bool, int: user logged status, userID
    """    
    print(Fore.LIGHTBLUE_EX, end="")
    print("---Login---" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX, end="")
    print("Username: " + Style.RESET_ALL)
    print("@", end="")
    user_input = input()

    # Check if username is in database
    # aux_db = (userID, username)
    username_in_database, aux_db = lookup_by_username(user_input)
    
    # If aux_db has a length of 0, username was not found
    if username_in_database:

        # Save username for next querie
        userID, username = aux_db
        print(Fore.LIGHTGREEN_EX, end="")
        print("Password: " + Style.RESET_ALL)
        user_input = input()

        # Get the password for username
        # aux_db = (password)
        match_result, aux_db = password_match(user_input, username)

        # Check if password matches
        # Gives the user 5 chances to get the password right
        # If not user is asked if he wants to return to login menu or change password
        if match_result:
            return True, userID
        else:
            attempts = 5
            
            while True:
                print(Fore.LIGHTRED_EX, end="")
                print("Password does not match, try again" + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print("Password: " + Style.RESET_ALL)
                user_input = input()
                
                if user_input in aux_db: #TODO Se puede cambiar a la funcion, pero son mas acciones a la base de datos
                    return True, userID
                
                if attempts == 1:
                    print(Fore.LIGHTRED_EX, end="")
                    print("Too many attempts!" + Style.RESET_ALL)
                    print(Fore.LIGHTGREEN_EX, end="")
                    print("(1)Change password       (2)Login Screen\n" +
                        Style.RESET_ALL)
                    op = input()
                    
                    while True:
                        if menu_op_in_range(op, [1, 2]):
                            break
                        else:
                            clear_screen()
                            print(Fore.LIGHTRED_EX, end="")
                            print("Invalid menu option! Try again"  + Style.RESET_ALL)
                            print(Fore.LIGHTGREEN_EX, end="")
                            print("(1)Change password       (2)Login Screen\n" +
                                Style.RESET_ALL)
                            op = input()
                            
                    if op == '1':
                        change_password(username)
                        clear_screen()
                        return True, userID
                    elif op == '2':
                        clear_screen()
                        return False, ""
                    
                attempts -= 1
                
                print("")
                print(Fore.LIGHTYELLOW_EX, end="")
                print("Attempts remaining " + str(attempts) + Style.RESET_ALL)

    else:
        clear_screen()
        print(Fore.LIGHTRED_EX, end="")
        print("Username not found!"   + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print("(1)Try again     (2)Return to title screen" + Style.RESET_ALL)
        op = input()
        
        while True:
            if menu_op_in_range(op, [1, 2]):
                break
            else:
                clear_screen()
                print(Fore.LIGHTRED_EX, end="")
                print("Invalid menu option! Try again"  + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print("(1)Try again     (2)Return to title screen" + Style.RESET_ALL)
                op = input()
        
        if op == '1':
            clear_screen()
            logged, id = login()
            return logged, id
        elif op == '2':
            clear_screen()
            login_screen()


def register():
    """Asks user for username, checks if it exists in database, if it does ask user for a new one.
    Asks user for password.
    Save both username and password to the database.

    Returns:
        int: userID
    """    
    print(Fore.LIGHTBLUE_EX, end="")
    print('---Register---' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX, end="")
    print("New username: " + Style.RESET_ALL)
    username = input()
    
    # Queries database for the username the user wants to use
    res = cur.execute("""
                SELECT username FROM user
                WHERE username = ?
                """, (username,))
    aux_db = res.fetchone()
    con.commit()
    
    # While the username is found in the database, aux_db will be True and the user will loop until unique username
    while aux_db:
        clear_screen()
        print(Fore.LIGHTRED_EX, end="")
        print("Username '" + str(aux_db[0]) +
                "' already exists!" + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print("New username: " + Style.RESET_ALL)
        username = input()
        res = cur.execute("""
                SELECT username FROM user
                WHERE username = ?
                """, (username,))
        aux_db = res.fetchone()
        con.commit()

    print(Fore.LIGHTGREEN_EX, end="")
    print("New password: " + Style.RESET_ALL)
    password = input()

    # Add new user to the database
    cur.execute("""
                INSERT INTO user (username, password, joinDate)
                VALUES (?, ?, ?)
                """, (username, password, datetime.datetime.now()))
    con.commit()
    
    # Gets username of the new user and returns it for later use.
    res = cur.execute("""
                SELECT userID FROM user
                WHERE username = ?
                """, (username,))
    aux_db = res.fetchone()
    con.commit()
    
    return aux_db[0]


def daily_stats_screen():
    """displays menu for the telemetry functions, gives user the choise of going to either one of them.
    """
    op = 0
    while op != '4':
        clear_screen()
        print(Fore.LIGHTBLUE_EX, end="")
        print("---Daily Stats---" + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print("(1) Number of users logged")
        print("(2) User with most events")
        print("(3) Most replied tweet")
        print("(4) Back" + Style.RESET_ALL)
        op = input()
        
        while True:
            if menu_op_in_range(op, [1, 2, 3, 4]):
                break
            else:
                clear_screen()
                print(Fore.LIGHTRED_EX, end="")
                print("Invalid menu option! Try again"  + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print("(1) Number of users logged")
                print("(2) User with most events")
                print("(3) Most replied tweet")
                print("(4) Back" + Style.RESET_ALL)
                op = input()
        
        if op == '1':
            clear_screen()
            users_logged_today()
        elif op == '2':
            clear_screen()
            user_most_events()
        elif op == '3':
            clear_screen()
            most_replied_tweet()
            
    return


def login_screen():
    """Start screen, gives user the choise to log in, register or see daily stats

    Returns:
        bool, int: User logged state and the user's ID
    """
    print(Fore.LIGHTBLUE_EX, end="")
    print("---Twitter Reloaded---" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX, end="")
    print("(1)LOGIN     (2)REGISTER     (3)Daily Stats      (4)EXIT" + Style.RESET_ALL)
    op = input()
    
    while True:
        if menu_op_in_range(op, [1, 2, 3, 4]):
            break
        else:
            clear_screen()
            print(Fore.LIGHTRED_EX, end="")
            print("Invalid menu option! Try again"  + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print("(1)LOGIN     (2)REGISTER     (3)Daily Stats      (4)EXIT" + Style.RESET_ALL)
            op = input()
    
    if op == '1':
        clear_screen()
        logged, userID = login()
        return logged, userID
    elif op == '2':
        clear_screen()
        userID = register()
        return True, userID
    elif op == '3':
        clear_screen()
        daily_stats_screen()
        main()
    elif op == '4':
        clear_screen()
        exit()


def new_tweet(userID):
    """Asks the user what they want the tweet to say, checks for character limit, and saves the tweet in the database

    Args:
        userID (int): Current user's ID
    """    
    print(Fore.LIGHTBLUE_EX, end="")
    print('---New tweet---' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX, end="")
    print("What's happening?" + Style.RESET_ALL)
    user_input = input()
    
    while len(user_input) > 300:
        print(Fore.LIGHTRED_EX, end="")
        print('\nTweet is too long, ' +
              str(len(user_input)) + ' chars' + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX, end="")
        print("What's happening? (but shorter)" + Style.RESET_ALL)
        user_input = input()
        
    curr_date = datetime.datetime.now()
    cur.execute("""
                INSERT INTO tweet (userID, date, tweet)
                VALUES (?, ?, ?)
                """, (userID, curr_date, user_input))
    con.commit()


def new_reply(tweetID, username, userID):
    """User is asked what they want on the reply, checks for character limit and saves to database,

    Args:
        tweetID (int): ID from the tweet the user is replying to.
        username (str): Username of the tweet's author.
        userID (int): ID of the reply's author.
    """    
    print(Fore.LIGHTBLUE_EX, end="")
    print("---Reply to @" + username + "---" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX, end="")
    print("Tweet your reply: " + Style.RESET_ALL)
    user_input = input()
    
    while len(user_input) > 300:
        print(Fore.LIGHTRED_EX, end="")
        print('\nReply is too long, ' +
              str(len(user_input)) + ' chars' + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX, end="")
        print("Tweet your reply: (but shorter)" + Style.RESET_ALL)
        user_input = input()
        
    curr_date = datetime.datetime.now()
    cur.execute("""
                INSERT INTO reply (tweetID, userID, reply, date)
                VALUES (?, ?, ?, ?)
                """, (tweetID, userID, user_input, curr_date))
    con.commit()


def show_replies(tweetID):
    """Prints the 10 newest replies to a tweet

    Args:
        tweetID (int): Tweet ID that is linked to the replies
    """    
    res = cur.execute("""
                SELECT userID, reply, date '[timestamp]' FROM reply
                WHERE tweetID = ?
                LIMIT 10
                """, (tweetID,))
    aux_db = res.fetchall()
    con.commit()
    
    # Displays 10 replies
    # date.strftime("%x") + ' ' + date.strftime("%X") is used for datetime formating, output mm/dd/yyyy hh:mm:ss
    for reply in aux_db:
        username = find_user(reply[0])
        reply_text = reply[1]
        date = reply[2]
        print(Fore.LIGHTCYAN_EX, end="")
        print('-----------------------' + Style.RESET_ALL)
        print('@' + username + '\t\t' +
              date.strftime("%x") + ' ' + date.strftime("%X"))
        print(reply_text)
        print(Fore.LIGHTCYAN_EX, end="")
        print('-----------------------' + Style.RESET_ALL)


def show_thread(tweet_info, userID):
    """Prints tweet and gives the option to reply or go back to the dashboard

    Args:
        tweet_info (list): [username, date, tweetID, tweet_text]
        userID (int): Current user's ID
    """    
    clear_screen()
    username = find_user(tweet_info[0])
    date = tweet_info[1]
    tweetID = tweet_info[2]
    tweet_text = tweet_info[3]
    
    # date.strftime("%x") + ' ' + date.strftime("%X") is used for datetime formating, output mm/dd/yyyy hh:mm:ss
    print(Fore.LIGHTBLUE_EX, end="")
    print("---Tweet thread---" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX, end="")
    print('-----------------------' + Style.RESET_ALL)
    print('@' + username + '\t\t' +
          date.strftime("%x") + ' ' + date.strftime("%X"))
    print(tweet_text)
    print(Fore.LIGHTCYAN_EX, end="")
    print('-----------------------' + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX, end="")
    print('\n--Replies--' + Style.RESET_ALL)
    
    show_replies(tweetID)
    
    print(Fore.LIGHTGREEN_EX, end="")
    print('\n(1)Reply       (2)Back' + Style.RESET_ALL)
    op = input()
    
    while True:
        if menu_op_in_range(op, [1, 2]):
            break
        else:
            clear_screen()
            print(Fore.LIGHTRED_EX, end="")
            print("Invalid menu option! Try again"  + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('(1)Reply       (2)Back' + Style.RESET_ALL)
            op = input()
    
    if op == '1':
        clear_screen()
        new_reply(tweetID, username, userID)
        return
    elif op == '2':
        clear_screen()
        pass


def show_tweets(userID):
    """Prints 10 newest tweets, gives the option to open the thread of each one

    Args:
        userID (int): Current user's ID
    """    
    print(Fore.LIGHTBLUE_EX, end="")
    print('---Lattest tweets---' + Style.RESET_ALL)
    res = cur.execute("""
                SELECT userID, date '[timestamp]', tweetID, tweet FROM tweet
                ORDER BY tweetID DESC
                LIMIT 10
                """)
    aux_db = res.fetchall()
    con.commit()
    
    count = 1
    for tweet in aux_db:
        username = find_user(tweet[0])
        date = tweet[1]
        tweet_text = tweet[3]
        
        # date.strftime("%x") + ' ' + date.strftime("%X") is used for datetime formating, output mm/dd/yyyy hh:mm:ss
        print(Fore.LIGHTCYAN_EX, end="")
        print('-----------------------' + Style.RESET_ALL)
        print('(' + str(count) + ')')
        print('@' + username + '\t\t' +
              date.strftime("%x") + ' ' + date.strftime("%X"))
        print(tweet_text)
        print(Fore.LIGHTCYAN_EX, end="")
        print('-----------------------' + Style.RESET_ALL)
        count += 1
        
    print(Fore.LIGHTGREEN_EX, end="")
    print('(X)Select tweet      (0)Back' + Style.RESET_ALL)
    op = input()
    
    while True:
        if menu_op_in_range(op, list(range(1, len(aux_db) + 1)) + [0]):
            break
        else:
            clear_screen()
            print(Fore.LIGHTRED_EX, end="")
            print("Invalid menu option! Try again"  + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('(X)Select tweet      (0)Back' + Style.RESET_ALL)
            op = input()
    
    if op == '0':
        return
    
    show_thread(aux_db[int(op) - 1], userID)
    show_tweets(userID)


def dashboard(userID):
    """Dashboard Menu, gives option to write new tweet, view tweets or exit the app. Calls logged_telemetry

    Args:
        userID (int): Current user's ID
    """    
    # Saves user login time to database 
    logged_telemetry(userID)
    
    op = 0
    while op != '3':
        clear_screen()
        print(Fore.LIGHTBLUE_EX, end="")
        print('---Dashboard---' + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print('(1)New tweet     (2)View tweets      (3)EXIT' + Style.RESET_ALL)
        op = input()
        
        while True:
            if menu_op_in_range(op, [1, 2, 3]):
                break
            else:
                clear_screen()
                print(Fore.LIGHTRED_EX, end="")
                print("Invalid menu option! Try again"  + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print('(1)New tweet     (2)View tweets      (3)EXIT' + Style.RESET_ALL)
                op = input()
    
        
        if op == '1':
            clear_screen()
            new_tweet(userID)
        elif op == '2':
            clear_screen()
            show_tweets(userID)
            
    clear_screen()
    exit()


def main():
    """Main program call, starts the app
    """    
    database_constructor()
    
    clear_screen()
    
    logged = False
    
    while not logged:
        logged, username = login_screen()
        
    dashboard(username)


# START
main()
