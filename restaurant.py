#!/usr/bin/env python3

import titles as m

reseta = []


def recetas_breakfast():
    print(m.breakfast_menu())
    bf = """
        Croissant Pistacho
        Huevos Puntilla
        Tostada Parisina
        Croissant Lemon
        Pan de Nuez
        Arepa de Huevo
        Empanada de Carne
        Empanada de Pollo
        Empanada de Hawaina
        """
    reseta.append(bf)

    def recetas_midfood():
        print(m.midfood_menu())
    mf = """
        Chicken Parm
        Pollo Toscano
        Pollo a la Cacerola
        Paella Mixta
        Salmon Pataraska
   """
    reseta.append(mf)

    def recetas_desserts():
        print(m.desserts_menu())
        ds = """
            Tarta Vaska
            Vaklava
            Matera Tiramisu 3.0
            Torta de Almohabana
            Helado Napolitano
        """
        resetan.append(ds)
