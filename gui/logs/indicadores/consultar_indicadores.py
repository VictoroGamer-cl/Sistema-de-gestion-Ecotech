import customtkinter as ctk
from tkinter import messagebox
from DAO import DAO
from indicadores import GestorIndicadores

class ConsultarIndicadoresFrame(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual=None, admin_actual=None):
        super().__init__(parent, fg_color="transparent")
        self.usuario_sistema = usuario_actual if usuario_actual else admin_actual
        self.dao = DAO()
        self.gestor_api = GestorIndicadores()
        self.ultimo_resultado = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # --- TÍTULO ---
        titulo_frame = ctk.CTkFrame(self, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(20, 10))
        
        ctk.CTkLabel(
            titulo_frame,
            text="Consulta de Indicadores Económicos",
            font=("Arial", 24, "bold"),
            text_color="#2E8B57"
        ).pack()

        # --- SECCIÓN FECHA (Centrada) ---
        fecha_frame = ctk.CTkFrame(self, fg_color="transparent")
        fecha_frame.pack(pady=5)
        
        ctk.CTkLabel(fecha_frame, text="Fecha consulta (Opcional):", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.entry_fecha = ctk.CTkEntry(
            fecha_frame, 
            width=150, 
            placeholder_text="DD-MM-YYYY"
        )
        self.entry_fecha.pack(side="left", padx=5)
        
        ctk.CTkLabel(fecha_frame, text="(Deje vacío para hoy)", font=("Arial", 10), text_color="gray").pack(side="left")

        # --- BOTONERA DE INDICADORES (Estilo Solicitado) ---
        acciones_frame = ctk.CTkFrame(self, fg_color="transparent")
        acciones_frame.pack(fill="x", pady=20, padx=20)
        
        # Lista de botones: (Texto, Código API, Color)
        botones_indicadores = [
            ("💰 UF", "uf", "#2E8B57"),          # Verde
            ("💵 Dólar", "dolar", "#1E90FF"),    # Azul
            ("💶 Euro", "euro", "#9370DB"),      # Morado
            ("📊 UTM", "utm", "#FF8C00"),        # Naranja
            ("📈 IPC", "ipc", "#FF6B6B")         # Rojo
        ]
        
        # Crear botones dinámicamente y centrarlos usando pack expand=True
        for texto, codigo, color in botones_indicadores:
            ctk.CTkButton(
                acciones_frame,
                text=texto,
                command=lambda c=codigo: self.consultar_api(c),
                width=140,
                height=40,
                fg_color=color,
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=5, expand=True)

        # --- SECCIÓN RESULTADOS ---
        self.panel_resultado = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=15)
        self.panel_resultado.pack(fill="both", expand=True, padx=40, pady=(10, 30))
        self.panel_resultado.pack_propagate(False) 
        
        self.crear_vista_inicial()

    def crear_vista_inicial(self):
        for widget in self.panel_resultado.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(
            self.panel_resultado, 
            text="👆 Seleccione un indicador arriba para consultar",
            font=("Arial", 16),
            text_color="gray"
        ).pack(expand=True)

    def consultar_api(self, codigo_moneda):
        fecha = self.entry_fecha.get().strip()
        
        if fecha and len(fecha) != 10:
             messagebox.showerror("Error", "Formato de fecha incorrecto. Use dd-mm-yyyy")
             return

        try:
            self.configure(cursor="watch")
            self.update()
            
            # Llamada al gestor
            resultado = self.gestor_api.obtener_indicador(codigo_moneda, fecha if fecha else None)
            
            self.configure(cursor="")
            
            if "error" in resultado:
                messagebox.showerror("Error API", resultado["error"])
            else:
                self.mostrar_resultados(resultado, codigo_moneda)
                
        except Exception as e:
            self.configure(cursor="")
            messagebox.showerror("Error", f"Error crítico: {str(e)}")

    def mostrar_resultados(self, resultado, codigo):
        self.ultimo_resultado = resultado
        
        for widget in self.panel_resultado.winfo_children():
            widget.destroy()
            
        content = ctk.CTkFrame(self.panel_resultado, fg_color="transparent")
        content.pack(expand=True)
        
        ctk.CTkLabel(
            content,
            text=resultado["indicador"].upper(),
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=(0, 10))
        
        valor = resultado["valor"]
        texto_valor = f"{valor}%" if codigo == "ipc" else f"${valor:,.2f}"
        
        ctk.CTkLabel(
            content,
            text=texto_valor,
            font=("Arial", 50, "bold"),
            text_color="#2E8B57"
        ).pack(pady=10)
        
        ctk.CTkLabel(content, text=f"📅 Fecha: {resultado['fecha']}", font=("Arial", 14), text_color="gray").pack()
        
        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(
            content,
            text="💾 Guardar en Historial",
            command=self.guardar_en_bd,
            width=200,
            height=40,
            fg_color="#4B4B4B",
            hover_color="#5C5C5C"
        )
        self.btn_guardar.pack(pady=30)

    def guardar_en_bd(self):
        if not self.ultimo_resultado: return
        try:
            nombre_usuario = "Desconocido"
            if self.usuario_sistema:
                nombre_usuario = self.usuario_sistema.get_username()
            
            exito = self.dao.registrar_consulta_indicador(
                self.ultimo_resultado['indicador'],
                self.ultimo_resultado['valor'],
                self.ultimo_resultado['fecha'],
                nombre_usuario,
                self.ultimo_resultado['origen']
            )
            
            if exito:
                messagebox.showinfo("Éxito", "Consulta guardada en el historial.")
                self.btn_guardar.configure(state="disabled", text="✅ Guardado", fg_color="#2E8B57")
            else:
                messagebox.showerror("Error", "No se pudo guardar en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")