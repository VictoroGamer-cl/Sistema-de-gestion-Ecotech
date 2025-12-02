import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from EcoTech import EcoTech

class ActualizarEmpleadoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.empleado_seleccionado = None
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Actualizar Empleado")
        self.log.geometry("500x600")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_seleccion()
    
    def mostrar_seleccion(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.contenido_frame,
            text="Seleccione empleado a actualizar:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        try:
            empleados = self.dao.obtener_empleados()
            
            if not empleados:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay empleados registrados",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame, height=200)
            scroll_frame.pack(fill="x", pady=20, padx=10)
            
            self.selected_empleado = ctk.StringVar()
            
            for emp in empleados:
                rb = ctk.CTkRadioButton(
                    scroll_frame,
                    text=f"ID: {emp.get_id()} - {emp.get_nombre()} - {emp.get_mail()}",
                    variable=self.selected_empleado,
                    value=str(emp.get_id())
                )
                rb.pack(anchor="w", pady=2)
            
            ctk.CTkButton(
                self.contenido_frame,
                text="Seleccionar",
                command=self.mostrar_formulario_actualizacion,
                width=120,
                height=35,
                fg_color="#FF8C00"
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados: {e}")
    
    def mostrar_formulario_actualizacion(self):

        if not self.selected_empleado.get():
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
        
        try:
            empleados = self.dao.obtener_empleados()
            id_empleado = int(self.selected_empleado.get())
            

            for emp in empleados:
                if emp.get_id() == id_empleado:
                    self.empleado_seleccionado = emp
                    break
            
            if not self.empleado_seleccionado:
                messagebox.showerror("Error", "Empleado no encontrado")
                return

            for widget in self.contenido_frame.winfo_children():
                widget.destroy()
            

            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Actualizar: {self.empleado_seleccionado.get_nombre()}",
                font=("Arial", 18, "bold")
            ).pack(pady=10)
            

            form_frame = ctk.CTkFrame(self.contenido_frame)
            form_frame.pack(fill="both", expand=True, pady=20)

            self.nombre_var = ctk.StringVar(value=self.empleado_seleccionado.get_nombre())
            self.direccion_var = ctk.StringVar(value=self.empleado_seleccionado.get_direccion())
            self.telefono_var = ctk.StringVar(value=str(self.empleado_seleccionado.get_telefono()))
            self.email_var = ctk.StringVar(value=self.empleado_seleccionado.get_mail())
            self.fecha_var = ctk.StringVar(value=self.empleado_seleccionado.get_fecheIC())
            self.salario_var = ctk.StringVar(value=str(self.empleado_seleccionado.get_salario()))
            

            campos = [
                ("Nombre:", self.nombre_var),
                ("Dirección:", self.direccion_var),
                ("Teléfono:", self.telefono_var),
                ("Email (@ecotech.cl):", self.email_var),
                ("Fecha Inicio (YYYY-MM-DD):", self.fecha_var),
                ("Salario:", self.salario_var)
            ]
            
            for i, (label, var) in enumerate(campos):
                ctk.CTkLabel(
                    form_frame,
                    text=label,
                    font=("Arial", 12)
                ).grid(row=i, column=0, sticky="w", padx=20, pady=10)
                
                ctk.CTkEntry(
                    form_frame,
                    textvariable=var,
                    width=300,
                    height=35
                ).grid(row=i, column=1, padx=20, pady=10)
            

            button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            button_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
            
            ctk.CTkButton(
                button_frame,
                text="Guardar Cambios",
                command=self.guardar_cambios,
                width=140,
                height=40,
                fg_color="#2E8B57",
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                button_frame,
                text="Cancelar",
                command=self.mostrar_seleccion,
                width=100,
                height=40,
                fg_color="gray"
            ).pack(side="left", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar formulario: {e}")
    
    def validar_email(self, email):
        patron = r'^[a-zA-Z0-9._%+-]+@ecotech\.cl$'
        import re
        return re.match(patron, email) is not None
    
    def validar_telefono(self, telefono):
        return len(str(telefono)) <= 9 and telefono > 0
    
    def validar_fecha(self, fecha):
        patron = r'^\d{4}-\d{2}-\d{2}$'
        import re
        if not re.match(patron, fecha):
            return False
        try:
            año, mes, dia = map(int, fecha.split('-'))
            return año > 2000 and 1 <= mes <= 12 and 1 <= dia <= 31
        except ValueError:
            return False
    
    def guardar_cambios(self):

        try:
            nombre = self.nombre_var.get().strip()
            direccion = self.direccion_var.get().strip()
            telefono_str = self.telefono_var.get().strip()
            email = self.email_var.get().strip()
            fecha = self.fecha_var.get().strip()
            salario_str = self.salario_var.get().strip()
            

            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            try:
                telefono = int(telefono_str)
                if not self.validar_telefono(telefono):
                    messagebox.showerror("Error", "Teléfono debe tener máximo 9 dígitos")
                    return
            except ValueError:
                messagebox.showerror("Error", "Teléfono debe ser un número válido")
                return
            
            if not self.validar_email(email):
                messagebox.showerror("Error", "Email debe usar dominio @ecotech.cl")
                return
            
            if not self.validar_fecha(fecha):
                messagebox.showerror("Error", "Fecha debe tener formato YYYY-MM-DD")
                return
            
            try:
                salario = int(salario_str)
                if salario <= 0:
                    messagebox.showerror("Error", "Salario debe ser positivo")
                    return
            except ValueError:
                messagebox.showerror("Error", "Salario debe ser un número válido")
                return
            

            empleado_actualizado = EcoTech(
                self.empleado_seleccionado.get_id(),
                nombre,
                direccion,
                telefono,
                email,
                fecha,
                salario,
                self.empleado_seleccionado.get_id_departamento(),
                self.empleado_seleccionado.get_id_administrador()
            )
            

            self.dao.actualizar_empleado(empleado_actualizado)
            
            messagebox.showinfo("Éxito", f"Empleado {nombre} actualizado correctamente")
            self.log.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar empleado: {e}")