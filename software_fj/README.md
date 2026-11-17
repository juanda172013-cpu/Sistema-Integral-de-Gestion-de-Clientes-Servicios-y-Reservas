# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas
Curso Programación 213023 – UNAD – Fase 4 (POO y manejo de excepciones). Sin base de datos.

## Ejecución
    python main.py
El registro de eventos y errores queda en `logs/eventos.log`.

## Módulos
| Archivo | Contenido |
|---|---|
| excepciones.py | Jerarquía de excepciones personalizadas |
| logger.py | Configuración del archivo de logs |
| entidades.py | `EntidadBase` (abstracta) y `Cliente` |
| servicios.py | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| reserva.py | `Reserva` (confirmar, cancelar, procesar) |
| gestor.py | Listas internas y operaciones protegidas |
| main.py | Simulación de 13 operaciones válidas e inválidas |
