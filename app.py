##pull test
##push test
##push test 2
from flask import Flask, render_template, request, make_response
import psycopg2, hashlib, os



app = Flask(__name__)
con = psycopg2.connect(database="kwitter", user="troyalfelt", password="Matlock",
host ="127.0.0.1", port="5432")
print("hey it actually worked")

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
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s""", (username,))
        account = cur.fetchone()
        if account:
            print('Account already exists')
        else:
            salt = os.urandom(32)   #Generate random salt
            password = hashlib.sha3_512(request.form['password'].encode('utf-8') + salt).hexdigest()
            cur.execute("""INSERT INTO users VALUES (%s, %s)""", (username, password, salt))
            con.commit()
            return render_template('/index.html')

    return render_template('/index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    usr = request.cookies.get('name')
    print(usr)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s AND password = %s""", (username, password))
        account = cur.fetchone()
        if account:
            print(username)
            res = make_response(render_template('/home.html'))
            res.set_cookie('name', username, max_age = 60*60*2*600)
            usr = request.cookies.get('name')
            print(usr)
            return res

        else:
            print("Incorrect username/password")

    return render_template('/login.html')

@app.route('/logout')
def leave():
    res = make_response(render_template('home.html'))
    res.set_cookie('name', '', expires=0)
    return res

@app.route('/home')
def main():
    return render_template('/home.html')



if __name__ == '__main__':
    app.run(debug = True)
