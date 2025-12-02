import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from datetime import datetime

class VerHistorialInformesLog:
    def __init__(self, parent, admin_actual):
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        self.crear_log()
    
    def crear_log(self):
        self.log = ctk.CTkToplevel(self.parent)
        self.log.title("Historial de Informes")
        self.log.geometry("800x600")
        self.log.transient(self.parent)
        self.log.grab_set()
        
        titulo_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            titulo_frame,
            text="Historial de Informes Generados",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            titulo_frame,
            text="Actualizar",
            command=lambda: self.cargar_historial(),
            width=100,
            height=35
        ).pack(side="right")
        
        self.contenido_frame = ctk.CTkFrame(self.log, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.cargar_historial()
    
    def cargar_historial(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        try:
            informes = self.dao.obtener_informes()
            
            if not informes:
                ctk.CTkLabel(
                    self.contenido_frame,
                    text="No hay informes en el historial",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            # Frame para estadísticas
            stats_frame = ctk.CTkFrame(self.contenido_frame, fg_color="#2B2B2B")
            stats_frame.pack(fill="x", pady=(0, 15), padx=10)
            
            total_informes = len(informes)
            pdf_count = sum(1 for inf in informes if inf.get_formato().lower() == 'pdf')
            excel_count = sum(1 for inf in informes if inf.get_formato().lower() == 'excel')
            
            stats_text = f"Total: {total_informes} informes | PDF: {pdf_count} | Excel: {excel_count}"
            ctk.CTkLabel(
                stats_frame,
                text=stats_text,
                font=("Arial", 12, "bold")
            ).pack(pady=8)
            
            # Frame scrollable para la tabla
            scroll_frame = ctk.CTkScrollableFrame(self.contenido_frame)
            scroll_frame.pack(fill="both", expand=True)
            
            # Headers de la tabla
            headers_frame = ctk.CTkFrame(scroll_frame, fg_color="#2B2B2B", height=40)
            headers_frame.pack(fill="x", pady=(0, 5))
            headers_frame.pack_propagate(False)
            
            headers = ["ID", "Nombre", "Tipo", "Formato", "Fecha", "Acciones"]
            widths = [60, 200, 120, 80, 150, 120]
            
            for i, header in enumerate(headers):
                ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=widths[i]
                ).grid(row=0, column=i, padx=2, pady=2)
            
            # Datos de informes
            for informe in informes:
                row_frame = ctk.CTkFrame(scroll_frame, height=40)
                row_frame.pack(fill="x", pady=2)
                row_frame.pack_propagate(False)
                
                # ID
                ctk.CTkLabel(
                    row_frame,
                    text=str(informe.get_id()),
                    font=("Arial", 11),
                    width=widths[0]
                ).grid(row=0, column=0, padx=2, pady=2)
                
                # Nombre
                ctk.CTkLabel(
                    row_frame,
                    text=informe.get_nombre_reporte(),
                    font=("Arial", 11),
                    width=widths[1]
                ).grid(row=0, column=1, padx=2, pady=2)
                
                # Tipo
                tipo_text = informe.get_tipo_reporte().replace("_", " ").title()
                ctk.CTkLabel(
                    row_frame,
                    text=tipo_text,
                    font=("Arial", 11),
                    width=widths[2]
                ).grid(row=0, column=2, padx=2, pady=2)
                
                # Formato
                formato_text = informe.get_formato().upper()
                ctk.CTkLabel(
                    row_frame,
                    text=formato_text,
                    font=("Arial", 11),
                    width=widths[3]
                ).grid(row=0, column=3, padx=2, pady=2)
                
                # Fecha
                fecha = informe.get_fecha_generacion()
                if hasattr(fecha, 'strftime'):
                    fecha_text = fecha.strftime("%Y-%m-%d %H:%M")
                else:
                    fecha_text = str(fecha)
                
                ctk.CTkLabel(
                    row_frame,
                    text=fecha_text,
                    font=("Arial", 11),
                    width=widths[4]
                ).grid(row=0, column=4, padx=2, pady=2)
                
                # Acciones
                action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[5])
                action_frame.grid(row=0, column=5, padx=2, pady=2)
                action_frame.grid_propagate(False)
                
                ctk.CTkButton(
                    action_frame,
                    text="Eliminar",
                    command=lambda inf=informe: self.eliminar_informe(inf),
                    width=60,
                    height=25,
                    font=("Arial", 10),
                    fg_color="#FF6B6B",
                    hover_color="#FF5252"
                ).pack(side="left", padx=2)
                
                # Configurar grid weights
                for i in range(len(headers)):
                    row_frame.columnconfigure(i, weight=1)
                    
        except Exception as e:
            ctk.CTkLabel(
                self.contenido_frame,
                text=f"Error al cargar historial: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=50)
    
    def eliminar_informe(self, informe):
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el informe?\n\n"
            f"Nombre: {informe.get_nombre_reporte()}\n"
            f"Tipo: {informe.get_tipo_reporte()}\n"
            f"Formato: {informe.get_formato()}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                if self.dao.eliminar_informe(informe.get_id()):
                    messagebox.showinfo("Éxito", "Informe eliminado correctamente")
                    self.cargar_historial()  # Recargar la lista
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el informe")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar informe: {e}")