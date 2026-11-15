# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Grupo **213023_489** - Curso **Programación (213023)** - UNAD - Fase 4: Componente práctico (Prácticas simuladas).
Sistema orientado a objetos en **Python 3.12**, sin base de datos: toda la información vive en
objetos y listas; solo se usa un archivo para los **logs** de eventos y errores.

## Ejecutar
```bash
python main.py
```
Genera `logs/software_fj.log` y simula 19 operaciones (válidas e inválidas).

## Estructura y responsables (un módulo por integrante)
| Módulo | Contenido | Integrante |
|---|---|---|
| `excepciones.py`, `logger_config.py` | Excepciones personalizadas y archivo de logs | Darwin Alexander Charry Bastos |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` (encapsulación y validaciones) | Angy Paola Gonzalez Cordoba |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` | Isabel Cristina Palacio Ospino |
| `reservas.py` | `Reserva` y `EstadoReserva` (confirmar, cancelar, procesar) | Nelson Daniel Restrepo Rosero |
| `gestor.py`, `main.py`, `README.md` | Gestor con listas internas y simulación | Eliana Andrea Briñez Zambrano |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** los tres servicios sobrescriben `calcular_costo`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados con `@property` y validación en los setters.
- **Sobrecarga (simulada):** `costo_total(horas, impuesto=None, descuento=None, **opciones)`.
- **Excepciones:** personalizadas (`SoftwareFJError` y 7 subclases), `try/except`, `try/except/else`,
  `try/except/finally` y encadenamiento con `raise ... from e`.
- **Logs:** cada evento y error queda en `logs/software_fj.log`.

## Flujo de trabajo en GitHub
Cada integrante edita su módulo desde su propia cuenta de GitHub y guarda sus cambios
con un commit y un mensaje claro (por ejemplo: "Mejora en servicios.py - Isabel").
