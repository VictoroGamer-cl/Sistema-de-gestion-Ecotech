import customtkinter as ctk
from tkinter import messagebox

class AdminDashboard:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("EcoTech - Panel Administrador")
        self.root.geometry("1200x700")
        
        self.admin_actual = None
        self.cargar_admin_actual()
        self.crear_interfaz()
        
    def cargar_admin_actual(self):
        try:
            from definiciones import Deficiones
            self.admin_actual = Deficiones.admin_actual
        except:
            self.admin_actual = None
    
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
            text="Panel Administrador",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        if self.admin_actual:
            info_frame = ctk.CTkFrame(self.sidebar, fg_color="#2B2B2B")
            info_frame.pack(pady=10, padx=10, fill="x")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{self.admin_actual.get_username()}",
                font=("Arial", 12, "bold")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                info_frame,
                text=f"{self.admin_actual.get_email()}",
                font=("Arial", 10),
                text_color="gray"
            ).pack(pady=(0, 5))
        
        self.crear_botones_navegacion()
        
        ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesion",
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
                    ("👥 Empleados", "empleados"),
                    ("🏢 Departamentos", "departamentos"),
                    ("📋 Proyectos", "proyectos"),
                    ("⏰ Horas Trabajadas", "horas"),
                    ("📊 Informes", "informes"),
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
            text="Dashboard Principal",
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
            "dashboard": "Menu Principal",
            "empleados": "Gestion de Empleados",
            "departamentos": "Gestion de Departamentos", 
            "proyectos": "Gestion de Proyectos",
            "horas": "Horas Trabajadas",
            "informes": "Generacion de Informes"
        }
        
        self.titulo_label.configure(text=titulos.get(seccion, "Dashboard"))
        
        for widget in self.contenido_dinamico.winfo_children():
            widget.destroy()
        
        if seccion == "dashboard":
            self.mostrar_dashboard()
        elif seccion == "empleados":
            self.mostrar_empleados()
        elif seccion == "departamentos":
            self.mostrar_departamentos()
        elif seccion == "proyectos":
            self.mostrar_proyectos()
        elif seccion == "horas":
            self.mostrar_horas()
        elif seccion == "informes":
            self.mostrar_informes()
        elif seccion == "indicadores":
            self.mostrar_indicadores()
    
    def mostrar_dashboard(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            contenido,
            text="Bienvenido al Sistema EcoTech",
            font=("Arial", 28, "bold"),
            text_color="#2E8B57"
        ).pack(pady=40)
        
        ctk.CTkLabel(
            contenido,
            text="Seleccione una opción del menú lateral para comenzar",
            font=("Arial", 16),
            text_color="gray"
        ).pack(pady=10)
        
        # Estadísticas rápidas
        stats_frame = ctk.CTkFrame(contenido, corner_radius=10)
        stats_frame.pack(pady=30, padx=50, fill="x")
        
        ctk.CTkLabel(
            stats_frame,
            text="Acciones Disponibles:",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        
        acciones = [
            "👥 Gestión completa de empleados",
            "🏢 Administración de departamentos", 
            "📋 Control de proyectos",
            "⏰ Registro de horas trabajadas",
            "📊 Generación de informes"
        ]
        
        for accion in acciones:
            ctk.CTkLabel(
                stats_frame,
                text=f"• {accion}",
                font=("Arial", 14)
            ).pack(pady=5)
    
    def mostrar_empleados(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        acciones_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones_frame.pack(fill="x", pady=20)

        botones_empleados = [
            ("📝 Registrar Empleado", "registrar_empleado", "#2E8B57"),
            ("👁️ Mostrar Empleado", "mostrar_empleado", "#1E90FF"),
            ("📋 Listar Todos", "listar_empleados", "#9370DB"),
            ("✏️ Actualizar", "actualizar_empleado", "#FF8C00"),
            ("🗑️ Eliminar", "eliminar_empleado", "#FF6B6B")
        ]
        
        for texto, comando, color in botones_empleados:
            ctk.CTkButton(
                acciones_frame,
                text=texto,
                command=lambda cmd=comando: self.ejecutar_accion_empleado(cmd),
                width=150,
                height=40,
                fg_color=color,
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Gestión Completa de Empleados",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Utilice los botones superiores para realizar las operaciones.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)
    
    def ejecutar_accion_empleado(self, accion):
        try:
            if accion == "registrar_empleado":
                from gui.logs.empleados.registrar_empleado import RegistrarEmpleadoLog
                log = RegistrarEmpleadoLog(self.root, self.admin_actual)
            elif accion == "mostrar_empleado":
                from gui.logs.empleados.mostrar_empleado import MostrarEmpleadoLog
                log = MostrarEmpleadoLog(self.root, self.admin_actual)
            elif accion == "listar_empleados":
                from gui.logs.empleados.listar_empleados import ListarEmpleadosLog
                log = ListarEmpleadosLog(self.root, self.admin_actual)
            elif accion == "actualizar_empleado":
                from gui.logs.empleados.actualizar_empleado import ActualizarEmpleadoLog
                log = ActualizarEmpleadoLog(self.root, self.admin_actual)
            elif accion == "eliminar_empleado":
                from gui.logs.empleados.eliminar_empleado import EliminarEmpleadoLog
                log = EliminarEmpleadoLog(self.root, self.admin_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la función: {e}")
    
    def mostrar_departamentos(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        acciones_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones_frame.pack(fill="x", pady=20)
        
        botones_departamentos = [
            ("🏢 Registrar Departamento", "registrar_departamento", "#2E8B57"),
            ("📋 Listar Departamentos", "listar_departamentos", "#1E90FF"),
            ("👥 Asignar Empleado", "asignar_empleado", "#9370DB"),
            ("🗑️ Eliminar Departamento", "eliminar_departamento", "#FF6B6B")
        ]
        
        for texto, comando, color in botones_departamentos:
            ctk.CTkButton(
                acciones_frame,
                text=texto,
                command=lambda cmd=comando: self.ejecutar_accion_departamento(cmd),
                width=180,
                height=40,
                fg_color=color,
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Gestión de Departamentos",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Utilice los botones superiores para realizar las operaciones.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)

    def ejecutar_accion_departamento(self, accion):
        try:
            if accion == "registrar_departamento":
                from gui.logs.departamentos.registrar_departamento import RegistrarDepartamentoLog
                RegistrarDepartamentoLog(self.root, self.admin_actual)
            elif accion == "listar_departamentos":
                from gui.logs.departamentos.listar_departamentos import ListarDepartamentosLog
                ListarDepartamentosLog(self.root, self.admin_actual)
            elif accion == "asignar_empleado":
                from gui.logs.departamentos.asignar_empleado import AsignarEmpleadoLog
                AsignarEmpleadoLog(self.root, self.admin_actual)
            elif accion == "eliminar_departamento":
                from gui.logs.departamentos.eliminar_departamento import EliminarDepartamentoLog
                EliminarDepartamentoLog(self.root, self.admin_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la función: {e}")
    
    def mostrar_proyectos(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        acciones_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones_frame.pack(fill="x", pady=20)
        
        botones_proyectos = [
            ("📋 Registrar Proyecto", "registrar_proyecto", "#2E8B57"),
            ("📊 Listar Proyectos", "listar_proyectos", "#1E90FF"),
            ("👥 Asignar Empleados", "asignar_empleados_proyecto", "#9370DB"),
            ("✏️ Actualizar Proyecto", "actualizar_proyecto", "#FF8C00"),
            ("🗑️ Eliminar Proyecto", "eliminar_proyecto", "#FF6B6B")
        ]
        
        for texto, comando, color in botones_proyectos:
            ctk.CTkButton(
                acciones_frame,
                text=texto,
                command=lambda cmd=comando: self.ejecutar_accion_proyecto(cmd),
                width=180,
                height=40,
                fg_color=color,
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Gestión de Proyectos",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Utilice los botones superiores para realizar las operaciones.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)

    def ejecutar_accion_proyecto(self, accion):
        try:
            if accion == "registrar_proyecto":
                from gui.logs.proyectos.registrar_proyecto import RegistrarProyectoLog
                RegistrarProyectoLog(self.root, self.admin_actual)
            elif accion == "listar_proyectos":
                from gui.logs.proyectos.listar_proyectos import ListarProyectosLog
                ListarProyectosLog(self.root, self.admin_actual)
            elif accion == "asignar_empleados_proyecto":  # NUEVA OPCIÓN
                from gui.logs.proyectos.asignar_empleados_proyecto import AsignarEmpleadosProyectoLog
                AsignarEmpleadosProyectoLog(self.root, self.admin_actual)
            elif accion == "actualizar_proyecto":
                from gui.logs.proyectos.seleccionar_proyecto import SeleccionarProyectoLog
                SeleccionarProyectoLog(self.root, self.admin_actual)
            elif accion == "eliminar_proyecto":
                from gui.logs.proyectos.eliminar_proyecto import EliminarProyectoLog
                EliminarProyectoLog(self.root, self.admin_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la función: {e}")
    
    def mostrar_horas(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        acciones_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            acciones_frame,
            text="📊 Administrar Horas",
            command=lambda: self.ejecutar_accion_horas("administrar_horas"),
            width=200,
            height=40,
            fg_color="#9370DB",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=5)
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Administración de Horas Trabajadas",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Vea y administre las horas trabajadas de todos los empleados.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)

    def ejecutar_accion_horas(self, accion):
        try:
            if accion == "administrar_horas":
                from gui.logs.horas.administrar_horas import AdministrarHorasLog
                AdministrarHorasLog(self.root, self.admin_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la función: {e}")
    
    def mostrar_informes(self):
        contenido = ctk.CTkFrame(self.contenido_dinamico, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        
        acciones_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones_frame.pack(fill="x", pady=20)
        
        botones_informes = [
            ("📊 Informe Empleados", "informe_empleados", "#2E8B57"),
            ("📈 Informe Proyectos", "informe_proyectos", "#1E90FF"),
            ("🏢 Informe Departamentos", "informe_departamentos", "#9370DB"),
            ("📋 Historial Informes", "historial_informes", "#FF8C00")
        ]
        
        for texto, comando, color in botones_informes:
            ctk.CTkButton(
                acciones_frame,
                text=texto,
                command=lambda cmd=comando: self.ejecutar_accion_informe(cmd),
                width=180,
                height=40,
                fg_color=color,
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)
        
        info_frame = ctk.CTkFrame(contenido, corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Generación de Informes",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        ctk.CTkLabel(
            info_frame,
            text="Genere informes en diferentes formatos (PDF/Excel) para análisis y reportes.",
            font=("Arial", 14),
            text_color="gray",
            justify="center"
        ).pack(pady=10)

    def ejecutar_accion_informe(self, accion):
        try:
            if accion == "informe_empleados":
                from gui.logs.informes.generar_informe_empleados import GenerarInformeEmpleadosLog
                GenerarInformeEmpleadosLog(self.root, self.admin_actual)
            elif accion == "informe_proyectos":
                from gui.logs.informes.generar_informe_proyectos import GenerarInformeProyectosLog
                GenerarInformeProyectosLog(self.root, self.admin_actual)
            elif accion == "informe_departamentos":
                from gui.logs.informes.generar_informe_departamentos import GenerarInformeDepartamentosLog
                GenerarInformeDepartamentosLog(self.root, self.admin_actual)
            elif accion == "historial_informes":
                from gui.logs.informes.ver_historial_informes import VerHistorialInformesLog
                VerHistorialInformesLog(self.root, self.admin_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la función: {e}")
    
    def mostrar_indicadores(self):
        try:
            from gui.logs.indicadores.consultar_indicadores import ConsultarIndicadoresFrame
            frame = ConsultarIndicadoresFrame(self.contenido_dinamico, admin_actual=self.admin_actual
            )
            frame.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar indicadores: {e}")
            
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            from definiciones import Deficiones
            Deficiones.admin_actual = None
            self.root.destroy()
            from gui.login_window import LoginWindow
            login = LoginWindow()
            login.run()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdminDashboard()
    app.run()