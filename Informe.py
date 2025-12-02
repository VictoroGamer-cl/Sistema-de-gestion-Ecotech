class Informe:
    def __init__(self, id_informe, nombre_reporte, tipo_reporte, formato, fecha_generacion, id_administrador):
        self._id = id_informe
        self._nombre_reporte = nombre_reporte
        self._tipo_reporte = tipo_reporte
        self._formato = formato
        self._fecha_generacion = fecha_generacion
        self._id_administrador = id_administrador

    def get_id(self):
        return self._id
        
    def get_nombre_reporte(self):
        return self._nombre_reporte
        
    def get_tipo_reporte(self):
        return self._tipo_reporte
        
    def get_formato(self):
        return self._formato
        
    def get_fecha_generacion(self):
        return self._fecha_generacion
        
    def get_id_administrador(self):
        return self._id_administrador

    def set_id(self, id_informe):
        if id_informe and id_informe > 0:
            self._id = id_informe
        else:
            raise ValueError("ID informe debe ser positivo")

    def set_nombre_reporte(self, nombre_reporte):
        if nombre_reporte and len(nombre_reporte.strip()) >= 3:
            self._nombre_reporte = nombre_reporte.strip()
        else:
            raise ValueError("Nombre reporte debe tener al menos 3 caracteres")
        
    def set_tipo_reporte(self, tipo_reporte):
        tipos_validos = ['empleados', 'proyectos', 'departamentos', 'horas']
        if tipo_reporte and tipo_reporte in tipos_validos:
            self._tipo_reporte = tipo_reporte
        else:
            raise ValueError(f"Tipo reporte debe ser: {', '.join(tipos_validos)}")
        
    def set_formato(self, formato):
        formatos_validos = ['pdf', 'excel', 'csv', 'html']
        if formato and formato in formatos_validos:
            self._formato = formato
        else:
            raise ValueError(f"Formato debe ser: {', '.join(formatos_validos)}")
        
    def set_fecha_generacion(self, fecha_generacion):
        import re
        if fecha_generacion and re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_generacion):
            self._fecha_generacion = fecha_generacion
        else:
            raise ValueError("Fecha generación debe tener formato YYYY-MM-DD")
        
    def set_id_administrador(self, id_administrador):
        if id_administrador and id_administrador > 0:
            self._id_administrador = id_administrador
        else:
            raise ValueError("ID administrador debe ser positivo")