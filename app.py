from flask import Flask, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
app = Flask(__name__)
app.secret_key = "aatish_secret_key"
 
# MySQL DB config
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='0044',
    database='major6',
    port = '3305'
)
#---------------College Dashboard-----------------
@app.route('/')
def home():
    return render_template('index.html')

#--------------student login page---------------------
@app.route('/studentlogin')
def stdlogin():
    # Pass show_error=False here so the modal stays hidden when opening the page normally
    return render_template('StudentLogin.html', show_error=False)

#-------------Teacher Login page---------------------
@app.route('/teacherlogin')
def thrlogin():
    return render_template('facultyLogin.html')

#-------------Admin Login Page
@app.route('/adminlogin')
def admlogin():
    return render_template('AdminLogin.html')

#------------- student password check---------
@app.route('/login', methods=['POST'])
def login():

    enrollment = request.form.get('enrollment')
    password = request.form.get('password')

    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM registration
    WHERE enrollment = %s
    """

    cursor.execute(sql, (enrollment,))

    user = cursor.fetchone()

    if user:

        # Match hashed password
        if check_password_hash(
                user['password'],
                password
        ):
            role = user['role']
            # Get role from database
            session['enrollment'] = user['enrollment']
            session['role'] = user['role']
            session['name'] = user['name']
            # Redirect according to role
            if role == "student":
                  return redirect(url_for('stdash'))

                
            else:
                return  render_template('StudentLogin.html', show_error=True)

        else:
            return render_template('StudentLogin.html', show_error=True)

    else:
        return render_template('StudentLogin.html', show_error=True)
    
#-----Teacher Password check------------
@app.route('/tlogin', methods=['POST'])
def tlogin():

    enrollment = request.form.get('enrollment')
    password = request.form.get('password')

    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM registration
    WHERE enrollment = %s
    """

    cursor.execute(sql, (enrollment,))

    user = cursor.fetchone()

    if user:

        # Match hashed password
        if check_password_hash(
                user['password'],
                password
        ):
            role = user['role']
            # Get role from database
            session['enrollment'] = user['enrollment']
            session['role'] = user['role']
            session['name'] = user['name']
            # Redirect according to role
            if role == "teacher":
                  return redirect(url_for('thdash'))
                
            else:
                return  render_template('facultyLogin.html', show_error=True)

        else:
            return render_template('facultyLogin.html', show_error=True)

    else:
        return render_template('facultyLogin.html', show_error=True)
    
