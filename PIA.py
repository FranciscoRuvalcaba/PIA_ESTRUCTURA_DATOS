import datetime
import time
from sqlite3 import Error
import sys
import sqlite3
SEPARADOR = ("-" * 80)
SEPARADOR1 = ("_" * 80)
nuevo_folio = 0

try:
    with sqlite3.connect("BD.db") as conn:
        micursor = conn.cursor()
        micursor.execute("SELECT Venta.Folio FROM Venta")
        #SE GENERA UNA CONSULTA PARA PODER SABER CUANTOS FOLIOS HASTA EL MOMENTO HAY EN LA BASE DE DATOS
        #Y SE GUARDA EN LA VARIABLE folios
        folios  = micursor.fetchall()
        folio = len(folios)
        
    while True:
        print("--------Menu--------")
        print("1.AGREGAR VENTA")
        print("2.CONSULTAR UNA VENTA")
        print("3.REPORTE DE VENTAS POR FECHA")
        print("4.SALIR")
        opcion = int(input("SELECCIONA UNA OPCION: "))
        print(f"{SEPARADOR}\n")
    
        if opcion == 1:
            subtotal = 0
            nuevo_folio = folio + nuevo_folio + 1
            fecha = datetime.date.today()
            nueva_venta = (nuevo_folio,fecha)
            
            print("\tAGREGAR VENTA")
            
            with sqlite3.connect("BD.db") as conn:
                micursor = conn.cursor()
                #AL MOMENTO DE ENTRAR A AGREGAR VENTA SE GENERA UN NUEVO FOLIO CON SU FECHA EN LA BASE DE DATOS
                micursor.execute("""INSERT INTO Venta VALUES(:nuevo_folio, :fecha)""",nueva_venta)                                       
            while True:
                descripcion = input('CUAL ES EL NOMBRE DEL ARTICULO?: ')
                if descripcion:
                    cantidad_articulo = int(input('ESCRIBE LA CANTIDAD DE ARTICULOS: '))
                    if cantidad_articulo>0:
                        precio_articulo = float(input('CUANTO VALE CADA ARTICULO?: '))
                        if precio_articulo>0:
                            monto_venta = cantidad_articulo * precio_articulo
                            articulos = (nuevo_folio, descripcion, cantidad_articulo, precio_articulo)
                            subtotal += monto_venta
                            with sqlite3.connect("BD.db") as conn:
                                micursor = conn.cursor()
                            #CUANDO SE TIENEN TODOS LOS DATOS DE LOS ARTICULOS SE GENERA
                            #UN INSERT DE MANERA ORGANIZADA CON LOS DATOS DEL ARTICULO Y FOLIO DE SU VENTA
                                micursor.execute("""INSERT INTO Detalle VALUES(:nuevo_folio , :descripcion , :cantidad_articulo , :precio_articulo)""", articulos)
                                print(SEPARADOR1)
                                print(f"SUBTOTAL DE VENTA HASTA EL MOMENTO: ${subtotal}")
                                print(SEPARADOR1)
                                respuesta = int(input("\nDESEAS CONTINUAR AGREGANDO ARTICULOS? 1[si], 2[no]: "))
                                print("{SEPARADOR}\n")
                            if respuesta != 1:
                                print(SEPARADOR1)
                                print("\tDATOS DE VENTA")
                                print(f"FOLIO: {nuevo_folio}\tFECHA: {fecha}\n")
                                print(f'SUBTOTAL: ${subtotal}')
                                iva = (subtotal*0.16)
                                print(f'IVA(16%): ${iva}')
                                total = (iva + subtotal)
                                print(f'TOTAL: ${total}')                             
                                print(SEPARADOR1)
                                break
                        else:
                            print("\nDATO NO VALIDO) INGRESAR NUMERO MAYOR A 0\n")   
                    else:
                        print("\nDATO NO VALIDO) INGRESAR NUMERO MAYOR A 0\n")
                else:
                    print("\n!!SE DEBE INGRESAR DATOS EN DESCRIPCION DEL ARTICULO!!\n")

        elif opcion == 2:
            print(SEPARADOR1)
            print("CONSULTAR UNA VENTA")
            folio_a_buscar = int(input("INGRESA EL NUMERO DE FOLIO A BUSCAR: "))
            busqueda = (folio_a_buscar,)
            print(SEPARADOR1)
            with sqlite3.connect("BD.db") as conn:
                micursor.execute("""SELECT Venta.Folio\
                            FROM Venta \
                            WHERE Venta.Folio = :folio_a_buscar """, busqueda)
                #SE HACE UNA CONSULTA EN LA BASE DE DATOS PARA PODER SABER SI EXISTE EL FOLIO.
                existe = micursor.fetchall()
            if existe:
                print(f"\nFOLIO DE TICKET: |{folio_a_buscar}|\n")
                micursor.execute("""SELECT Venta.Folio, Venta.Fecha, Detalle.Descripcion, Detalle.Cantidad, Detalle.Precio_Unitario \
                            FROM Venta \
                            INNER JOIN Detalle ON Detalle.Venta = Venta.Folio\
                            WHERE Venta.Folio = :folio_a_buscar """, busqueda)
                #SI EL FOLIO EXISTE, SE GENERA OTRA CONSULTA CON TODOS LOS DATOS DE LA VENTAS QUE HAYA HECHO. 
                registros = micursor.fetchall()
                if registros:
                    print(f'Folio\tFecha\t\tDescripcion\tCantidad\tPrecio Unitario')
                    print("-"*100)
                    for Folio, Fecha, Descripcion, Cantidad, Precio_Unitario in registros:
                        print(f'{Folio}\t{Fecha}\t{Descripcion}\t\t{Cantidad}\t\t${Precio_Unitario:,.2f}')
                print(f"{SEPARADOR1}\n")
            
            else:
                print("-"*30)
                print(f"EL NUMERO DE FOLIO: {folio_a_buscar}, NO ESTA REGISTRADO")
                print("-"*30)
                
        elif opcion == 3:
            print(SEPARADOR1)
            print("REPORTE DE VENTAS POR FECHA")
            fecha_capturada = input("INGRESA LA FECHA A BUSCAR CON FORMATO dd/mm/aaaa: \n")
            fecha_a_buscar = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
            busqueda = (fecha_a_buscar,)
            print(SEPARADOR1)
            with sqlite3.connect("BD.db") as conn:
                micursor.execute("""SELECT Venta.Fecha\
                            FROM Venta \
                            WHERE Venta.Fecha = :fecha_a_buscar """, busqueda)
                        #SE HACE UNA CONSULTA EN LA BASE DE DATOS PARA PODER SABER SI EXISTE LA FECHA.
                existe = micursor.fetchall()
            if existe:
                print(f"\nREPORTE DE FECHA: |{fecha_a_buscar}|\n")
                micursor.execute("""SELECT Venta.Folio, Venta.Fecha, Detalle.Descripcion, Detalle.Cantidad, Detalle.Precio_Unitario \
                            FROM Venta \
                            INNER JOIN Detalle ON Detalle.Venta = Venta.Folio\
                            WHERE Venta.Fecha = :fecha_a_buscar """, busqueda)
                            #SI LA FECHA EXISTE, SE GENERA OTRA CONSULTA CON TODOS LOS DATOS DE LA VENTAS QUE HAYA HECHO EN LA FECHA. 
                registros = micursor.fetchall()
                if registros:
                    print(f'Folio\tFecha\t\tDescripcion\tCantidad\tPrecio Unitario')
                    print("-"*100)
                    for Folio, Fecha, Descripcion, Cantidad, Precio_Unitario in registros:
                        print(f'{Folio}\t{Fecha}\t{Descripcion}\t\t{Cantidad}\t\t${Precio_Unitario:,.2f}')
                print(f"{SEPARADOR1}\n")
            else:
                print("-"*30)
                print(f"LA FECHA INGRESADA: {fecha_a_buscar}, NO ESTA REGISTRADA")
                print("-"*30)                
        elif opcion == 4:
            break
        else:
            print("RESPUESTA NO VALIDA")
except Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")