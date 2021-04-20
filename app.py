from flask import Flask, render_template, request
from validate_email import validate_email
import psycopg2, hashlib, os

app = Flask(__name__)
con = psycopg2.connect(database="kwitter", user="akesh201", password="Matlock",
host ="127.0.0.1", port="5432")

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        cur = con.cursor()
        cur.execute("""SELECT password FROM users WHERE user_name = %s""", (username,))
        password = cur.fetchone()
        print(password)
        if hashlib.sha3_512(request.form['password'].encode('utf-8')).hexdigest() == ''.join(password):
            print("Successfully logged in")
        else:
            print("Wrong username or password")
        
    return render_template('home.html')
            
@app.route('/create', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s""", (username,))    #find any accounts with the same username
        account = cur.fetchone()
        cur.execute("""SELECT FROM users WHERE email = %s""", (email,))
        email_used = cur.fetchone()
        if account:
            print('Account already exists')
        elif not validate_email(email, check_mx=True):
            print('Invalid email address')
        elif email_used:
            print('Email address already in use')
        else:
            salt = os.urandom(32)   #Generate random salt
            print(salt)
            password = hashlib.sha3_512(request.form['password'].encode('utf-8')).hexdigest()    #Retrieve password, and hash password and salt
            cur.execute("""INSERT INTO users VALUES (%s, %s, %s)""", (username, password, email))    #Store username, password, salt, and email
            con.commit()    #Commit changes to the database
            return render_template('/home.html')

    return render_template('/index.html')



if __name__ == '__main__':
    app.run(debug = True)
