#pip install flask
#pip install flask_sqlalchemy

from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pytz

#create flask app instance 
app = Flask(__name__)

#create sqlite database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)


#est time zone setting
est = pytz.timezone('America/New_York')

now = datetime.now(est)
current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")

print("Current time:", current_time)

#define model of a to do list task
class Task(db.Model):
    #db.column is a cokumn in. the database
    #PICK ONE to be the "primary_Key"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    
    current = datetime.now(est)

    date_created = db.Column(db.String(30), default = current.strftime("%Y-%m-%d %H:%M:%S.%f"))
    
    #String representaton of the object
    def __repr__(self):
        return f'<Task {self.id}>'
    
#flask route for disllaying all tasks
@app.route('/', methods=['GET', 'POST'])
def index():
    #ADD new task to database (if user does)
    if request.method == 'POST':
        task_content = request.form['content']
        current = datetime.now(est)
        new_task = Task(content=task_content, date_created=current.strftime("%Y-%m-%d %H:%M:%S.%f"))
        try:
            
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding task to'
    #SELECT all task objects from database
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

#route for deleting tasks
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


    
#create the database intance in main method 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port="5421")
