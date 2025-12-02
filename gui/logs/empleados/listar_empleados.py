import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class ListarEmpleadosLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Lista de Empleados")
        self.log.geometry("900x600")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Lista Completa de Empleados",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            titulo_frame,
            text="Actualizar",
            command=self.cargar_empleados,
            width=100,
            height=35
        ).pack(side="right")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.cargar_empleados()
    
    def cargar_empleados(self):
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
            
            headers_frame = ctk.CTkFrame(scroll_frame, fg_color="#2B2B2B", height=40)
            headers_frame.pack(fill="x", pady=(0, 5))
            headers_frame.pack_propagate(False)
            
            headers = ["ID", "Nombre", "Email", "Teléfono", "Salario", "Fecha Inicio"]
            widths = [80, 200, 250, 120, 120, 120]
            
            for i, header in enumerate(headers):
                ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=widths[i]
                ).grid(row=0, column=i, padx=2, pady=2)
            
            for empleado in empleados:
                row_frame = ctk.CTkFrame(scroll_frame, height=40)
                row_frame.pack(fill="x", pady=2)
                row_frame.pack_propagate(False)
                
                ctk.CTkLabel(
                    row_frame,
                    text=str(empleado.get_id()),
                    font=("Arial", 11),
                    width=widths[0]
                ).grid(row=0, column=0, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=empleado.get_nombre(),
                    font=("Arial", 11),
                    width=widths[1]
                ).grid(row=0, column=1, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=empleado.get_mail(),
                    font=("Arial", 11),
                    width=widths[2]
                ).grid(row=0, column=2, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=str(empleado.get_telefono()),
                    font=("Arial", 11),
                    width=widths[3]
                ).grid(row=0, column=3, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=f"${empleado.get_salario():,}",
                    font=("Arial", 11),
                    width=widths[4]
                ).grid(row=0, column=4, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=empleado.get_fecheIC(),
                    font=("Arial", 11),
                    width=widths[5]
                ).grid(row=0, column=5, padx=2, pady=2)
                
                for i in range(len(headers)):
                    row_frame.columnconfigure(i, weight=1)
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar empleados: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)