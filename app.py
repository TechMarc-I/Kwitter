from flask import Flask, render_template, request, make_response, redirect
from validate_email import validate_email
import psycopg2, hashlib, os



app = Flask(__name__)
con = psycopg2.connect(database="kwitter", user="akesh201", password="Matlock",
host ="127.0.0.1", port="5432")

pepper = r'e_XT<tUB%"Gg4F\or57i{^&MAcAaiH@-z|T&y3w8#HTcp~8GcS9K{Y&x?ZC_dxi}*m<T0sr{in\"SDf2\_\6$*{gqe>E2yDZ]}XJ'

@app.route('/')
def home():
    usr = request.cookies.get('name')
    print(usr)
    return render_template('/home.html')

@app.route('/create', methods = ['GET', 'POST'])
def register():
    usr = request.cookies.get('name')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm = request.form['confirm']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s""", (username,))
        account = cur.fetchone()
        cur.execute("""SELECT FROM users WHERE email = %s""", (email,))
        email_used = cur.fetchone()
        if account:
            print('Account already exists')
        elif not validate_email(email, check_mx=True):
            print('Invalid email address')
        elif email_used:
            print('Email address already in use')

        elif password == confirm:
            salt = os.urandom(32)   #Generate random salt
            s = ""
            for i in salt:
                s += str(i)
            salt = s

            password = hashlib.sha256((request.form['password'] + salt + pepper).encode('utf-8')).hexdigest()   #Retrieve password, and hash password and salt
            cur.execute("""INSERT INTO users VALUES (%s, %s, %s, %s)""", (username, password, email, salt))    #Store username, password, salt, and email
            con.commit()    #Commit changes to the database
            print("Success!")
            res = make_response(redirect('/login'))
            res.set_cookie('name', username, max_age = 60&60*1200)
            return res
        else:
            print("Password does not match confirmation, please try again.")


    return render_template('/create.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    usr = request.cookies.get('name')
    print(usr)
    if request.method == 'POST':
        username = request.form['username']
        cur = con.cursor()
        cur.execute("""SELECT user_name, password, salt FROM users WHERE user_name = %s OR email = %s""", (username, username))
        user_info = cur.fetchall()
        if user_info:
            username = user_info[0][0]
            password = user_info[0][1]
            salt = user_info[0][2]
        else:
            username = None
            password = None
            salt = None

        if password and password == hashlib.sha256((request.form['password'] + salt + pepper).encode('utf-8')).hexdigest():
            print(username)
            res = make_response(redirect('/home'))
            res.set_cookie('name', username, max_age = 60*60*2*600)
            usr = request.cookies.get('name')
            print(usr)
            return res
        else:
            print("Incorrect username/password")

    return render_template('/index.html')

@app.route('/logout')
def leave():
    res = make_response(redirect('/login'))
    res.set_cookie('name', '', expires=0)
    return res

@app.route('/home')
def main():
    print(request.cookies.get('name'))
    return render_template('/home.html')

if __name__ == '__main__':
    app.run(debug = True)
