import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from Informe import Informe

class GenerarInformeDepartamentosLog(ctk.CTkToplevel):
    def __init__(self, parent, admin_actual):
        super().__init__(parent)
        self.parent = parent
        self.admin_actual = admin_actual
        self.dao = DAO()
        
        self.title("Generar Informe de Departamentos")
        self.geometry("500x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.crear_interfaz()
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="Generar Informe de Departamentos",
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        
        nombre_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nombre_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            nombre_frame,
            text="Nombre del archivo:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        self.nombre_var = ctk.StringVar()
        ctk.CTkEntry(
            nombre_frame,
            textvariable=self.nombre_var,
            placeholder_text="Ej: informe_departamentos_enero",
            width=300,
            height=35
        ).pack(fill="x", pady=5)
        
        info_frame = ctk.CTkFrame(main_frame, fg_color="#2B2B2B", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Información:",
            font=("Arial", 12, "bold"),
            text_color="#87CEEB"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            info_frame,
            text="• El informe incluirá todos los departamentos registrados\n• Formato: PDF\n• Se guardará en la carpeta de reportes del sistema",
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
        
        botones_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botones_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            botones_frame,
            text="📊 Generar Informe",
            command=self.generar_informe,
            height=40,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            botones_frame,
            text="Cancelar",
            command=self.destroy,
            height=40,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=("Arial", 12)
        ).pack(side="left")
    
    def generar_informe(self):
        nombre_archivo = self.nombre_var.get().strip()
        
        if not nombre_archivo:
            messagebox.showerror("Error", "El nombre del archivo es obligatorio")
            return
        
        try:
            departamentos = self.dao.obtener_departamentos()
            
            if not departamentos:
                messagebox.showwarning("Advertencia", "No hay departamentos para generar el informe")
                return
            
            ruta = self.dao.generar_reporte_departamentos_pdf(departamentos, nombre_archivo)
            
            if ruta.startswith("Error:"):
                messagebox.showerror("Error", f"No se pudo generar el informe: {ruta}")
                return

            informe = Informe(
                None,
                f"Informe Departamentos - {nombre_archivo}",
                "departamentos",
                "pdf",
                None,
                self.admin_actual.get_id()
            )
            self.dao.guardar_informe(informe)
            
            messagebox.showinfo("Éxito", 
                f"✅ Informe de departamentos generado exitosamente\n\n"
                f"📊 Departamentos incluidos: {len(departamentos)}\n"
                f"📍 Ubicación: {ruta}"
            )
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al generar informe: {str(e)}")