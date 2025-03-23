from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.usuario import Usuario
from app.models.Producto import Producto

from app.config.db import db

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/")
def home():
    productos = Producto.query.all()

    return render_template("principal.html",productos=productos)

@home_blueprint.route("/documentacion")
def documentacion():
    return render_template("documentacion.html")

