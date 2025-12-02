import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class AsignarEmpleadoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Asignar Empleado a Departamento")
        self.log.geometry("600x800")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Asignar Empleado a Departamento",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_seleccion()
    
    def mostrar_seleccion(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            empleados = self.dao.obtener_empleados()
            departamentos = self.dao.obtener_departamentos()
            
            if not empleados:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay empleados registrados",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            if not departamentos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay departamentos registrados",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            form_frame = ctk.CTkFrame(self.contenido_frame)
            form_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Seleccionar Empleado:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            scroll_empleados = ctk.CTkScrollableFrame(form_frame, height=50)
            scroll_empleados.pack(fill="x", pady=5, padx=20)
            
            self.selected_empleado = ctk.StringVar()
            
            for emp in empleados:
                depto_actual = f" (Depto: {emp.get_id_departamento()})" if emp.get_id_departamento() else ""
                rb = ctk.CTkRadioButton(
                    scroll_empleados,
                    text=f"ID: {emp.get_id()} - {emp.get_nombre()}{depto_actual}",
                    variable=self.selected_empleado,
                    value=str(emp.get_id())
                )
                rb.pack(anchor="w", pady=2)
            
            ctk.CTkLabel(
                form_frame,
                text="Seleccionar Departamento:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            scroll_departamentos = ctk.CTkScrollableFrame(form_frame, height=50)
            scroll_departamentos.pack(fill="x", pady=5, padx=20)
            
            self.selected_departamento = ctk.StringVar()
            
            for depto in departamentos:
                rb = ctk.CTkRadioButton(
                    scroll_departamentos,
                    text=f"ID: {depto.get_id()} - {depto.get_nombre()}",
                    variable=self.selected_departamento,
                    value=str(depto.get_id())
                )
                rb.pack(anchor="w", pady=2)
            
            button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=30)

            ctk.CTkButton(
                button_frame,
                text="✅ Asignar Empleado",
                command=self.asignar_empleado,
                width=250,
                height=50,
                fg_color="#2E8B57",
                hover_color="#3CB371",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
    
    def asignar_empleado(self):
        if not self.selected_empleado.get():
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
        
        if not self.selected_departamento.get():
            messagebox.showwarning("Advertencia", "Seleccione un departamento")
            return
        
        try:
            id_empleado = int(self.selected_empleado.get())
            id_departamento = int(self.selected_departamento.get())
            
            self.dao.asignar_empleado_departamento(id_empleado, id_departamento)
            
            messagebox.showinfo("Éxito", "Empleado asignado al departamento correctamente")
            self.log.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al asignar empleado: {e}")