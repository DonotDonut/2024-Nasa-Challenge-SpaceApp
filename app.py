"""
Flash.py is the backend of the clas 

to run the following code write 
1) set FLASK_APP=Flash.py
flask run
 
2) 'python Flash.py' in the terminal 
"""

from flask import Flask

app = Flask(__name__)

# Route for the home page 
@app.rounter('/')
def intro(): 
    #return render_template('intro.html') #for specific html class 
    return 'he'
"""
# Route for the spaceship 
@app.rounter('/')
def home(): 
    return render_template('home.html') #for specific html class 
"""


if __name__ == "__main__": 
    app.run(debug=True)
