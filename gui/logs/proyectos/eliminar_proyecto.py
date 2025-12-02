import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class EliminarProyectoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Eliminar Proyecto")
        self.log.geometry("500x500")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Eliminar Proyecto",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_lista_proyectos()
    
    def mostrar_lista_proyectos(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.contenido_frame,
            text="Seleccione proyecto a eliminar:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        try:
            proyectos = self.dao.obtener_proyectos()
            
            if not proyectos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay proyectos registrados",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame, height=250)
            scroll_frame.pack(fill="x", pady=20, padx=10)
            
            self.selected_proyecto = ctk.StringVar()
            
            for proy in proyectos:
                frame_proyecto = ctk.CTkFrame(scroll_frame, height=50)
                frame_proyecto.pack(fill="x", pady=2, padx=5)
                frame_proyecto.pack_propagate(False)
                
                rb = ctk.CTkRadioButton(
                    frame_proyecto,
                    text=f"ID: {proy.get_id()} - {proy.get_nombre_proyecto()}",
                    variable=self.selected_proyecto,
                    value=str(proy.get_id())
                )
                rb.pack(side="left", padx=10, pady=10)
                
                ctk.CTkLabel(
                    frame_proyecto,
                    text=f"Fecha: {proy.get_fecha_inicio()}",
                    font=("Arial", 10),
                    text_color="gray"
                ).pack(side="right", padx=10, pady=10)
            
            ctk.CTkButton(
                self.contenido_frame,
                text="Eliminar Proyecto",
                command=self.confirmar_eliminacion,
                width=150,
                height=40,
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {e}")
    
    def confirmar_eliminacion(self):
        if not self.selected_proyecto.get():
            messagebox.showwarning("Advertencia", "Seleccione un proyecto")
            return
        
        try:
            proyectos = self.dao.obtener_proyectos()
            id_proyecto = int(self.selected_proyecto.get())
            
            proyecto_seleccionado = None
            for proy in proyectos:
                if proy.get_id() == id_proyecto:
                    proyecto_seleccionado = proy
                    break
            
            if not proyecto_seleccionado:
                messagebox.showerror("Error", "Proyecto no encontrado")
                return
            
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar el proyecto?\n\n"
                f"Nombre: {proyecto_seleccionado.get_nombre_proyecto()}\n"
                f"Descripción: {proyecto_seleccionado.get_descripcion()}\n"
                f"Fecha inicio: {proyecto_seleccionado.get_fecha_inicio()}\n"
                f"ID: {proyecto_seleccionado.get_id()}\n\n"
                f"Esta acción no se puede deshacer."
            )
            
            if respuesta:
                self.dao.eliminar_proyecto(id_proyecto)
                messagebox.showinfo("Éxito", "Proyecto eliminado correctamente")
                self.log.destroy()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar proyecto: {e}")