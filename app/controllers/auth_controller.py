from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from app.models.usuario import Usuario
from app.config.db import db

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/no-autorizado")
def no_autorizado():
    return render_template("no_autorizado.html"), 401

@auth_blueprint.route("/")
def home():
    return redirect(url_for("principal"))

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:  # Si ya está autenticado, redirigirlo a su vista correspondiente
        if current_user.es_admin:
            return redirect(url_for("admin.dashboard"))
        elif current_user.es_empleado:
            return redirect(url_for("empleado.dashboard"))
        else:
            return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Usuario.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            flash("Inicio de sesión exitoso", "success")

            # Redirigir al usuario según su tipo
            if user.es_admin:
                return redirect(url_for("admin.dashboard"))
            elif user.es_empleado:
                return redirect(url_for("empleado.dashboard"))
            else:
                return redirect(url_for("user.dashboard"))

        flash("Credenciales incorrectas", "danger")

    return render_template("login.html")

@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))