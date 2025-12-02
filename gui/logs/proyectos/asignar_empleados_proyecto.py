import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class AsignarEmpleadosProyectoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.proyecto_seleccionado = None
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Asignar Empleados a Proyecto")
        self.log.geometry("600x700")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Asignar Empleados a Proyecto",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_seleccion_proyecto()
    
    def mostrar_seleccion_proyecto(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.contenido_frame,
            text="Seleccione un proyecto:",
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
                command=self.mostrar_formulario_asignacion,
                width=120,
                height=35,
                fg_color="#2E8B57",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {e}")
    
    def mostrar_formulario_asignacion(self):
        if not self.selected_proyecto.get():
            messagebox.showwarning("Advertencia", "Seleccione un proyecto")
            return
        
        try:
            proyectos = self.dao.obtener_proyectos()
            id_proyecto = int(self.selected_proyecto.get())
            
            for proy in proyectos:
                if proy.get_id() == id_proyecto:
                    self.proyecto_seleccionado = proy
                    break
            
            if not self.proyecto_seleccionado:
                messagebox.showerror("Error", "Proyecto no encontrado")
                return
            
            for widget in self.contenido_frame.winfo_children():
                widget.destroy()
            
            # Título con información del proyecto
            titulo_frame = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
            titulo_frame.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(
                titulo_frame,
                text=f"Asignar Empleados a: {self.proyecto_seleccionado.get_nombre_proyecto()}",
                font=("Arial", 18, "bold")
            ).pack(side="left")
            
            # Frame principal
            main_frame = ctk.CTkFrame(self.contenido_frame)
            main_frame.pack(fill="both", expand=True, pady=10)
            
            # Sección: Empleados disponibles
            ctk.CTkLabel(
                main_frame,
                text="Empleados Disponibles:",
                font=("Arial", 14, "bold")
            ).pack(pady=10)
            
            empleados = self.dao.obtener_empleados()
            empleados_asignados = self.dao.obtener_empleados_proyecto(id_proyecto)
            ids_empleados_asignados = [emp.get_id() for emp in empleados_asignados]
            
            empleados_disponibles = [emp for emp in empleados if emp.get_id() not in ids_empleados_asignados]
            
            if not empleados_disponibles:
                ctk.CTkLabel(
                    main_frame,
                    text="No hay empleados disponibles para asignar",
                    font=("Arial", 12),
                    text_color="gray"
                ).pack(pady=10)
            else:
                scroll_empleados = ctk.CTkScrollableFrame(main_frame, height=150)
                scroll_empleados.pack(fill="x", pady=10, padx=20)
                
                self.empleados_seleccionados = {}
                
                for emp in empleados_disponibles:
                    frame_emp = ctk.CTkFrame(scroll_empleados, fg_color="transparent")
                    frame_emp.pack(fill="x", pady=2)
                    
                    check_var = ctk.BooleanVar()
                    check = ctk.CTkCheckBox(
                        frame_emp,
                        text=f"ID: {emp.get_id()} - {emp.get_nombre()} - {emp.get_mail()}",
                        variable=check_var,
                        font=("Arial", 11)
                    )
                    check.pack(side="left", padx=5)
                    
                    # Campo para rol
                    rol_var = ctk.StringVar(value="Miembro")
                    rol_entry = ctk.CTkEntry(
                        frame_emp,
                        textvariable=rol_var,
                        width=120,
                        height=25,
                        placeholder_text="Rol"
                    )
                    rol_entry.pack(side="right", padx=5)
                    
                    self.empleados_seleccionados[emp.get_id()] = {
                        'checkbox': check_var,
                        'rol': rol_var,
                        'empleado': emp
                    }
            
            # Sección: Empleados ya asignados
            if empleados_asignados:
                ctk.CTkLabel(
                    main_frame,
                    text="Empleados Asignados:",
                    font=("Arial", 14, "bold")
                ).pack(pady=(20, 10))
                
                scroll_asignados = ctk.CTkScrollableFrame(main_frame, height=120)
                scroll_asignados.pack(fill="x", pady=10, padx=20)
                
                for emp in empleados_asignados:
                    frame_emp = ctk.CTkFrame(scroll_asignados, fg_color="#2B2B2B")
                    frame_emp.pack(fill="x", pady=2, padx=2)
                    
                    ctk.CTkLabel(
                        frame_emp,
                        text=f"ID: {emp.get_id()} - {emp.get_nombre()} - Rol: {getattr(emp, 'rol_proyecto', 'Miembro')}",
                        font=("Arial", 11)
                    ).pack(side="left", padx=10, pady=5)
                    
                    ctk.CTkButton(
                        frame_emp,
                        text="Quitar",
                        command=lambda e=emp: self.quitar_empleado(e),
                        width=60,
                        height=25,
                        fg_color="#FF6B6B",
                        font=("Arial", 10)
                    ).pack(side="right", padx=10, pady=5)
            
            # Botones
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=20)
            
            ctk.CTkButton(
                button_frame,
                text="Asignar Empleados Seleccionados",
                command=self.asignar_empleados,
                width=250,
                height=40,
                fg_color="#2E8B57",
                font=("Arial", 12, "bold")
            ).pack(pady=5)
            
            ctk.CTkButton(
                button_frame,
                text="Volver",
                command=self.mostrar_seleccion_proyecto,
                width=150,
                height=35,
                fg_color="gray"
            ).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar formulario: {e}")
    
    def asignar_empleados(self):
        try:
            empleados_a_asignar = []
            
            for emp_id, datos in self.empleados_seleccionados.items():
                if datos['checkbox'].get():
                    rol = datos['rol'].get().strip() or "Miembro"
                    empleados_a_asignar.append({
                        'id': emp_id,
                        'rol': rol,
                        'nombre': datos['empleado'].get_nombre()
                    })
            
            if not empleados_a_asignar:
                messagebox.showwarning("Advertencia", "Seleccione al menos un empleado")
                return
            
            for emp in empleados_a_asignar:
                success = self.dao.asignar_empleado_proyecto(
                    emp['id'], 
                    self.proyecto_seleccionado.get_id(),
                    emp['rol']
                )
                if not success:
                    messagebox.showerror("Error", f"No se pudo asignar a {emp['nombre']}")
                    return
            
            messagebox.showinfo("Éxito", 
                f"Empleados asignados exitosamente al proyecto:\n"
                f"{self.proyecto_seleccionado.get_nombre_proyecto()}\n\n"
                f"Empleados asignados: {len(empleados_a_asignar)}"
            )
            self.mostrar_formulario_asignacion()  # Recargar
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al asignar empleados: {e}")
    
    def quitar_empleado(self, empleado):
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Quitar a {empleado.get_nombre()} del proyecto?\n\n"
            f"Proyecto: {self.proyecto_seleccionado.get_nombre_proyecto()}"
        )
        
        if respuesta:
            try:
                success = self.dao.desasignar_empleado_proyecto(
                    empleado.get_id(),
                    self.proyecto_seleccionado.get_id()
                )
                
                if success:
                    messagebox.showinfo("Éxito", f"{empleado.get_nombre()} quitado del proyecto")
                    self.mostrar_formulario_asignacion()  # Recargar
                else:
                    messagebox.showerror("Error", "No se pudo quitar al empleado")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al quitar empleado: {e}")