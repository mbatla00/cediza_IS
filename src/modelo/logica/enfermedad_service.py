"""
SERVICIO DE ENFERMEDADES
"""
from src.modelo.dao import EnfermedadDAO
from src.modelo.vo.enfermedadVO import Enfermedad


class EnfermedadService:

    @staticmethod
    def listar_todas() -> list:
        return EnfermedadDAO.get_all()

    @staticmethod
    def crear(nombre: str) -> tuple[bool, str, int | None]:
        if not nombre or not nombre.strip():
            return False, "El nombre de la enfermedad es obligatorio", None
        enfermedad = Enfermedad(nombre=nombre.strip())
        if EnfermedadDAO.create(enfermedad):
            return True, "Enfermedad creada", None
        return False, "Error al crear la enfermedad", None

    @staticmethod
    def asignar_a_paciente(paciente: str, enfermedad_id: int) -> bool:
        return EnfermedadDAO.add_to_paciente(paciente, enfermedad_id)

    @staticmethod
    def eliminar_de_paciente(paciente: str, enfermedad_id: int) -> bool:
        return EnfermedadDAO.remove_from_paciente(paciente, enfermedad_id)