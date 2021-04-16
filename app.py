##pull test
##push test
##push test 2
from flask import Flask, render_template, request, make_response
import psycopg2

app = Flask(__name__)
con = psycopg2.connect(database="kwitter", user="troyalfelt", password="Matlock",
host ="127.0.0.1", port="5432")
print("hey it actually worked")

@app.route('/create', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s""", (username,))
        account = cur.fetchone()
        if account:
            print('Account already exists')
        else:
            cur.execute("""INSERT INTO users VALUES (%s, %s)""", (username, password ))
            con.commit()
            return render_template('/home.html')

    return render_template('/index.html')

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s AND password = %s""", (username, password))
        account = cur.fetchone()
        if account:
            print('Success!')
            res = make_response(render_template('/home.html'))
            res.set_cookie('name', username, max_age = 60*60*2)
            return res

        else:
            var = make_response("Value of cookie is {}".format(request.cookies.get('name')))
            print(var)

    return render_template('/index.html')

@app.route('/home')
def getcookie():
    name = request.cookies.get('name')
    return '<h1>welcome '+name

@app.route('/logout')
def leave():
    res = make_response(render_template('index.html'))
    res.set_cookie('name', 'username', max_age=0)
    return res

if __name__ == '__main__':
    app.run(debug = True)

usr = request.cookies.get('name')
