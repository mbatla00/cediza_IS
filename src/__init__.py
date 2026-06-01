"""
PUNTO DE ENTRADA DEL PAQUETE SRC

Este archivo ya NO contiene código de Flask.
Ahora solo expone los controladores y el modelo para que la vista los pueda usar.

La aplicación es de escritorio con PySide6.
"""

# Exponemos los controladores para que la vista pueda importarlos fácilmente
from .controlador import (
    AuthController,
    AdminController,
    PacienteController,
    TrabajadorController
)

# Exponemos el modelo para quien lo necesite
from .modelo import (
    # Factories
    UsuarioFactory,
    # DAOs
    UsuarioDAO,
    PacienteDAO,
    TrabajadorDAO,
    # VOs
    Usuario,
    Paciente,
    Trabajador,
    Admin,
    Auxiliar,
    Coordinador,
    Especialista,
    PacPub,
    PacPri,
    Comentario,
    EvaluacionProfesional,
    Sesion,
    Familiar,
    Cuestionario,
    Pregunta,
    Respuesta
)

__all__ = [
    # Controladores
    'AuthController',
    'AdminController', 
    'PacienteController',
    'TrabajadorController',
    # DAOs
    'UsuarioDAO',
    'PacienteDAO',
    'TrabajadorDAO',
    # VOs
    'Usuario',
    'Paciente',
    'Trabajador',
    'Admin',
    'Auxiliar',
    'Coordinador',
    'Especialista',
    'PacPub',
    'PacPri',
    'Comentario',
    'EvaluacionProfesional',
    'Sesion',
    'Familiar',
    'Cuestionario',
    'Pregunta',
    'Respuesta',
    # Factory
    'UsuarioFactory'
]