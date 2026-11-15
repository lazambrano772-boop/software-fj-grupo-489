"""
main.py
Simulación de 19 operaciones (válidas e inválidas) de Software FJ.
El programa NUNCA se detiene: cada operación se ejecuta dentro de ejecutar().
Ejecutar con:  python main.py
"""
from excepciones import SoftwareFJError
from gestor import GestorSoftwareFJ
from logger_config import ARCHIVO_LOG, obtener_logger

logger = obtener_logger()
contador = {"total": 0, "exitosas": 0, "controlados": 0, "inesperados": 0}


def ejecutar(titulo, funcion, *args, **kwargs):
    """Ejecuta una operación con try/except/else/finally y registra el resultado."""
    contador["total"] += 1
    n = contador["total"]
    print(f"\n--- Operación {n:02d}: {titulo}")
    logger.info(f"=== Operación {n:02d}: {titulo}")
    try:
        resultado = funcion(*args, **kwargs)
    except SoftwareFJError as e:                 # Error controlado del dominio
        contador["controlados"] += 1
        logger.error(f"Operación {n:02d} falló (controlado): {e}")
        print(f"    ERROR CONTROLADO -> {e}")
        if e.__cause__ is not None:              # Encadenamiento de excepciones
            print(f"    Causa original  -> {type(e.__cause__).__name__}: {e.__cause__}")
        return None
    except Exception as e:                       # Error inesperado: el sistema sigue
        contador["inesperados"] += 1
        logger.critical(f"Operación {n:02d} error INESPERADO: {type(e).__name__}: {e}")
        print(f"    ERROR INESPERADO -> {type(e).__name__}: {e} (el sistema continúa)")
        return None
    else:
        contador["exitosas"] += 1
        print(f"    OK -> {resultado}")
        return resultado
    finally:
        logger.debug(f"Operación {n:02d} finalizada.")


def flujo_reserva(gestor, id_cliente, id_servicio, horas, **kw):
    """Crea, confirma y procesa una reserva."""
    r = gestor.crear_reserva(id_cliente, id_servicio, horas, **kw)
    gestor.confirmar_reserva(r.id)
    gestor.procesar_reserva(r.id)
    return r


def ocupacion_sin_proteccion(gestor):
    """Función con un bug a propósito (división por cero) para probar errores inesperados."""
    return 100 / (gestor.resumen()["reservas"] - gestor.resumen()["reservas"])


def main():
    logger.info("########## INICIO DE LA SIMULACIÓN SOFTWARE FJ ##########")
    g = GestorSoftwareFJ()
    print("SOFTWARE FJ - Sistema de Gestión de Clientes, Servicios y Reservas")

    # --- Clientes ---
    ana = ejecutar("Registro válido de cliente (Ana)", g.registrar_cliente,
                   nombre="Ana María Pérez", documento="1023456789",
                   email="ana.perez@correo.com", telefono="3001234567")
    carlos = ejecutar("Registro válido de cliente (Carlos)", g.registrar_cliente,
                      nombre="Carlos Rojas", documento="1034567890",
                      email="carlos.rojas@correo.com", telefono="3012345678")
    ejecutar("Registro inválido: correo mal formado", g.registrar_cliente,
             nombre="Pedro Gil", documento="5566778", email="pedro-correo.com", telefono="3105556677")
    ejecutar("Registro inválido: documento duplicado", g.registrar_cliente,
             nombre="Ana Duplicada", documento="1023456789",
             email="otra@correo.com", telefono="3009998877")
    ejecutar("Registro con parámetro faltante (sin teléfono)", g.registrar_cliente,
             nombre="Luis Mora", documento="9988776", email="luis@correo.com")

    # --- Servicios ---
    sala = ejecutar("Creación válida de servicio: sala", g.crear_servicio, "sala",
                    nombre="Sala Innovación", tarifa_hora=80000, capacidad=30)
    equipo = ejecutar("Creación válida de servicio: equipo", g.crear_servicio, "equipo",
                      nombre="Portátiles Pro", tarifa_hora=15000, tipo_equipo="Portátil", cantidad=5)
    asesoria = ejecutar("Creación válida de servicio: asesoría", g.crear_servicio, "asesoria",
                        nombre="Asesoría en Ciberseguridad", tarifa_hora=120000,
                        especialidad="Seguridad", nivel="senior")
    ejecutar("Creación inválida: tarifa negativa", g.crear_servicio, "sala",
             nombre="Sala Defectuosa", tarifa_hora=-5000, capacidad=10)
    ejecutar("Creación inválida: tipo de servicio inexistente", g.crear_servicio, "catering",
             nombre="Catering", tarifa_hora=1000)

    # --- Reservas ---
    ejecutar("Reserva exitosa de sala (3 h, 10 % de descuento)", flujo_reserva,
             g, ana.id, sala.id, 3, descuento=0.10)
    ejecutar("Reserva fallida: duración excesiva (20 h en sala)", g.crear_reserva,
             ana.id, sala.id, 20)
    equipo.deshabilitar()
    ejecutar("Reserva fallida: servicio no disponible", flujo_reserva,
             g, carlos.id, equipo.id, 4)
    equipo.habilitar()
    pend = ejecutar("Reserva de asesoría + cancelación válida",
                    lambda: (lambda r: (g.cancelar_reserva(r.id, "El cliente lo solicitó"), r)[1])(
                        g.crear_reserva(carlos.id, asesoria.id, 2)))
    ejecutar("Operación no permitida: cancelar una reserva ya procesada",
             lambda: (lambda r: (g.cancelar_reserva(r.id), r)[1])(
                 flujo_reserva(g, ana.id, asesoria.id, 1, urgente=True)))
    ejecutar("Cálculo inconsistente: descuento del 150 %", flujo_reserva,
             g, carlos.id, sala.id, 2, descuento=1.5)
    ejecutar("Reserva con cliente inexistente", g.crear_reserva, "CLI-999", sala.id, 2)

    # --- Extras ---
    ejecutar("Sobrecarga de costo_total (4 variantes)", lambda: {
        "solo_horas": sala.costo_total(3),
        "con_impuesto_8%": sala.costo_total(3, 0.08),
        "impuesto_y_descuento": sala.costo_total(3, 0.19, 0.10),
        "con_catering": sala.costo_total(3, con_catering=True)})
    ejecutar("Error inesperado (división por cero sin proteger)", ocupacion_sin_proteccion, g)

    # --- Resumen ---
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    for linea in g.listar_reservas():
        print("  ", linea)
    print(f"\nTotal operaciones     : {contador['total']}")
    print(f"Exitosas              : {contador['exitosas']}")
    print(f"Errores controlados   : {contador['controlados']}")
    print(f"Errores inesperados   : {contador['inesperados']}")
    print(f"Estado del sistema    : {g.resumen()}")
    print(f"Log de eventos/errores: {ARCHIVO_LOG}")
    logger.info(f"########## FIN DE LA SIMULACIÓN: {contador} ##########")


if __name__ == "__main__":
    main()
