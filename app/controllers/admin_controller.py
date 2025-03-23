from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.Producto import Producto
from app.models.Ingrediente import Ingrediente
from app.config.db import db
from app.seeders.insertar_productos import cargar_productos
from app.seeders.insertar_ingredientes import cargar_ingredientes

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

# Dashboard principal
@admin_blueprint.route("/dashboard")
@login_required
def dashboard():
    if not current_user.es_admin:
        return redirect(url_for("auth.no_autorizado"))  # Redirige si no es admin

    productos = Producto.query.all()
    ingredientes = Ingrediente.query.all()

    return render_template(
        "admin/dashboard.html",
        user=current_user,
        productos=productos,
        ingredientes=ingredientes
    )

# Ruta para vender un producto
@admin_blueprint.route("/vender-producto/<int:producto_id>", methods=["POST"])
@login_required
def vender_producto_route(producto_id):
    if not current_user.es_admin:
        return redirect(url_for("auth.no_autorizado"))  # Redirige si no es admin

    producto = Producto.query.get_or_404(producto_id)
    
    try:
        mensaje = producto.consumir_ingredientes()
        db.session.commit()
        flash(mensaje, "success")
    except ValueError as e:
        db.session.rollback()
        flash(f"¡Oh no! Nos hemos quedado sin {e}", "danger")
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error inesperado al intentar vender el producto.", "danger")
    
    return redirect(url_for("admin.dashboard"))

# Ruta para cargar ingredientes
@admin_blueprint.route("/cargar-ingredientes", methods=["POST"])
@login_required
def cargar_ingredientes_route():
    if not current_user.es_admin:
        return redirect(url_for("auth.no_autorizado"))  # Redirige si no es admin

    try:
        cargar_ingredientes()
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cargar ingredientes: {str(e)}", "danger")
        
    return redirect(url_for("admin.dashboard"))

# Ruta para cargar productos
@admin_blueprint.route("/cargar-productos", methods=["POST"])
@login_required
def cargar_productos_route():
    if not current_user.es_admin:
        return redirect(url_for("auth.no_autorizado"))  # Redirige si no es admin

    # Verificar si hay ingredientes antes de cargar productos
    ingredientes = Ingrediente.query.all()
    if not ingredientes:
        flash("Primero debes cargar los ingredientes antes de agregar productos.", "warning")
        return redirect(url_for("admin.dashboard"))

    try:
        cargar_productos()
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cargar productos: {str(e)}", "danger")
        
    return redirect(url_for("admin.dashboard"))
