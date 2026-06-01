"""
MODELO DEL SISTEMA

Contiene:
- DAOs: Acceso a datos (cada DAO tiene sus queries arriba)
- VOs: Value Objects (solo getters, sin setters)
- Factories: Patrón factory para crear objetos
- Servicios: Lógica de negocio (lo nuevo que añadimos)
- Conexión: Conexión a BD con patrón Singleton
"""

# Factories
from .factories import UsuarioFactory

# DAOs
from .dao import (
    UsuarioDAO, PacienteDAO, TrabajadorDAO,
    AdministradorDAO, AuxiliarDAO, CoordinadorDAO, EspecialistaDAO,
    PacPubDAO, PacPriDAO, ComentarioDAO, EvaluacionProfesionalDAO,
    SesionDAO, FamiliarDAO, CuestionarioDAO, PreguntaDAO, RespuestaDAO, EnfermedadDAO, PacienteEnfermedadDAO
)

# VOs
from .vo import (
    Usuario, Paciente, Trabajador, Admin, Auxiliar, Coordinador, Especialista,
    PacPub, PacPri, Comentario, EvaluacionProfesional, Sesion, Familiar,
    Cuestionario, Pregunta, Respuesta, Enfermedad, PacienteEnfermedad
)


# Servicios (nuevo)
from .logica import (
    UsuarioService, PacienteService, TrabajadorService, AuthService,
    EnfermedadService, FamiliarService, ComentarioService,
    EvaluacionService, SesionService, CuestionarioService, RespuestaService
)


__all__ = [
    # Factories
    'UsuarioFactory',
    # DAOs
    'UsuarioDAO', 'PacienteDAO', 'TrabajadorDAO',
    'AdministradorDAO', 'AuxiliarDAO', 'CoordinadorDAO', 'EspecialistaDAO',
    'PacPubDAO', 'PacPriDAO', 'ComentarioDAO', 'EvaluacionProfesionalDAO',
    'SesionDAO', 'FamiliarDAO', 'CuestionarioDAO', 'PreguntaDAO', 'RespuestaDAO',
    # VOs
    'Usuario', 'Paciente', 'Trabajador', 'Admin', 'Auxiliar', 'Coordinador', 'Especialista',
    'PacPub', 'PacPri', 'Comentario', 'EvaluacionProfesional', 'Sesion', 'Familiar',
    'Cuestionario', 'Pregunta', 'Respuesta',
    # Servicios
    'UsuarioService', 'PacienteService', 'TrabajadorService', 'AuthService',
    'EnfermedadService', 'FamiliarService', 'ComentarioService',
    'EvaluacionService', 'SesionService', 'CuestionarioService', 'RespuestaService'
]

