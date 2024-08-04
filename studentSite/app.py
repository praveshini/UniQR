from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import base64
from datetime import datetime
from flask import Flask, request,  render_template,redirect, url_for
from haversine import haversine, Unit
import cv2
import face_recognition
import shutil
import  numpy as np
import json




import psycopg2
from psycopg2.extras import RealDictCursor



app = Flask(__name__)
CORS(app)  # Initialize CORS with default settings




# Create an uploads directory if it does not exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/capture/')
def capture():
    print("capture")
    return render_template('captur.html')

def convertFeaturesFromString(code):
    temp=code.rstrip()
    temp=temp.split(',')
    print("convert")
    print(temp)
    res=[]
    for i in temp[1:len(temp)-1]:
        if '-' in i:

            res.append(-(float(i[1:])))
        else:
            res.append(float(i))
    return res

def convertFeaturestoString(code):
    temp=""
    for i in code:
        temp=temp+str(i)+','
    return temp


@app.route('/upload', methods=['POST','GET'])
def upload_image():
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'message': 'No image data found'}), 400
        
        image_data = data['image']
        # Extract base64 data and remove metadata
        if image_data.startswith('data:image/jpeg;base64,'):
            image_data = image_data.replace('data:image/jpeg;base64,', '')
        '''else:
            return jsonify({'message': 'Invalid image format'}), 400'''
        
        # Decode the base64 data
        try:
            image_bytes = base64.b64decode(image_data)
            filename = f"current.jpg"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save the image to file
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            image = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            if len(face_locations)>1:
                return render_template('multiple.html')
            elif len(face_locations)==0:
                return render_template('noFace.html')


            studEncode = face_recognition.face_encodings(image)[0]
            conn = get_db_connection()
            cur = conn.cursor()
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
                

                print("Feat",feat)
                if  result==True:#comparison
                    print(roll[dat.index(feat)][0])
                    courses=str(cour[0])
                    query='SELECT "Present" FROM public."Class" WHERE  "Roll"= %s;'
                    cur.execute(query,(str(roll[dat.index(feat)][0]),))
                    flag=cur.fetchone()
                    if flag[0]==0:

                    
                    
                        query=f'UPDATE public."Class" SET "{courses}" = "{courses}" + 1,"Present"= 1 WHERE  "Roll"= %s;'

                        cur.execute(query,(str(roll[dat.index(feat)][0]),))
                        
                        conn.commit()
                        return jsonify({'redirect': True, 'redirect_url': url_for("present")})
                    else:
                        return jsonify({'redirect': True, 'redirect_url': url_for("twice")})


                 #check in db

            #result=face_recognition.compare_faces([studEncode], facEncode)[0]
            return jsonify({'redirect': True, 'redirect_url': url_for("absent")})
            



        except Exception as e:
            print(f"Error: {e}")
            '''return jsonify({'message': 'Error saving image'}), 500'''
            return jsonify({'redirect': True, 'redirect_url': url_for("absent")})
        
        finally:
            shutil.rmtree('uploads')
            

    
@app.route('/twice/',methods=['GET'])
def twice():
    return render_template('twice.html')

@app.route('/absent/',methods=['GET'])
def absent():
    return render_template('absent.html')

@app.route('/present/',methods=['GET'])
def present():
    return render_template('present.html')

@app.route('/',methods=['GET','POST'])
def location():
    
    if request.method=='POST':

        print("hello")
        data = request.get_json()
        print(data)
        latitude = data['latitude']
        longitude = data['longitude']
        time=data['time']
        #print(f'Received location: Latitude={latitude}, Longitude={longitude}'+str(time))
        
        curLoc=(latitude,longitude)
        conn = get_db_connection()
        cur = conn.cursor()
        
        query='SELECT "Latitude","Longitude","Time" FROM public."Faculty" WHERE  "CurrentClass"= %s;'
        cur.execute(query,("22PC",))
        data=cur.fetchone()
        print(data)
        timeFac=float(data[2])

        locFaculty=(float(data[0]),float(data[1]))
        cur.close()
        conn.close()

        if(time>timeFac+60000000): #6mins
            return jsonify({'redirect': True, 'redirect_url': url_for('absent')})
        else:
            print("hell")
            if  haversine(locFaculty, curLoc, unit='mi')<=100:
                print("hi")
                return jsonify({'redirect': True, 'redirect_url': url_for('capture')})
            else:
                print("helllo")
                return jsonify({'redirect': True, 'redirect_url': url_for('capture')})

        '''cur.execute('SELECT "FacultyId" FROM "Student" WHERE "Class" = "22PC"')
        faculty=cur.fetchone()

        cur.execute('SELECT "Location" FROM "Faculty" WHERE "FacultyId" = %s', (faculty,))
        locFaculty = cur.fetchone()'''



        
            
    
    return render_template('intro.html')


        
    

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="Attendance",
        user="postgres",
        password="Hacker#9"
    )
    return conn

if __name__ == '__main__':
    app.run(port=3000)
