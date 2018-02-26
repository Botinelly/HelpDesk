from flask import render_template, flash, url_for, redirect, Flask, send_file
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
from app import app, db, lm
import numpy as np
import pandas as pd
from io import BytesIO

from app.models.tables import User, Post
from app.models.forms import LoginForm, CallForm, EditForm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/index")
@login_required
def index():
    return render_template('index.html')

@app.route("/chamado", methods=["POST", "GET"])
@login_required
def chamado():
    a = False
    form = CallForm()
    l = []
    l.append(form.category2.data)
    l.append(form.category3.data)
    l.append(form.category4.data)
    l.append(form.category5.data)
    if form.category.data == 'None' or form.category.data == None:
        pass
    else:
        for x in l:
            if form.category.data != None and x != 'None' and x != None:

                c = Post(form.category.data, x, form.obs.data, User.get_name(current_user), 1)
                db.session.add(c)
                db.session.commit()
                aux = Post.query.filter_by(id = c.id).first()
                flash("Chamado número " + str(aux) + " efetuado com sucesso! ")
                #flash(str(aux))
                return redirect(url_for("index"))
                break


    return render_template('chamado.html',  form = form)

@app.route("/lista", methods=["POST", "GET"])
@login_required
def lista():
    form = EditForm()
    teste = form.form_id.data
    upd = Post.query.filter_by(id = teste).first()
    print(upd)

    if(upd != None):
        upd.status = form.options.data
        db.session.add(upd)
        db.session.commit()

    x = Post.query.all()
    return render_template('lista.html', post = x, form = form)

@app.route("/stats")
@login_required
def stats():
    aux = Post.query.all()
    comp = [[0, "Impressora"],[0, "Instalação/Configuração de Software"],[0, "Otimização/Formatação de PC"],[0, "Acesso à rede (Pastas ou Internet)"]]
    print(aux[1].category)
    for i in aux:
        if i.category == "Impressora":
            comp[0][0] +=1
        elif i.category == "Software":
            comp[1][0] += 1
        elif i.category == "Otimização":
            comp[2][0] += 1
        elif i.category == "Rede":
            comp[3][0] += 1

    return render_template('estatistica.html', comp = comp)

@app.route("/meuchamado")
@login_required
def meuchamado():
    x = Post.query.filter_by(user_id = User.get_name(current_user)).all()
    return render_template('meu_chamado.html', post = x)

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Login Inválido")

    return render_template('login.html', form = form)

@app.route("/download")
def download():
    #create a random Pandas dataframe
    aux = Post.query.all()
    comp = [["Impressora", 0],["Instalação/Configuração de Software", 0],["Otimização/Formatação de PC", 0],["Acesso à rede (Pastas ou Internet)", 0]]
    for i in aux:
        if i.category == "Impressora":
            comp[0][1] +=1
        elif i.category == "Software":
            comp[1][1] += 1
        elif i.category == "Otimização":
            comp[2][1] += 1
        elif i.category == "Rede":
            comp[3][1] += 1
    labels = ['categoria', 'Demanda']
    df_1 = pd.DataFrame.from_records(comp, columns = labels)

    #create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    #taken from the original question
    df_1.to_excel(writer, merge_cells = False, sheet_name = "tabela")
    workbook = writer.book
    worksheet = writer.sheets["tabela"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')
    worksheet.set_column(0,9,28)

    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="data.xlsx", as_attachment=True)


@app.route("/logout")
def logout():
    logout_user()
    flash("Deslogado")
    return redirect(url_for("login"))
