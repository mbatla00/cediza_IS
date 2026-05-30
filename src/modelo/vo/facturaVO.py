class Factura:
    """VO para la factura de un paciente en una fecha"""
    
    def __init__(self, codigoFactura=None, Paciente=None, Administrador=None,
                 fechaEmision=None, importeTotal=0.00, estadoPago='pendiente'):
        self._codigoFactura = codigoFactura
        self._paciente = Paciente
        self._administrador = Administrador
        self._fechaEmision = None
        self._importeTotal = importeTotal
        self._estadoPago = estadoPago
        if fechaEmision:
            self.fechaEmision = fechaEmision

    @property
    def codigoFactura(self):
        return self._codigoFactura

    @property
    def paciente(self):
        return self._paciente

    @property
    def administrador(self):
        return self._administrador

    @property
    def fechaEmision(self):
        return self._fechaEmision

    @property
    def importeTotal(self):
        return self._importeTotal

    @property
    def estadoPago(self):
        return self._estadoPago

    def to_dict(self):
        return {
            'codigoFactura': self.codigoFactura,
            'paciente': self.paciente,
            'administrador': self.administrador,
            'fechaEmision': str(self.fechaEmision) if self.fechaEmision else None,
            'importeTotal': float(self.importeTotal),
            'estadoPago': self.estadoPago
        }

    def __repr__(self):
        return f"<Factura codigo={self.codigoFactura} paciente={self.paciente} estado={self.estadoPago}>"