class Administrador:
    def __init__(self, id_administrador, username, password, email, nivel_acceso):
        self._id = id_administrador
        self._username = username
        self._password = password
        self._email = email
        self._nivel_acceso = nivel_acceso

    def get_id(self):
        return self._id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_email(self):
        return self._email

    def get_nivel_acceso(self):
        return self._nivel_acceso

    def set_id(self, id_administrador):
        if id_administrador and id_administrador > 0:
            self._id = id_administrador
        else:
            raise ValueError("ID administrador debe ser positivo")

    def set_username(self, username):
        if username and len(username.strip()) >= 3:
            self._username = username.strip()
        else:
            raise ValueError("Username debe tener al menos 3 caracteres")

    def set_password(self, password):
        if password and len(password) >= 4:
            self._password = password
        else:
            raise ValueError("Password debe tener al menos 4 caracteres")

    def set_email(self, email):
        import re
        if email and re.match(r'^[a-zA-Z0-9._%+-]+@ecotech\.cl$', email):
            self._email = email
        else:
            raise ValueError("Email debe usar dominio @ecotech.cl")

    def set_nivel_acceso(self, nivel_acceso):
        if nivel_acceso in [1, 2, 3]:
            self._nivel_acceso = nivel_acceso
        else:
            raise ValueError("Nivel acceso debe ser 1, 2 o 3")

    def __str__(self):
        return f"ID: {self._id}\nUsername: {self._username}\nEmail: {self._email}\nNivel Acceso: {self._nivel_acceso}"