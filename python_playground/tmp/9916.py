from typing import NamedTuple

class Medicamento(NamedTuple):
    nombre : str 
    cantidad : int
    precio : float
    stock_minimo : int

    def __str__(self):
        return f"Nombre: {self.nombre} Cantidad: {self.cantidad} Precio: {self.precio} Stock mínimo: {self.stock_minimo}"

    def __repr__(self):
        return f"Nombre: {self.nombre} Cantidad: {self.cantidad} Precio: {self.precio} Stock mínimo: {self.stock_minimo}"

medicamentos = [
    Medicamento(nombre = "Paracetamol", cantidad = 100, precio = 5, stock_minimo = 50),
    Medicamento(nombre = "Ibuprofeno", cantidad = 50, precio = 7, stock_minimo = 20),
    Medicamento(nombre = "Aspirina", cantidad = 80, precio = 4, stock_minimo = 40),
    Medicamento(nombre = "Amoxicilina", cantidad = 10, precio = 10, stock_minimo = 40),
]

def agregar_medicamento(nombre, cantidad, precio, stock_minimo):
    medicamentos.append(Medicamento(nombre, cantidad, precio, stock_minimo))
    print(f"Medicamento agregado al stock. {nombre}")

# Función para actualizar la cantidad de medicamentos en stock
def actualizar_cantidad(nombre : str, new_cantidad : int):
    for medicamento in medicamentos:
        if medicamento.nombre == nombre:
            medicamento = medicamento._replace(cantidad = new_cantidad)
            print(f"Cantidad actualizada. {medicamento.nombre}")
            print(medicamento.cantidad)
            return
    print("El medicamento no está en el stock.")

def buscar_medicamento(nombre : str):
    for medicamento in medicamentos:
        if medicamento.nombre == nombre:
            print(f"Nombre: {medicamento.nombre}")
            print(f"Cantidad: {medicamento.cantidad}")
            print(f"Precio: {medicamento.precio}")
            return
    print("El medicamento no está en el stock.")

# Recorrer la lista de medicamentos y establecer la cantidad actual en cero
def listar_medicamentos():
    for medicamento in medicamentos:
        print(f"Nombre: {medicamento.nombre}")
        print(f"Cantidad: {medicamento.cantidad}")
        print(f"Precio: {medicamento.precio}")
        print(f"Stock mínimo: {medicamento.stock_minimo}")
        print("--------------------------")

# Función para generar una alerta cuando el stock de un medicamento está por debajo del mínimo
def generar_alerta(nombre : str):
    for medicamento in medicamentos:
        if medicamento.nombre == nombre and medicamento.cantidad < medicamento.stock_minimo:
            print(f"ALERTA: El stock de {medicamento.nombre} está por debajo del mínimo.\nStock actual: {medicamento.cantidad}") 

# Función para realizar un pedido de medicamentos cuando el stock está por debajo del mínimo
def realizar_pedido(nombre):
    for medicamento in medicamentos:
        if medicamento.nombre == nombre and medicamento.cantidad < medicamento.stock_minimo:
            print(f"Realizando un pedido de {medicamento.nombre} al proveedor... stocke mínimo: {medicamento.stock_minimo}") 
            print(f"Pedido realizado. {medicamento.nombre} cantidad: {medicamento.stock_minimo - medicamento.cantidad}")
    # Código para enviar el pedido al proveedor

"""
while True:
    print("1. Agregar medicamento")
    print("2. Actualizar cantidad")
    print("3. Buscar medicamento")
    print("4. Listar medicamentos")
    print("5. Salir")
    opcion = int(input("Selecciona una opción: "))
    if opcion == 1:
        print("Agregar Medicamento: ")
        nombre = input("Nombre del medicamento: ")
        cantidad = int(input("Cantidad disponible: "))
        precio = float(input("Precio unitario: "))
        stock_minimo = int(input("Stock mínimo: "))
        agregar_medicamento(nombre, cantidad, precio, stock_minimo)
    elif opcion == 2:
        print("Actualizar: ")
        nombre = input("Nombre del medicamento: ")
        cantidad = int(input("Cantidad a agregar: "))
        precio = float(input("Precio unitario: "))
        actualizar_cantidad(nombre, 10)
    elif opcion == 3:
        nombre = input("Buscar: ")
        buscar_medicamento(nombre)
    elif opcion == 4:
        listar_medicamentos()
    elif opcion == 5:
        break
"""

if __name__ == "__main__":

# Ejemplo de uso: Actualizar el stock de paracetamol
    actualizar_cantidad(nombre = "Paracetamol", new_cantidad= 100)

# Ejemplo de uso: Generar una alerta si el stock de ibuprofeno está por debajo del mínimo
    for medicamento in medicamentos:
        generar_alerta(medicamento.nombre)

# Ejemplo de uso: Realizar un pedido de amoxicilina si el stock está por debajo del mínimo
    for medicamento in medicamentos:
        if medicamento.nombre == "Amoxicilina":
            realizar_pedido(medicamento.nombre)
# Recorrer la lista de medicamentos y establecer la cantidad actual en cero
for medicamento in medicamentos:
    actualizar_cantidad(medicamento.nombre, new_cantidad = 0)

