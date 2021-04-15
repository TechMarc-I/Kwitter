##pull test

from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
con = psycopg2.connect(database="kwitter", user="troyalfelt", password="Matlock",
host ="127.0.0.1", port="5432")
print("hey it actually worked")

@app.route('/', methods = ['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug = True)
