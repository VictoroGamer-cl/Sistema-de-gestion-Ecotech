import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class EliminarEmpleadoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Eliminar Empleado")
        self.log.geometry("500x500")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_lista_empleados()
    
    def mostrar_lista_empleados(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.contenido_frame,
            text="Seleccione empleado a eliminar:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        try:
            empleados = self.dao.obtener_empleados()
            
            if not empleados:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay empleados registrados",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame, height=250)
            scroll_frame.pack(fill="x", pady=20, padx=10)
            
            self.selected_empleado = ctk.StringVar()
            
            for emp in empleados:
                frame_empleado = ctk.CTkFrame(scroll_frame, height=50)
                frame_empleado.pack(fill="x", pady=2, padx=5)
                frame_empleado.pack_propagate(False)
                
                rb = ctk.CTkRadioButton(
                    frame_empleado,
                    text=f"ID: {emp.get_id()} - {emp.get_nombre()}",
                    variable=self.selected_empleado,
                    value=str(emp.get_id())
                )
                rb.pack(side="left", padx=10, pady=10)
                
                ctk.CTkLabel(
                    frame_empleado,
                    text=emp.get_mail(),
                    font=("Arial", 10),
                    text_color="gray"
                ).pack(side="right", padx=10, pady=10)
            
            ctk.CTkButton(
                self.contenido_frame,
                text="Eliminar Empleado",
                command=self.confirmar_eliminacion,
                width=150,
                height=40,
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados: {e}")
    
    def confirmar_eliminacion(self):
        if not self.selected_empleado.get():
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
        
        try:
            empleados = self.dao.obtener_empleados()
            id_empleado = int(self.selected_empleado.get())
            
            empleado_seleccionado = None
            for emp in empleados:
                if emp.get_id() == id_empleado:
                    empleado_seleccionado = emp
                    break
            
            if not empleado_seleccionado:
                messagebox.showerror("Error", "Empleado no encontrado")
                return
            
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar al empleado?\n\n"
                f"Nombre: {empleado_seleccionado.get_nombre()}\n"
                f"Email: {empleado_seleccionado.get_mail()}\n"
                f"ID: {empleado_seleccionado.get_id()}\n\n"
                f"Esta acción no se puede deshacer."
            )
            
            if respuesta:
                resultado = self.dao.eliminar_empleado(id_empleado)
                
                if resultado:
                    messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                    self.log.destroy()
                else:
                    messagebox.showerror("Error", 
                        "No se pudo eliminar el empleado. "
                        "Puede que tenga registros relacionados."
                    )
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar empleado: {e}")