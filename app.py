##pull test
##push test
##push test 2
from flask import Flask, render_template, request, make_response, redirect
import psycopg2, hashlib, os



app = Flask(__name__)

con = psycopg2.connect(database="kwitter", user="troyalfelt", password="Matlock",
host ="127.0.0.1", port="5432")


print("hey it actually worked")

class Post:
    def __init__(self, id_num, usr, post_con):
        self.id_num = id_num
        self.usr = usr
        self.post_con = post_con

@app.route('/')
def home():
    usr = request.cookies.get('name')
    print(usr)
    return redirect('/home')

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
        if account:
            print('Account already exists')
        elif password == confirm:
            cur.execute("""INSERT INTO users(user_name, password, email) VALUES (%s, %s, %s)""", (username, password, email))
            con.commit()
            print("Success!")
            res = make_response(redirect('/cookie'))
            res.set_cookie('name', username, max_age = 60*60*1200)
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
        password = request.form['password']
        cur = con.cursor()
        cur.execute("""SELECT * FROM users WHERE user_name = %s AND password = %s""", (username, password))
        account = cur.fetchone()
        if account:
            print(username)
            res = make_response(redirect('/cookie'))
            res.set_cookie('name', username, max_age = 60*60*2*600)
            usr = request.cookies.get('name')
            print(usr)
            return res

        else:
            print("Incorrect username/password")

    return render_template('/login.html')

@app.route('/cookie')
def set_id():
    username = request.cookies.get('name')
    print(username)
    res = make_response(redirect('/home'))
    cur = con.cursor()
    cur.execute("""SELECT id FROM users WHERE user_name = %s""", (username,))
    str_id = str(cur.fetchone())
    id = str_id.strip("(,)")
    print(id)
    res.set_cookie('id', id, max_age = 60*60*120000)
    return res


@app.route('/logout')
def leave():
    res = make_response(redirect('/home'))
    res.set_cookie('name', '', expires=0)
    res.set_cookie('id', '', expires=0)
    return res

@app.route('/make_post', methods = ['POST'])
def pst():
    if request.method == "POST":
        if request.cookies.get('name') != None and request.cookies.get('id') != None:
            username = request.cookies.get('name')
            id = int(request.cookies.get('id'))
            print(id)
            post = request.form['post_space']
            cur = con.cursor()
            cur.execute("""INSERT INTO posts(id, user_name, post) VALUES(%s, %s, %s)""", (id, username, post))
            con.commit()
            print("frick yeah")
    return redirect('/home')

@app.route('/home')
def main():
    dict = []
    cur = con.cursor()
    cur.execute("""SELECT post FROM posts""")
    all_posts = cur.fetchall()
    for i in all_posts:
        cur.execute("""SELECT id FROM posts WHERE post = %s""", (i))
        id = cur.fetchone()
        cur.execute(""" SELECT user_name FROM posts WHERE post = %s""", (i))
        name = cur.fetchone()
        x = Post(id, name, i)
        dict.append(x)
    return render_template('/home.html', all_posts = all_posts, dict = dict)

@app.route('/delete/<post>', methods = ['POST'])
def remove(post):
    cur = con.cursor()
    cur.execute("""DELETE FROM posts WHERE post = %s""", (post,))
    con.commit()
    print("yeyeyeye")
    return redirect('/home')





if __name__ == '__main__':
    app.run(debug = True)
