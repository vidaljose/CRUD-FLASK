from flask import Flask, render_template,request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

import os

dbdir = "sqlite:///"+ os.path.abspath(os.getcwd())+"/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

#creando la base de datos
class Usuarios(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    usuario = db.Column(db.String(20),unique=True,nullable=False)



@app.route("/",methods=["GET","POST"])
def index():
    
    lista = Usuarios.query.order_by(Usuarios.id).all()

    if request.method == "POST":
        if (request.form["usuario"] != ""):
            nuevo_usuario = Usuarios(usuario=request.form["usuario"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            lista=Usuarios.query.order_by(Usuarios.id).all()
            return render_template("index.html",lista = lista)

    return render_template("index.html",lista = lista)
    #return "hola mundo"

@app.route("/delete")
def delete():
    id = request.args.get('id')
    actualizar_usuario = Usuarios.query.filter_by(id=id).first()
    db.session.delete(actualizar_usuario)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update", methods = ["GET","POST"])
def update():
    elemento_id = request.args.get('id')
    #lista = Usuarios.query.order_by(Usuarios.id).all()
    lista = Usuarios.query.order_by(Usuarios.id).all()
   
    if request.method == "POST":
        if (request.form["usuario"] != ""):
            usuario_actualizar = Usuarios.query.filter_by(id = int(elemento_id)).first()
            usuario_actualizar.usuario = request.form["usuario"]
            db.session.commit()
            lista=Usuarios.query.order_by(Usuarios.id).all()
            return redirect(url_for("index")) 

    
    return render_template("update.html",lista = lista,id = int(elemento_id))

if __name__ == ("__main__"):
    db.create_all()
    app.run(debug = True)
