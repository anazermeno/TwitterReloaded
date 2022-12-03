# TwitterReloaded

## ##TwitterReloaded

Twitter is a service that allows groups of friends, family and co-workers to communicate and stay in touch through quick and frequent messages.
People post Tweets, which can contain photos, videos, links, and text.

## ##HowDoesThisWorks

### How to run

```
python3 client.py

```

The useropenas the application, pushes the bottom of LOGIN and enters user and password, once the information is confirmed, the "Home Dashboard" opens, with the possibility of: View Tweets, Click on Tweets, Publish a Tweet, and Reply a Tweet.

# SOLID Practices
1. __Open Closed Principle__: System task are distributed in different functions, as can be seen in each of the report generators, all tasks have been split into their own function block.

2. __Interface Segregation Principle__: Because the system has been segregated, functions do not depend on each other, if we have an error we would know where the problem is and thanks to that we can fix it right away. The system splits interfaces that are large like the creation of a new account into smaller and more specific ones like a function for data validation for similar users, a correct password, if it is save correctly in the data base, and showing errors if necessary. 

3. __Substitution Principle__: Because the classes are substitutable for the parent class, ensuring that derived classes will and can be extended without changing the behavior of these classes. This helps us avoid changes that might be unexpected or with a wrong outcome.

4. __Single Responsibility Principle__: The classes are specifically considered to make an specific application or functionality, this states that a module is responsible for one action.

5. __Dependency Inversion Principle__: The code modules and functions are highly independent from each other and are meant to cover the defined functionality objectives without interfering with other segments of the program.

# Design patterns

1. __Behavioral- Iterator__: Inside our system, we can see this pattern applied because inside the  users_logged_today(): function we let the user choose to print to  the terminal or a text file the list of users that were logged in with their username and timestamp. The function fills the dict with the keys being dates and a list of the usernames that logged in that day. This pattern allows to extract the traversal behavior of a collection(the list) into a separate object so we can use it to print the list into terminal or inside a text file.

2. __Behavioral-Observer__: Inside our system we have a menu where the user can choose the option he/she wants to use. This choice allows the system to only display what the user wants, after the option is sent to all the events that are chained to this option so it can work perfectly. For example, if the option is to create a new tweet, this option asks the user what they want the tweet to say, checks for character limit, and saves the tweet in the database. 