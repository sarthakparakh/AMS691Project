import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_session import Session
from flask import Flask, render_template, request, redirect, flash
import sqlite3
import hashlib
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger
# Initialize Flask app
app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
COMBINED_FOLDER = 'combined'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMBINED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMBINED_FOLDER'] = COMBINED_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}

# SQLite database setup
DB_NAME = 'students.db'

# Secret key for session management
app.secret_key = os.urandom(24)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sop_filename TEXT,
            lor1_filename TEXT,
            lor2_filename TEXT,
            lor3_filename TEXT,
            resume_filename TEXT,
            combined_filename TEXT,
            cgpa REAL,
            gre INTEGER,
            toefl INTEGER,
            sop_score REAL,
            lor_score REAL,
            resume_score REAL,
            final_score REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Flask-Session setup
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Sample student data for testing (you can replace this with a database later)
students_data = []

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the homepage (Login page)
'''@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_type = request.form['user_type']  # student or university
        username = request.form['username']
        password = request.form['password']
        
        # Simple hardcoded check (replace with actual DB later)
        if user_type == 'student' and username == 'student' and password == 'student':
            session['user_type'] = 'student'
            return redirect(url_for('student_dashboard'))
        elif user_type == 'university' and username == 'admin' and password == 'admin':
            session['user_type'] = 'university'
            return redirect(url_for('university_dashboard'))
        else:
            return 'Invalid credentials! Please try again.'

    return render_template('login.html')'''

# Route for student dashboard (upload page)
'''@app.route('/student', methods=['GET', 'POST'])
def student_dashboard():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Handle file uploads for SOP, LOR, Resume, and scores
        sop_file = request.files['sop']
        lor_file = request.files['lor']
        resume_file = request.files['resume']
        
        cgpa = float(request.form['cgpa'])
        gre = int(request.form['gre'])
        toefl = int(request.form['toefl'])
        
        if sop_file and lor_file and resume_file:
            if allowed_file(sop_file.filename) and allowed_file(lor_file.filename) and allowed_file(resume_file.filename):
                sop_filename = secure_filename(sop_file.filename)
                lor_filename = secure_filename(lor_file.filename)
                resume_filename = secure_filename(resume_file.filename)

                sop_file.save(os.path.join(app.config['UPLOAD_FOLDER'], sop_filename))
                lor_file.save(os.path.join(app.config['UPLOAD_FOLDER'], lor_filename))
                resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))

                # Store the student data (in a real app, you would store it in a DB)
                student = {
                    'name': 'Student Name',
                    'sop_filename': sop_filename,
                    'lor_filename': lor_filename,
                    'resume_filename': resume_filename,
                    'cgpa': cgpa,
                    'gre': gre,
                    'toefl': toefl,
                    'sop_score': analyze_sop(sop_filename),
                    'lor_score': analyze_lor(lor_filename),
                    'resume_score': analyze_resume(resume_filename),
                    'final_score': calculate_final_score(cgpa, gre, toefl)
                }
                students_data.append(student)

                return render_template('upload_success.html', student=student)

    return render_template('student_dashboard.html')
'''

