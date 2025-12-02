import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from HoraTrabajada import HoraTrabajada
from datetime import datetime

class RegistrarHorasLog:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Registrar Horas Trabajadas")
        self.log.geometry("500x700")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Registrar Horas Trabajadas",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        form_frame = ctk.CTkFrame(self.contenido_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            form_frame,
            text="Fecha (YYYY-MM-DD):",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        self.fecha_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
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
            text="Horas trabajadas:",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        self.horas_var = ctk.StringVar()
        horas_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.horas_var,
            width=300,
            height=35,
            placeholder_text="Ej: 8.5"
        )
        horas_entry.pack(pady=10)
        
        ctk.CTkLabel(
            form_frame,
            text="Descripción de tareas:",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        self.descripcion_text = ctk.CTkTextbox(
            form_frame,
            width=300,
            height=120
        )
        self.descripcion_text.pack(pady=10)
        
        ctk.CTkButton(
            form_frame,
            text="Registrar Horas",
            command=self.registrar_horas,
            width=200,
            height=40,
            fg_color="#2E8B57",
            font=("Arial", 12, "bold")
        ).pack(pady=20)
    
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
    
    def registrar_horas(self):
        fecha = self.fecha_var.get().strip()
        horas_str = self.horas_var.get().strip()
        descripcion = self.descripcion_text.get("1.0", "end-1c").strip()
        
        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "Fecha debe tener formato YYYY-MM-DD")
            return
        
        try:
            horas = float(horas_str)
            if horas <= 0 or horas > 24:
                messagebox.showerror("Error", "Horas deben estar entre 0 y 24")
                return
        except ValueError:
            messagebox.showerror("Error", "Horas deben ser un número válido")
            return
        
        if not descripcion:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return
        
        try:
            id_empleado = self.usuario_actual.get_id_empleado()
            
            nueva_hora = HoraTrabajada(
                None,
                fecha,
                horas,
                descripcion,
                id_empleado
            )
            
            self.dao.registrar_hora_trabajada(nueva_hora)
            
            messagebox.showinfo("Éxito", "Horas registradas exitosamente")
            self.log.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar horas: {e}")