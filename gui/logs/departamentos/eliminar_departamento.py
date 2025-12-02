import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class EliminarDepartamentoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Eliminar Departamento")
        self.log.geometry("500x500")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Eliminar Departamento",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_lista_departamentos()
    
    def mostrar_lista_departamentos(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.contenido_frame,
            text="Seleccione departamento a eliminar:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        try:
            departamentos = self.dao.obtener_departamentos()
            
            if not departamentos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay departamentos registrados",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame, height=250)
            scroll_frame.pack(fill="x", pady=20, padx=10)
            
            self.selected_departamento = ctk.StringVar()
            
            for depto in departamentos:
                frame_depto = ctk.CTkFrame(scroll_frame, height=50)
                frame_depto.pack(fill="x", pady=2, padx=5)
                frame_depto.pack_propagate(False)
                
                rb = ctk.CTkRadioButton(
                    frame_depto,
                    text=f"ID: {depto.get_id()} - {depto.get_nombre()}",
                    variable=self.selected_departamento,
                    value=str(depto.get_id())
                )
                rb.pack(side="left", padx=10, pady=10)
                
                ctk.CTkLabel(
                    frame_depto,
                    text=f"Gerente: {depto.get_nombre_gerente()}",
                    font=("Arial", 10),
                    text_color="gray"
                ).pack(side="right", padx=10, pady=10)
            
            ctk.CTkButton(
                self.contenido_frame,
                text="Eliminar Departamento",
                command=self.confirmar_eliminacion,
                width=150,
                height=40,
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los departamentos: {e}")
    
    def confirmar_eliminacion(self):
        if not self.selected_departamento.get():
            messagebox.showwarning("Advertencia", "Seleccione un departamento")
            return
        
        try:
            departamentos = self.dao.obtener_departamentos()
            id_departamento = int(self.selected_departamento.get())
            
            departamento_seleccionado = None
            for depto in departamentos:
                if depto.get_id() == id_departamento:
                    departamento_seleccionado = depto
                    break
            
            if not departamento_seleccionado:
                messagebox.showerror("Error", "Departamento no encontrado")
                return
            
            empleados = self.dao.obtener_empleados()
            empleados_en_departamento = [emp for emp in empleados if emp.get_id_departamento() == id_departamento]
            
            if empleados_en_departamento:
                messagebox.showerror("Error", 
                    f"No se puede eliminar el departamento '{departamento_seleccionado.get_nombre()}'\n\n"
                    f"Tiene {len(empleados_en_departamento)} empleado(s) asignado(s).\n"
                    f"Reasigne los empleados primero."
                )
                return
            
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar el departamento?\n\n"
                f"Nombre: {departamento_seleccionado.get_nombre()}\n"
                f"Gerente: {departamento_seleccionado.get_nombre_gerente()}\n"
                f"ID: {departamento_seleccionado.get_id()}\n\n"
                f"Esta acción no se puede deshacer."
            )
            
            if respuesta:
                self.dao.eliminar_departamento(id_departamento)
                messagebox.showinfo("Éxito", "Departamento eliminado correctamente")
                self.log.destroy()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar departamento: {e}")