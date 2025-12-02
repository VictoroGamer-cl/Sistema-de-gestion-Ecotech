import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from Proyecto import Proyecto

class ActualizarProyectoLog:
    def __init__(self, parent, admin_actual, id_proyecto):
        self.parent = parent
        self.admin_actual = admin_actual
        self.id_proyecto = id_proyecto
        self.dao = DAO()
        self.proyecto_seleccionado = None
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Actualizar Proyecto")
        self.log.geometry("600x950")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.cargar_proyecto()
    
    def cargar_proyecto(self):
        try:
            proyectos = self.dao.obtener_proyectos()
            
            for proy in proyectos:
                if proy.get_id() == self.id_proyecto:
                    self.proyecto_seleccionado = proy
                    break
            
            if not self.proyecto_seleccionado:
                messagebox.showerror("Error", "Proyecto no encontrado")
                self.log.destroy()
                return
            
            self.mostrar_formulario()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar proyecto: {e}")
            self.log.destroy()
    
    def mostrar_formulario(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            departamentos = self.dao.obtener_departamentos()
            
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Actualizar Proyecto: {self.proyecto_seleccionado.get_nombre_proyecto()}",
                font=("Arial", 20, "bold")
            ).pack(pady=10)
            
            form_frame = ctk.CTkFrame(self.contenido_frame)
            form_frame.pack(fill="both", expand=True, pady=20)
            
            self.nombre_var = ctk.StringVar(value=self.proyecto_seleccionado.get_nombre_proyecto())
            self.fecha_var = ctk.StringVar(value=self.proyecto_seleccionado.get_fecha_inicio())
            
            ctk.CTkLabel(
                form_frame,
                text="Nombre del Proyecto:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            ctk.CTkEntry(
                form_frame,
                textvariable=self.nombre_var,
                width=400,
                height=35
            ).pack(pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Descripción:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            self.descripcion_text = ctk.CTkTextbox(
                form_frame,
                width=400,
                height=120
            )
            self.descripcion_text.pack(pady=10)
            self.descripcion_text.insert("1.0", self.proyecto_seleccionado.get_descripcion())
            
            ctk.CTkLabel(
                form_frame,
                text="Fecha Inicio (YYYY-MM-DD):",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            ctk.CTkEntry(
                form_frame,
                textvariable=self.fecha_var,
                width=400,
                height=35
            ).pack(pady=10)
            
            ctk.CTkLabel(
                form_frame,
                text="Departamento:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            # DEFINIR la variable SIEMPRE (fuera del if)
            self.selected_departamento = ctk.StringVar(value=str(self.proyecto_seleccionado.get_id_departamento() or "0"))

            ctk.CTkLabel(
                form_frame,
                text="Departamento:",
                font=("Arial", 12, "bold")
            ).pack(pady=10)

            if departamentos:
                # Frame contenedor con altura fija
                depto_container = ctk.CTkFrame(form_frame, height=100)
                depto_container.pack(fill="x", pady=5, padx=20)
                depto_container.pack_propagate(False)
                
                # Scrollable frame dentro del contenedor
                depto_frame = ctk.CTkScrollableFrame(depto_container)
                depto_frame.pack(fill="both", expand=True, padx=5, pady=5)
                
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
                ).pack(pady=5)
            
            button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=30)
            
            ctk.CTkButton(
                button_frame,
                text="Guardar Cambios",
                command=self.guardar_cambios,
                width=200,
                height=45,
                fg_color="#2E8B57",
                font=("Arial", 14, "bold")
            ).pack(pady=10)
            
            ctk.CTkButton(
                button_frame,
                text="Cancelar",
                command=self.log.destroy,
                width=150,
                height=35,
                fg_color="gray"
            ).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar formulario: {e}")
    
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
    
    def guardar_cambios(self):
        try:
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
            
            id_departamento = None
            if self.selected_departamento.get() != "0":
                id_departamento = int(self.selected_departamento.get())
            
            proyecto_actualizado = Proyecto(
                self.proyecto_seleccionado.get_id(),
                nombre,
                descripcion,
                fecha,
                id_departamento
            )
            
            self.dao.actualizar_proyecto(proyecto_actualizado)
            
            messagebox.showinfo("Éxito", f"Proyecto '{nombre}' actualizado correctamente")
            self.log.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar proyecto: {e}")