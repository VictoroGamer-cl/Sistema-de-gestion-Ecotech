import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class SeleccionarProyectoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Seleccionar Proyecto")
        self.log.geometry("500x550")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Seleccionar Proyecto a Actualizar",
            font=("Arial", 18, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_seleccion()
    
    def mostrar_seleccion(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.contenido_frame,
            text="Seleccione el proyecto a actualizar:",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        try:
            proyectos = self.dao.obtener_proyectos()
            
            if not proyectos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay proyectos registrados",
                    font=("Arial", 12),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame, height=200)
            scroll_frame.pack(fill="x", pady=20, padx=10)
            
            self.selected_proyecto = ctk.StringVar()
            
            for proy in proyectos:
                rb = ctk.CTkRadioButton(
                    scroll_frame,
                    text=f"ID: {proy.get_id()} - {proy.get_nombre_proyecto()}",
                    variable=self.selected_proyecto,
                    value=str(proy.get_id())
                )
                rb.pack(anchor="w", pady=2)
            
            ctk.CTkButton(
                self.contenido_frame,
                text="Continuar",
                command=self.continuar_actualizacion,
                width=120,
                height=40,
                fg_color="#2E8B57",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {e}")
    
    def continuar_actualizacion(self):
        if not self.selected_proyecto.get():
            messagebox.showwarning("Advertencia", "Seleccione un proyecto")
            return
        
        try:
            from gui.logs.proyectos.actualizar_proyecto import ActualizarProyectoLog
            id_proyecto = int(self.selected_proyecto.get())
            self.log.destroy()
            ActualizarProyectoLog(self.parent, self.admin_actual, id_proyecto)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el formulario: {e}")