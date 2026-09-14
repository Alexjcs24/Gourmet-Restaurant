#!/usr/bin/env python
#variables a definir

#codigo_plato: str
#nombre_plato: str
#categoria: str
#disponible: bool
#cantidad: int
#cantidadMax: int
#subtotal: float
#selection: str

#NOMBRES DE LOS INTEGRANTES DEL PROYECTO:
#JESUS ESTEBAN MUNOZ GOMEZ
#ALBEIRO ANDRES RODGERS PEREZ


import subprocess

precio: float
caantidad: int

#aqui hago varias funciones con menus para definir cada tipo de comida del restaurante

#categoria: postres

def menuPostres():
    #menu de postres
    subprocess.call(["cmd.exe", "/C", "cls"])
    print("##############")
    print("##  POSTRES ##")
    print("#############")

    print("1. Tiramisú ")
    print("2. Volcán de arequipe ")
    print("3. Volcán de chocolate ")
    print("4. Tres Leches ")
    print("5. Gelato Cheese de Limón ")
    print("6. Gelato Chocolate Dubai ")
    print("7. Gelato Pistaccio ")
    print("8. Banana Split ")
    print("9. Helado Napolitano ")
    print("0. Salir ")
    selection = input("Que opcion Deseas escoger: \n ")

    match selection:
        case 1:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### TIRAMISU ###")
            print("Descripcion:")
            print("Postre italiano con capas de bizcocho al café, crema de queso y licor, espolvoreado con cocoa.")
            print(f"PRECIO: ")
            print("16.900$")
            precio = 16900
        case 2:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### VOLCAN DE AREQUIPE ###")
            print("DESCRIPCION:")
            print("Volcán con centro fundido de arequipe, fresas frescas y gelato de vainilla.")
            print(f"PRECIO: ")
            print("17.900$")
            precio = 17900

        case 3:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### VOLCAN DE CHOCOLATE ###")
            print("DESCRIPCION:")
            print("Volcán con centro fundido de chocolate, fresas frescas y gelato de vainilla.")
            print(f"PRECIO: ")
            print("17.900$")
            precio = 17900
        case 4:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### STROMBOLI DE CHOCOLATE ###")
            print("DESCRIPCION:")
            print("Capas de bizcocho, crema de café sedosa y ganache de chocolate intenso.")
            print(f"PRECIO: ")
            print("17.900$")
            precio = 17900
        case 5:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### GELATO CHEESE DE LIMON ###")
            print("DESCRIPCION:")
            print("Tarta de queso con limón y galleta triturada.")
            print(f"PRECIO: ")
            print("7.500$")
            precio = 7500
        case 6:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### GELATO CHOCOLATE DUBAI ###")
            print("DESCRIPCION:")
            print("Gelato de chocolate oscuro, crema de pistacchio tostado y trozos de hojaldre")
            print(f"PRECIO: ")
            print("17.900$")
            precio = 17900
        case 7:
            subprocess.call(["cmd.exe", "/C", "cls"])
            print("### GELATO PISTACCIO ###")
            print("DESCRIPCION:")
            print("Gelato hecho con auténtico pistacchio tostado sin sabores artificiales")
            print(f"PRECIO: ")
            print("7.500$")
            precio = 7500
            pass


print("-- RESTAURANT GOURMET --")
print("!!Bienvenidos a nuestro pequeno emprendimiento!! ")

#esta variable es para seleccionar darle al cliente la opcion para ingresar al menu
selection = input("Deseas ingresar a nuestro menu?S/n")

if (selection != "s" or selection != "n"):
    print("ERROR: seleccion no valida")
elif (selection == "s" or selection == "S"):
    print(menuPostres())




