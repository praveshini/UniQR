import os
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, send_file
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import qrcode
from io import BytesIO
import base64
from datetime import datetime
import face_recognition
import shutil
import numpy as  np
import json


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Generate a secure random key
secret_key = secrets.token_hex(16)
print(f"Generated secret key: {secret_key}")

# Create the Flask application instance
app = Flask(__name__, static_url_path='')

# Set the secret key for session management and security
app.secret_key = secret_key

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="Attendance",
        user="postgres",
        password="Hacker#9"
    )
    return conn

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/adminLogin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        usernameA = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."Admin" WHERE "UserID" = %s AND "Password" = %s', (usernameA, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            return redirect(url_for('user'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('admin'))
    return render_template('adminlogin.html')

@app.route('/staff-login/', methods=['GET', 'POST'])
def staffLogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('staffLogin'))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."Faculty" WHERE "FacultyId" = %s AND "Password" = %s', (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return redirect(url_for('generateQR'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('staffLogin'))
    return render_template('staff-login.html')

@app.route('/add-user/', methods=['GET', 'POST'])
def user():
    return render_template('add-user.html')

@app.route('/add-admin/', methods=['GET', 'POST'])
def addAdmin():
    if request.method == 'POST':
        name = request.form['name']
        user_id = request.form['UserId']
        email = request.form['Email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO public."Admin" ("Name", "Password", "UserID", "Email") VALUES (%s, %s, %s, %s)', (name, password, user_id, email))
            conn.commit()
            flash('Admin added successfully!')
            return redirect(url_for('user'))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if 'unique_violation' in str(e):
                flash('UserID already exists')
            else:
                flash(f'Database error: {e}')
            return redirect(url_for('addAdmin'))

    return render_template('add-admin.html')



def isUnique(studEncode):
            conn=get_db_connection()
            cur=conn.cursor()
            query='SELECT "Features" FROM public."Student" WHERE  "Class"= %s;'
            cur.execute(query,("22PC",))
            dat=cur.fetchall()
            query='SELECT "Roll" FROM public."Student" WHERE  "Class"= %s;'
            cur.execute(query,("22PC",))
            roll=cur.fetchall()
            
            query='SELECT "CurrentCourse" FROM public."Student" WHERE  "Class"= %s;'
            cur.execute(query,("22PC",))
            cour=cur.fetchone()

            for feat in dat:
                print(type(feat[0]))
                print(feat[0])


# Convert list to NumPy array
                retrieved_array = np.array(list(feat[0]))

                result=face_recognition.compare_faces([studEncode], retrieved_array)[0]
                

                if result==True:
                    return False
            return True

@app.route('/duplicate/', methods=['GET', 'POST'])
def duplicate():
    return render_template('duplicate.html')

@app.route('/add-stud/', methods=['GET', 'POST'])
def addStudent():
    if request.method == 'POST':
        name = request.form['name']
        rollno = request.form['rollno']
        course = request.form['course']

        conn = get_db_connection()
        cur = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        image_filename = f"uploads/current.jpg"
        image = face_recognition.load_image_file(image_filename)
        face_locations = face_recognition.face_locations(image)
        shutil.rmtree('uploads')


        try:
            studEncode = face_recognition.face_encodings(image)[0]
            print(studEncode)
            features=studEncode
        except:
            if len(face_locations)>1:
                shutil.rmtree('uploads')

                return render_template('multiple.html')
            elif len(face_locations)==0:
                shutil.rmtree('uploads')

                return render_template('noFace.html')

        if isUnique(features):
        
        
            array_json = json.dumps(features.tolist())
            cur.execute('INSERT INTO public."Student" ("Roll", "Name", "Class","Features") VALUES (%s, %s, %s,%s)', (rollno, name, course,array_json))
            conn.commit()
            cur.execute('INSERT INTO public."Class" ("Roll") VALUES (%s)', (rollno, ))
            conn.commit()
            cur.close()
            conn.close()
        else:
            flash('Student already present!!')

            return redirect(url_for('duplicate'),)

            

       


        flash('Student added successfully!')
        return redirect(url_for('user'))
    
    return render_template('add-stud.html')

@app.route('/add-staff/', methods=['GET', 'POST'])
def addStaff():
    if request.method == 'POST':
        name = request.form['name']
        staff_id = request.form['staffid']
        course = request.form['course']
        password = request.form['password'] 
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO public."Faculty" ("Name", "Password", "FacultyId", "CourseID") VALUES (%s, %s, %s, %s)', (name, password, staff_id, course))
            conn.commit()
            
            cur.close()
            conn.close()

            flash('Staff added successfully!')
            return redirect(url_for('user'))
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Database error: {e}")
            flash(f'Database error: {e}')
            return redirect(url_for('addStaff'))

    return render_template('add-staff.html')

@app.route('/generate/', methods=['GET', 'POST'])
def generateQR():
    if request.method == 'POST':
       
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        time = data['time']
        
        curLoc = (latitude, longitude)
        cours=data["course"]
        currClass=data["currClass"]
        print(data)
        
        
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            query='UPDATE public."Faculty" SET "Latitude"= %s , "Longitude"=%s,"Time"=%s, "CurrentClass"=%s  WHERE "CourseID"=%s;'
            cur.execute(query,(str(latitude),str(longitude),str(time),str(currClass),str(cours)))
            
            
            query='SELECT "FacultyId" FROM public."Faculty" WHERE  "CourseID"= %s;'
            cur.execute(query,(str(cours),))
            facId=cur.fetchone()

            query='UPDATE public."Student" SET "CurrentCourse"= %s,"CurrentStaff"= %s  WHERE "Class"= %s;'
            cur.execute(query,(str(cours),str(facId[0]),str(currClass),))

        except Exception as e:
            print(e)

       

        conn.commit()
        cur.close()

        conn.close()
        return jsonify({'redirect': True, 'redirect_url': url_for('qr')})

    return render_template('generate.html')

@app.route('/capture/')
def capture():
    buffer = generate_qr_code()
    return send_file(buffer, mimetype='image/png')

@app.route('/absent/')
def absent():
    return "Absent Page"

def generate_qr_code():
    qr_data = "http://127.0.0.1:3000"
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@app.route('/qr1/')
def qr():
    return render_template('qr.html')

@app.route('/qr2/')
def qr_code():
    buffer = generate_qr_code()
    return send_file(buffer, mimetype='image/png')

# New routes for webcam capture
@app.route('/webcam-capture/')
def webcam_capture():
    return render_template('capture.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data['image']

    # Decode the base64 image data
    image_data = image_data.split(",")[1]
    image_data = base64.b64decode(image_data)

    # Save the image to the server
    UPLOAD_FOLDER = 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    image_filename = f"uploads/current.jpg"
    with open(image_filename, "wb") as image_file:
        image_file.write(image_data)
    

    # Redirect to a success page or send a success message
    return jsonify({
        'status': 'success',
        'message': 'Image uploaded successfully',
        'redirect_url': url_for('success_page')
    })

@app.route('/success')
def success_page():
    return "Image uploaded and processed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
