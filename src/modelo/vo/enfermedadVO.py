class Enfermedad:
    def __init__(self, id=None, nombre=None):
        self._id = id
        self._nombre = nombre

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    def to_dict(self):
        return {
            'id': self._id,
            'nombre': self._nombre
        }

    def __repr__(self):
        return f"<Enfermedad id={self._id} nombre={self._nombre}>"