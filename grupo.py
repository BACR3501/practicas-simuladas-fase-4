
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACION - CODIGO 213023
# PROYECTO: SISTEMA INTEGRAL SOFTWARE 
# GESTION DE CLIENTES, SERVICIOS Y RESERVAS
# ============================================================

import logging
from abc import ABC, abstractmethod

# CONFIGURACION DEL ARCHIVO DE REGISTRO DE ERRORES
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================================
# 1. EXCEPCIONES PERSONALIZADAS
# ============================================================

class ErrorSistema(Exception):
    pass


class DatoInvalidoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaError(ErrorSistema):
    pass


# ============================================================
# 2. CLASE ABSTRACTA ENTIDAD
# ============================================================

class Entidad(ABC):

    def __init__(self, identificador):
        if not identificador:
            raise DatoInvalidoError("El identificador es obligatorio.")

        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass


# ============================================================
# 3. CLASE CLIENTE
# ============================================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        if len(nombre.strip()) < 2:
            raise DatoInvalidoError("Nombre invalido.")

        if "@" not in correo or "." not in correo:
            raise DatoInvalidoError("Correo electronico invalido.")

        if len(str(telefono)) < 7 or not str(telefono).isdigit():
            raise DatoInvalidoError("Telefono invalido.")

        self._nombre = nombre
        self._correo = correo
        self._telefono = str(telefono)

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def describir(self):
        return f"Cliente: {self.nombre}"


# ============================================================
# 4. CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa):
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa debe ser mayor que cero.")

        self.codigo = codigo
        self.nombre = nombre
        self.tarifa = tarifa
        self.disponible = True

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no esta disponible."
            )

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass


# ============================================================
# 5. SERVICIO DE RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar_disponibilidad()

        if horas <= 0:
            raise DatoInvalidoError("Horas invalidas.")

        subtotal = self.tarifa * horas
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Sala: {self.nombre}"


# ============================================================
# 6. SERVICIO DE ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar_disponibilidad()

        if horas <= 0:
            raise DatoInvalidoError("Horas invalidas.")

        subtotal = self.tarifa * horas * 1.05
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Equipo: {self.nombre}"


# ============================================================
# 7. SERVICIO DE ASESORIAS ESPECIALIZADAS
# ============================================================

class Asesoria(Servicio):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar_disponibilidad()

        if horas <= 0:
            raise DatoInvalidoError("Horas invalidas.")

        subtotal = (self.tarifa * horas) + 20000
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Asesoria: {self.nombre}"


# ============================================================
# 8. CLASE RESERVA
# ============================================================

class Reserva:

    def __init__(self, codigo, cliente, servicio, horas):
        if horas <= 0:
            raise ReservaError("La duracion debe ser mayor que cero.")

        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.costo = 0

    def confirmar(self, impuesto=0.19, descuento=0):
        if self.estado != "PENDIENTE":
            raise ReservaError("La reserva no esta pendiente.")

        self.costo = self.servicio.calcular_costo(
            self.horas, impuesto, descuento
        )

        self.estado = "CONFIRMADA"

        logging.info("Reserva confirmada: %s", self.codigo)

        return self.costo

    def cancelar(self):
        if self.estado != "PENDIENTE":
            raise ReservaError("No se puede cancelar esta reserva.")

        self.estado = "CANCELADA"

        logging.info("Reserva cancelada: %s", self.codigo)

    def procesar(self):
        try:
            return self.confirmar()

        except Exception as error:
            raise ReservaError(
                "Error al procesar la reserva."
            ) from error


# ============================================================
# 9. CLASE GESTOR DEL SISTEMA
# ============================================================

class GestorSistema:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.nombre)
        return "Cliente registrado correctamente."

    def registrar_servicio(self, servicio):
        self.servicios.append(servicio)
        logging.info("Servicio registrado: %s", servicio.nombre)
        return "Servicio registrado correctamente."

    def crear_reserva(self, reserva):
        self.reservas.append(reserva)
        logging.info("Reserva creada: %s", reserva.codigo)
        return "Reserva creada correctamente."


# ============================================================
# 10. FUNCION PARA CONTROLAR ERRORES
# ============================================================

def ejecutar_operacion(nombre, funcion):

    print("\n" + nombre)

    try:
        resultado = funcion()

    except Exception as error:
        print("ERROR CONTROLADO:", error)
        logging.exception("Error en la operacion: %s", nombre)

    else:
        print("RESULTADO:", resultado)

    finally:
        print("Operacion finalizada.")


# ============================================================
# 11. EJECUCION DEL SISTEMA
# ============================================================

