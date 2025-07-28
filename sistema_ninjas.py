
from io import open
import random

# ------------------- Árbol de Habilidades ---------------------
class NodoHabilidad:
    def __init__(self, habilidad,puntos):
        self.habilidad = habilidad
        self.puntos=puntos
        self.izquierda = None
        self.derecha = None

def crear_arbol_ejemplo():
    raiz = NodoHabilidad("Ataque Rápido", random.randint(5,10))
    raiz.izquierda = NodoHabilidad("Golpe Básico", random.randint(5,10))
    raiz.derecha = NodoHabilidad("Patada Voladora", random.randint(5,10))
    raiz.izquierda.izquierda = NodoHabilidad("Puñetazo Fuerte", random.randint(5,10))
    return raiz

def sumar_puntos(nodo):
    if nodo is None:
        return 0
    return nodo.puntos+sumar_puntos(nodo.izquierda)+sumar_puntos(nodo.derecha)


def preorden_guardar(nodo, archivo):
    if nodo:
        archivo.write(nodo.habilidad + "\n")
        preorden_guardar(nodo.izquierda, archivo)
        preorden_guardar(nodo.derecha, archivo)

def guardar_arbol_habilidades(nombre, arbol): #cuando se busque las habilidades de ese ninja se le guarda el nombre como minusculas
    with open(f"habilidades_{nombre}.txt", "w", encoding="utf-8") as f:
        preorden_guardar(arbol, f)