@app.route('/student', methods=['GET', 'POST'])
def student_dashboard():
    print("Student123")

    username = session.get('username')  # Retrieve username from session
    print("Ussrnmae in student is", username)

    if 'user_type' not in session or session['user_type'] != 'student':
        print("something wrong")
        return redirect(url_for('index'))

    if request.method == 'POST':
        # File uploads
        print("Inside POST")
        sop_file = request.files['sop']
        lor1_file = request.files['lor1']
        lor2_file = request.files['lor2']
        lor3_file = request.files['lor3']
        resume_file = request.files['resume']

        # Student data
        cgpa = float(request.form['cgpa'])
        gre = int(request.form['gre'])
        toefl = int(request.form['toefl'])

        print("Valid 1")
        if all([sop_file, lor1_file, lor2_file, lor3_file, resume_file]):
            if all([allowed_file(f.filename) for f in [sop_file, lor1_file, lor2_file, lor3_file, resume_file]]):
                # Secure filenames
                print("Valid 2")
                sop_filename = secure_filename(sop_file.filename)
                lor1_filename = secure_filename(lor1_file.filename)
                lor2_filename = secure_filename(lor2_file.filename)
                lor3_filename = secure_filename(lor3_file.filename)
                resume_filename = secure_filename(resume_file.filename)

                # Save individual files
                #student_name = "Sarthak"
                student_name = username
                student_directory = os.path.join(app.config['UPLOAD_FOLDER'], student_name)
                os.makedirs(student_directory, exist_ok=True)

                '''sop_file.save(os.path.join(app.config['UPLOAD_FOLDER'], sop_filename))
                lor1_file.save(os.path.join(app.config['UPLOAD_FOLDER'], lor1_filename))
                lor2_file.save(os.path.join(app.config['UPLOAD_FOLDER'], lor2_filename))
                lor3_file.save(os.path.join(app.config['UPLOAD_FOLDER'], lor3_filename))
                resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))'''

                sop_file.save(os.path.join(student_directory, sop_filename))
                lor1_file.save(os.path.join(student_directory, lor1_filename))
                lor2_file.save(os.path.join(student_directory, lor2_filename))
                lor3_file.save(os.path.join(student_directory, lor3_filename))
                resume_file.save(os.path.join(student_directory, resume_filename))

                print("Valid 3")
                # Combine files into a single PDF
                combined_filename = f"combined_{student_name}.pdf"
                combined_path = os.path.join(app.config['COMBINED_FOLDER'], combined_filename)
                merger = PdfMerger()
                for filepath in [sop_filename, lor1_filename, lor2_filename, lor3_filename, resume_filename]:
                    #merger.append(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
                    merger.append(os.path.join(student_directory, filepath))
                merger.write(combined_path)
                merger.close()

                print("Valid 4")

                # Analyze files and calculate scores
                sop_score = analyze_sop(sop_filename)
                lor_score = round((analyze_lor(lor1_filename) + analyze_lor(lor2_filename) + analyze_lor(lor3_filename)) / 3, 2)
                resume_score = analyze_resume(resume_filename)
                final_score = calculate_final_score(cgpa, gre, toefl)

                # Insert data into the database
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO student_submissions (
                        name, sop_filename, lor1_filename, lor2_filename, lor3_filename,
                        resume_filename, combined_filename, cgpa, gre, toefl,
                        sop_score, lor_score, resume_score, final_score
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    username, sop_filename, lor1_filename, lor2_filename, lor3_filename,
                    resume_filename, combined_filename, cgpa, gre, toefl,
                    sop_score, lor_score, resume_score, final_score
                ))
                conn.commit()
                conn.close()

                # Pass the student data to the success page
                student = {
                    'name': username,
                    'cgpa': cgpa,
                    'gre': gre,
                    'toefl': toefl,
                    'sop_score': sop_score,
                    'lor_score': lor_score,
                    'resume_score': resume_score,
                    'final_score': final_score,
                    'combined_filename': combined_filename
                }
                return render_template('student_upload_success.html', student=student)

    return render_template('student_dashboard.html')
# Route for university dashboard (view all students)
@app.route('/university', methods=['GET'])
def university_dashboard():
    if 'user_type' not in session or session['user_type'] != 'university':
        return redirect(url_for('index'))
    
    #conn = sqlite3.connect(DB_NAME)
    
    #conn = get_db_connection()
    conn = sqlite3.connect(DB_NAME)
    students = conn.execute('SELECT * FROM student_submissions').fetchall()
    conn.close()

    print(students)
    student_data = []
    for student in students:
        student_info = {
            'name': student[1],
            'cgpa': student[8],
            'gre': student[9],
            'toefl': student[10],
            'calculated_json': {
                'cgpa_weighted': float(student[8]) * 0.3,  # Example calculation
                'gre_weighted': float(student[9]) * 0.4,    # Example calculation
                'toefl_weighted': float(student[10]) * 0.3,  # Example calculation
                'total_score': (float(student[8]) * 0.3) + (float(student[9]) * 0.4) + (float(student[10]) * 0.3)  # Example total score calculation
            }
        }
        student_data.append(student_info)

    # Sort students by final score (rank list)
    #sorted_students = sorted(students_data, key=lambda x: x['final_score'], reverse=True)

    #return render_template('university_dashboard.html', students=sorted_students)
    return render_template('university_dashboard.html', students = student_data)


