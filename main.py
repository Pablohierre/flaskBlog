from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from pprint import pprint

app = Flask(__name__)
cliente = pymongo.MongoClient("mongodb://localhost:27017")
db = cliente['blog']
global username


@app.route("/", methods=['GET'])
def login():
    print("Esto es el login")
    return render_template("login.html")


@app.route("/", methods=['POST'])
def loginform():
    print("submits the form")
    usuario = request.form['username']
    contrasena = request.form['password']

    print("aqui llega")

    global username
    u = db['users'].find_one({"username": usuario}, {"username": 1})

    print(u)

    username = u.get("username")

    print(username)

    return redirect(url_for('mostrarposts'))


@app.route("/home", methods=['GET'])
def mostrarposts():
    posts = db['blog_entries'].find({"username": username}).limit(5)
    entries = []

    for x in posts:
        entries.append(x)

    return render_template("home.html", blog_entries=entries)  # esto es para pasarselo a la plantilla


@app.route("/home/entry/<string:id>", methods=['GET'])
def postIndividual(id):
    print("Accediendo al post")
    entry = []
    entry.append(db['blog_entries'].find_one({"_id": ObjectId(id)}))

    return render_template("entry.html", blog_entries=entry)


@app.route("/anadir", methods=['GET'])
def anadirGet():
    return render_template("anadir.html")


@app.route("/anadir", methods=['POST'])
def anadirPost():
    print("añadiendo post")
    # user=id
    global username
    descripcion = request.form['descripcion']
    contenido = request.form['contenido']
    fecha = datetime.now()
    blog = db['blog_entries']
    nueva_entrada = {  # "usuario":usuario,
        "descripcion": descripcion,
        "contenido": contenido,
        "fecha": fecha,
        "username": username
    }

    blog.insert_one(nueva_entrada)
    return redirect(url_for('mostrarposts'))


app.run()
