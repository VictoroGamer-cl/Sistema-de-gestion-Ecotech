from EcoTech import EcoTech
from DAO import DAO
from Departamento import Departamento
from Administrador import Administrador
from Usuarios import Usuario
from HoraTrabajada import HoraTrabajada
from Proyecto import Proyecto
from Informe import Informe
import getpass
import re
empleados = []
indice = 0
dao = DAO()


def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@ecotech\.cl$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    return len(str(telefono)) <= 9 and telefono > 0

def limpiar_input(texto):
    if texto is None:
        return ""
    texto_limpio = re.sub(r'[<>\'";\(\)&\|]', '', str(texto))
    return texto_limpio.strip()

def validar_fecha(fecha):
    patron = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(patron, fecha):
        return False
    try:
        año, mes, dia = map(int, fecha.split('-'))
        return año > 2000 and 1 <= mes <= 12 and 1 <= dia <= 31
    except ValueError:
        return False

class Deficiones:
    admin_actual = None
    usuario_actual = None
    def mostrar_menu():
        print("\n" + "="*40)
        print("        SISTEMA ECO-TECH")
        print("="*40)
        
        if Deficiones.admin_actual is not None:
            print(f"Admin: {Deficiones.admin_actual.get_username()}")
            print("="*40)
            print("1. Registrar empleado")
            print("2. Actualizar empleado")
            print("3. Mostrar empleado")
            print("4. Mostrar todos los empleados")
            print("5. Eliminar empleado")
            print("6. Registrar departamento")
            print("7. Listar departamentos")
            print("8. Asignar empleado a departamento")
            print("9. Ver empleados por departamento")
            print("10. Eliminar departamento")
            print("11. Registrar nuevo administrador")
            print("12. Ver información del admin actual")
            print("13. Ver horas trabajadas empleados")
            print("14. Registrar proyecto")
            print("15. Listar proyectos")
            print("16. Actualizar proyecto")
            print("17. Eliminar proyecto")
            print("18. Generar informe empleados")     
            print("19. Generar informe proyectos")       
            print("20. Generar informe departamentos")    
            print("21. Ver historial informes") 
            print("01. Cerrar sesión")                   
            print("0. Salir")
            print("="*40)
            OPCIONES = {
                "1": Deficiones.registrar_empleado,
                "2": Deficiones.actualizar_empleado,
                "3": Deficiones.mostrar_empleado,
                "4": Deficiones.mostrar_todos_empleados,
                "5": Deficiones.eliminar_empleado,
                "6": Deficiones.registrar_departamento,
                "7": Deficiones.listar_departamentos,
                "8": Deficiones.asignar_empleado_departamento,
                "9": Deficiones.mostrar_empleados_por_departamento,
                "10": Deficiones.eliminar_departamento,
                "11": Deficiones.registrar_administrador,
                "12": Deficiones.mostrar_info_admin_actual,
                "13": Deficiones.administrar_horas_trabajadas,
                "14": Deficiones.registrar_proyecto,
                "15": Deficiones.listar_proyectos,
                "16": Deficiones.actualizar_proyecto,
                "17": Deficiones.eliminar_proyecto,
                "18": Deficiones.generar_informe_empleados,      
                "19": Deficiones.generar_informe_proyectos,      
                "20": Deficiones.generar_informe_departamentos,  
                "21": Deficiones.ver_historial_informes,         
                "01": Deficiones.logout_administrador     
            }
            
        elif Deficiones.usuario_actual is not None:
            print(f"Usuario: {Deficiones.usuario_actual.get_username()}")
            print("="*40)
            print("1. Ver información de mi usuario")
            print("2. Registrar horas trabajadas")
            print("3. Ver mis horas trabajadas")
            print("4. Listar proyectos")
            print("01. Cerrar sesión")                    
            print("0. Salir")
            print("="*40)
            OPCIONES = {
                "1": Deficiones.mostrar_info_usuario_actual,
                "2": Deficiones.registrar_horas_trabajadas,
                "3": Deficiones.ver_mis_horas_trabajadas,
                "4": Deficiones.listar_proyectos,
                "01": Deficiones.logout_usuario           #
            }
            
        else:
            print("        Sistema de Gestión EcoTech")
            print("="*40)
            print("1. Iniciar sesión como administrador")
            print("2. Iniciar sesión como usuario")
            print("0. Salir")
            print("="*40)
            
            OPCIONES = {
                "1": Deficiones.login_administrador,
                "2": Deficiones.login_usuario,
            }
        
        return OPCIONES

    def confirmar_salir_pestana():
        while True:
            respuesta = input("\n¿Desea salir de esta pestaña? (S/N): ").strip().upper()
            if respuesta == 'S':
                return True
            if respuesta == 'N' or respuesta == '':
                return False
            print("Respuesta inválida. Ingrese 'S' o 'N'.")

    def mostrar_empleado():
        while True:
            try:
                empleados = dao.obtener_empleados()
            except Exception as e:
                print(f"Error al obtener empleados: {e}")
                return
            if not empleados:
                print("No hay empleados registrados.")
                return

            print("\n--- LISTA DE EMPLEADOS ---")
            for emp in empleados:
                print(f"ID:{emp.get_id()}- Nombre: {emp.get_nombre()}")

            try:
                id_empleado = int(input("\nIngrese el ID del empleado para ver sus datos (Ingrese 0 para salir): "))
            except ValueError:
                print("ID inválido.")
                if Deficiones.confirmar_salir_pestana():
                    return
                else:
                    continue

            if id_empleado == 0:
                return

            empleado_encontrado = None
            for emp in empleados:
                if emp.get_id() == id_empleado:
                    empleado_encontrado = emp
                    break

            if empleado_encontrado:
                print(f"\n--- DETALLES DEL EMPLEADO ID: {id_empleado} ---")
                print(f"ID: {empleado_encontrado.get_id()}")
                print(f"Nombre: {empleado_encontrado.get_nombre()}")
                print(f"Direccion: {empleado_encontrado.get_direccion()}")
                print(f"Telefono: {empleado_encontrado.get_telefono()}")
                print(f"Email: {empleado_encontrado.get_mail()}")
                print(f"Fecha de inicio: {empleado_encontrado.get_fecheIC()}")
                print(f"Salario: {empleado_encontrado.get_salario()}")
            else:
                print(f"No se encontro el empleado con el id: {id_empleado}")


            if Deficiones.confirmar_salir_pestana():
                return

    def mostrar_todos_empleados():

        while True:
            try:
                empleados = dao.obtener_empleados()
            except Exception as e:
                print(f"Error al obtener empleados: {e}")
                return
            if not empleados:
                print("No hay empleados registrados")
                return
            print("\n--- DETALLES DE TODOS LOS EMPLEADOS ---")
            for emp in empleados:
                print(f"\n--- EMPLEADO ID: {emp.get_id()} ---")
                print(f"Nombre: {emp.get_nombre()}")
                print(f"Dirección: {emp.get_direccion()}")
                print(f"Teléfono: {emp.get_telefono()}")
                print(f"Email: {emp.get_mail()}")
                print(f"Fecha de inicio: {emp.get_fecheIC()}")
                print(f"Salario: {emp.get_salario()}")
                print("-" * 30)

            if Deficiones.confirmar_salir_pestana():
                return
    

    def registrar_empleado():
        print("\n--- REGISTRAR NUEVO EMPLEADO ---")
        nombre = limpiar_input(input("Ingrese el nombre del empleado: "))
        if not nombre:
            print("Error: Nombre no válido")
            return
        
        direccion = limpiar_input(input("Ingrese la dirección del empleado: "))
        
        while True:
            try:
                telefono = int(limpiar_input(input("Ingrese el teléfono del empleado (máximo 9 dígitos): ")))
                if validar_telefono(telefono):
                    break
                else:
                    print("Número de teléfono no válido")
            except ValueError:
                print("Por favor ingrese solo números")

        while True:
            email = limpiar_input(input("Ingrese el email del empleado (@ecotech.cl): "))
            if not email:
                print("Por favor vuelve a ingresar el email correctamente.")
                continue
            if not validar_email(email):
                print("Error: Email debe usar @ecotech.cl. Por favor vuelve a ingresar el email correctamente.")
                continue
            break
        

        while True:
            fecha_inicio = limpiar_input(input("Ingrese la fecha de inicio del contrato (YYYY-MM-DD): "))
            if not fecha_inicio:
                print("Por favor vuelve a ingresar la fecha correctamente.")
                continue
            if not validar_fecha(fecha_inicio):
                print("Error: Formato de fecha no válido. Use YYYY-MM-DD. Por favor vuelve a ingresar la fecha correctamente.")
                continue
            break
        
        try:
            salario = int(limpiar_input(input("Ingrese el salario del empleado: ")))
            if salario <= 0:
                print("Error: Salario debe ser positivo")
                return
        except ValueError:
            print("Error: Salario debe ser un número")
            return
        

        empleado_nuevo = EcoTech(None, nombre, direccion, telefono, email, fecha_inicio, salario, None, Deficiones.admin_actual.get_id())
        try:
            id_empleado_generado = dao.registrar_empleado(empleado_nuevo)  
        except Exception as e:
            print(f"Error al registrar empleado en la base de datos: {e}")
            return
        

        from datetime import datetime
        username = nombre.lower().replace(" ", "")
        contraseña = f"{nombre.lower().replace(' ', '')}{datetime.now().day}"
        contraseña_cifrada = dao.cifrar_password(contraseña)
        
        usuario_auto = Usuario(None, username, contraseña_cifrada, "empleados,departamentos", id_empleado_generado)
        try:
            dao.registrar_usuario(usuario_auto)
        except Exception as e:
            print(f"Error al crear usuario automático: {e}")
        
        print(f"Empleado {nombre} registrado exitosamente")
        print(f"Usuario creado automáticamente:")
        print(f"Username: {username}")
        print(f"Contraseña: {contraseña}")

    def actualizar_empleado():
        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        if not empleados:
            print("No hay empleados registrados.")
            return
        
        print("\n--- EMPLEADOS REGISTRADOS ---")
        for emp in empleados:
            print(f"ID: {emp.get_id()} - Nombre: {emp.get_nombre()}")

        try:
            id_input = input("\nIngrese el ID del empleado a actualizar (0 para volver al menu): ")
            if id_input == "0":
                return
            id_empleado = int(id_input)
        except ValueError:
            print("Error: el ID debe ser un numero")
            return
        
        empleado_existente = None
        for emp in empleados:
            if emp.get_id() == id_empleado:
                empleado_existente = emp
                break
        
        if not empleado_existente:
            print(f"No se encontró empleado con ID {id_empleado}")
            return
        
        print(f"\nActualizando empleado: {empleado_existente.get_nombre()}")
        nombre = limpiar_input(input(f"Nuevo nombre [{empleado_existente.get_nombre()}]: ")) or empleado_existente.get_nombre()
        direccion = limpiar_input(input(f"Nueva dirección [{empleado_existente.get_direccion()}]: ")) or empleado_existente.get_direccion()
        
        telefono_input = limpiar_input(input(f"Nuevo teléfono [{empleado_existente.get_telefono()}]: "))
        if telefono_input:
            if not validar_telefono(int(telefono_input)):
                print("Error: Teléfono no válido")
                return
            telefono = int(telefono_input)
        else:
            telefono = empleado_existente.get_telefono()
        
        email = limpiar_input(input(f"Nuevo email [{empleado_existente.get_mail()}]: ")) or empleado_existente.get_mail()
        if not validar_email(email):
            print("Error: Email debe usar @ecotech.cl")
            return
        
        fecha_input = limpiar_input(input(f"Nueva fecha de inicio [{empleado_existente.get_fecheIC()}] (YYYY-MM-DD): "))
        if fecha_input:
            if not validar_fecha(fecha_input):
                print("Error: Formato de fecha no válido")
                return
            fecha_inicio = fecha_input
        else:
            fecha_inicio = empleado_existente.get_fecheIC()
        
        salario_input = limpiar_input(input(f"Nuevo salario [{empleado_existente.get_salario()}]: "))
        if salario_input:
            try:
                salario = int(salario_input)
                if salario <= 0:
                    print("Error: Salario debe ser positivo")
                    return
            except ValueError:
                print("Error: Salario debe ser un número")
                return
        else:
            salario = empleado_existente.get_salario()
        
        empleado_actualizado = EcoTech(id_empleado, nombre, direccion, telefono, email, fecha_inicio, salario)
        dao.actualizar_empleado(empleado_actualizado)

    def eliminar_empleado():
        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        if not empleados:
            print("No hay empleados registrados.")
            return
        print("\n--- Empleados Registrados ---")
        for emp in empleados:
            print(f"ID: {emp.get_id()} - Nombre: {emp.get_nombre()}")
        id_empleado = int(input("\nIngrese el ID del empleado a eliminar: "))
        empleado_existente = None
        for emp in empleados:
            if emp.get_id() == id_empleado:
                empleado_existente = emp
                break
        if not empleado_existente:
            print(f"No se encontro empleado con ID {id_empleado}")
            return
        print(f"\n--- EMPLEADO A ELIMINAR ---")
        print(f"ID: {empleado_existente.get_id()}")
        print(f"Nombre: {empleado_existente.get_nombre()}")
        print(f"Email: {empleado_existente.get_mail()}")

        confirmacion = input(f"\n¿Esta seguro de que desea eliminar este empelado?(s/n): ")
        if confirmacion.lower() == "s":
            try:
                eliminado = dao.eliminar_empleado(id_empleado)
            except Exception as e:
                eliminado = False

            if eliminado:
                print(f"Empleado {empleado_existente.get_nombre()} eliminado exitosamente")
            else:

                mensaje_error = None
                if hasattr(dao, 'last_error') and dao.last_error:
                    mensaje_error = dao.last_error

                if mensaje_error and ("1451" in mensaje_error or "foreign key" in mensaje_error.lower() or "Cannot delete or update a parent row" in mensaje_error):
                    print("No se pudo eliminar el empleado: existen registros relacionados (por ejemplo en 'Usuarios'). Elimine o reasigne esos registros primero.")
                elif mensaje_error:
                    print(f"No se pudo eliminar el empleado: {mensaje_error}")
                else:
                    print("No se pudo eliminar el empleado por un error desconocido.")
        else:
            print(f"Eliminacion Cancelada")

    def registrar_departamento():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden registrar departamentos")
            return
        
        print("\n--- REGISTRAR NUEVO DEPARTAMENTO ---")
        nombre = limpiar_input(input("Nombre del departamento: "))
        if not nombre:
            print("Error: Nombre no válido")
            return
        

        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        if not empleados:
            print("No hay empleados registrados. Debe registrar empleados primero.")
            return
            
        print("\n--- EMPLEADOS DISPONIBLES PARA GERENTE ---")
        for emp in empleados:
            print(f"ID: {emp.get_id()} - {emp.get_nombre()}")
        
        try:
            id_gerente = int(input("\nIngrese el ID del empleado que será gerente: "))
        except ValueError:
            print("Error: El ID debe ser un número.")
            return
        

        empleado_gerente = None
        for emp in empleados:
            if emp.get_id() == id_gerente:
                empleado_gerente = emp
                break
        
        if not empleado_gerente:
            print(f"No se encontró empleado con ID {id_gerente}")
            return
        

        if not validar_email(empleado_gerente.get_mail()):
            print("Error: El gerente debe tener email @ecotech.cl")
            return
        

        from Departamento import Departamento
        nuevo_departamento = Departamento(None, nombre, id_gerente, empleado_gerente.get_nombre())

        try:
            dao.registrar_departamento(nuevo_departamento)
        except Exception as e:
            print(f"Error al registrar departamento: {e}")

    def listar_departamentos():
        try:
            departamentos = dao.obtener_departamentos()
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
            return
        if not departamentos:
            print("No hay departamentos registrados.")
            return
        
        print("\n--- LISTA DE DEPARTAMENTOS ---")
        for depto in departamentos:
            print(f"ID: {depto.get_id()} - {depto.get_nombre()} (Gerente: {depto.get_nombre_gerente()} - ID: {depto.get_id_gerente()})")
        if Deficiones.confirmar_salir_pestana():
            return

    def asignar_empleado_departamento():
        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        if not empleados:
            print("No hay empleados registrados.")
            return

        print("\n--- EMPLEADOS ---")
        for emp in empleados:
            depto = f", Departamento: {emp.get_id_departamento()}" if emp.get_id_departamento() else ""
            print(f"ID: {emp.get_id()} - {emp.get_nombre()}{depto}")


        try:
            departamentos = dao.obtener_departamentos()
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
            return
        if not departamentos:
            print("No hay departamentos registrados.")
            return

        print("\n--- DEPARTAMENTOS ---")
        for depto in departamentos:
            print(f"ID: {depto.get_id()} - {depto.get_nombre()}")

        try:
            id_empleado = int(input("\nIngrese ID del empleado a asignar: "))
            id_departamento = int(input("Ingrese ID del departamento: "))
        except ValueError:
            print("Error: Los IDs deben ser números.")
            return


        empleado_encontrado = next((emp for emp in empleados if emp.get_id() == id_empleado), None)
        if not empleado_encontrado:
            print(f"No se encontró empleado con ID {id_empleado}. Revise el ID e intente de nuevo.")
            return


        departamento_encontrado = next((d for d in departamentos if d.get_id() == id_departamento), None)
        if not departamento_encontrado:
            print(f"No se encontró departamento con ID {id_departamento}. Revise el ID e intente de nuevo.")
            return


        try:
            dao.asignar_empleado_departamento(id_empleado, id_departamento)
            print(f"Empleado {empleado_encontrado.get_nombre()} asignado al departamento '{departamento_encontrado.get_nombre()}' (ID {id_departamento}) correctamente.")
        except Exception as e:

            mensaje_error = None
            if hasattr(dao, 'last_error') and dao.last_error:
                mensaje_error = dao.last_error
            else:
                mensaje_error = str(e)
            print(f"No se pudo asignar el empleado: {mensaje_error}")

    def mostrar_empleados_por_departamento():
        while True:
            try:
                departamentos = dao.obtener_departamentos()
            except Exception as e:
                print(f"Error al obtener departamentos: {e}")
                return
            if not departamentos:
                print("No hay departamentos registrados.")
                return

            print("\n--- DEPARTAMENTOS ---")
            for depto in departamentos:
                print(f"ID: {depto.get_id()} - {depto.get_nombre()}")

            try:
                id_departamento = int(input("\nIngrese ID del departamento para ver empleados (0 para salir): "))
            except ValueError:
                print("Error: El ID debe ser un número.")
                if Deficiones.confirmar_salir_pestana():
                    return
                else:
                    continue

            if id_departamento == 0:
                return

            try:
                empleados = dao.obtener_empleados()
            except Exception as e:
                print(f"Error al obtener empleados: {e}")
                return
            empleados_departamento = [emp for emp in empleados if emp.get_id_departamento() == id_departamento]

            if not empleados_departamento:
                print(f"No hay empleados en este departamento.")
            else:
                print(f"\n--- EMPLEADOS DEL DEPARTAMENTO {id_departamento} ---")
                for emp in empleados_departamento:
                    print(f"ID: {emp.get_id()} - {emp.get_nombre()} - {emp.get_mail()}")

            if Deficiones.confirmar_salir_pestana():
                return
    
    def eliminar_departamento():

        try:
            departamentos = dao.obtener_departamentos()
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
            return
        if not departamentos:
            print("No hay departamentos registrados.")
            return
    
        print("\n--- DEPARTAMENTOS REGISTRADOS ---")
        for depto in departamentos:
            print(f"ID: {depto.get_id()} - {depto.get_nombre()} (Gerente: {depto.get_nombre_gerente()})")
    

        try:
            id_input = input("\nIngrese el ID del departamento a eliminar (0 para volver al menú): ")
            if id_input == "0":
                print("Volviendo al menú principal...")
                return
            id_departamento = int(id_input)
        except ValueError:
            print("Error: El ID debe ser un número.")
            return


        departamento_existente = None
        for depto in departamentos:
            if depto.get_id() == id_departamento:
                departamento_existente = depto
                break
    
        if not departamento_existente:
            print(f"No se encontró departamento con ID {id_departamento}")
            return

        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        empleados_en_departamento = [emp for emp in empleados if emp.get_id_departamento() == id_departamento]
    
        if empleados_en_departamento:
            print(f"\nNO se puede eliminar el departamento '{departamento_existente.get_nombre()}'")
            print(f"Tiene {len(empleados_en_departamento)} empleado(s) asignado(s):")
            for emp in empleados_en_departamento:
                print(f"  - {emp.get_nombre()} (ID: {emp.get_id()})")
            print("\nReasigne los empleados a otro departamento primero.")
            return
    
        print(f"\n--- DEPARTAMENTO A ELIMINAR ---")
        print(f"ID: {departamento_existente.get_id()}")
        print(f"Nombre: {departamento_existente.get_nombre()}")
        print(f"Gerente: {departamento_existente.get_nombre_gerente()}")
    
        confirmacion = input("\n¿Está seguro de que desea eliminar este departamento? (s/n): ").strip().lower()
    
        if confirmacion == 's':

            dao.eliminar_departamento(id_departamento)
            print(f"Departamento '{departamento_existente.get_nombre()}' eliminado exitosamente.")
        else:
            print("Eliminación cancelada.")

    def mostrar_estadisticas():
        if not Deficiones.admin_actual and not Deficiones.usuario_actual:
            print("Debe iniciar sesión para ver estadísticas")
            return
        
        try:
            stats = dao.obtener_estadisticas_empleados()
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return
        if not stats:
            print("No hay datos para mostrar estadísticas")
            return
        
        print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
        print(f"Total empleados: {stats['total_empleados']}")
        print(f"Promedio salarial: ${stats['promedio_salario']:,.2f}")
        if Deficiones.confirmar_salir_pestana():
            return
        
    def registrar_administrador():
        print("\n--- REGISTRAR NUEVO ADMINISTRADOR ---")
        username = limpiar_input(input("Username: "))
        password = limpiar_input(input("Password: "))
        email = limpiar_input(input("Email (@ecotech.cl): "))
        
        if not validar_email(email):
            print("Error: Email debe usar @ecotech.cl")
            return
    
        try:
            nivel_acceso = int(input("Nivel de acceso (1-3): "))
        except ValueError:
            print("Error: El nivel de acceso debe ser un número.")
            return
        nuevo_admin = Administrador(None, username, password, email, nivel_acceso)
        try:
            dao.registrar_administrador(nuevo_admin)
        except Exception as e:
            print(f"Error al registrar administrador: {e}")

    def login_administrador():
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        try:
            admin = dao.login_administrador(username, password)
        except Exception as e:
            print(f"Error en login_administrador: {e}")
            return False
        if admin:
            Deficiones.admin_actual = admin
            print(f"¡Bienvenido {admin.get_username()}!")
            return True
        else:
            print("Credenciales incorrectas.")
            return False

    def logout_administrador():
        Deficiones.admin_actual = None
        print("Sesión cerrada exitosamente.")

    def mostrar_info_admin_actual():
        if Deficiones.admin_actual:
            print(f"\n--- ADMIN ACTUAL ---")
            print(f"Username: {Deficiones.admin_actual.get_username()}")
            print(f"Email: {Deficiones.admin_actual.get_email()}")
            print(f"Nivel Acceso: {Deficiones.admin_actual.get_nivel_acceso()}")
        else:
            print("No hay administrador logueado.")
        if Deficiones.confirmar_salir_pestana():
            return


    def login_usuario():
        print("\n--- LOGIN USUARIO ---")
        username = input("Username: ")
        password = getpass.getpass("Contraseña: ")
        try:
            usuario = dao.login_usuario(username, password)
        except Exception as e:
            print(f"Error en login_usuario: {e}")
            return False
        if usuario:
            Deficiones.usuario_actual = usuario
            print(f"¡Bienvenido {usuario.get_username()}!")
            return True
        else:
            print("Credenciales incorrectas.")
            return False


    def mostrar_info_usuario_actual():
        if Deficiones.usuario_actual:
            print(f"\n--- INFORMACIÓN DEL USUARIO ---")
            print(f"ID: {Deficiones.usuario_actual.id}")
            print(f"Username: {Deficiones.usuario_actual.username}")
        else:
            print("No hay usuario logueado.")
        if Deficiones.confirmar_salir_pestana():
            return
            
    def logout_usuario():
        Deficiones.usuario_actual = None
        print("Sesión cerrada exitosamente.")

    def registrar_horas_trabajadas():
        if not Deficiones.usuario_actual:
            print("Solo los usuarios empleados pueden registrar horas trabajadas")
            return
        
        print("\n--- REGISTRO DE HORAS TRABAJADAS ---")
        
        id_empleado = Deficiones.usuario_actual.get_id_empleado()
        
        fecha = limpiar_input(input("Fecha (YYYY-MM-DD): "))
        if not validar_fecha(fecha):
            print("Error: Formato de fecha no válido")
            return
        
        try:
            horas = float(limpiar_input(input("Horas trabajadas: ")))
            if horas <= 0 or horas > 24:
                print("Error: Horas deben estar entre 0 y 24")
                return
        except ValueError:
            print("Error: Las horas deben ser un número")
            return
        
        descripcion = limpiar_input(input("Descripción de tareas realizadas: "))
        
        nueva_hora = HoraTrabajada(None, fecha, horas, descripcion, id_empleado)
        try:
            dao.registrar_hora_trabajada(nueva_hora)
        except Exception as e:
            print(f"Error al registrar horas trabajadas: {e}")

    def ver_mis_horas_trabajadas():

        if not Deficiones.usuario_actual:
            print("Solo los usuarios empleados pueden ver sus horas")
            return
        id_empleado = Deficiones.usuario_actual.get_id_empleado()
        try:
            horas = dao.obtener_horas_empleado(id_empleado)
        except Exception as e:
            print(f"Error al obtener horas del empleado: {e}")
            return
        if not horas:
            print("No hay horas registradas")
            return
        print(f"\n--- MIS HORAS TRABAJADAS ---")
        total_horas = 0
        for hora in horas:
            print(f"Fecha: {hora.get_fecha()} | Horas: {hora.get_horas_trabajadas()} | Tareas: {hora.get_descripcion_tareas()}")
            total_horas += hora.get_horas_trabajadas()
        print(f"\nTotal de horas registradas: {total_horas}")
        if Deficiones.confirmar_salir_pestana():
            return

    def administrar_horas_trabajadas():

        if not Deficiones.admin_actual:
            print("Solo administradores pueden ver todas las horas")
            return
        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        if not empleados:
            print("No hay empleados registrados")
            return
        print("\n--- HORAS TRABAJADAS DE EMPLEADOS ---")
        for emp in empleados:
            horas_emp = dao.obtener_horas_empleado(emp.get_id())
            total_horas = sum(h.get_horas_trabajadas() for h in horas_emp)
            print(f"Empleado: {emp.get_nombre()} | Total horas: {total_horas}")
        if Deficiones.confirmar_salir_pestana():
            return

    def registrar_proyecto():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden registrar proyectos")
            return
        
        print("\n--- REGISTRAR NUEVO PROYECTO ---")
        nombre = limpiar_input(input("Nombre del proyecto: "))
        if not nombre:
            print("Error: Nombre no válido")
            return
        
        descripcion = limpiar_input(input("Descripción: "))
        

        while True:
            fecha_inicio = limpiar_input(input("Fecha de inicio (YYYY-MM-DD): "))
            if not fecha_inicio:
                print("Por favor vuelve a ingresar la fecha correctamente.")
                continue
            if not validar_fecha(fecha_inicio):
                print("Error: Formato de fecha no válido. Use YYYY-MM-DD. Por favor vuelve a ingresar la fecha correctamente.")
                continue
            break
        
        try:
            departamentos = dao.obtener_departamentos()
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
            departamentos = []
        id_departamento = None
        if departamentos:
            print("\n--- DEPARTAMENTOS DISPONIBLES ---")
            for depto in departamentos:
                print(f"ID: {depto.get_id()} - {depto.get_nombre()}")


            while True:
                id_input = input("ID del departamento (0 para ninguno): ").strip()
                if id_input == "0" or id_input == "":
                    id_departamento = None
                    break
                try:
                    candidato = int(id_input)
                except ValueError:
                    print("ID inválido. Ingrese un número válido o 0 para ninguno.")
                    continue

                if any(d.get_id() == candidato for d in departamentos):
                    id_departamento = candidato
                    break
                else:
                    print(f"No se encontró departamento con ID {candidato}. Revise la lista e intente de nuevo.")
        
        nuevo_proyecto = Proyecto(None, nombre, descripcion, fecha_inicio, id_departamento)
        try:
            dao.registrar_proyecto(nuevo_proyecto)
        except Exception as e:
            print(f"Error al registrar proyecto: {e}")

    def listar_proyectos():
        try:
            proyectos = dao.obtener_proyectos()
        except Exception as e:
            print(f"Error al obtener proyectos: {e}")
            return
        if not proyectos:
            print("No hay proyectos registrados")
            return
        print("\n--- LISTA DE PROYECTOS ---")
        for proy in proyectos:
            depto = f" | Departamento: {proy.get_id_departamento()}" if proy.get_id_departamento() else ""
            print(f"ID: {proy.get_id()} - {proy.get_nombre_proyecto()}{depto}")
            print(f"   Descripción: {proy.get_descripcion()}")
            print(f"   Fecha inicio: {proy.get_fecha_inicio()}")
        if Deficiones.confirmar_salir_pestana():
            return

    def actualizar_proyecto():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden actualizar proyectos")
            return
        
        try:
            proyectos = dao.obtener_proyectos()
        except Exception as e:
            print(f"Error al obtener proyectos: {e}")
            return
        if not proyectos:
            print("No hay proyectos registrados")
            return
        
        print("\n--- PROYECTOS DISPONIBLES ---")
        for proy in proyectos:
            print(f"ID: {proy.get_id()} - {proy.get_nombre_proyecto()}")
        
        try:
            id_proyecto = int(input("\nID del proyecto a actualizar: "))
        except ValueError:
            print("ID inválido")
            return
        
        proyecto_existente = None
        for proy in proyectos:
            if proy.get_id() == id_proyecto:
                proyecto_existente = proy
                break
        
        if not proyecto_existente:
            print("Proyecto no encontrado")
            return
        
        print(f"\nActualizando: {proyecto_existente.get_nombre_proyecto()}")
        nombre = limpiar_input(input(f"Nuevo nombre [{proyecto_existente.get_nombre_proyecto()}]: ")) or proyecto_existente.get_nombre_proyecto()
        descripcion = limpiar_input(input(f"Nueva descripción [{proyecto_existente.get_descripcion()}]: ")) or proyecto_existente.get_descripcion()
        
        fecha = limpiar_input(input(f"Nueva fecha inicio [{proyecto_existente.get_fecha_inicio()}]: ")) or proyecto_existente.get_fecha_inicio()
        if not validar_fecha(fecha):
            print("Error: Formato de fecha no válido")
            return
        
        proyecto_actualizado = Proyecto(id_proyecto, nombre, descripcion, fecha, proyecto_existente.get_id_departamento())
        dao.actualizar_proyecto(proyecto_actualizado)

    def eliminar_proyecto():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden eliminar proyectos")
            return
        try:
            proyectos = dao.obtener_proyectos()
        except Exception as e:
            print(f"Error al obtener proyectos: {e}")
            return
        if not proyectos:
            print("No hay proyectos registrados")
            return
        print("\n--- PROYECTOS DISPONIBLES ---")
        for proy in proyectos:
            print(f"ID: {proy.get_id()} - {proy.get_nombre_proyecto()}")
        try:
            id_proyecto = int(input("\nID del proyecto a eliminar: "))
        except ValueError:
            print("ID inválido")
            return

        confirmacion = input("¿Está seguro de eliminar este proyecto? (s/n): ")
        if confirmacion.lower() == 's':
            dao.eliminar_proyecto(id_proyecto)
        else:
            print("Eliminación cancelada")

    def generar_informe_empleados():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden generar informes")
            return
        
        print("\n--- INFORME DE EMPLEADOS ---")
        print("1. Generar PDF")
        print("2. Generar Excel")
        
        opcion = input("Seleccione formato: ")
        nombre_archivo = input("Nombre del archivo: ")
        
        try:
            empleados = dao.obtener_empleados()
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return
        if not empleados:
            print("No hay empleados para generar informe")
            return
        
        if opcion == "1":
            try:
                ruta = dao.generar_reporte_empleados_pdf(empleados, nombre_archivo)
                informe = Informe(None, f"Informe Empleados - {nombre_archivo}", "empleados", "pdf", None, Deficiones.admin_actual.get_id())
                dao.guardar_informe(informe)
            except Exception as e:
                print(f"Error al generar informe PDF: {e}")
                return
            print(f"PDF generado: {ruta}")
        elif opcion == "2":
            try:
                ruta = dao.generar_reporte_empleados_excel(empleados, nombre_archivo)
                informe = Informe(None, f"Informe Empleados - {nombre_archivo}", "empleados", "excel", None, Deficiones.admin_actual.get_id())
                dao.guardar_informe(informe)
            except Exception as e:
                print(f"Error al generar informe Excel: {e}")
                return
            print(f"Excel generado: {ruta}")
        else:
            print("Opción inválida")

    def generar_informe_proyectos():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden generar informes")
            return
        
        try:
            proyectos = dao.obtener_proyectos()
        except Exception as e:
            print(f"Error al obtener proyectos: {e}")
            return
        if not proyectos:
            print("No hay proyectos para generar informe")
            return
        
        nombre_archivo = input("Nombre del archivo PDF: ")
        try:
            ruta = dao.generar_reporte_proyectos_pdf(proyectos, nombre_archivo)
            informe = Informe(None, f"Informe Proyectos - {nombre_archivo}", "proyectos", "pdf", None, Deficiones.admin_actual.get_id())
            dao.guardar_informe(informe)
            print(f"PDF de proyectos generado: {ruta}")
        except Exception as e:
            print(f"Error al generar informe de proyectos: {e}")

    def generar_informe_departamentos():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden generar informes")
            return
        
        try:
            departamentos = dao.obtener_departamentos()
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
            return
        if not departamentos:
            print("No hay departamentos para generar informe")
            return
        
        nombre_archivo = input("Nombre del archivo PDF: ")
        try:
            ruta = dao.generar_reporte_departamentos_pdf(departamentos, nombre_archivo)
            informe = Informe(None, f"Informe Departamentos - {nombre_archivo}", "departamentos", "pdf", None, Deficiones.admin_actual.get_id())
            dao.guardar_informe(informe)
            print(f"PDF de departamentos generado: {ruta}")
        except Exception as e:
            print(f"Error al generar informe de departamentos: {e}")

    def ver_historial_informes():
        if not Deficiones.admin_actual:
            print("Solo administradores pueden ver historial")
            return 
        print("Historial de informes - estamos trabajando para eso")

