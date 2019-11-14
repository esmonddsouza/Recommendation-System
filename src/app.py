from flask import Flask, render_template, request, redirect, url_for, session
import database as dp
from datetime import datetime
import secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

database = dp.Database()
conn = database.createConnection()
database.createTables(conn)
genre=database.readGenre(conn)
genre_ID=database.readGenreID(conn)

def calculateAge(birthDate):
    today = datetime.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


@app.route('/')
def hello():
    return render_template("login-page.html")


@app.route('/registration')
def reg():
    return render_template("registration-page.html")


@app.route('/hello', methods=['POST'])
def register():
    if request.method == 'POST':

        req = request.form

        username = req.get('username')
        password = req.get('password')

        if username:
            session["USERNAME"] = username
            session["USER_ID"] = database.readUser(conn, username)
            #return render_template('home-page.html', username = username)
            return render_template('home-page.html')
        
        else:
            return render_template('login-page.html')


@app.route('/registered', methods=['POST'])
def welcome():

    req = request.form

    user = req.get('username')
    password = req.get('password')
    gender = req.get('gender')
    #nationality = request.form['nationality']
    #email = request.form['email']
    dob = req.get('DOB')
    # if the user is adult or not
    adult = False
    if calculateAge(datetime.strptime(dob, '%Y-%m-%d')) > 18:
        adult = True

    # connection
    database = dp.Database()

    con = database.createConnection()
    database.createTables(con)
    database.inputUser(con, user, password, adult)
    username = database.readUser(con, user)
    session["USERNAME"] = user
    #session["USER_ID"] = dp.Database.readUser(conn = conn, username = session.get("USERNAME"))
    session["USER_ID"] = username
    return render_template('welcome-page.html', username=user,genrename=genre,genreid=genre_ID)

@app.route('/genre_page',methods=['POST'])
def genre_section():
    #user = request.form['username']
    con_genre = database.createConnection()
    #database.createTables(con_genre)s
    checkboxes=request.form.getlist('check')
    test_arr=[]
    genre_name=[]
    total_genres=len(checkboxes)
    percent=[]
    i=0
    for check in checkboxes:
        test_arr.append(str(check))
        percent.append(round((100/total_genres),2))
        print(test_arr)
        #id=database.readGenreID(con_genre,test_arr[i])
        print(session)
        database.input_preferences(conn = con_genre, username = session.get("USER_ID")[-1], genre = test_arr[i], percent = percent[i])
        i=i+1
    #print(user_set)
    return render_template('home-page.html')

    
@app.route('/check_user', methods=['POST'])
def print_user_details():
    if request.method == 'POST':
        if request.form['username'] != "":
            username = request.form['username']
            password = request.form['password']
        return render_template('user_home.html', username=username, password=password)


if __name__ == '__main__':
    app.run()