# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso **Programación (213023)** - UNAD - Fase 4: Componente práctico (Prácticas simuladas).
Sistema orientado a objetos en **Python 3.12**, sin base de datos: toda la información vive en
objetos y listas; solo se usa un archivo para los **logs** de eventos y errores.

## Ejecutar
```bash
python main.py
```
Genera `logs/software_fj.log` y simula 19 operaciones (válidas e inválidas).

## Estructura y responsables sugeridos (un módulo por integrante)
| Módulo | Contenido | Integrante |
|---|---|---|
| `excepciones.py`, `logger_config.py` | Excepciones personalizadas y archivo de logs | Integrante 1 |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` (encapsulación y validaciones) | Integrante 2 |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` | Integrante 3 |
| `reservas.py` | `Reserva` y `EstadoReserva` (confirmar, cancelar, procesar) | Integrante 4 |
| `gestor.py`, `main.py`, `README.md` | Gestor con listas internas y simulación | Integrante 5 |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** los tres servicios sobrescriben `calcular_costo`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados con `@property` y validación en los setters.
- **Sobrecarga (simulada):** `costo_total(horas, impuesto=None, descuento=None, **opciones)`.
- **Excepciones:** personalizadas (`SoftwareFJError` y 7 subclases), `try/except`, `try/except/else`,
  `try/except/finally` y encadenamiento con `raise ... from e`.
- **Logs:** cada evento y error queda en `logs/software_fj.log`.

## Flujo de trabajo en GitHub
Cada integrante trabaja en su rama (`git checkout -b feature/nombre-modulo`), hace commits con mensajes claros
y abre un Pull Request hacia `main`.
