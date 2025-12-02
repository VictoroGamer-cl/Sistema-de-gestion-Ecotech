import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from Proyecto import Proyecto

class RegistrarProyectoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Registrar Proyecto")
        self.log.geometry("500x850")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Registrar Nuevo Proyecto",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            departamentos = self.dao.obtener_departamentos()
            
            form_frame = ctk.CTkFrame(self.contenido_frame)
            form_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Nombre del Proyecto:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            self.nombre_var = ctk.StringVar()
            nombre_entry = ctk.CTkEntry(
                form_frame,
                textvariable=self.nombre_var,
                width=300,
                height=35,
                placeholder_text="Ej: Sistema de Gestión EcoTech"
            )
            nombre_entry.pack(pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Descripción:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            self.descripcion_text = ctk.CTkTextbox(
                form_frame,
                width=300,
                height=90
            )
            self.descripcion_text.pack(pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Fecha Inicio (YYYY-MM-DD):",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            self.fecha_var = ctk.StringVar()
            fecha_entry = ctk.CTkEntry(
                form_frame,
                textvariable=self.fecha_var,
                width=300,
                height=35,
                placeholder_text="2024-01-01"
            )
            fecha_entry.pack(pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Departamento (Opcional):",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            if departamentos:
                depto_frame = ctk.CTkScrollableFrame(form_frame, height=20)
                depto_frame.pack(fill="x", pady=5, padx=10)
                
                self.selected_departamento = ctk.StringVar(value="0")
                
                ctk.CTkRadioButton(
                    depto_frame,
                    text="Ninguno",
                    variable=self.selected_departamento,
                    value="0"
                ).pack(anchor="w", pady=2)
                
                for depto in departamentos:
                    ctk.CTkRadioButton(
                        depto_frame,
                        text=f"ID: {depto.get_id()} - {depto.get_nombre()}",
                        variable=self.selected_departamento,
                        value=str(depto.get_id())
                    ).pack(anchor="w", pady=2)
            else:
                ctk.CTkLabel(
                    form_frame,
                    text="No hay departamentos registrados",
                    font=("Arial", 10),
                    text_color="gray"
                ).pack(pady=10)
            
            ctk.CTkButton(
                form_frame,
                text="Registrar Proyecto",
                command=self.registrar_proyecto,
                width=200,
                height=40,
                fg_color="#2E8B57",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
    
    def validar_fecha(self, fecha):
        import re
        patron = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(patron, fecha):
            return False
        try:
            año, mes, dia = map(int, fecha.split('-'))
            return año > 2000 and 1 <= mes <= 12 and 1 <= dia <= 31
        except ValueError:
            return False
    
    def registrar_proyecto(self):
        nombre = self.nombre_var.get().strip()
        descripcion = self.descripcion_text.get("1.0", "end-1c").strip()
        fecha = self.fecha_var.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre del proyecto es obligatorio")
            return
        
        if not descripcion:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return
        
        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "Fecha debe tener formato YYYY-MM-DD")
            return
        
        try:
            id_departamento = None
            if self.selected_departamento.get() != "0":
                id_departamento = int(self.selected_departamento.get())
            
            nuevo_proyecto = Proyecto(
                None,
                nombre,
                descripcion,
                fecha,
                id_departamento
            )
            
            self.dao.registrar_proyecto(nuevo_proyecto)
            
            messagebox.showinfo("Éxito", f"Proyecto '{nombre}' registrado exitosamente")
            self.log.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar proyecto: {e}")