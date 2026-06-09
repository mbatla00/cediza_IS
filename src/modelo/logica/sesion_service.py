"""
SERVICIO DE SESIONES
"""
from src.modelo.dao import SesionDAO
from src.modelo.vo import Sesion
from datetime import date


class SesionService:

    @staticmethod
    def obtener_por_especialista(especialista: str) -> list:
        return SesionDAO.get_by_especialista(especialista)

    @staticmethod
    def obtener_por_paciente(paciente: str) -> list:
        return SesionDAO.get_by_paciente(paciente)

    @staticmethod
    def obtener_por_id(id_sesion: int):
        return SesionDAO.get_by_id(id_sesion)

    @staticmethod
    def crear(datos: dict) -> tuple[bool, str]:
        sesion = Sesion(
            Paciente=datos.get('paciente'),
            Especialista=datos.get('especialista'),
            comentarios=datos.get('comentarios', ''),
            Fecha=datos.get('fecha'),
            Hora=datos.get('hora')
        )
        if SesionDAO.create(sesion):
            return True, "Sesión creada correctamente"
        return False, "Error al crear sesión"

    @staticmethod
    def actualizar(id_sesion: int, datos: dict, especialista: str) -> tuple[bool, str]:
        sesion = SesionDAO.get_by_id(id_sesion)
        if not sesion:
            return False, "Sesión no encontrada"
        if sesion.especialista != especialista:
            return False, "No puedes editar sesiones de otro especialista"

        sesion_actualizada = Sesion(
            idSesion=id_sesion,
            Paciente=sesion.paciente,
            Especialista=sesion.especialista,
            comentarios=datos.get('comentarios', sesion.comentarios),
            Fecha=datos.get('fecha', sesion.fecha),
            Hora=datos.get('hora', sesion.hora)
        )

        if SesionDAO.update(sesion_actualizada):
            return True, "Sesión actualizada correctamente"
        return False, "Error al actualizar sesión"

    @staticmethod
    def eliminar(id_sesion: int, especialista: str) -> tuple[bool, str]:
        sesion = SesionDAO.get_by_id(id_sesion)
        if not sesion:
            return False, "Sesión no encontrada"
        if sesion.especialista != especialista:
            return False, "No puedes eliminar sesiones de otro especialista"

        hoy = date.today()
        if sesion.fecha and sesion.fecha < hoy:
            return False, "No se pueden eliminar sesiones pasadas"

        if SesionDAO.delete(id_sesion):
            return True, "Sesión eliminada correctamente"
        return False, "Error al eliminar sesión"