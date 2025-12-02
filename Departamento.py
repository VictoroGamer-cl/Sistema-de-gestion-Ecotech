class Departamento:
    def __init__(self, id_departamento, nombre_departamento, id_gerente, nombre_gerente):
        self._id = id_departamento
        self._nombre = nombre_departamento
        self._id_gerente = id_gerente
        self._nombre_gerente = nombre_gerente
        
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_id_gerente(self):
        return self._id_gerente

    def get_nombre_gerente(self):
        return self._nombre_gerente

    # SETTERS
    def set_id(self, id_departamento):
        if id_departamento and id_departamento > 0:
            self._id = id_departamento
        else:
            raise ValueError("ID departamento debe ser positivo")

    def set_nombre(self, nombre_departamento):
        if nombre_departamento and len(nombre_departamento.strip()) >= 3:
            self._nombre = nombre_departamento.strip()
        else:
            raise ValueError("Nombre departamento debe tener al menos 3 caracteres")

    def set_id_gerente(self, id_gerente):
        if id_gerente and id_gerente > 0:
            self._id_gerente = id_gerente
        else:
            raise ValueError("ID gerente debe ser positivo")

    def set_nombre_gerente(self, nombre_gerente):
        if nombre_gerente and len(nombre_gerente.strip()) >= 2:
            self._nombre_gerente = nombre_gerente.strip()
        else:
            raise ValueError("Nombre gerente debe tener al menos 2 caracteres")

    def __str__(self):
        return f"ID: {self._id}\nNombre: {self._nombre}\nID Gerente: {self._id_gerente}\nNombre Gerente: {self._nombre_gerente}"