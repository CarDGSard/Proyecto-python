#proyecto: idea adaptar una base de datos-almacenar informacion e modificarla desde un menu

#registro de actividades
#importar modulos
import sqlite3

#inializar colorama y base de datos

db = "base de datos"
conection = sqlite3.connect(db)
cursor = conection.cursor()
#ID TAREA INCREMENTAL
#TAREA FINALIZADA O NO
#descripcion de la tarea
#tiempo-resolucion-tarea


cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                tiempo INTERGER NOT NULL, 
                finalizada BOOLEAN NOT NULL
               ''')
#cierre y comit de la conexion
conection.commit()
conection.close()

#funciones para agregar, modificar, eliminar y mostrar tareas
