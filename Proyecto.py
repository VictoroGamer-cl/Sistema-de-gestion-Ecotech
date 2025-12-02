class Proyecto:
    def __init__(self, id_proyecto, nombre_proyecto, descripcion, fecha_inicio, id_departamento=None):
        self._id = id_proyecto
        self._nombre_proyecto = nombre_proyecto
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._id_departamento = id_departamento

    def get_id(self):
        return self._id
        
    def get_nombre_proyecto(self):
        return self._nombre_proyecto
        
    def get_descripcion(self):
        return self._descripcion
        
    def get_fecha_inicio(self):
        return self._fecha_inicio
        
    def get_id_departamento(self):
        return self._id_departamento

    def set_id(self, id_proyecto):
        if id_proyecto and id_proyecto > 0:
            self._id = id_proyecto
        else:
            raise ValueError("ID proyecto debe ser positivo")

    def set_nombre_proyecto(self, nombre_proyecto):
        if nombre_proyecto and len(nombre_proyecto.strip()) >= 3:
            self._nombre_proyecto = nombre_proyecto.strip()
        else:
            raise ValueError("Nombre proyecto debe tener al menos 3 caracteres")
        
    def set_descripcion(self, descripcion):
        if descripcion is not None:
            self._descripcion = descripcion
        else:
            raise ValueError("Descripción no puede ser None")
        
    def set_fecha_inicio(self, fecha_inicio):
        import re
        if fecha_inicio and re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_inicio):
            self._fecha_inicio = fecha_inicio
        else:
            raise ValueError("Fecha inicio debe tener formato YYYY-MM-DD")
        
    def set_id_departamento(self, id_departamento):
        if id_departamento is None or (id_departamento and id_departamento > 0):
            self._id_departamento = id_departamento
        else:
            raise ValueError("ID departamento debe ser positivo o None")