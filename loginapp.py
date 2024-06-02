'''simple login manager project that connects with mysql database. User can create username and password. Script checks if username is already in use in database
and if it is not in use - creates new user and updates database. User can then log in.'''

import PySimpleGUI as sg
from mysql.connector import connect, Error
from getpass import getpass

try:
    with connect( #connecting to database
        host="localhost", 
        user=input("Enter username: "), #username - root
        password=getpass("Enter password: "), #getpass - safe to type in
        database="python" #connects (uses) database
    ) as connection:
        

    #list of usernames and dictionary of usernames&passwords
        list_of_usernames = []
        dict_of_usernames_and_passwords = {}
        check_user_availability = "SELECT * FROM users"
        with connection.cursor() as cursor:
            cursor.execute(check_user_availability) #checking for usernames in database
            for i in cursor.fetchall(): #fetchall returns are tuples [(1, 'login', 'password'), ...]
                list_of_usernames.append(i[1]) #creating a list of usernames, i[2] returns username
                dict_of_usernames_and_passwords[i[1]] = i[2]



        #starting window
        layout = [[sg.Text("What do you want to do?")],
          [sg.Button('Log in')],
          [sg.Button('Register')]]
        window = sg.Window('Python login manager', layout)
        event, values = window.read() #read() triggers the window with chosen text and buttons
        
        #window if u press 'Log in'
        window.close()
        if event == 'Log in': #event represents which button had been pressed
            layout2 = [[sg.Text("Please enter your username and password")], #layout2 for second window and further actions
                      [sg.Input('Username')],
                      [sg.Input('Password')],
                      [sg.Button('Submit')]]
            window = sg.Window('Python login manager', layout2) #to actually login users data has to be found in database
            event,values = window.read()

            #window if u logged in successfully
            if (values[0], values[1]) in dict_of_usernames_and_passwords.items(): #username and password have to match record in database
                window.close()
                layout = [[sg.Text(f"Welcome home {values[0]}, thanks for playing the game!")],
                          [sg.Button('Good game, well played!')],
                          [sg.Button('Bad game')]]
                window = sg.Window('Python login manager', layout)
                event,values = window.read()

            else:
                window.close()
                layout = [[sg.Text(f"Nice try! Keep trying")]]
                window = sg.Window('Python login manager', layout)
                event,values = window.read()

                if event != 0:
                    window.close()
        
        #window if you choose 'Register'
        elif event == 'Register':
            window.close() 
            layout2 = [[sg.Text("Please submit your desired username and password")],
                       [sg.Input('Username')],
                       [sg.Input('Password')],
                       [sg.Input('Confirm password')],
                       [sg.Button('Submit')]]
            window = sg.Window('Python login manager', layout2)
            event,values = window.read()
            
            #window if passwords don't match
            while values[1] != values[2]: #if given passwords don't match, client has to repeat the action.
                window.close()
                layout3 = [[sg.Text("Passwords must be the same")],
                       [sg.Input(values[0])],
                       [sg.Input(values[1])],
                       [sg.Input('Confirm password')],
                       [sg.Button('Submit')]]
                window = sg.Window('Python login manager', layout3)
                event,values = window.read()

            #window if username is already taken
            while values[0] in list_of_usernames: #repeat the loop until desired username is not already in use (in db)
                window.close() #close previous window
                layout3 = [[sg.Text("Username is already in use")], 
                   [sg.Input(values[0])],
                   [sg.Input(values[1])],
                   [sg.Input(values[1])],
                   [sg.Button('Submit')]]
                window = sg.Window('Python login manager', layout3)
                event,values = window.read()


            #Registration succeed
            insert_user_query=f"INSERT INTO users (login, password) VALUES('{values[0]}', '{values[1]}');"
            with connection.cursor() as cursor: #A query that needs to be executed is sent to cursor.execute() in string format.
                cursor.execute(insert_user_query) 
                connection.commit() #have to commit to perform any modification
            print('USER REGISTERED SUCCESSFULLY')

        
except Error as e:
    print(e)
