"""Simulación de 12 operaciones del sistema Software FJ."""
from gestor import GestorFJ  # Gestor principal
from logger import obtener_logger  # Logger del sistema
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio  # Servicios


def mostrar(numero, titulo, resultado):  # Imprime el resultado de cada operación
    estado = "OK" if resultado not in (None, False) else "ERROR CONTROLADO (ver logs/eventos.log)"  # Estado
    print(f"Operación {numero:02d} - {titulo}: {estado}")  # Línea de resumen


def main():  # Función principal
    log = obtener_logger()  # Logger
    log.info("===== INICIO DE LA SIMULACIÓN SOFTWARE FJ =====")  # Marca de inicio
    g = GestorFJ()  # Gestor con listas internas

    # 1. Cliente válido
    ana = g.registrar_cliente(nombre="Ana Torres", correo="ana@correo.com", telefono="3001234567")
    mostrar(1, "Registrar cliente válido", ana)
    # 2. Cliente con correo inválido
    mostrar(2, "Cliente con correo inválido", g.registrar_cliente(nombre="Luis Pérez", correo="luis-correo", telefono="3112223344"))
    # 3. Cliente con parámetro faltante
    mostrar(3, "Cliente sin teléfono", g.registrar_cliente(nombre="Marta Gómez", correo="marta@correo.com"))
    # 4. Servicio sala válido
    sala = g.crear_servicio(ReservaSala, nombre="Sala Ejecutiva", tarifa=50000, capacidad=10)
    mostrar(4, "Crear servicio de sala", sala)
    # 5. Servicio equipo con tarifa negativa
    mostrar(5, "Equipo con tarifa negativa", g.crear_servicio(AlquilerEquipo, nombre="Portátil", tarifa=-100))
    # 6. Asesoría válida
    asesoria = g.crear_servicio(AsesoriaEspecializada, nombre="Arquitectura de Software", tarifa=80000, nivel="senior")
    mostrar(6, "Crear asesoría senior", asesoria)
    # 7. Reserva exitosa
    r1 = g.crear_reserva(ana, sala, 3)
    mostrar(7, "Reserva exitosa", r1)
    # 8. Reserva con servicio no disponible
    equipo = g.crear_servicio(AlquilerEquipo, nombre="Proyector", tarifa=40000, cantidad=2, disponible=False)
    mostrar(8, "Reserva de servicio no disponible", g.crear_reserva(ana, equipo, 2))
    # 9. Procesar reserva con descuento e impuesto (sobrecarga por parámetros opcionales)
    costo = g.procesar_reserva(r1, impuesto=0.19, descuento=0.10)
    mostrar(9, f"Procesar reserva con descuento (costo={costo})", costo)
    # 10. Cancelar reserva ya procesada (operación no permitida)
    mostrar(10, "Cancelar reserva ya procesada", g.cancelar_reserva(r1))
    # 11. Reserva con cliente None
    mostrar(11, "Reserva con cliente None", g.crear_reserva(None, asesoria, 2))
    # 12. Reserva con duración inválida (excepción encadenada)
    mostrar(12, "Asesoría de 20 horas", g.crear_reserva(ana, asesoria, 20))
    # 13. Instanciar clase abstracta
    mostrar(13, "Instanciar Servicio abstracto", g.crear_servicio(Servicio, nombre="X", tarifa=10))

    # Demostración de sobrecarga de cálculo de costos
    print("\nVariantes de calcular_costo en la sala (3 h):")
    print("  Solo duración:           ", sala.calcular_costo(3))
    print("  Con impuesto 8 %:        ", sala.calcular_costo(3, 0.08))
    print("  Con impuesto y descuento:", sala.calcular_costo(3, 0.19, 0.15))

    print(f"\nResumen: {len(g.clientes)} clientes, {len(g.servicios)} servicios, {len(g.reservas)} reservas.")
    log.info("===== FIN DE LA SIMULACIÓN: el sistema continuó estable =====")  # Marca de fin
    print("La aplicación terminó sin interrupciones. Revise logs/eventos.log")


if __name__ == "__main__":  # Punto de entrada
    main()  # Ejecuta la simulación
