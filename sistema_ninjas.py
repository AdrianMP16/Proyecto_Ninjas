from io import open
import random
import os

# ------------------- Árbol de Habilidades ---------------------
class NodoHabilidad:
    def __init__(self, habilidad, puntos):
        self.habilidad = habilidad
        self.puntos = puntos
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
    return nodo.puntos + sumar_puntos(nodo.izquierda) + sumar_puntos(nodo.derecha)

def preorden_guardar(nodo, archivo):
    if nodo:
        archivo.write(f"{nodo.habilidad},{nodo.puntos}\n")
        preorden_guardar(nodo.izquierda, archivo)
        preorden_guardar(nodo.derecha, archivo)

def guardar_arbol_habilidades(nombre, arbol):
    with open(f"habilidades_{nombre}.txt", "w", encoding="utf-8") as f:
        preorden_guardar(arbol, f)

def leer_habilidades(archivo):
    print(f"Intentando leer el archivo: {os.path.abspath(archivo)}")
    try:
        with open(archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            datos = []
            for linea in lineas:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    habilidad = partes[0]
                    puntos = int(partes[1])
                    datos.append((habilidad, puntos))
            return iter(datos)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    except Exception as e:
        raise Exception(f"Error al leer el archivo {archivo}: {e}")

def mostrar_arbol_desde_archivo(nombre):
    nombre = nombre.strip().lower()  
    archivo = f"habilidades_{nombre}.txt"
    try:
        datos = leer_habilidades(archivo)
        arbol = reconstruir_arbol(datos)
        if arbol:
            print(f"Árbol de habilidades de {nombre.capitalize()}:")
            imprimir_arbol(arbol)
        else:
            print(f"No se encontraron habilidades para {nombre.capitalize()}.")
    except FileNotFoundError as e:
        print(e)  
    except Exception as e:
        print(f"Error al procesar el árbol de habilidades: {e}")

def reconstruir_arbol(datos):
    try:
        habilidad, puntos = next(datos)
    except StopIteration:
        return None
    nodo = NodoHabilidad(habilidad, puntos)
    nodo.izquierda = reconstruir_arbol(datos)
    nodo.derecha = reconstruir_arbol(datos)
    return nodo

def imprimir_arbol(nodo, nivel=0):
    if nodo:
        print("  " * nivel + f"- {nodo.habilidad} ({nodo.puntos})")
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
    habilidades = generar_atributos(estilo)
    arbol = crear_arbol_ejemplo()
    dic_ninjas[id_actual] = {
        "nombre": nombre,
        "habilidades": habilidades,
        "arbol": arbol,
        "puntos": 0
    }
    guardar_arbol_habilidades(nombre, arbol)
    guardar_ninjas(dic_ninjas, "ninjas.txt")  
    print("Ninja registrado.")
    return id_actual + 1

def guardar_ninjas(ninjas, archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            for id_ninja, datos in ninjas.items():
                f.write(f"ID: {id_ninja}\n")
                f.write(f"Nombre: {datos['nombre']}\n")
                for attr, valor in datos["habilidades"].items():
                    if attr == "agilidad":
                        attr = "Velocidad"
                    elif attr == "resistencia":
                        attr = "Energia"
                    elif attr == "estilo":
                        attr = "Estilo de pelea"
                    f.write(f"{attr}: {valor}\n")
                f.write(f"Puntos: {datos['puntos']}\n")
                f.write("\n")  
        print("Ninjas guardados exitosamente.")
    except Exception as e:
        print(f"Error al guardar ninjas: {e}")

def mostrar_todos(dic_ninjas):
    if not dic_ninjas:  
        print("No hay ninjas registrados.")
        return
    for id_ninja, datos in dic_ninjas.items():
        print(f"ID: {id_ninja}")
        print(f"Nombre: {datos['nombre']}")
        for atr, val in datos['habilidades'].items():  
            print(f"{atr.capitalize()}: {val}")
        print(f"Puntos: {datos['puntos']}")
        print("-" * 30)

def mostrar_arbol(dic_ninjas, id_ninja):
    if id_ninja in dic_ninjas:
        if "arbol" in dic_ninjas[id_ninja]:
            imprimir_arbol(dic_ninjas[id_ninja]['arbol'])
        else:
            print(f"Error: El ninja {dic_ninjas[id_ninja]['nombre']} no tiene un árbol de habilidades definido.")
    else:
        print("ID no encontrado")

def actualizar_atributos(ninjas_dict, id_ninja):
    if id_ninja not in ninjas_dict:
        print("Ninja no encontrado.")
        return
    
    ninja = ninjas_dict[id_ninja]
    while True:
        print(f"\nActualizando ninja: {ninja['nombre']} (ID: {id_ninja})")
        print("1. Nombre")
        print("2. Fuerza")
        print("3. Velocidad")
        print("4. Energia")
        print("5. Poder")
        print("6. Estilo de pelea")
        print("7. Salir")
        opcion = input("Seleccione un atributo: ")
        
        if opcion == '1':
            ninja['nombre'] = input("Nuevo nombre: ")
        elif opcion == '2':
            val = input("Nueva Fuerza (50-100): ")
            if val.isdigit() and 50 <= int(val) <= 100:
                ninja['habilidades']['fuerza'] = int(val)
            else:
                print("Valor inválido.")
        elif opcion == '3':
            val = input("Nueva Velocidad (50-100): ")
            if val.isdigit() and 50 <= int(val) <= 100:
                ninja['habilidades']['velocidad'] = int(val)
            else:
                print("Valor inválido.")
        elif opcion == '4':
            val = input("Nueva Energia (50-100): ")
            if val.isdigit() and 50 <= int(val) <= 100:
                ninja['habilidades']['energia'] = int(val)
            else:
                print("Valor inválido.")
        elif opcion == '5':
            val = input("Nuevo Poder (50-100): ")
            if val.isdigit() and 50 <= int(val) <= 100:
                ninja['habilidades']['poder'] = int(val)
            else:
                print("Valor inválido.")
        elif opcion == '6':
            ninja['habilidades']['estilo'] = input("Nuevo estilo de pelea: ")
        elif opcion == '7':
            break
        else:
            print("Opción inválida.")

def eliminar_ninja(dic_ninjas, archivo_ninjas):
    if not dic_ninjas:
        print("No hay ninjas registrados para eliminar.")
        return
    print("\n--- Eliminar Ninja ---")
    print("Ninjas registrados:")
    for id_ninja, datos in dic_ninjas.items():
        print(f"ID: {id_ninja} | Nombre: {datos['nombre']}")
    try:
        id_ninja = int(input("Ingrese el ID del ninja a eliminar: "))
        if id_ninja not in dic_ninjas:
            print("ID no encontrado.")
            return
        nombre = dic_ninjas[id_ninja]['nombre']
        confirmar = input(f"¿Estas seguro de eliminar al ninja {nombre}? (si/no): ").strip().lower()
        if confirmar != 'si':
            print("Eliminación cancelada.")
            return
        archivo_habilidades = f"habilidades_{nombre}.txt"
        ninja_eliminado = dic_ninjas.pop(id_ninja)
        print(f"Ninja {ninja_eliminado['nombre']} eliminado exitosamente.")
        try:
            if os.path.exists(archivo_habilidades):
                os.remove(archivo_habilidades)
                print(f"Archivo de habilidades {archivo_habilidades} eliminado.")
            else:
                print(f"No se encontró el archivo de habilidades para {nombre}.")
        except Exception as e:
            print(f"Error al eliminar el archivo de habilidades: {e}")
        guardar_ninjas(dic_ninjas, archivo_ninjas)
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Error al eliminar el ninja: {e}")

def menu_admin(dic_ninjas):
    id_actual = max(dic_ninjas.keys(), default=0) + 1
    archivo_ninjas = "ninjas.txt"
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Registrar Ninja")
        print("2. Mostrar Todos")
        print("3. Ver árbol de habilidades")
        print("4. Eliminar Ninja")
        print("5. Actualizar Habilidades")
        print("6. Salir")
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
            eliminar_ninja(dic_ninjas, archivo_ninjas)
        elif op == "5":
            mostrar_todos(dic_ninjas)
            t=int(input("Ingrese la id del ninja que quiere actualizar: "))
            actualizar_atributos(dic_ninjas,t)
        elif op == "6":
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
        if nombre == "":
            print("Nombre no valido")
            return
        apellido = input("Ingrese su apellido: ").strip()
        if apellido == "":
            print("Apellido no valido")
            return
        id = int(input("Ingrese su identificación: "))
        id_text = str(id)
        if len(id_text) < 10:
            print("ID invalida")
            return
        edad = int(input("Ingrese su edad: "))
        usuario = input("Ingrese su usuario (correo): ").strip()
        if '@' not in usuario:
            print("usuario no valido")
            return
        elif '.' not in usuario:
            print("Usuario no valido")
            return
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
            puntos = 0
            for linea in info:
                linea = linea.strip()
                if linea.startswith("ID:"):
                    if id_ninja is not None:
                        try:
                            datos_habilidades = leer_habilidades(f"habilidades_{nombre}.txt")
                            arbol = reconstruir_arbol(datos_habilidades)
                        except FileNotFoundError:
                            arbol = crear_arbol_ejemplo()
                        ninjas[id_ninja] = {
                            "nombre": nombre,
                            "habilidades": habilidades,
                            "puntos": puntos,
                            "arbol": arbol
                        }
                    id_ninja = int(linea.split(":")[1].strip())
                    habilidades = {}
                    puntos = 0
                elif linea.startswith("Nombre:"):
                    nombre = linea.split(":")[1].strip()
                elif linea.startswith("Puntos:"):
                    puntos = int(linea.split(":")[1].strip())
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
                try:
                    datos_habilidades = leer_habilidades(f"habilidades_{nombre}.txt")
                    arbol = reconstruir_arbol(datos_habilidades)
                except FileNotFoundError:
                    arbol = crear_arbol_ejemplo()
                ninjas[id_ninja] = {
                    "nombre": nombre,
                    "habilidades": habilidades,
                    "puntos": puntos,
                    "arbol": arbol
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
        if "habilidades" not in n1 or "habilidades" not in n2:
            print("Error: Uno o ambos ninjas no tienen habilidades definidas.")
            return
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
        guardar_ninjas(ninjas, "ninjas.txt")
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
            if "habilidades" not in n1 or "habilidades" not in n2:
                print(f"Error: Uno o ambos ninjas ({n1['nombre']}, {n2['nombre']}) no tienen habilidades definidas.")
                continue
            p1 = sum(n1["habilidades"].get(k, 0) for k in ["fuerza", "agilidad", "resistencia"])
            p2 = sum(n2["habilidades"].get(k, 0) for k in ["fuerza", "agilidad", "resistencia"])
            if p1 > p2:
                print(f"{n1['nombre']} vence a {n2['nombre']}")
                n1['puntos'] += 10
                ganadores.append((id1, n1))
            else:
                print(f"{n2['nombre']} vence a {n1['nombre']}")
                n2['puntos'] += 10
                ganadores.append((id2, n2))
        participantes = ganadores
        ronda += 1
        guardar_ninjas(ninjas, "ninjas.txt")
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
            nombre = input("Nombre del ninja para ver su arbol: ").strip().lower()
            mostrar_arbol_desde_archivo(nombre)
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
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()