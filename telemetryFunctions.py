import sqlite3 as sq
from helperFunctions import clear_screen, today, menu_op_in_range
from colorama import Fore, Style

# Database connection
con = sq.connect("twitterReloaded.db",
                 detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
cur = con.cursor()

def users_logged_today():
    """Telemetry function
    Gives user the choise to print to terminal or to a text file.
    Prints how many unique users logged in today and their usernames.
    """    
    op = 0
    
    while op != '3':
        res = cur.execute("""SELECT username, date '[timestamp]' FROM telemetry
                      INNER JOIN user
                      ON telemetry.userID = user.userID
                      """)
        aux_db = res.fetchall()
        con.commit()
        
        by_dates = {} # {date: [username]}
        
        # Fills the dict with the keys being dates and a list of the usernames that logged in that day
        for row in aux_db:
            if not (row[1].date() in by_dates):
                by_dates[row[1].date()] = [row[0]]
            else:
                by_dates[row[1].date()] += [row[0]]

        clear_screen()
        
        if not today() in by_dates:
            print(Fore.LIGHTBLUE_EX, end="")
            print("---Number of users logged today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("No logins today :(" + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            return
        
        
        print(Fore.LIGHTBLUE_EX, end="")
        print("---Number of users logged today---" + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print("(1)Show in app        (2)Print to file        (3)Back" + Style.RESET_ALL)
        op = input()
        
        while True:
            if menu_op_in_range(op, [1, 2, 3]):
                break
            else:
                clear_screen()
                print(Fore.LIGHTRED_EX, end="")
                print("Invalid menu option! Try again"  + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print("(1)Show in app        (2)Print to file        (3)Back" + Style.RESET_ALL)
                op = input()
        
        if op == '1':
            clear_screen()
            print(Fore.LIGHTBLUE_EX, end="")
            print("---Number of users logged today---" + Style.RESET_ALL)
            
            aux_list = []
            
            # Filters dict for todays date and gets the unique usernames from the values
            for item in by_dates[today()]:
                if not (item in aux_list):
                    aux_list.append(item)
                    
            print(Fore.LIGHTMAGENTA_EX, end="")
            print('Number of unique users logged in today: ' + Style.RESET_ALL +
                  str(len(aux_list)) + '\n')
            
            print(Fore.LIGHTMAGENTA_EX, end="")
            print('Users looged in today:' + Style.RESET_ALL)
            
            for item in aux_list:
                if item == aux_list[-1]:
                    print(item)
                else:
                    print(item, end=', ')
                    
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            
        elif op == '2':
            clear_screen()
            
            f = open('loggedUsersToday.txt', 'w')
            
            f.write("---Number of users logged today---\n")
            aux_list = []
            
            for item in by_dates[today()]:
                if not (item in aux_list):
                    aux_list.append(item)
                    
            f.write('Number of unique users logged in today: ' +
                    str(len(aux_list)) + '\n')
            f.write('Users looged in today:\n')
            
            for item in aux_list:
                if item == aux_list[-1]:
                    f.write(item)
                else:
                    f.write(item + ', ')
                    
            f.close()
            
            print(Fore.LIGHTBLUE_EX, end="")
            print("---Number of users logged today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print('File created!')
            print('The file is called "loggedUsersToday.txt"' + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            
    clear_screen()
    return


def user_most_events():
    """Telemetry Function
    Gives user the choise to print to terminal or to a text file.
    Prints username of who had most events today, number of tweets, number of replies, tweets and replies written today.
    """    
    op = 0
    while op != '3':
        res = cur.execute("""SELECT username, tweet, date '[timestamp]' FROM tweet
                                INNER JOIN user
                                ON tweet.userID = user.userID
                                """)
        tweet_aux_db = res.fetchall()
        con.commit()

        res = cur.execute("""SELECT username, reply, date '[timestamp]' FROM reply
                             INNER JOIN user
                             ON reply.userID = user.userID
                             """)
        reply_aux_db = res.fetchall()
        con.commit()

        by_user = {}  # {username: [[tweets], [replies]]}

        # Fills by_user dict as shown above
        for row in tweet_aux_db:
            if row[2].date() == today():
                if not (row[0] in by_user):
                    by_user[row[0]] = [[row[1]], []]
                else:
                    by_user[row[0]][0] += [row[1]]

        for row in reply_aux_db:
            if row[2].date() == today():
                if not (row[0] in by_user):
                    by_user[row[0]] = [[], [row[1]]]
                else:
                    by_user[row[0]][1] += [row[1]]

        # If there is no tweet or replies today displays message and returns user to telemety menu
        if not by_user:
            print(Fore.LIGHTBLUE_EX, end="")
            print("---User with most events today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("No tweets or replies today :(" + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            return

        # Lambda function to get the user with most event (tweets and replies) today
        # Return the username and events matrix [[tweets], [replies]]
        user, events = max(by_user.items(), key=lambda x: len(set(x[1][0])) + len(set(x[1][1])))

        clear_screen()
        print(Fore.LIGHTBLUE_EX, end="")
        print("---User with most events today---" + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print("(1)Show in app        (2)Print to file        (3)Back" + Style.RESET_ALL)
        op = input()
        
        while True:
            if menu_op_in_range(op, [1, 2, 3]):
                break
            else:
                clear_screen()
                print(Fore.LIGHTRED_EX, end="")
                print("Invalid menu option! Try again"  + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print("(1)Show in app        (2)Print to file        (3)Back" + Style.RESET_ALL)
                op = input()
        
        if op == '1':
            clear_screen()
            print(Fore.LIGHTBLUE_EX, end="")
            print("---User with most events today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("User with most events today is:" + Style.RESET_ALL)
            print("@" + user + "\n")
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("Number of tweets today: " + Style.RESET_ALL)
            print(str(len(events[0])) + "\n")
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("Number of replies today: " + Style.RESET_ALL)
            print(str(len(events[1])) + "\n")
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("Total events today: " + Style.RESET_ALL)
            print(str(len(events[0]) + len(events[1])) + "\n")
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("Tweets today (up to 5):" + Style.RESET_ALL)
            count = 0
            
            if not events[0]:
                print(Fore.LIGHTMAGENTA_EX, end="")
                print("No tweets today" + Style.RESET_ALL)
            else:
                for tweet in events[0]:
                    if count == 4:
                        break
                    print('"' + tweet + '"')
                    count += 1
            
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("\nReplies today (up tp 5):" + Style.RESET_ALL)
            count = 0
            if not events[1]:
                print(Fore.LIGHTMAGENTA_EX, end="")
                print("No replies today")
            else:
                for reply in events[1]:
                    if count == 4:
                        break
                    print('"' + reply + '"')
                    count += 1
                    
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()

        elif op == '2':
            f = open("userWithMostEvents.txt", "w")
            f.write("---User with most events today---" + "\n")
            f.write("User with most events today is:" + "\n")
            f.write("@" + user + "\n\n")
            f.write("Number of tweets today: " + "\n")
            f.write(str(len(events[0])) + "\n\n")
            f.write("Number of replies today: " + "\n")
            f.write(str(len(events[1])) + "\n\n")
            f.write("Total events today: \n")
            f.write(str(len(events[0]) + len(events[1])) + "\n\n")
            f.write("Tweets today (up to 5):" + "\n")
            count = 0
            if not events[0]:
                f.write("No tweets today" + "\n")
            else:
                for tweet in events[0]:
                    if count == 4:
                        break
                    f.write('"' + tweet + '"' + "\n")
                    count += 1

            f.write("\nReplies today (up tp 5):" + "\n")
            count = 0
            if not events[1]:
                f.write("No replies today" + "\n")
            else:
                for reply in events[1]:
                    if count == 4:
                        break
                    f.write('"' + reply + '"' + "\n")
                    count += 1

            f.close()
            
            clear_screen()
            print(Fore.LIGHTBLUE_EX, end="")
            print("---User with most events today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print('File created!')
            print('The file is called "loggedUsersToday.txt"'+ Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            
    return

def most_replied_tweet():
    """Telemetry function
    Gives user the choise to print to terminal or to a text file.
    Prints the most replied tweet today, the number of replies and the replies.
    """    
    op = 0
    while op != '3':
        res = cur.execute("""SELECT B.username, C.tweet, A.reply, A.date '[timestamp]' FROM reply A
                            INNER JOIN user B
                            ON B.userID = A.userID
                            INNER JOIN tweet C
                            ON C.tweetID = A.tweetID
                        """)
        aux_db = res.fetchall()
        con.commit()
        
        by_dates = {}  # {tweet: [replies]}

        # Fills by_dates dict as shown above
        for row in aux_db:
            if row[3].date() == today():
                if not (row[1] in by_dates):
                    by_dates[row[1]] = [row[2]]
                else:
                    by_dates[row[1]] += [row[2]]

        """
        We where thinking of adding extra functionality to 
        for row in aux_db:
            if not (row[3].date() in by_dates):
                by_dates[row[3].date()] = []
                if not (row[1] in by_dates[row[3].date()]):
                    aux_dict = {row[1]: [row[2]]}
                    by_dates[row[3].date()] = aux_dict
                else:
                    by_dates[row[3].date()][row[1]] += [row[2]]
            else:
                if not (row[1] in by_dates[row[3].date()]):
                    by_dates[row[3].date()][row[1]] = [row[2]]
                else:
                    by_dates[row[3].date()][row[1]] += [row[2]]
        """
        
        if not by_dates:
            print(Fore.LIGHTBLUE_EX, end="")
            print("---Most replied tweet today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("No replies today :(" + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            return
        
        # Lamda function that finds the tweet with most replies in the by_date dict
        # Return the tweet and list of replies
        tweet, replies = max(by_dates.items(), key=lambda x: len(set(x[1])))
        
        clear_screen()
        print(Fore.LIGHTBLUE_EX, end="")
        print("---Most replied tweet today---" + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX, end="")
        print("(1)Show in app        (2)Print to file        (3)Back" + Style.RESET_ALL)
        op = input()
        
        while True:
            if menu_op_in_range(op, [1, 2, 3]):
                break
            else:
                clear_screen()
                print(Fore.LIGHTRED_EX, end="")
                print("Invalid menu option! Try again"  + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX, end="")
                print("(1)Show in app        (2)Print to file        (3)Back" + Style.RESET_ALL)
                op = input()

        if op == '1':
            clear_screen()
            print(Fore.LIGHTBLUE_EX, end="")
            print("---Most replied tweet today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("The tweet with most replies today is: " + Style.RESET_ALL)
            print('"' + tweet + '"' + '\n')
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("The number of replies is: " + Style.RESET_ALL)
            print(str(len(replies)) + '\n')
            print(Fore.LIGHTMAGENTA_EX, end="")
            print("The replies to the tweet (up to 10):" + Style.RESET_ALL)
            
            count = 0
            for reply in replies:
                if count == 10:
                    break
                print('"' + reply + '"')
                count += 1
                
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
            
        elif op == '2':
            clear_screen()
            f = open('mostRepliedTweet.txt', 'w')

            f.write("---Most replied tweet today---" + '\n')
            f.write("The tweet with most replies today is:\n")
            f.write('"' + tweet + '"\n\n')
            f.write("The number of replies is:\n")
            f.write(str(len(replies)) + '\n\n')
            f.write("The replies to the tweet:\n")
            
            for reply in replies:
                f.write('"' + reply + '"')
                f.write('\n')

            f.close()
            
            print(Fore.LIGHTBLUE_EX, end="")
            print("---Most replied tweet today---" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX, end="")
            print('File created!')
            print('The file is called "mostRepliedTweet.txt"' + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX, end="")
            print('\nHit any key to return' + Style.RESET_ALL)
            input()
    return

