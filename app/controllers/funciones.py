from app.models.Ingrediente import Ingrediente

def esto_es_sano(calorias:float,esvegetariano:bool)->bool:
    if(esvegetariano == True):
        return True
    else:
        if(calorias>100):
            return False
        else:
            return True
        
def las_calorias(lista_calorias:list)->float:
    sumacalorias = sum(lista_calorias)
    return round(sumacalorias*0.95)


def costos(primer_ingrediente:dict,segundo_ingrediente:dict,tercer_ingrediente:dict)->float:
    return primer_ingrediente["precio"] + segundo_ingrediente["precio"] + tercer_ingrediente["precio"]

def rentabilidad(precio:float,primer_ingrediente:dict,segundo_ingrediente:dict,tercer_ingrediente:dict)->float:
    return precio-(primer_ingrediente["precio"] + segundo_ingrediente["precio"] + tercer_ingrediente["precio"])

def el_mejor_producto(primer_producto:dict,segundo_producto:dict,tercer_producto:dict,cuarto_producto:dict)->float:
    mejor_producto = primer_producto  
    
    if segundo_producto["rentabilidad"] > mejor_producto["rentabilidad"]:
        mejor_producto = segundo_producto
    
    if tercer_producto["rentabilidad"] > mejor_producto["rentabilidad"]:
        mejor_producto = tercer_producto

    if cuarto_producto["rentabilidad"] > mejor_producto["rentabilidad"]:
        mejor_producto = cuarto_producto

    return mejor_producto["nombre"]

def abastecer_ingrediente(ingrediente: Ingrediente, cantidad: float) -> None:
    ingrediente.inventario += cantidad


def renovar_inventario(ingredientes: list) -> list:
    for ingrediente in ingredientes:
        if ingrediente.inventario == 0:
            ingrediente.inventario = 10
    return ingredientes


def vender_producto(ingrediente: Ingrediente, cantidad: int) -> Ingrediente:
    if ingrediente.inventario < cantidad:
        raise ValueError("No hay suficiente stock para vender este producto.")
    ingrediente.inventario -= cantidad
    return ingrediente


