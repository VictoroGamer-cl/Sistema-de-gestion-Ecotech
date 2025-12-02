import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class VerProyectosAsignadosLog:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Mis Proyectos Asignados")
        self.log.geometry("800x600")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Mis Proyectos Asignados",
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
            id_empleado = self.usuario_actual.get_id_empleado()
            proyectos = self.dao.obtener_proyectos_por_empleado(id_empleado)
            
            if not proyectos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No tienes proyectos asignados actualmente",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            

            empleados = self.dao.obtener_empleados()
            empleado_actual = None
            for emp in empleados:
                if emp.get_id() == id_empleado:
                    empleado_actual = emp
                    break
            
            departamento_info = ""
            if empleado_actual and empleado_actual.get_id_departamento():
                departamentos = self.dao.obtener_departamentos()
                for depto in departamentos:
                    if depto.get_id() == empleado_actual.get_id_departamento():
                        departamento_info = f"Departamento: {depto.get_nombre()}"
                        break
            

            info_frame = ctk.CTkFrame(self.contenido_frame, fg_color="#2B2B2B")
            info_frame.pack(fill="x", pady=(0, 15), padx=10)
            
            info_text = f"Proyectos asignados - {departamento_info} - Total: {len(proyectos)} proyecto(s)"
            ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=("Arial", 12, "bold")
            ).pack(pady=8)
            

            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame)
            scroll_frame.pack(fill="both", expand=True)
            
            for proyecto in proyectos:
                proyecto_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
                proyecto_frame.pack(fill="x", pady=8, padx=5)
                

                header_frame = ctk.CTkFrame(proyecto_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=15, pady=10)
                
                ctk.CTkLabel(
                    header_frame,
                    text=proyecto.get_nombre_proyecto(),
                    font=("Arial", 16, "bold")
                ).pack(side="left")
                

                estado_frame = ctk.CTkFrame(header_frame, fg_color="#2E8B57", corner_radius=8)
                estado_frame.pack(side="right", padx=(10, 0))
                
                ctk.CTkLabel(
                    estado_frame,
                    text="ACTIVO",
                    font=("Arial", 10, "bold"),
                    text_color="white"
                ).pack(padx=8, pady=3)
                

                if proyecto.get_descripcion():
                    desc_frame = ctk.CTkFrame(proyecto_frame, fg_color="transparent")
                    desc_frame.pack(fill="x", padx=15, pady=(0, 10))
                    
                    ctk.CTkLabel(
                        desc_frame,
                        text=proyecto.get_descripcion(),
                        font=("Arial", 12),
                        wraplength=700,
                        justify="left"
                    ).pack(anchor="w")
                

                detalles_frame = ctk.CTkFrame(proyecto_frame, fg_color="#2B2B2B")
                detalles_frame.pack(fill="x", padx=10, pady=(0, 10))
                
                detalles_grid = ctk.CTkFrame(detalles_frame, fg_color="transparent")
                detalles_grid.pack(fill="x", padx=10, pady=8)
                

                ctk.CTkLabel(
                    detalles_grid,
                    text=f"ID: {proyecto.get_id()}",
                    font=("Arial", 11),
                    text_color="gray"
                ).grid(row=0, column=0, padx=10, pady=2, sticky="w")
                

                ctk.CTkLabel(
                    detalles_grid,
                    text=f"Inicio: {proyecto.get_fecha_inicio()}",
                    font=("Arial", 11),
                    text_color="gray"
                ).grid(row=0, column=1, padx=10, pady=2, sticky="w")
                

                if proyecto.get_id_departamento():
                    depto_info = f"Depto ID: {proyecto.get_id_departamento()}"
                    ctk.CTkLabel(
                        detalles_grid,
                        text=depto_info,
                        font=("Arial", 11),
                        text_color="gray"
                    ).grid(row=0, column=2, padx=10, pady=2, sticky="w")

                if hasattr(proyecto, 'rol_empleado'):
                    rol_text = f"Rol: {proyecto.rol_empleado}"
                    ctk.CTkLabel(
                        detalles_grid,
                        text=rol_text,
                        font=("Arial", 11),
                        text_color="#9370DB"
                    ).grid(row=0, column=3, padx=10, pady=2, sticky="w")
                    
                detalles_grid.columnconfigure(0, weight=1)
                detalles_grid.columnconfigure(1, weight=1)
                detalles_grid.columnconfigure(2, weight=1)
                detalles_grid.columnconfigure(3, weight=1)
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar proyectos: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)