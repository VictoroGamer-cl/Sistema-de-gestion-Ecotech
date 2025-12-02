from gui.login_window import LoginWindow

def main():
    try:
        print("Iniciando EcoTech Sistema de Gestión")
        app = LoginWindow()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()