@app.route('/university_student_rank', methods=['GET'])
def university_dashboard_rank():
    if 'user_type' not in session or session['user_type'] != 'university':
        return redirect(url_for('index'))
    
    #conn = sqlite3.connect(DB_NAME)
    
    #conn = get_db_connection()
    conn = sqlite3.connect(DB_NAME)
    students = conn.execute('SELECT * FROM student_submissions').fetchall()
    conn.close()

    print(students)
    student_data = []
    for student in students:
        student_info = {
            'name': student[1],
            'cgpa': student[8],
            'gre': student[9],
            'toefl': student[10],
            'calculated_json': {
                'cgpa_weighted': float(student[8]) * 0.3,  # Example calculation
                'gre_weighted': float(student[9]) * 0.4,    # Example calculation
                'toefl_weighted': float(student[10]) * 0.3,  # Example calculation
                'total_score': (float(student[8]) * 0.3) + (float(student[9]) * 0.4) + (float(student[10]) * 0.3)  # Example total score calculation
            }
        }
        student_data.append(student_info)

    # Sort students by final score (rank list)
    #sorted_students = sorted(students_data, key=lambda x: x['final_score'], reverse=True)

    #return render_template('university_dashboard.html', students=sorted_students)
    return render_template('university_student_rank.html', students = student_data)

# Function to analyze SOP (basic analysis based on text length)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Signup page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("Inside signuipppppss")
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']

        # Validate password and confirm password
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect('/signup')

        print("Inside signuiwwwwwwpppp")
        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save user credentials in the database
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email,password, user_type) VALUES (?, ?, ?, ?)', 
                         (username, email, hashed_password, user_type))
            conn.commit()
            flash("Signup successful! You can now log in.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists. Try another one.", "error")
            return redirect('/signup')
        finally:
            conn.close()
    return render_template('signup.html')

# Login page route (for reference)
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Log in..")
    if request.method == 'POST':
        print("Loggiii in..")
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        # Hash the password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check credentials in the database
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                             (username, hashed_password)).fetchone()
        conn.close()

        print("user =", user)
        if user_type == 'student':
            session['user_type'] = 'student'
            session['username'] = username
            return redirect(url_for('student_dashboard'))
            #flash("Login successful!", "success")
            #print("Student")
            #return redirect('/student')  # Replace with your dashboard route
        if user_type == 'university':
            print("Uni")
            session['user_type'] = 'university'
            flash("Login successful!", "success")
            session['username'] = username
            return redirect(url_for('university_dashboard'))
            #return redirect('/university') 
        else:
            print("Ptani")
            flash("Invalid username or password.", "error")
            #return redirect('/login')
    return render_template('login.html')


def analyze_sop(sop_filename):
    return len(sop_filename) // 100  # Simple placeholder logic

def analyze_lor(lor_filename):
    return len(lor_filename) // 150  # Simple placeholder logic

def analyze_resume(resume_filename):
    return len(resume_filename) // 200  # Simple placeholder logic

# Function to calculate final score based on CGPA, GRE, TOEFL, and document scores
def calculate_final_score(cgpa, gre, toefl):
    cgpa_score = (cgpa / 10) * 10  # Scale to 10
    gre_score = (gre / 340) * 10   # Scale to 10
    toefl_score = (toefl / 120) * 10  # 

if __name__ == "__main__":
    app.run(debug=True)