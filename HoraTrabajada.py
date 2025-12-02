class HoraTrabajada:
    def __init__(self, id_registro, fecha, horas_trabajadas, descripcion_tareas, id_empleado):
        self._id = id_registro
        self._fecha = fecha
        self._horas_trabajadas = horas_trabajadas
        self._descripcion_tareas = descripcion_tareas
        self._id_empleado = id_empleado

    def get_id(self):
        return self._id
        
    def get_fecha(self):
        return self._fecha
        
    def get_horas_trabajadas(self):
        return self._horas_trabajadas
        
    def get_descripcion_tareas(self):
        return self._descripcion_tareas
        
    def get_id_empleado(self):
        return self._id_empleado

    def set_id(self, id_registro):
        if id_registro and id_registro > 0:
            self._id = id_registro
        else:
            raise ValueError("ID registro debe ser positivo")

    def set_fecha(self, fecha):
        import re
        if fecha and re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            self._fecha = fecha
        else:
            raise ValueError("Fecha debe tener formato YYYY-MM-DD")
        
    def set_horas_trabajadas(self, horas_trabajadas):
        if horas_trabajadas and 0 < horas_trabajadas <= 24:
            self._horas_trabajadas = horas_trabajadas
        else:
            raise ValueError("Horas trabajadas deben estar entre 0 y 24")
        
    def set_descripcion_tareas(self, descripcion_tareas):
        if descripcion_tareas and len(descripcion_tareas.strip()) > 0:
            self._descripcion_tareas = descripcion_tareas.strip()
        else:
            raise ValueError("Descripción tareas no puede estar vacía")
        
    def set_id_empleado(self, id_empleado):
        if id_empleado and id_empleado > 0:
            self._id_empleado = id_empleado
        else:
            raise ValueError("ID empleado debe ser positivo")