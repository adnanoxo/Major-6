from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong secret in production

# Upload folder setup
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0044',
    'database': '<D_database>'
}

# ------------------- Home -------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------- Register -------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# ------------------- Login -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

# ------------------- Dashboard -------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# ------------------- ERP Form -------------------
@app.route('/erp_form', methods=['GET', 'POST'])
def erp_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Save uploaded files
        photo = request.files['photo']
        cast_cer = request.files['cast_cer']
        res_cer = request.files['res_cer']
        incm_cer = request.files['incm_cer']

        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        cast_path = os.path.join(app.config['UPLOAD_FOLDER'], cast_cer.filename)
        res_path = os.path.join(app.config['UPLOAD_FOLDER'], res_cer.filename)
        incm_path = os.path.join(app.config['UPLOAD_FOLDER'], incm_cer.filename)

        photo.save(photo_path)
        cast_cer.save(cast_path)
        res_cer.save(res_path)
        incm_cer.save(incm_path)

        # Get form data
        data = (
            photo_path,
            request.form.get('Fname'),
            request.form.get('Mname'),
            request.form.get('Lname'),
            request.form.get('Ftname'),
            request.form.get('Occupation'),
            request.form.get('Mtname'),
            request.form.get('Occ'),
            request.form.get('DOB'),
            request.form.get('Gender'),
            request.form.get('qualification'),
            request.form.get('Cat'),
            request.form.get('inc'),
            request.form.get('Rlg'),
            request.form.get('PhNo'),
            request.form.get('emailUser') + '@gmail.com',
            request.form.get('P.code'),
            request.form.get('Add'),
            request.form.get('P.add'),
            cast_path,
            res_path,
            incm_path
        )

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO erp_data (
                photo, fname, mname, lname, father_name, father_occupation,
                mother_name, mother_occupation, dob, gender, qualification,
                category, income, religion, phone, email, pincode,
                address, permanent_address, caste_certificate,
                residence_certificate, income_certificate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("success.html")

    return render_template('erp_form.html')

# ------------------- Logout -------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------- Run App -------------------
if __name__ == '__main__':
    app.run(debug=True)
