import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class VerMisHorasLog:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Mis Horas Trabajadas")
        self.log.geometry("700x500")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Mis Horas Trabajadas",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            titulo_frame,
            text="Actualizar",
            command=lambda: self.cargar_horas(),
            width=100,
            height=35
        ).pack(side="right")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.cargar_horas()
    
    def cargar_horas(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            id_empleado = self.usuario_actual.get_id_empleado()
            horas = self.dao.obtener_horas_empleado(id_empleado)
            
            if not horas:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay horas registradas",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame)
            scroll_frame.pack(fill="both", expand=True)
            
            headers_frame = ctk.CTkFrame(scroll_frame, fg_color="#2B2B2B", height=40)
            headers_frame.pack(fill="x", pady=(0, 5))
            headers_frame.pack_propagate(False)
            
            headers = ["Fecha", "Horas", "Descripción"]
            widths = [120, 80, 400]
            
            for i, header in enumerate(headers):
                ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=widths[i]
                ).grid(row=0, column=i, padx=2, pady=2)
            
            total_horas = 0
            
            for hora in horas:
                row_frame = ctk.CTkFrame(scroll_frame, height=50)
                row_frame.pack(fill="x", pady=2)
                row_frame.pack_propagate(False)
                
                ctk.CTkLabel(
                    row_frame,
                    text=hora.get_fecha(),
                    font=("Arial", 11),
                    width=widths[0]
                ).grid(row=0, column=0, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=str(hora.get_horas_trabajadas()),
                    font=("Arial", 11),
                    width=widths[1]
                ).grid(row=0, column=1, padx=2, pady=2)
                
                desc_label = ctk.CTkLabel(
                    row_frame,
                    text=hora.get_descripcion_tareas(),
                    font=("Arial", 11),
                    width=widths[2],
                    wraplength=380,
                    justify="left"
                )
                desc_label.grid(row=0, column=2, padx=2, pady=2)
                
                total_horas += hora.get_horas_trabajadas()
                
                for i in range(len(headers)):
                    row_frame.columnconfigure(i, weight=1)
            
            total_frame = ctk.CTkFrame(self.contenido_frame, fg_color="#2B2B2B")
            total_frame.pack(fill="x", pady=10, padx=20)
            
            ctk.CTkLabel(
                total_frame,
                text=f"Total de horas registradas: {total_horas}",
                font=("Arial", 14, "bold")
            ).pack(pady=10)
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar horas: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)