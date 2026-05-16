from flask import Flask, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
app = Flask(__name__)
app.secret_key = "aatish_secret_key"
 
# MySQL DB config
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='aatish2004',
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
    return render_template('StudentLogin.html')
#-------------Teacher Login page---------------------
@app.route('/teacherlogin')
def thrlogin():
    return render_template('facultyLogin.html')

#-------------Admin Login Page
@app.route('/adminlogin')
def admlogin():
    return render_template('AdminLogin.html')
#-------------password check---------
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

            elif role == "teacher":
                return redirect(url_for('thdash'))
                
            elif role == "admin":
                return redirect(url_for('adash'))
            else:
                return "Invalid Role"

        else:
            return "Wrong Password"

    else:
        return "User Not Found"

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
    return redirect(url_for('stdlogin'))

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
    return redirect(url_for('thrlogin'))
#-----------------student dashboqrd----------------
@app.route('/studentdashboard')
def stdash():
    enrollment = session.get('enrollment')
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registration WHERE enrollment=%s", (enrollment,)
                   )
    student =  cursor.fetchone()
    return render_template('student_dash.html', student = student)

#-----------------teacher dashboard--------------
@app.route('/teacherdashboard')
def thdash():
    return render_template('teacher_dash.html')

#-----------Admin Dashboard--------------
@app.route('/admindashboard')
def adash():
    return render_template('dashboard.html')
 
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
    select registration.enrollment, registration.name,
      result.semester from registration inner join 
        result on registration.enrollment = result.enrollment 
        where registration.enrollment = '%s';
    """
    print
    cursor.execute(sql, (enrollment,))

    ruser = cursor.fetchall()
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
                return "Invalid Role"

        else:
            return "Wrong Password"

    else:
        return "User Not Found"
    

#--------------marksheet----------
@app.route('/marksheet')
def marksheet():
    return render_template('marksheet.html')

@app.route('/resultlogin')
def result():
    return render_template('result_verification.html')
    
#--------run app-------------   
if __name__ == '__main__':
    app.run(debug=True, port=5050)
