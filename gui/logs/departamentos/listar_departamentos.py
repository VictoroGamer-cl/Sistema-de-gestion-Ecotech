import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO

class ListarDepartamentosLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Lista de Departamentos")
        self.log.geometry("800x500")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Lista de Departamentos",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            titulo_frame,
            text="Actualizar",
            command=self.cargar_departamentos,
            width=100,
            height=35
        ).pack(side="right")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.cargar_departamentos()
    
    def cargar_departamentos(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        loading_label = ctk.CTkLabel(
            self.contenido_frame,
            text="Cargando departamentos...",
            font=("Arial", 14),
            text_color="gray"
        )
        loading_label.pack(pady=50)
        
        self.log.update()
        
        try:
            departamentos = self.dao.obtener_departamentos()
            loading_label.destroy()
            if not departamentos:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay departamentos registrados",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame)
            scroll_frame.pack(fill="both", expand=True)
            
            headers_frame = ctk.CTkFrame(scroll_frame, fg_color="#2B2B2B", height=40)
            headers_frame.pack(fill="x", pady=(0, 5))
            headers_frame.pack_propagate(False)
            
            headers = ["ID", "Nombre", "Gerente", "ID Gerente"]
            widths = [80, 250, 250, 100]
            
            for i, header in enumerate(headers):
                ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=widths[i]
                ).grid(row=0, column=i, padx=2, pady=2)
            
            for depto in departamentos:
                row_frame = ctk.CTkFrame(scroll_frame, height=40)
                row_frame.pack(fill="x", pady=2)
                row_frame.pack_propagate(False)
                
                ctk.CTkLabel(
                    row_frame,
                    text=str(depto.get_id()),
                    font=("Arial", 11),
                    width=widths[0]
                ).grid(row=0, column=0, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=depto.get_nombre(),
                    font=("Arial", 11),
                    width=widths[1]
                ).grid(row=0, column=1, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=depto.get_nombre_gerente(),
                    font=("Arial", 11),
                    width=widths[2]
                ).grid(row=0, column=2, padx=2, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=str(depto.get_id_gerente()),
                    font=("Arial", 11),
                    width=widths[3]
                ).grid(row=0, column=3, padx=2, pady=2)
                
                for i in range(len(headers)):
                    row_frame.columnconfigure(i, weight=1)
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar departamentos: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)