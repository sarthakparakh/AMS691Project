# Student Profile Management and Ranking System AMS 691

This project is a Flask-based web application for managing and evaluating student profiles. It allows students to upload their documents and information, while universities can view, rank, and assess these profiles.

---

## Features
1. **Student Dashboard:**
   - Students can upload their Statement of Purpose (SOP), Letters of Recommendation (LORs), and Resume.
   - The uploaded files are saved securely in organized directories.
   - Automatic merging of uploaded PDFs into a single file for streamlined management.
   - Evaluation of SOP, LORs, and Resume with calculated scores.
   - Final scores are computed based on CGPA, GRE, and TOEFL scores.

2. **University Dashboard:**
   - View a list of all student submissions.
   - Automatic ranking of students based on scores.
   - Display detailed weighted scores (e.g., CGPA, GRE, TOEFL contributions).
   - View generated responses or analysis results for individual students.

3. **PDF Merging:**
   - All submitted files are merged into a single PDF for ease of access.

4. **SQLite Database Integration:**
   - Stores student submissions, filenames, scores, and other metrics securely.

5. **Session Management:**
   - Flask-Session handles user sessions for secure login and navigation.

---

## Project Structure

```
project-root/
|-- app.py                          # Main Flask application
|-- ams691.db                       # SQLite database file
|-- uploads/                        # Directory for uploaded student files
|-- data/
|   |-- student_profiles/           # Combined PDF files for each student
|   |-- response/                   # JSON responses for each student's analysis
|   |-- rank/                       # Ranking JSON file (rank.json)
|-- templates/                      # HTML templates for pages
|   |-- student_dashboard.html      # Student upload page
|   |-- university_dashboard.html   # University view page
|   |-- student_upload_success.html # Success page after student uploads
|-- static/                         # Static files like CSS/JS (if any)
|-- ranking/
|   |-- rank.py                     # Ranking logic and calculations
|-- rag/
|   |-- chat.py                     # Processes student profiles
|-- requirements.txt                # Python dependencies
```

---

## Prerequisites

Before running the project, ensure the following are installed:

- **Python 3.8+**
- **Flask**
- **Flask-Session**
- **PyPDF2**
- **SQLite3**

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

---

## Database Setup

To initialize the SQLite database, run the following command:

```bash
python app.py
```

The database will be created with the table `student_submissions` to store student records.

---

## How to Run the Application

1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd project-root
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Access the application in your browser at:
   ```
   http://127.0.0.1:5000/
   ```

---

## Endpoints

### 1. Student Dashboard
   - **URL:** `/student`
   - **Method:** `GET` | `POST`
   - **Description:** Allows students to upload their SOP, LORs, Resume, and input CGPA, GRE, and TOEFL scores.

### 2. University Dashboard
   - **URL:** `/university`
   - **Method:** `GET`
   - **Description:** Displays all student submissions, including calculated and weighted scores.

### 3. Ranked Student List
   - **URL:** `/university_student_rank`
   - **Method:** `GET`
   - **Description:** Generates and displays a ranked list of students based on their final scores.

---

## Key Functions and Logic

### 1. **`allowed_file(filename)`**
   - Checks if the uploaded file has a valid extension.

### 2. **PDF Merging**
   - The uploaded files are merged using PyPDF2 and saved under `data/student_profiles`.

### 3. **Score Calculation**
   - Scores for SOP, LORs, and Resume are generated using placeholder methods like `analyze_sop()` and `analyze_resume()`.
   - Final score = weighted sum of CGPA, GRE, and TOEFL.

### 4. **Database Integration**
   - Student data is stored in the SQLite database using the `student_submissions` table.

---

## Sample Data Flow
1. **Student Upload:**
   - Student uploads 1 SOP, 3 LORs, and 1 Resume.
   - Data is saved to a structured directory and database.
   - PDFs are merged into a single file for easy reference.

2. **University View:**
   - University accesses the dashboard to view student data and scores.
   - Ranking logic (`rank.py`) calculates final scores and ranks students.

---

## Future Improvements
- Add secure login and registration for students and university users.
- Integrate AI models for analyzing and scoring uploaded documents.
- Enhance the ranking logic with advanced metrics.
- Add visualizations for better insights into student performance.
- Deploy the application using cloud services like AWS or Heroku.

---

## Dependencies
The project uses the following libraries:
- Flask
- Flask-Session
- PyPDF2
- SQLite3

Install dependencies via:
```bash
pip install -r requirements.txt
```

---

## Author
Sarthak, Kushagra, Tanvi

---

## Acknowledgments
- Flask Documentation: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
- PyPDF2 Documentation: [https://pypi.org/project/PyPDF2/](https://pypi.org/project/PyPDF2/)
- SQLite3 Reference: [https://sqlite.org/](https://sqlite.org/)
