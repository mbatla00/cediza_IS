"""
CONTROLADORES DEL SISTEMA

REGLAS IMPORTANTES (según la profesora):
- Los controladores SOLO trabajan con Value Objects (VO)
- Los controladores NO llaman a DAOs directamente
- Los controladores NO tienen conexiones a la BD
- Los controladores NO tienen SQL
- Los controladores NO tienen lógica de negocio compleja

La lógica de negocio está en src/modelo/servicios/
Los DAOs están en src/modelo/dao/
Los VOs están en src/modelo/vo/

Los controladores son solo un puente entre la VISTA (PySide6) y los SERVICIOS.
"""
from .auth_controller import AuthController
from .admin_controller import AdminController
from .paciente_controller import PacienteController
from .trabajador_controller import TrabajadorController


# Lista de lo que se puede importar desde fuera
__all__ = [
    'AuthController',
    'AdminController', 
    'PacienteController',
    'TrabajadorController'
]