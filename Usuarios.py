class Usuario:
    def __init__(self, id_usuario, username, contraseña, modulos, id_empleado):
        self._id = id_usuario
        self._username = username
        self._contraseña = contraseña
        self._modulos = modulos
        self._id_empleado = id_empleado


    def get_id(self):
        return self._id

    def get_username(self):
        return self._username

    def get_contraseña(self):
        return self._contraseña

    def get_modulos(self):
        return self._modulos

    def get_id_empleado(self):
        return self._id_empleado

    def set_id(self, id_usuario):
        if id_usuario and id_usuario > 0:
            self._id = id_usuario
        else:
            raise ValueError("ID usuario debe ser positivo")

    def set_username(self, username):
        if username and len(username.strip()) >= 3:
            self._username = username.strip()
        else:
            raise ValueError("Username debe tener al menos 3 caracteres")

    def set_contraseña(self, contraseña):
        if contraseña and len(contraseña) >= 4:
            self._contraseña = contraseña
        else:
            raise ValueError("Contraseña debe tener al menos 4 caracteres")

    def set_modulos(self, modulos):
        if modulos and len(modulos.strip()) > 0:
            self._modulos = modulos.strip()
        else:
            raise ValueError("Módulos no pueden estar vacíos")

    def set_id_empleado(self, id_empleado):
        if id_empleado and id_empleado > 0:
            self._id_empleado = id_empleado
        else:
            raise ValueError("ID empleado debe ser positivo")

    def __str__(self):
        return f"ID: {self._id}\nUsername: {self._username}\nMódulos: {self._modulos}\nID Empleado: {self._id_empleado}"