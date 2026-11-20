"""Pruebas sencillas del módulo de servicios. Ejecutar desde la raíz del proyecto."""

from models.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from exceptions.custom_exceptions import ServicioNoDisponibleError


sala = ReservaSala("Sala A", 20000, 10)
equipo = AlquilerEquipo("Portátil", 15000, "Computador", 5000)
asesoria = AsesoriaEspecializada("Asesoría Python", 30000, "Programación", 10000)

# Casos correctos: comprobamos que el precio sea el esperado.
assert sala.calcular_costo(3) == 60000
assert sala.calcular_costo(3, descuento=10) == 54000
assert equipo.calcular_costo(2) == 35000
assert asesoria.calcular_costo(2) == 70000
assert sala.validar_parametros(2) is True
print("OK: los servicios calculan los precios correctamente")

# Casos incorrectos: el sistema debe rechazar datos inválidos.
errores_controlados = 0

try:
    sala.calcular_costo(-2)
except ValueError:
    errores_controlados += 1
    print("OK: se rechazó una duración negativa")

try:
    ReservaSala("Sala B", 20000, 0)
except ValueError:
    errores_controlados += 1
    print("OK: se rechazó una capacidad incorrecta")

try:
    equipo.calcular_costo(2, descuento=120)
except ValueError:
    errores_controlados += 1
    print("OK: se rechazó un descuento incorrecto")

sala.disponible = False
try:
    sala.calcular_costo(1)
except ServicioNoDisponibleError:
    errores_controlados += 1
    print("OK: se rechazó un servicio no disponible")

assert errores_controlados == 4, "Faltó detectar algún error"
print("Todas las pruebas del módulo pasaron.")
print("El programa terminó correctamente después de los errores.")