def leer_habilidades(archivo):
    with open(archivo,"r",encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        datos=[]
        for linea in lineas:
            partes=linea.strip().split(",")
            if len(partes)==2:
                habilidad=partes[0]
                puntos=int(partes[1])
                datos.append((habilidad,puntos))

def reconstruir_arbol(datos):
    try:
        habilidad,puntos=next(datos)
    except StopIteration:
        return None
    nodo=NodoHabilidad(habilidad,puntos)
    nodo.izquierda=reconstruir_arbol(datos)
    nodo.derecha=reconstruir_arbol(datos)
    return nodo

def imprimir_arbol(nodo, nivel=0):
    if nodo:
        print("  " * nivel + "- " + nodo.habilidad)
        imprimir_arbol(nodo.izquierda, nivel + 1)
        imprimir_arbol(nodo.derecha, nivel + 1)

# ------------------- Funciones Administrador ---------------------
def generar_atributos(estilo):
    return {
        "estilo": estilo,
        "fuerza": random.randint(50, 100),
        "velocidad": random.randint(50, 100),
        "energia": random.randint(50, 100),
        "poder": random.randint(50, 100),
    }

def registrar_ninja(dic_ninjas, id_actual):
    nombre = input("Nombre del ninja: ").strip().lower()
    estilo = input("Estilo de pelea: ").strip().lower()
    atributos = generar_atributos(estilo)
    arbol = crear_arbol_ejemplo()
    dic_ninjas[id_actual] = {
        "nombre": nombre,
        "atributos": atributos,
        "arbol": arbol
    }
    guardar_arbol_habilidades(nombre, arbol)
    print("Ninja registrado.")
    return id_actual + 1

def mostrar_todos(dic_ninjas):
    for id_ninja, datos in dic_ninjas.items():
        print(f"ID: {id_ninja}")
        print(f"Nombre: {datos['nombre']}")
        for atr, val in datos['atributos'].items():
            print(f"{atr.capitalize()}: {val}")
        print("-" * 30)

def mostrar_arbol(dic_ninjas, id_ninja):
    if id_ninja in dic_ninjas:
        imprimir_arbol(dic_ninjas[id_ninja]['arbol'])
    else:
        print("ID no encontrado")

def menu_admin(dic_ninjas):
    id_actual = max(dic_ninjas.keys(), default=0) + 1
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Registrar Ninja")
        print("2. Mostrar Todos")
        print("3. Ver árbol de habilidades")
        print("4. Salir")
        op = input("Opción: ")
        if op == "1":
            id_actual = registrar_ninja(dic_ninjas, id_actual)
        elif op == "2":
            mostrar_todos(dic_ninjas)
        elif op == "3":
            try:
                id_sel = int(input("Ingrese ID del ninja: "))
                mostrar_arbol(dic_ninjas, id_sel)
            except ValueError:
                print("ID inválido.")
        elif op == "4":
            break
        else:
            print("Opción inválida.")

# ------------------- Jugador: Registro y Login ---------------------
def guardar(usuarios, archivo):
    try:
        with open(archivo, "a", encoding="utf-8") as info:
            for id, datos in usuarios.items():
                info.write(f"Nombre: {datos['nombre']} {datos['apellido']} | Identificacion: {id} | Edad: {datos['edad']} | Usuario: {datos['usuario']} | Contraseña: {datos['contra']}\n")
    except Exception as n:
        print(f"Error al guardar información de usuario: {n}")

def nuevo_jugador(usuarios):
    try:
        print("---- Registro de nuevo jugador ----\n")
        nombre = input("Ingrese su nombre: ").strip()
        apellido = input("Ingrese su apellido: ").strip()
        id = int(input("Ingrese su identificación: "))
        edad = int(input("Ingrese su edad: "))
        usuario = input("Ingrese su usuario (correo): ").strip()
        contra = input("Contraseña (8+, 1 mayús, 1 número): ").strip()
        if len(contra) < 8 or not any(c.isupper() for c in contra) or not any(c.isdigit() for c in contra):
            print("Contraseña inválida")
            return
        usuarios[id] = {"nombre": nombre, "apellido": apellido, "edad": edad, "usuario": usuario, "contra": contra}
        guardar(usuarios, "usuarios.txt")
        print("Jugador registrado exitosamente")
    except ValueError:
        print("Error: Datos inválidos")

def login(archivo):
    usuarios = {}
    try:
        with open(archivo, "r", encoding="utf-8") as info:
            for linea in info:
                partes = linea.strip().split(" | ")
                datos = {}
                for p in partes:
                    clave, valor = p.split(":", 1)
                    datos[clave.strip()] = valor.strip()
                id_str = datos["Identificacion"]
                usuarios[id_str] = {
                    "nombre": datos["Nombre"].split()[0],
                    "apellido": datos["Nombre"].split()[1],
                    "edad": int(datos["Edad"]),
                    "usuario": datos["Usuario"],
                    "contra": datos["Contraseña"]
                }
        intento = 0
        while intento < 3:
            user = input("Ingrese su usuario: ").strip()
            key = input("Ingrese su contraseña: ").strip()
            for id_usuario, datos in usuarios.items():
                if user == datos['usuario'] and key == datos['contra']:
                    print("Inicio de sesión exitoso")
                    return id_usuario
            print("Usuario o contraseña incorrectos")
            intento += 1
        print("Demasiados intentos fallidos.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def cargar_ninjas(archivo):
    ninjas = {}
    try:
        with open(archivo, "r", encoding="utf-8") as info:
            id_ninja = None
            nombre = None
            habilidades = {}
            for linea in info:
                linea = linea.strip()
                if linea.startswith("ID:"):
                    if id_ninja is not None:
                        ninjas[id_ninja] = {
                            "nombre": nombre,
                            "habilidades": habilidades,
                            "puntos": 0
                        }
                    id_ninja = int(linea.split(":")[1].strip())
                    habilidades = {}
                elif linea.startswith("Nombre:"):
                    nombre = linea.split(":")[1].strip()
                elif ":" in linea:
                    clave, valor = linea.split(":", 1)
                    clave = clave.strip()
                    if clave == "Energia":
                        clave = "resistencia"
                    elif clave == "Velocidad":
                        clave = "agilidad"
                    elif clave == "Estilo de pelea":
                        clave = "estilo"
                    habilidades[clave] = int(valor.strip()) if clave != "estilo" else valor.strip()
            if id_ninja is not None:
                ninjas[id_ninja] = {
                    "nombre": nombre,
                    "habilidades": habilidades,
                    "puntos": 0
                }
    except Exception as e:
        print(f"Error al leer archivo: {e}")
    return ninjas

def mostrar_arbol_habilidades(ninjas):
    if not ninjas:
        print("No hay ninjas registrados.")
        return
    print("\n-----Ninjas Registrados-----")
    for id_ninja, datos in ninjas.items():
        print(f"ID: {id_ninja} | Nombre: {datos['nombre']}")
    try:
        id_ninja = int(input("Ingrese el ID del ninja: "))
        if id_ninja in ninjas:
            datos = ninjas[id_ninja]
            print(f"\nID: {id_ninja}")
            print(f"Nombre: {datos['nombre']}")
            print("Habilidades:")
            for attr, valor in datos["habilidades"].items():
                print(f"{attr.capitalize()}: {valor}")
            print(f"Puntos: {datos['puntos']}")
        else:
            print("Ninja no encontrado.")
    except ValueError:
        print("ID inválido.")

def simular_combate_1v1(ninjas):
    ids = list(ninjas.keys())
    if len(ids) < 2:
        print("Se necesitan al menos 2 ninjas.")
        return
    print("Seleccione dos ninjas por ID:")
    for i in ids:
        print(f"{i}: {ninjas[i]['nombre']}")
    try:
        id1 = int(input("ID primer ninja: "))
        id2 = int(input("ID segundo ninja: "))
        if id1 not in ninjas or id2 not in ninjas or id1 == id2:
            print("IDs inválidos.")
            return
        n1 = ninjas[id1]
        n2 = ninjas[id2]
        p1 = sum(n1["habilidades"].get(k, 0) for k in ["fuerza", "agilidad", "resistencia"])
        p2 = sum(n2["habilidades"].get(k, 0) for k in ["fuerza", "agilidad", "resistencia"])
        if p1 > p2:
            print(f"{n1['nombre']} gana!")
            n1["puntos"] += 10
        elif p2 > p1:
            print(f"{n2['nombre']} gana!")
            n2["puntos"] += 10
        else:
            print("¡Empate!")
    except ValueError:
        print("ID inválido.")

def simular_torneo(ninjas):
    participantes = list(ninjas.items())
    if len(participantes) < 2:
        print("Se necesitan al menos 2 ninjas.")
        return
    random.shuffle(participantes)
    ronda = 1
    while len(participantes) > 1:
        print(f"\n--- Ronda {ronda} ---")
        ganadores = []
        for i in range(0, len(participantes), 2):
            if i + 1 >= len(participantes):
                ganadores.append(participantes[i])
                continue
            id1, n1 = participantes[i]
            id2, n2 = participantes[i + 1]
            p1 = sum(n1["habilidades"].get(k, 0) for k in ["fuerza", "agilidad", "resistencia"])
            p2 = sum(n2["habilidades"].get(k, 0) for k in ["fuerza", "agilidad", "resistencia"])
            if p1 > p2:
                print(f"{n1['nombre']} vence a {n2['nombre']}")
                n1["puntos"] += 10
                ganadores.append((id1, n1))
            else:
                print(f"{n2['nombre']} vence a {n1['nombre']}")
                n2["puntos"] += 10
                ganadores.append((id2, n2))
        participantes = ganadores
        ronda += 1
    print(f"¡Campeón del torneo: {participantes[0][1]['nombre']}!")

def consultar_ranking(ninjas):
    ranking = sorted(ninjas.values(), key=lambda x: x["puntos"], reverse=True)
    print("\n--- RANKING ---")
    for n in ranking:
        print(f"{n['nombre']}: {n['puntos']} puntos")

def menu_usuario(ninjas):
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1. Ver árbol de habilidades")
        print("2. Combate 1v1")
        print("3. Torneo")
        print("4. Ranking")
        print("5. Salir")
        op = input("Opción: ")
        if op == "1":
            mostrar_arbol_habilidades(ninjas)
        elif op == "2":
            simular_combate_1v1(ninjas)
        elif op == "3":
            simular_torneo(ninjas)
        elif op == "4":
            consultar_ranking(ninjas)
        elif op == "5":
            break
        else:
            print("Opción inválida.")

# ------------------- MAIN ---------------------
def main():
    archivo_usuarios = "usuarios.txt"
    archivo_ninjas = "ninjas.txt"
    ninjas = cargar_ninjas(archivo_ninjas)
    while True:
        print("\n=== SISTEMA DE NINJAS ===")
        print("1. Administrador")
        print("2. Registrar jugador")
        print("3. Iniciar sesión jugador")
        print("4. Salir")
        op = input("Opción: ")
        if op == "1":
            user = input("Usuario admin: ")
            pwd = input("Contraseña: ")
            if user == "useradmin" and pwd == "1234":
                menu_admin(ninjas)
            else:
                print("Credenciales incorrectas.")
        elif op == "2":
            nuevo_jugador({})
        elif op == "3":
            id_usuario = login(archivo_usuarios)
            if id_usuario:
                menu_usuario(ninjas)
        elif op == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
