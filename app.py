from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'
mysql = MySQL(app)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/registrati/", methods=["GET", "POST"])
def registrati():
    if request.method=='GET':
        return render_template("register.html")
    else:
        nome= request.form.get("nome", "None")
        cognome= request.form.get("cognome", "None")
        username= request.form.get("username", "None")
        password= request.form.get("password", "None")
        confirmPassword= request.form.get("confirmPassword", "None")

        if nome=="None" or cognome=="None" or username=="None" or password=="None" or confirmPassword=="None":
            return render_template("register.html")
        elif password!=confirmPassword:
            render_template("register.html")
    
        query="SELECT username FROM users WHERE username=%s"
        cursor=mysql.connection.cursor()
        cursor.execute(query,(username,))
        if cursor.fetchone():
            return render_template("register.html")
        
        query="INSERT INTO users(username,password,nome,cognome) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(username, generate_password_hash(password), nome, cognome))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("homepage"))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method=='GET':
        render_template("login.html")
    else:
        username= request.form.get("username", "None")
        password= request.form.get("password", "None")
        query="SELECT * FROM users WHERE username=%s AND password=%s"
        cursor=mysql.connection.cursor()
        cursor.execute(query,(username, password))
        if cursor.fetchone():
            return render_template("paginaLogin.html")
        







app.run(debug=True)
