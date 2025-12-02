class EcoTech:
    def __init__(self, idEmpleado, nombreEmpleado, direccionEmpleado, telefonoEmpleado, 
                 mailEmpleado, fechaInicioContrato, salarioEmpleado, idDepartamento=None, idAdministrador=None):
        self._id = idEmpleado
        self._nombre = nombreEmpleado
        self._direccion = direccionEmpleado
        self._telefono = telefonoEmpleado
        self._mail = mailEmpleado
        self._fecha_inicio = fechaInicioContrato
        self._salario = salarioEmpleado
        self._id_departamento = idDepartamento
        self._id_administrador = idAdministrador

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_direccion(self):
        return self._direccion

    def get_telefono(self):
        return self._telefono

    def get_mail(self):
        return self._mail

    def get_fecheIC(self):
        return self._fecha_inicio

    def get_salario(self):
        return self._salario

    def get_id_departamento(self):
        return self._id_departamento

    def get_id_administrador(self):
        return self._id_administrador


    def set_id(self, id_empleado):
        if id_empleado and id_empleado > 0:
            self._id = id_empleado
        else:
            raise ValueError("ID debe ser positivo")

    def set_nombre(self, nombre):
        if nombre and len(nombre.strip()) >= 2:
            self._nombre = nombre.strip()
        else:
            raise ValueError("Nombre debe tener al menos 2 caracteres")

    def set_direccion(self, direccion):
        self._direccion = direccion

    def set_telefono(self, telefono):
        if telefono and len(str(telefono)) <= 12 and str(telefono).isdigit():
            self._telefono = telefono
        else:
            raise ValueError("Teléfono debe tener máximo 12 dígitos")

    def set_mail(self, mail):
        import re
        if mail and re.match(r'^[a-zA-Z0-9._%+-]+@ecotech\.cl$', mail):
            self._mail = mail
        else:
            raise ValueError("Email debe usar dominio @ecotech.cl")

    def set_fecheIC(self, fecha):
        import re
        if fecha and re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            self._fecha_inicio = fecha
        else:
            raise ValueError("Fecha debe tener formato YYYY-MM-DD")

    def set_salario(self, salario):
        if salario and salario > 0:
            self._salario = salario
        else:
            raise ValueError("Salario debe ser positivo")

    def set_id_departamento(self, id_departamento):
        self._id_departamento = id_departamento

    def set_id_administrador(self, id_administrador):
        if id_administrador and id_administrador > 0:
            self._id_administrador = id_administrador
        else:
            raise ValueError("ID administrador debe ser positivo")

    def __str__(self):
        return f"ID: {self._id}\nNombre: {self._nombre}\nDirección: {self._direccion}\nTeléfono: {self._telefono}\nEmail: {self._mail}\nFecha Inicio Contrato: {self._fecha_inicio}\nSalario: {self._salario}\nID Departamento: {self._id_departamento}"