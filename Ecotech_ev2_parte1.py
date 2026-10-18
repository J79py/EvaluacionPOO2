import sqlite3
from datetime import date
from typing import List

# =====================================================================
# CLASES BASE Y HERENCIA (PASO 2: PRINCIPIOS DE POO)
# =====================================================================

class Empleado:
    """Clase base que encapsula los datos comunes de todo el personal."""
    def __init__(self, id_empleado: str, nombre: str, salario_base: float):
        # Atributos privados (Encapsulamiento estricto con doble guion bajo)
        self.__id_empleado = id_empleado
        self.__nombre = nombre
        self.__salario_base = salario_base

    # Métodos de acceso públicos (Getters) para proteger los atributos privados
    def get_id_empleado(self) -> str:
        return self.__id_empleado

    def get_nombre(self) -> str:
        return self.__nombre

    def get_salario_base(self) -> float:
        return self.__salario_base

    def calcular_pago(self) -> float:
        return self.__salario_base


class EmpleadoContratista(Empleado):
    """Subclase que aplica Herencia para evitar duplicación de código."""
    def __init__(self, id_empleado: str, nombre: str, salario_base: float, tarifa_hora: float):
        # Reutiliza el constructor de la clase padre (Empleado)
        super().__init__(id_empleado, nombre, salario_base)
        self.__tarifa_hora = tarifa_hora

    def calcular_pago_por_horas(self, horas: int) -> float:
        """Lógica especializada reutilizando el salario base del padre."""
        return self.get_salario_base() + (horas * self.__tarifa_hora)

# MODELADO DE RELACIONES

class RegistroHora:
    """Clase asociativa entre Empleado y Proyecto para dar trazabilidad."""
    def __init__(self, fecha: date, cantidad_horas: int, empleado: Empleado):
        self.__fecha = fecha
        self.__cantidad_horas = cantidad_horas
        self.__empleado = empleado

    def get_cantidad_horas(self) -> int:
        return self.__cantidad_horas


class Informe:
    """Clase dependiente de Proyecto (Relación de Composición)."""
    def __init__(self, id_informe: str, contenido: str):
        self.__id_informe = id_informe
        self.__contenido = contenido

class Proyecto:
    """Clase que gestiona iniciativas y sus colecciones tipadas."""
    def __init__(self, id_proyecto: str, nombre_proyecto: str):
        self.__id_proyecto = id_proyecto
        self.__nombre_proyecto = nombre_proyecto
        self.__asociaciones_horas: List[RegistroHora] = []
        self.__informes: List[Informe] = []

    def registrar_horas(self, fecha: date, horas: int, empleado: Empleado) -> None:
        """Método original estable y directo."""
        nuevo_registro = RegistroHora(fecha, horas, empleado)
        self.__asociaciones_horas.append(nuevo_registro)
        print(f"   [OK] Horas registradas: {horas} hrs para {empleado.get_nombre()}")

    def calcular_total_horas(self) -> int:
        return sum(reg.get_cantidad_horas() for reg in self.__asociaciones_horas)

class Departamento:
    """Clase que agrupa empleados (Relación de Agregación)."""
    def __init__(self, id_departamento: str, nombre_departamento: str):
        self.__id_departamento = id_departamento
        self.__nombre_departamento = nombre_departamento
        self.__empleados: List[Empleado] = []

    def asignar_empleado(self, empleado: Empleado) -> None:
        if empleado not in self.__empleados:
            self.__empleados.append(empleado)
            print(f"   [OK] {empleado.get_nombre()} asignado a {self.__nombre_departamento}")

# CONEXIÓN A LA BASE DE DATOS

class ConexionBaseDatos:
    """Clase encargada de validar la viabilidad técnica de la persistencia."""
    def __init__(self, nombre_bd: str = "ecotech_solutions.db"):
        self.__nombre_bd = nombre_bd

    def verificar_conexion(self) -> bool:
        """Establece una conexión de prueba con la librería oficial sqlite3."""
        conexion = None
        try:
            conexion = sqlite3.connect(self.__nombre_bd)
            cursor = conexion.cursor()
            
            # Crear una tabla de prueba técnica
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS control_conexion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estado TEXT,
                    fecha TEXT
                )
            """)
            cursor.execute("INSERT INTO control_conexion (estado, fecha) VALUES (?, ?)", 
                           ("Conexion Exitosa", str(date.today())))
            conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return False
        finally:
            if conexion:
                conexion.close()

# BLOQUE DE EJECUCIÓN 

if __name__ == "__main__":
    print("==================================================")
    print("--- INICIANDO PROTOTIPO ECOTECH SOLUTIONS ---")
    print("==================================================")
    
    # Pruebas Paso 3: Base de Datos
    print("\n[Paso 3] Ejecutando verificación de persistencia...")
    db = ConexionBaseDatos()
    if db.verificar_conexion():
        print("   [ÉXITO] ¡Conexión establecida correctamente con sqlite3!")
    else:
        print("   [FALLO] No se pudo conectar a la base de datos.")

    # Pruebas Pasos 1 y 2: POO y Relaciones
    print("\n[Pasos 1 y 2] Instanciando objetos del dominio...")
    
    # Creación de Departamento y Personal (Demostrando Herencia)
    depto_ti = Departamento("D01", "Tecnología de la Sostenibilidad")
    empleado_planta = Empleado("E01", "Ana Gomez", 3200.0)
    empleado_externo = EmpleadoContratista("E02", "Carlos Ruiz", 1200.0, 30.0)
    
    # Agregar personal (Agregación)
    depto_ti.asignar_empleado(empleado_planta)
    depto_ti.asignar_empleado(empleado_externo)
    
    # Registrar jornadas en proyectos (Asociación y Trazabilidad)
    print("\n[Control de Gestión] Registrando actividades en proyectos...")
    proyecto_solar = Proyecto("P10", "Paneles Inteligentes Atacama")
    proyecto_solar.registrar_horas(date(2026, 10, 15), 8, empleado_planta)
    proyecto_solar.registrar_horas(date(2026, 10, 16), 6, empleado_externo)
    
    # Mostrar resultados consolidados (Reporte Confiable)
    print(f"\n[Reporte Final] Total horas acumuladas: {proyecto_solar.calcular_total_horas()} hrs.")
    print("==================================================")
