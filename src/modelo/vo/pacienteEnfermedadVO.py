class PacienteEnfermedad:
    def __init__(self, paciente=None, enfermedad_id=None):
        self._paciente = paciente
        self._enfermedad_id = enfermedad_id

    @property
    def paciente(self):
        return self._paciente

    @property
    def enfermedad_id(self):
        return self._enfermedad_id

    def to_dict(self):
        return {
            'paciente': self._paciente,
            'enfermedad_id': self._enfermedad_id
        }

    def __repr__(self):
        return f"<PacienteEnfermedad paciente={self._paciente} enfermedad={self._enfermedad_id}>"