def main():

    sistema = GestorSistema()

    print("=" * 55)
    print(" SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
    print("=" * 55)

    # OPERACION 1: REGISTRO DE CLIENTE
    cliente1 = Cliente(
        "C001",
        "Ana Perez",
        "ana@gmail.com",
        "3001234567"
    )

    ejecutar_operacion(
        "1. Registrar cliente",
        lambda: sistema.registrar_cliente(cliente1)
    )

    # OPERACION 2: REGISTRO DE OTRO CLIENTE
    cliente2 = Cliente(
        "C002",
        "Luis Gomez",
        "luis@gmail.com",
        "3101234567"
    )

    ejecutar_operacion(
        "2. Registrar segundo cliente",
        lambda: sistema.registrar_cliente(cliente2)
    )

    # OPERACION 3: CLIENTE CON CORREO INVALIDO
    ejecutar_operacion(
        "3. Registrar cliente con correo invalido",
        lambda: Cliente(
            "C003",
            "Carlos Ruiz",
            "correo_invalido",
            "3001112233"
        )
    )

    # OPERACION 4: CREAR SERVICIO DE SALA
    sala = ReservaSala(
        "S001",
        "Sala de reuniones",
        50000
    )

    ejecutar_operacion(
        "4. Registrar sala",
        lambda: sistema.registrar_servicio(sala)
    )

    # OPERACION 5: CREAR SERVICIO DE EQUIPO
    equipo = AlquilerEquipo(
        "E001",
        "Computador portatil",
        15000
    )

    ejecutar_operacion(
        "5. Registrar equipo",
        lambda: sistema.registrar_servicio(equipo)
    )

    # OPERACION 6: CREAR SERVICIO DE ASESORIA
    asesoria = Asesoria(
        "A001",
        "Asesoria de programacion",
        80000
    )

    ejecutar_operacion(
        "6. Registrar asesoria",
        lambda: sistema.registrar_servicio(asesoria)
    )

    # OPERACION 7: SERVICIO CON TARIFA INVALIDA
    ejecutar_operacion(
        "7. Crear servicio con tarifa invalida",
        lambda: ReservaSala(
            "S002",
            "Sala incorrecta",
            -5000
        )
    )

    # OPERACION 8: CREAR RESERVA
    reserva1 = Reserva(
        "R001",
        cliente1,
        sala,
        2
    )

    ejecutar_operacion(
        "8. Crear reserva",
        lambda: sistema.crear_reserva(reserva1)
    )

    # OPERACION 9: CONFIRMAR RESERVA
    ejecutar_operacion(
        "9. Confirmar reserva",
        lambda: f"Costo: ${reserva1.confirmar():,.2f}"
    )

    # OPERACION 10: RESERVA CON DURACION INVALIDA
    ejecutar_operacion(
        "10. Crear reserva con duracion invalida",
        lambda: Reserva(
            "R002",
            cliente2,
            equipo,
            0
        )
    )

    # OPERACION 11: CREAR SEGUNDA RESERVA
    reserva2 = Reserva(
        "R003",
        cliente2,
        asesoria,
        1
    )

    ejecutar_operacion(
        "11. Crear segunda reserva",
        lambda: sistema.crear_reserva(reserva2)
    )

    # OPERACION 12: CANCELAR RESERVA
    ejecutar_operacion(
        "12. Cancelar reserva",
        lambda: (reserva2.cancelar() or "Reserva cancelada.")
    )

    # OPERACION 13: SERVICIO NO DISPONIBLE
    sala.disponible = False

    reserva3 = Reserva(
        "R004",
        cliente1,
        sala,
        1
    )

    ejecutar_operacion(
        "13. Intentar reservar sala no disponible",
        reserva3.confirmar
    )

    # OPERACION 14: CANCELAR RESERVA CONFIRMADA
    ejecutar_operacion(
        "14. Cancelar reserva confirmada",
        reserva1.cancelar
    )

    # OPERACION 15: CALCULO CON DESCUENTO
    ejecutar_operacion(
        "15. Calcular costo con descuento",
        lambda: (
            f"${equipo.calcular_costo(3, 0.19, 0.10):,.2f}"
        )
    )

    # MOSTRAR RESULTADOS FINALES
    print("\n" + "=" * 55)
    print("RESUMEN DEL SISTEMA")
    print("=" * 55)

    print("Clientes registrados:", len(sistema.clientes))
    print("Servicios registrados:", len(sistema.servicios))
    print("Reservas registradas:", len(sistema.reservas))

    for reserva in sistema.reservas:
        print(
            reserva.codigo,
            "-",
            reserva.cliente.nombre,
            "-",
            reserva.estado
        )

    print("\nSistema ejecutado correctamente.")
    print("Los eventos y errores estan guardados en software_fj.log.")


# ============================================================
# 12. INICIAR PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()