#------------admin password check------------
@app.route('/alogin', methods=['POST'])
def alogin():

    enrollment = request.form.get('enrollment')
    password = request.form.get('password')

    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM registration
    WHERE enrollment = %s
    """

    cursor.execute(sql, (enrollment,))

    user = cursor.fetchone()

    if user:

        # Match hashed password
        if check_password_hash(
                user['password'],
                password
        ):
            role = user['role']
            # Get role from database
            session['enrollment'] = user['enrollment']
            session['role'] = user['role']
            session['name'] = user['name']
            # Redirect according to role
            if role == "admin":
                   
               return redirect(url_for('adash'))
            else:
                return  render_template('AdminLogin.html', show_error=True)

        else:
            return  render_template('AdminLogin.html', show_error=True)

    else:
        return render_template('AdminLogin.html', show_error=True)

#-----------student registration page---------------
@app.route('/sreg')
def sdr():
    return render_template('student_registration.html')

#-------------Student Registration----------------
@app.route('/sregister', methods=['POST'])
def sregisters():
    enrollment = request.form.get('enrollment')
    name = request.form.get('name')
    email = request.form.get('email')
    password =generate_password_hash(
        request.form.get('password')
    )
    course = request.form.get('course')
    role = "student"
  
    cursor =db.cursor()
    sql_query="INSERT INTO registration (enrollment, name, email, password,role, course) VALUES (%s, %s,%s, %s,%s,%s)"
    cursor.execute(sql_query,(enrollment,name,email,password,role,course))
    db.commit()
    cursor.close()
     

    # ⬇️ CHANGE THE OLD REDIRECT / RETURN LINE TO THIS ⬇️
    return render_template('student_registration.html', registration_success=True)

#-----------------Teacher Registration-----------------------
@app.route('/treg')
def thr():
    return render_template('T_register.html')

@app.route('/tregister', methods=['POST'])
def tregisters():
    enrollment = request.form.get('enrollment')
    name = request.form.get('name')
    email = request.form.get('email')
    password =generate_password_hash(
        request.form.get('password')
    )
    course = request.form.get('course')
    role = "teacher"
  
    cursor =db.cursor()
    sql_query="INSERT INTO registration (enrollment, name, email, password,role, course) VALUES (%s, %s,%s, %s,%s,%s)"
    cursor.execute(sql_query,(enrollment,name,email,password,role,course))
    db.commit()
    cursor.close() 

    # ⬇️ CHANGE THE OLD REDIRECT / RETURN LINE TO THIS ⬇️
    return render_template('T_register.html', registration_success=True)

#-----------------student dashboard----------------
@app.route('/studentdashboard')
def stdash():
    enrollment = session.get('enrollment')
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registration WHERE enrollment=%s", (enrollment,))
    student =  cursor.fetchone()
    return render_template('student_dash.html', student = student)

#-----------------teacher dashboard--------------
@app.route('/teacherdashboard')
def thdash():
    enrollment = session.get('enrollment')
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registration WHERE enrollment=%s", (enrollment,))
    teacher = cursor.fetchone()
    return render_template('teacher_dash.html', teacher=teacher)

#-----------Admin Dashboard--------------
@app.route('/admindashboard')
def adash():
    enrollment = session.get('enrollment')

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM registration WHERE enrollment=%s",
        (enrollment,)
    )

    admin = cursor.fetchone()

    return render_template('dashboard.html', admin=admin)
 
#-------------------Logout------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

#---------------result upload-------------
@app.route('/uploadmarks', methods=['POST'])
def uploadmarks():

    enrollment = request.form.get('enrollment')
    batch = request.form.get('batch')
    semester = request.form.get('semester')

    subject = request.form.getlist('subject[]')
    marks = request.form.getlist('marks[]')

    cursor = db.cursor()

    for sub, marks in zip(subject, marks):

        sql = """
        INSERT INTO result (enrollment, batch, semester, subject, marks)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (enrollment, batch, semester, sub, marks))

    db.commit()

    return redirect(url_for('thdash'))

#---------------view results-------------------
@app.route('/rlogin', methods=['POST'])
def rlogin():

    enrollment = request.form.get('enrollment')
    password = request.form.get('password')

    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM registration
    WHERE enrollment = %s
    """
    cursor.execute(sql, (enrollment,))

    ruser = cursor.fetchone()
    print(ruser)
    if ruser:

        # Match hashed password
        if check_password_hash(
                ruser['password'],
                password
        ):
            role = ruser['role']
            # Get role from database
            session['enrollment'] = ruser['enrollment']
            session['role'] = ruser['role']
            session['name'] = ruser['name']
            # Redirect according to role
            if role == "student":
                  return redirect(url_for('marksheet'))

            else:
                return redirect(url_for('result'))

        else:
            return redirect(url_for('wronglogin'))

    else:
        return redirect(url_for('wronglogin'))

#--------------marksheet----------
@app.route('/marksheet')
def marksheet():
    enrollment = session.get('enrollment')
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT r.enrollment, r.name, m.batch,
           m.subject, m.marks, m.semester
    FROM registration r
    INNER JOIN result m
    ON r.enrollment = m.enrollment
    WHERE r.enrollment = %s
    """
    
    cursor.execute(query, (enrollment,))
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM registration WHERE enrollment=%s", (enrollment,))
    student =  cursor.fetchone()
    
    return render_template('marksheet.html',student=student, data = data)
     
@app.route('/resultlogin')
def result():
    return render_template('result_verification.html')

# CHANGED: Re-renders 'StudentLogin.html' but injects show_error=True to trigger your popup modal
#@app.route('/wronglogin')
#def wronglogin():
 #   return render_template('StudentLogin.html', show_error=True)

#--------run app-------------   
if __name__ == '__main__':
    app.run(debug=True, port=5050)