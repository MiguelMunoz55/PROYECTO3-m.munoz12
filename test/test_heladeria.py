import unittest
from app.controllers.funciones import (
    esto_es_sano, las_calorias, costos, rentabilidad, el_mejor_producto, 
    abastecer_ingrediente, renovar_inventario, vender_producto
)
from app.models.Ingrediente import Ingrediente


class TestHeladeria(unittest.TestCase):

    def test_esto_es_sano(self):
        self.assertTrue(esto_es_sano(80, True))
        self.assertFalse(esto_es_sano(120, False))
        self.assertTrue(esto_es_sano(90, False))

    def test_las_calorias(self):
        self.assertEqual(las_calorias([100, 200, 300]), 570)
        self.assertEqual(las_calorias([0, 0, 0]), 0)
        self.assertEqual(las_calorias([100]), 95)

    def test_costos(self):
        ing1 = {"nombre": "Fresa", "precio": 50}
        ing2 = {"nombre": "Chocolate", "precio": 70}
        ing3 = {"nombre": "Vainilla", "precio": 30}
        self.assertEqual(costos(ing1, ing2, ing3), 150)

    def test_rentabilidad(self):
        ing1 = {"precio": 50}
        ing2 = {"precio": 30}
        ing3 = {"precio": 20}
        self.assertEqual(rentabilidad(150, ing1, ing2, ing3), 50)
        self.assertEqual(rentabilidad(100, ing1, ing2, ing3), 0)

    def test_el_mejor_producto(self):
        prod1 = {"nombre": "Copa Fresa", "rentabilidad": 50}
        prod2 = {"nombre": "Malteada Choco", "rentabilidad": 70}
        prod3 = {"nombre": "Helado Vainilla", "rentabilidad": 60}
        prod4 = {"nombre": "Banana Split", "rentabilidad": 80}
        
        self.assertEqual(el_mejor_producto(prod1, prod2, prod3, prod4), "Banana Split")

    def test_abastecer_ingrediente(self):
        fresa = Ingrediente(nombre="Fresa", inventario=10, precio=50, calorias=80, es_vegetariano=True)
        
        abastecer_ingrediente(fresa, 20)
        self.assertEqual(fresa.inventario, 30)

    def test_renovar_inventario(self):
        chocolate = Ingrediente(nombre="Chocolate", inventario=0, precio=70, calorias=120, es_vegetariano=False)
        vainilla = Ingrediente(nombre="Vainilla", inventario=5, precio=30, calorias=90, es_vegetariano=True)
        
        ingredientes = [chocolate, vainilla]
        renovar_inventario(ingredientes)
        
        self.assertEqual(chocolate.inventario, 10) 
        self.assertEqual(vainilla.inventario, 5) 

    def test_vender_producto_exito(self):
        fresa = Ingrediente(nombre="Fresa", inventario=10, precio=50, calorias=80, es_vegetariano=True)
        chocolate = Ingrediente(nombre="Chocolate", inventario=5, precio=70, calorias=120, es_vegetariano=False)
        
        vender_producto(fresa, 2)
        vender_producto(chocolate, 1)

        self.assertEqual(fresa.inventario, 8)
        self.assertEqual(chocolate.inventario, 4)

    def test_vender_producto_falla(self):
        fresa = Ingrediente(nombre="Fresa", inventario=10, precio=50, calorias=80, es_vegetariano=True)
        chocolate = Ingrediente(nombre="Chocolate", inventario=1, precio=70, calorias=120, es_vegetariano=False)
        
        with self.assertRaises(ValueError):
            vender_producto(chocolate, 3)

if __name__ == '__main__':
    unittest.main()