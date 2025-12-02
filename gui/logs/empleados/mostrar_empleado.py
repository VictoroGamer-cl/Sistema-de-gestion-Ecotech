import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class MostrarEmpleadoLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Mostrar Empleado")
        self.log.geometry("500x400")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Buscar Empleado",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_busqueda()
    
    def mostrar_busqueda(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        busqueda_frame = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        busqueda_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            busqueda_frame,
            text="Seleccione un empleado:",
            font=("Arial", 14)
        ).pack(pady=10)
        
        try:
            empleados = self.dao.obtener_empleados()
            
            if not empleados:
                ctk.CTkLabel(
                    busqueda_frame,
                    text="No hay empleados registrados",
                    font=("Arial", 12),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(busqueda_frame, height=150)
            scroll_frame.pack(fill="x", pady=10)
            
            self.selected_empleado = ctk.StringVar()
            
            for emp in empleados:
                rb = ctk.CTkRadioButton(
                    scroll_frame,
                    text=f"ID: {emp.get_id()} - {emp.get_nombre()}",
                    variable=self.selected_empleado,
                    value=str(emp.get_id())
                )
                rb.pack(anchor="w", pady=2)
            
            ctk.CTkButton(
                busqueda_frame,
                text="Ver Detalles",
                command=self.mostrar_detalles,
                width=120,
                height=35
            ).pack(pady=10)
            
        except Exception as e:
            ctk.CTkLabel(
                busqueda_frame,
                text=f"Error: {str(e)}",
                font=("Arial", 12),
                text_color="red"
            ).pack(pady=20)
    
    def mostrar_detalles(self):
        if not self.selected_empleado.get():
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
        
        try:
            empleados = self.dao.obtener_empleados()
            id_empleado = int(self.selected_empleado.get())
            
            empleado_encontrado = None
            for emp in empleados:
                if emp.get_id() == id_empleado:
                    empleado_encontrado = emp
                    break
            
            if not empleado_encontrado:
                messagebox.showerror("Error", "Empleado no encontrado")
                return
            
            for widget in self.contenido_frame.winfo_children():
                widget.destroy()
            
            detalles_frame = ctk.CTkFrame(self.contenido_frame)
            detalles_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            info_text = f"""
ID: {empleado_encontrado.get_id()}
Nombre: {empleado_encontrado.get_nombre()}
Dirección: {empleado_encontrado.get_direccion()}
Teléfono: {empleado_encontrado.get_telefono()}
Email: {empleado_encontrado.get_mail()}
Fecha Inicio: {empleado_encontrado.get_fecheIC()}
Salario: ${empleado_encontrado.get_salario():,}
"""
            
            textbox = ctk.CTkTextbox(detalles_frame, font=("Arial", 12))
            textbox.pack(fill="both", expand=True, padx=10, pady=10)
            textbox.insert("1.0", info_text)
            textbox.configure(state="disabled")
            
            ctk.CTkButton(
                detalles_frame,
                text="Volver",
                command=self.mostrar_busqueda,
                width=100,
                height=35
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")