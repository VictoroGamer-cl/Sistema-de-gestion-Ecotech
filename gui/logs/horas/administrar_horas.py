import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class AdministrarHorasLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Administrar Horas Trabajadas")
        self.log.geometry("800x600")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Horas Trabajadas - Todos los Empleados",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            titulo_frame,
            text="Actualizar",
            command=lambda: self.cargar_horas_empleados(),
            width=100,
            height=35
        ).pack(side="right")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.cargar_horas_empleados()
    
    def cargar_horas_empleados(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            empleados = self.dao.obtener_empleados()
            
            if not empleados:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay empleados registrados",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame)
            scroll_frame.pack(fill="both", expand=True)
            
            for emp in empleados:
                try:
                    horas_emp = self.dao.obtener_horas_empleado(emp.get_id())
                    total_horas = sum(h.get_horas_trabajadas() for h in horas_emp)
                    
                    emp_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
                    emp_frame.pack(fill="x", pady=5, padx=5)
                    
                    header_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
                    header_frame.pack(fill="x", padx=15, pady=10)
                    
                    ctk.CTkLabel(
                        header_frame,
                        text=f"{emp.get_nombre()}",
                        font=("Arial", 14, "bold")
                    ).pack(side="left")
                    
                    ctk.CTkLabel(
                        header_frame,
                        text=f"Total horas: {total_horas}",
                        font=("Arial", 12),
                        text_color="gray"
                    ).pack(side="right")
                    
                    if horas_emp:
                        for hora in horas_emp[:3]:  # Mostrar solo las 3 más recientes
                            hora_frame = ctk.CTkFrame(emp_frame, fg_color="#2B2B2B")
                            hora_frame.pack(fill="x", padx=10, pady=2)
                            
                            ctk.CTkLabel(
                                hora_frame,
                                text=f"{hora.get_fecha()} - {hora.get_horas_trabajadas()} hrs - {hora.get_descripcion_tareas()}",
                                font=("Arial", 10),
                                wraplength=600,
                                justify="left"
                            ).pack(padx=10, pady=5)
                        
                        if len(horas_emp) > 3:
                            ctk.CTkLabel(
                                emp_frame,
                                text=f"... y {len(horas_emp) - 3} registros más",
                                font=("Arial", 10),
                                text_color="gray"
                            ).pack(pady=5)
                    
                except Exception as e:
                    continue  # Continuar con el siguiente empleado si hay error
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar horas: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)