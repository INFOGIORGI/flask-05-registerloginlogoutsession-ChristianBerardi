from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

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
        nome= request.form.get("nome")
        cognome= request.form.get("cognome")
        username= request.form.get("username")
        password= request.form.get("password")
        confirmPassword= request.form.get("confirmPassword")

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
        cursor.execute(query,(username, password, nome, cognome))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("homepage"))

app.run(debug=True)
