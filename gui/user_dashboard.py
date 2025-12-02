import customtkinter as ctk
from tkinter import messagebox

class UserDashboard:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("EcoTech - Panel Usuario")
        self.root.geometry("1000x600")
        
        self.usuario_actual = None
        self.cargar_usuario_actual()
        self.crear_interfaz()
        
    def cargar_usuario_actual(self):
        try:
            from definiciones import Deficiones
            self.usuario_actual = Deficiones.usuario_actual
        except:
            self.usuario_actual = None
            
    def crear_interfaz(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        self.crear_sidebar()
        self.crear_contenido_principal()
        
        self.mostrar_seccion("dashboard")
        
    def crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.main_frame, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.sidebar.grid_propagate(False)
        
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=20, padx=10, fill="x")
        
        ctk.CTkLabel(
            logo_frame,
            text="EcoTech",
            font=("Arial", 20, "bold"),
            text_color="#2E8B57"
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="Panel Usuario",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        if self.usuario_actual:
            info_frame = ctk.CTkFrame(self.sidebar, fg_color="#2B2B2B")
            info_frame.pack(pady=10, padx=10, fill="x")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{self.usuario_actual.get_username()}",
                font=("Arial", 12, "bold")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                info_frame,
                text="Empleado",
                font=("Arial", 10),
                text_color="gray"
            ).pack(pady=(0, 5))
        
        self.crear_botones_navegacion()
        
        ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            hover_color="#FF6B6B"
        ).pack(side="bottom", pady=20, padx=10, fill="x")
    
    def crear_botones_navegacion(self):
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, pady=20, padx=10)
        
        botones_nav = [
            ("🏠 Menu Principal", "dashboard"),
            ("⏰ Registrar Horas", "registrar_horas"),
            ("📋 Mis Horas", "mis_horas"),
            ("📊 Proyectos Asignados", "proyectos"),
            ("💲 Indicadores", "indicadores")
        ]
        
        self.botones = {}
        
        for texto, comando in botones_nav:
            btn = ctk.CTkButton(
                nav_frame,
                text=texto,
                command=lambda cmd=comando: self.mostrar_seccion(cmd),
                anchor="w",
                height=40,
                fg_color="transparent",
                hover_color="#2B2B2B"
            )
            btn.pack(fill="x", pady=2)
            self.botones[comando] = btn
    
    def crear_contenido_principal(self):
        self.contenido = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=(0, 0))
        
        self.titulo_frame = ctk.CTkFrame(self.contenido, fg_color="transparent", height=80)
        self.titulo_frame.pack(fill="x", padx=20, pady=20)
        self.titulo_frame.pack_propagate(False)
        
        self.titulo_label = ctk.CTkLabel(
            self.titulo_frame,
            text="Dashboard Usuario",
            font=("Arial", 24, "bold")
        )
        self.titulo_label.pack(side="left")
        
        self.contenido_dinamico = ctk.CTkFrame(self.contenido, fg_color="transparent")
        self.contenido_dinamico.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def mostrar_seccion(self, seccion):
        for btn in self.botones.values():
            btn.configure(fg_color="transparent")
        
        if seccion in self.botones:
            self.botones[seccion].configure(fg_color="#2E8B57")
        
        titulos = {
            "dashboard": "Menu Usuario",
            "registrar_horas": "Registrar Horas Trabajadas",
            "mis_horas": "Mis Horas Trabajadas", 
            "proyectos": "Proyectos Asignados"
        }
        
        self.titulo_label.configure(text=titulos.get(seccion, "Dashboard"))
        
        for widget in self.contenido_dinamico.winfo_children():
            widget.destroy()
        
        if seccion == "dashboard":
            self.mostrar_dashboard()
        elif seccion == "registrar_horas":
            self.mostrar_registrar_horas()
        elif seccion == "mis_horas":
            self.mostrar_mis_horas()
        elif seccion == "proyectos":
            self.mostrar_proyectos()
        elif seccion == "indicadores":
            self.mostrar_indicadores()
    
    def mostrar_dashboard(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            contenido,
            text=f"Bienvenido {self.usuario_actual.get_username()}",
            font=("Arial", 28, "bold"),
            text_color="#2E8B57"
        ).pack(pady=40)
        
        ctk.CTkLabel(
            contenido,
            text="Sistema de Gestión EcoTech - Panel de Usuario",
            font=("Arial", 16),
            text_color="gray"
        ).pack(pady=10)
        
        stats_frame = ctk.CTkFrame(contenido, corner_radius=10)
        stats_frame.pack(pady=30, padx=50, fill="x")
        
        ctk.CTkLabel(
            stats_frame,
            text="Acciones Disponibles:",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        
        acciones = [
            "⏰ Registrar horas trabajadas",
            "📋 Ver mi historial de horas", 
            "📊 Consultar proyectos asignados",
            "👤 Gestionar información personal"
        ]
        
        for accion in acciones:
            ctk.CTkLabel(
                stats_frame,
                text=f"• {accion}",
                font=("Arial", 14)
            ).pack(pady=5)
    
    def mostrar_registrar_horas(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Registro de Horas Trabajadas",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            header_frame,
            text="+ Nueva Hora",
            command=self.registrar_horas,
            width=150,
            height=35,
            fg_color="#2E8B57",
            font=("Arial", 12, "bold")
        ).pack(side="right", padx=(10, 0))
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Registro de Horas",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Utilice el botón 'Nueva Hora' para registrar sus horas trabajadas.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)
    
    def mostrar_mis_horas(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Mis Horas Trabajadas",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            header_frame,
            text="Actualizar",
            command=self.ver_mis_horas,
            width=120,
            height=35,
            fg_color="#1E90FF",
            font=("Arial", 12, "bold")
        ).pack(side="right", padx=(10, 0))
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Historial de Horas",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Utilice el botón 'Actualizar' para ver su historial completo de horas.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)
    
    def mostrar_proyectos(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Mis Proyectos Asignados",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            header_frame,
            text="Actualizar",
            command=self.ver_proyectos_asignados,
            width=120,
            height=35,
            fg_color="#1E90FF",
            font=("Arial", 12, "bold")
        ).pack(side="right", padx=(10, 0))
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Proyectos Asignados",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Utilice el botón 'Actualizar' para ver los proyectos asignados a su departamento.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)

    def ver_proyectos_asignados(self):
        try:
            from gui.logs.proyectos.ver_proyectos_asignados import VerProyectosAsignadosLog
            VerProyectosAsignadosLog(self.root, self.usuario_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")

    def registrar_horas(self):
        try:
            from gui.logs.horas.registrar_horas import RegistrarHorasLog
            RegistrarHorasLog(self.root, self.usuario_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")
    
    def ver_mis_horas(self):
        try:
            from gui.logs.horas.ver_mis_horas import VerMisHorasLog
            VerMisHorasLog(self.root, self.usuario_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")
    
    def mostrar_indicadores(self):
            try:
                from gui.logs.indicadores.consultar_indicadores import ConsultarIndicadoresFrame
                frame = ConsultarIndicadoresFrame(self.contenido_dinamico, usuario_actual=self.usuario_actual)
                frame.pack(fill="both", expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar indicadores: {e}")

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            from definiciones import Deficiones
            Deficiones.usuario_actual = None
            self.root.destroy()
            from gui.login_window import LoginWindow
            login = LoginWindow()
            login.run()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = UserDashboard()
    app.run()