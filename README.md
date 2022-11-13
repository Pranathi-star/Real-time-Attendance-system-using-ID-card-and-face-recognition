# Real-time-Attendance-system-using-ID-card-and-face-recognition-for-CBIT
Mini Project for semester 5.

#### Steps to run it on your local system using the Windows Command Prompt:

1. (optional but recommended) Create a virtual environment and activate it using 

```
$ python -m venv <name_of_virtual_env>

$ <name_of_virtual_environment>\Scripts\activate.bat
```
2. Clone the repository using:

```
$ git clone https://github.com/Pranathi-star/Real-time-Attendance-system-using-ID-card-and-face-recognition.git
```

3. Move into the cloned directory using 

```
$ cd Real-time-Attendance-system-using-ID-card-and-face-recognition
```

4. Move into the flask project directory using 

```
$ cd flask_cbit_smart_attendance
```

5. Install the required dependencies using

```
$ pip install -r requirements.txt --use-deprecated=legacy-resolver
```

6. Set the Flask app as run.py using

```
$ set FLASK_APP = run.py
```

7. (for development purposes) Set the project on debug mode using

```
$ set FLASK_ENV=development
```
8. Set up the database and create an Admin for the portal using the steps mentioned in the image below.

![image](https://drive.google.com/file/d/1x5OatE8K8rGUbeAkwu2er-Oq8cEUBTUL/view?usp=sharing)

9. Run the project!
```
$ flask run
```
