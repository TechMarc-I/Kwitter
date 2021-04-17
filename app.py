from flask import Flask, render_template, request
import psycopg2, hashlib, os

app = Flask(__name__)
con = psycopg2.connect(database="kwitter", user="akesh201", password="Matlock",
host ="127.0.0.1", port="5432")
print("hey it actually worked")

@app.route('/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s""", (username,))    #find any accounts with the same username
        account = cur.fetchone()
        if account:
            print('Account already exists')
        else:
            salt = os.urandom(32)   #Generate random salt
            password = hashlib.sha3_512(request.form['password'].encode('utf-8') + salt).hexdigest()    #Retrieve password, and hash password and salt
            cur.execute("""INSERT INTO users VALUES (%s, %s, %s)""", (username, password, salt))    #Store username, password, and salt
            con.commit()    #Commit changes to the database
            return render_template('/home.html')

    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug = True)
