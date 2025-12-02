import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class ListarProyectosLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Lista de Proyectos")
        self.log.geometry("900x600")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Lista de Proyectos",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            titulo_frame,
            text="Actualizar",
            command=lambda: self.cargar_proyectos(),
            width=100,
            height=35
        ).pack(side="right")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.cargar_proyectos()
    
    def cargar_proyectos(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            proyectos = self.dao.obtener_proyectos()
            
            if not proyectos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay proyectos registrados",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame)
            scroll_frame.pack(fill="both", expand=True)
            
            for proyecto in proyectos:
                proyecto_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
                proyecto_frame.pack(fill="x", pady=5, padx=5)
                
                header_frame = ctk.CTkFrame(proyecto_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=15, pady=10)
                
                ctk.CTkLabel(
                    header_frame,
                    text=f"ID: {proyecto.get_id()} - {proyecto.get_nombre_proyecto()}",
                    font=("Arial", 14, "bold")
                ).pack(side="left")
                
                depto_info = f" | Departamento: {proyecto.get_id_departamento()}" if proyecto.get_id_departamento() else " | Sin departamento"
                ctk.CTkLabel(
                    header_frame,
                    text=depto_info,
                    font=("Arial", 12),
                    text_color="gray"
                ).pack(side="right")
                
                ctk.CTkLabel(
                    proyecto_frame,
                    text=f"Descripción: {proyecto.get_descripcion()}",
                    font=("Arial", 12),
                    wraplength=800,
                    justify="left"
                ).pack(padx=15, pady=(0, 5), anchor="w")
                
                ctk.CTkLabel(
                    proyecto_frame,
                    text=f"Fecha inicio: {proyecto.get_fecha_inicio()}",
                    font=("Arial", 11),
                    text_color="gray"
                ).pack(padx=15, pady=(0, 10), anchor="w")
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar proyectos: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)