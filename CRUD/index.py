from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)



mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/') 
def index():
    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ajecutar
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit() #Termina la conexión
    return render_template('empleados/index.html', empleados=empleados)

#Código para eliminar
@app.route('/destroy/<int:id>') 
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/')
 
 #Editar
@app.route('/edit/<int:id>') 
def editar(id):
    conn = mysql.connect()
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()   
    return render_template('empleados/editar.html', empleados=empleados)
  
@app.route('/update', methods=['POST']) 
def update():   
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _dir= request.form['txtDireccion']
    id = request.form['txtId']
    sql = "UPDATE empleados SET Nombre= %s, Correo=%s, Direccion=%s WHERE id=%s ;"
    datos = (_nombre, _correo, _dir,id)
    
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ajecutar
    cursor.execute(sql,datos)
    conn.commit() #Termina la conexión
    return redirect('/')
    
 #Guardar   
@app.route('/guardar') 
def guardar():
     return render_template('empleados/guardar.html')


@app.route('/store', methods=['POST']) 
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _dir= request.form['txtDireccion']
    sql = "INSERT INTO `empleados` (`id`, `Nombre`, `Correo`, `Direccion`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre, _correo, _dir)
    
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ajecutar
    cursor.execute(sql,datos)
    conn.commit() #Termina la conexión
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    