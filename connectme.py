import csv
import os

ARCHIVO = "contactos.csv"

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        contactos = list(csv.DictReader(f))
else:
    contactos = []

while True:
    print("\n===== CONNECTME - DIRECTORIO DE CONTACTOS =====")
    print("1. Registrar contacto")
    print("2. Buscar contacto")
    print("3. Listar contactos")
    print("4. Eliminar contacto")
    print("5. Salir")

    op = input("Seleccione una opción: ")

    if op == "1":
        nombre = input("Nombre: ")
        telefono = input("Teléfono: ")
        correo = input("Correo: ")
        cargo = input("Cargo: ")

        if any(c["correo"] == correo for c in contactos):
            print("Ese correo ya está registrado.")
            continue

        contactos.append({"nombre": nombre, "telefono": telefono, "correo": correo, "cargo": cargo})
        print("Contacto agregado.")

    elif op == "2":
        criterio = input("Buscar por nombre o correo: ").lower()
        encontrados = [c for c in contactos if criterio in c["nombre"].lower() or criterio == c["correo"].lower()]
        if encontrados:
            for c in encontrados:
                print(f"- {c['nombre']} | {c['telefono']} | {c['correo']} | {c['cargo']}")
        else:
            print("No se encontró ningún contacto.")

    elif op == "3":
        if not contactos:
            print("No hay contactos registrados.")
        else:
            print("\nLista de contactos:")
            for c in contactos:
                print(f"- {c['nombre']} | {c['telefono']} | {c['correo']} | {c['cargo']}")

    elif op == "4":
        correo = input("Correo del contacto a eliminar: ")
        nuevos = [c for c in contactos if c["correo"] != correo]
        if len(nuevos) == len(contactos):
            print(" No existe ese contacto.")
        else:
            contactos = nuevos
            print(" Contacto eliminado.")

    elif op == "5":
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "telefono", "correo", "cargo"])
            writer.writeheader()
            writer.writerows(contactos)
        print("Saliendo del programa")
        break
    else:
        print("Opción no existente.")
