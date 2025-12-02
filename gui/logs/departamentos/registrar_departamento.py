import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from Departamento import Departamento

class RegistrarDepartamentoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Registrar Departamento")
        self.log.geometry("500x500")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Registrar Nuevo Departamento",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            empleados = self.dao.obtener_empleados()
            
            if not empleados:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay empleados registrados. Debe registrar empleados primero.",
                    font=("Arial", 12),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            form_frame = ctk.CTkFrame(self.contenido_frame)
            form_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Nombre del Departamento:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            self.nombre_var = ctk.StringVar()
            nombre_entry = ctk.CTkEntry(
                form_frame,
                textvariable=self.nombre_var,
                width=300,
                height=35,
                placeholder_text="Ej: Recursos Humanos"
            )
            nombre_entry.pack(pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Seleccionar Gerente:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            scroll_frame = ctk.CTkScrollableFrame(form_frame, height=150)
            scroll_frame.pack(fill="x", pady=10, padx=20)
            
            self.selected_gerente = ctk.StringVar()
            
            for emp in empleados:
                rb = ctk.CTkRadioButton(
                    scroll_frame,
                    text=f"ID: {emp.get_id()} - {emp.get_nombre()} - {emp.get_mail()}",
                    variable=self.selected_gerente,
                    value=str(emp.get_id())
                )
                rb.pack(anchor="w", pady=2)
            
            ctk.CTkButton(
                form_frame,
                text="Registrar Departamento",
                command=self.registrar_departamento,
                width=200,
                height=40,
                fg_color="#2E8B57",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados: {e}")
    
    def registrar_departamento(self):
        nombre = self.nombre_var.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre del departamento es obligatorio")
            return
        
        if not self.selected_gerente.get():
            messagebox.showwarning("Advertencia", "Seleccione un gerente")
            return
        
        try:
            empleados = self.dao.obtener_empleados()
            id_gerente = int(self.selected_gerente.get())
            
            gerente_encontrado = None
            for emp in empleados:
                if emp.get_id() == id_gerente:
                    gerente_encontrado = emp
                    break
            
            if not gerente_encontrado:
                messagebox.showerror("Error", "Gerente no encontrado")
                return
            
            nuevo_departamento = Departamento(
                None,
                nombre,
                id_gerente,
                gerente_encontrado.get_nombre()
            )
            
            self.dao.registrar_departamento(nuevo_departamento)
            
            messagebox.showinfo("Éxito", f"Departamento '{nombre}' registrado exitosamente")
            self.log.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar departamento: {e}")