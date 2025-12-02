import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from EcoTech import EcoTech
from Usuarios import Usuario
import re

class RegistrarEmpleadoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_dialog()
    
    def validar_email(self, email):
        patron = r'^[a-zA-Z0-9._%+-]+@ecotech\.cl$'
        return re.match(patron, email) is not None

    def validar_telefono(self, telefono):
        return len(str(telefono)) <= 9 and telefono > 0

    def validar_fecha(self, fecha):
        patron = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(patron, fecha):
            return False
        try:
            año, mes, dia = map(int, fecha.split('-'))
            return año > 2000 and 1 <= mes <= 12 and 1 <= dia <= 31
        except ValueError:
            return False

    def limpiar_input(self, texto):
        if texto is None:
            return ""
        texto_limpio = re.sub(r'[<>\'";\(\)&\|]', '', str(texto))
        return texto_limpio.strip()

    def crear_dialog(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Registrar Nuevo Empleado")
        self.dialog.geometry("500x650")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        

        self.nombre_var = ctk.StringVar()
        self.direccion_var = ctk.StringVar()
        self.telefono_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.fecha_var = ctk.StringVar()
        self.salario_var = ctk.StringVar()
        
        self.crear_formulario()
    
    def crear_formulario(self):
        # Título
        ctk.CTkLabel(
            self.dialog, 
            text="Registrar Nuevo Empleado", 
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        

        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=25, pady=15)
        

        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        

        form_frame.columnconfigure(1, weight=1)

        campos = [
            ("Nombre:", "nombre_var", 0),
            ("Dirección:", "direccion_var", 1),
            ("Teléfono:", "telefono_var", 2),
            ("Email (@ecotech.cl):", "email_var", 3),
            ("Fecha Inicio (YYYY-MM-DD):", "fecha_var", 4),
            ("Salario:", "salario_var", 5)
        ]
        
        for i, (label, var_name, row) in enumerate(campos):
            ctk.CTkLabel(
                form_frame, 
                text=label, 
                font=("Arial", 12)
            ).grid(row=row, column=0, sticky="w", pady=12, padx=(0, 10))
            
            entry = ctk.CTkEntry(
                form_frame, 
                textvariable=getattr(self, var_name),
                width=300, 
                height=35
            )
            entry.grid(row=row, column=1, sticky="ew", pady=12)
        

        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkButton(
            button_frame, 
            text="Guardar Empleado", 
            command=self.guardar_empleado,
            fg_color="#2E8B57",
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=10)
    
    def guardar_empleado(self):

        nombre = self.limpiar_input(self.nombre_var.get())
        if not nombre:
            messagebox.showerror("Error", "Nombre no válido")
            return
        
        direccion = self.limpiar_input(self.direccion_var.get())
        
        try:
            telefono = int(self.limpiar_input(self.telefono_var.get()))
            if not self.validar_telefono(telefono):
                messagebox.showerror("Error", "Número de teléfono no válido (máximo 9 dígitos)")
                return
        except ValueError:
            messagebox.showerror("Error", "Teléfono debe ser un número")
            return
        
        email = self.limpiar_input(self.email_var.get())
        if not self.validar_email(email):
            messagebox.showerror("Error", "Email debe usar @ecotech.cl")
            return
        
        fecha_inicio = self.limpiar_input(self.fecha_var.get())
        if not self.validar_fecha(fecha_inicio):
            messagebox.showerror("Error", "Formato de fecha no válido. Use YYYY-MM-DD")
            return
        
        try:
            salario = int(self.limpiar_input(self.salario_var.get()))
            if salario <= 0:
                messagebox.showerror("Error", "Salario debe ser positivo")
                return
        except ValueError:
            messagebox.showerror("Error", "Salario debe ser un número")
            return
        

        empleado_nuevo = EcoTech(
            None, nombre, direccion, telefono, email, 
            fecha_inicio, salario, None, self.admin_actual.get_id()
        )
        
        try:
            id_empleado_generado = self.dao.registrar_empleado(empleado_nuevo)
            
            if id_empleado_generado:
                username = nombre.lower().replace(" ", ".")
                contraseña = f"{nombre.lower().replace(' ', '')}hcet"
                
                try:
                    usuario_auto = Usuario(
                        id_usuario=None,
                        username=username,
                        contraseña=contraseña,
                        modulos="empleados,departamentos",
                        id_empleado=id_empleado_generado
                    )
                    
                    self.dao.registrar_usuario(usuario_auto)
                    
                    messagebox.showinfo("Éxito", 
                        f"Empleado {nombre} registrado exitosamente\n\n"
                        f"Usuario creado automáticamente:\n"
                        f"Username: {username}\n"
                        f"Contraseña: {contraseña}")
                    
                except Exception as user_error:
                    messagebox.showwarning("Advertencia", 
                        f"Empleado {nombre} registrado exitosamente\n\n"
                        f"Pero hubo un error al crear el usuario automático:\n{user_error}")
                
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el empleado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar empleado: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    dialog = RegistrarEmpleadoLog(root, None)
    root.mainloop()