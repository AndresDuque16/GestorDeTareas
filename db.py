from tkinter import *
import sqlite3  #es un gestor de bases de datos incluido en python

root = Tk()
root.title('Gestor de Tareas')
root.geometry('400x500')#tamaño de la ventana inicial

conn = sqlite3.connect('gestorTareas.db') #se le asigna el nombre de la base de datos a conectar

c = conn.cursor()#se lñe asigna diferentes tareas como crear la tabla, crear leer y poder modificar o borrar

#con execute lo que se logra es generar la primera consulta a realizar la cual se coloca en doble"""
c.execute("""
  CREATE TABLE if not exists gestorTareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT NOT NULL,
    completed BOOLEAN NOT NULL
  );
""") 

conn.commit() #crea la consulta y la ejecuta en sqlite


#funcion para eliminar tareas
def remove(id):
  def _remove():
    c.execute("DELETE FROM gestorTareas WHERE id = ?",(id, ))
    conn.commit()
    render_tareas()
  return _remove 
  
#se realiza un Currying
def complete(id):
  def _complete(): #se crea una funcion dentro de otra función con el objetivo de que muestre la posicion correcta de id y no de
    #la ultima que itera

    tarea = c.execute("SELECT * from  gestorTareas WHERE id= ?",(id, )).fetchone() #para devolver solo el elemento que encuentre
    c.execute("UPDATE gestorTareas SET completed= ?  WHERE id = ?",(not tarea[3], id)) #actualiza el valor en el campo de tarea completado
    conn.commit() #para ejecutar el script
    render_tareas() #para renderizar
    
  return _complete


#definicion de función para realizar el listado de las tareas
def render_tareas():
  rows = c.execute("SELECT * FROM gestorTareas").fetchall() #selecciona toda la info de la base de datos
  
  #eliminar los elementos que se encuentran dentro del frame
  for widget in frame.winfo_children(): #optiene los elementos hijos 
    widget.destroy() #elimina los elementos optenidos


  for i in range(0, len(rows)):
    id = rows[i][0] #para sacar el primer elemento de la tabla
    completed = rows[i][3] #selecciona estado de la tare
    descripcion = rows[i][2] #seleciona descripcion de la tarea
    #para verificar si el campo esta completado o no y que cambie de color(negro sin seleccionar, rojo seleccionado)
    color = '#ff0000' if completed else '#000000'
    l = Checkbutton(frame, text=descripcion, fg= color, width=42, anchor='w', command= complete(id)) #crea un checkbutton con la info de descripcion
    l.grid(row=i, column=0, sticky='w')
    #boton para eliminar tareas
    btn = Button(frame, text='Eliminar', command= remove(id))
    btn.grid(row =i , column=1)

    l.select() if completed else l.deselect()

#definicion d efuncion para agregar datos a base de datos
def addTarea():
  tarea =  e.get()#optiene el valor de la entrada de dato de tarea label

  #se coloca un condicional para validar si existe una tarea en el entry
  if tarea:
    #en values se coloca ? para pasar los valores en una tupla
    c.execute("""
            INSERT INTO gestorTareas (descripcion, completed) VALUES (?, ?)
            """, (tarea, False))#tupla para prevenir inyeccion de sql
    conn.commit() #crea la consulta y la ejecuta en sqlite
    e.delete(0, END)#SE DEJA EN BLANCO EL CAMPO DE ENTRY
    render_tareas()#se coloca con el objetivo de renderizar la aplicacion
  else:
    pass #pase esto si noi existe nada para agregar

  
l = Label(root, text='Tarea')#etiqueta
l.grid(row=0, column=0)

e = Entry(root, width=40)#entrada para escribir la tarea
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command= addTarea)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)#sticky.. se encuentre pegado a todo lado, 
#padx espaciado a los bordes

e.focus()#para que aparesca el cursor en el campo de texto

root.bind('<Return>', lambda x: addTarea) #return=revento que se va a ascuchar y la funcion es addTarea que se 
#pasa por un lamda

render_tareas()# se coloca para que cuando se abra la aplicacion se visualice las tareas

root.mainloop()


