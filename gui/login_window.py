import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading

class LoginWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("EcoTech - Sistema de Gestion")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        self.center_window()
        self.create_widgets()
        self.tipo_usuario = None
        
    def center_window(self):
        self.root.update_idletasks()
        width = 600
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="EcoTech",
            font=("Arial", 32, "bold"),
            text_color="#2E8B57"
        )
        self.title_label.pack(pady=(30, 10))
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Sistema de Gestion",
            font=("Arial", 18),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 40))
        
        self.seleccion_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.seleccion_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.seleccion_frame,
            text="Seleccione tipo de usuario:",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 30))
        
        self.admin_btn = ctk.CTkButton(
            self.seleccion_frame,
            text="Administrador",
            command=lambda: self.seleccionar_tipo("admin"),
            width=250,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        self.admin_btn.pack(pady=20)
        
        self.user_btn = ctk.CTkButton(
            self.seleccion_frame,
            text="Usuario",
            command=lambda: self.seleccionar_tipo("user"),
            width=250,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#1E90FF",
            hover_color="#4169E1"
        )
        self.user_btn.pack(pady=20)
        
        self.login_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.footer_label = ctk.CTkLabel(
            self.main_frame,
            text="© 2025 EcoTech - Todos los derechos reservados",
            font=("Arial", 12),
            text_color="gray"
        )
        self.footer_label.pack(side="bottom", pady=20)
        
    def seleccionar_tipo(self, tipo):
        self.tipo_usuario = tipo
        
        if tipo == "admin":
            self.admin_btn.configure(fg_color="#2E8B57")
            self.user_btn.configure(fg_color="#1E90FF")
        else:
            self.admin_btn.configure(fg_color="#1E90FF")
            self.user_btn.configure(fg_color="#2E8B57")
            
        self.mostrar_formulario_login()
        
    def mostrar_formulario_login(self):
        self.seleccion_frame.pack_forget()
        self.footer_label.pack_forget()
        
        self.login_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        tipo_texto = "Administrador" if self.tipo_usuario == "admin" else "Usuario"
        ctk.CTkLabel(
            self.login_frame,
            text=f"Iniciar como {tipo_texto}",
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 30))
        
        self.username_label = ctk.CTkLabel(
            self.login_frame,
            text="Usuario:",
            font=("Arial", 16, "bold")
        )
        self.username_label.pack(anchor="w", pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Ingrese su usuario",
            width=350,
            height=50,
            font=("Arial", 16),
            corner_radius=10
        )
        self.username_entry.pack(pady=(0, 20), fill="x")
        
        self.password_label = ctk.CTkLabel(
            self.login_frame,
            text="Contraseña:",
            font=("Arial", 16, "bold")
        )
        self.password_label.pack(anchor="w", pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Ingrese su contraseña",
            show="•",
            width=350,
            height=50,
            font=("Arial", 16),
            corner_radius=10
        )
        self.password_entry.pack(pady=(0, 30), fill="x")
        
        button_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        
        self.login_btn = ctk.CTkButton(
            button_frame,
            text="Iniciar Sesion",
            command=self.login,
            width=200,
            height=55,
            font=("Arial", 18, "bold"),
            corner_radius=10,
            fg_color="#2E8B57"
        )
        self.login_btn.pack(pady=10)
        
        self.volver_btn = ctk.CTkButton(
            button_frame,
            text="Volver",
            command=self.volver_seleccion,
            width=150,
            height=40,
            font=("Arial", 14),
            fg_color="transparent",
            border_width=1
        )
        self.volver_btn.pack(pady=10)
        
        self.progress = ctk.CTkProgressBar(self.login_frame, width=350, height=4)
        self.progress.pack(pady=10)
        self.progress.set(0)
        self.progress.pack_forget()
        
        self.status_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            font=("Arial", 14),
            wraplength=350
        )
        self.status_label.pack(pady=10)
        
        self.footer_label.pack(side="bottom", pady=20)
        self.username_entry.focus()
        
    def volver_seleccion(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()
            
        self.login_frame.pack_forget()
        self.seleccion_frame.pack(pady=20, padx=40, fill="both", expand=True)
        self.tipo_usuario = None
        
    def show_loading(self, show=True):
        if show:
            self.progress.pack(pady=10)
            self.progress.start()
        else:
            self.progress.pack_forget()
            self.progress.stop()
            
    def set_status(self, message, is_error=False):
        color = "red" if is_error else "green"
        self.status_label.configure(text=message, text_color=color)
        
    def login(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.set_status("Complete todos los campos", True)
            return
            
        self.show_loading(True)
        self.set_status("Conectando...")
        
        if self.tipo_usuario == "admin":
            thread = threading.Thread(target=self._login_admin_thread, args=(username, password))
        else:
            thread = threading.Thread(target=self._login_user_thread, args=(username, password))
            
        thread.daemon = True
        thread.start()
        
    def _login_admin_thread(self, username, password):
        try:
            from DAO import DAO
            from definiciones import Deficiones
            
            dao = DAO()
            admin = dao.login_administrador(username, password)
            self.root.after(0, self._login_admin_callback, admin)
            
        except Exception as e:
            self.root.after(0, self._login_error_callback, str(e))
            
    def _login_admin_callback(self, admin):
        self.show_loading(False)
        
        if admin:
            from definiciones import Deficiones
            Deficiones.admin_actual = admin
            self.set_status("Login exitoso! Redirigiendo...")
            self.root.after(1500, self.open_admin_dashboard)
        else:
            self.set_status("Credenciales incorrectas", True)
            
    def _login_user_thread(self, username, password):
        try:
            from DAO import DAO
            from definiciones import Deficiones
            
            dao = DAO()
            user = dao.login_usuario(username, password)
            self.root.after(0, self._login_user_callback, user)
            
        except Exception as e:
            self.root.after(0, self._login_error_callback, str(e))
            
    def _login_user_callback(self, user):
        self.show_loading(False)
        
        if user:
            from definiciones import Deficiones
            Deficiones.usuario_actual = user
            self.set_status("Login exitoso! Redirigiendo...")
            self.root.after(1500, self.open_user_dashboard)
        else:
            self.set_status("Credenciales incorrectas", True)
            
    def _login_error_callback(self, error_msg):
        self.show_loading(False)
        self.set_status(f"Error: {error_msg}", True)
        
    def open_admin_dashboard(self):
        try:
            print("Intentando importar AdminDashboard...")  
            from gui.admin_dashboard import AdminDashboard
            print("AdminDashboard importado correctamente")  
            self.root.destroy()
            admin_dash = AdminDashboard()
            admin_dash.run()
        except ImportError as e:
            print(f"Error importando AdminDashboard: {e}")  
            messagebox.showerror("Error", f"No se pudo cargar el dashboard: {e}")

    def open_user_dashboard(self):
        try:
            print("Intentando importar UserDashboard...")  
            from gui.user_dashboard import UserDashboard
            print("UserDashboard importado correctamente")  
            self.root.destroy()
            user_dash = UserDashboard()
            user_dash.run()
        except ImportError as e:
            print(f"Error importando UserDashboard: {e}")  
            messagebox.showerror("Error", f"No se pudo cargar el dashboard: {e}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()