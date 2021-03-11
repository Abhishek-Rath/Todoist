from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100),  nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) ->str:
        return "{} - {}".format(self.id,self.task)



@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="POST":
        taskTitle=request.form['title']
        taskDesc=request.form['description']
        task=Todo(task=taskTitle, description=taskDesc)
        db.session.add(task)
        db.session.commit()
    allTasks=Todo.query.all()
    return render_template("index.html", allTasks=allTasks)


@app.route('/delete/<int:id>')
def delete(id):
    del_rec=Todo.query.filter_by(id=id).first()
    db.session.delete(del_rec)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    if request.method=='POST':
        taskTitle=request.form['title']
        taskDesc=request.form['description']
        up_task=Todo.query.filter_by(id=id).first()
        up_task.task=taskTitle
        up_task.description=taskDesc
        db.session.add(up_task)
        db.session.commit()
        return redirect('/')
    up_task=Todo.query.filter_by(id=id).first()
    return render_template('update.html', up_task=up_task)
if __name__=='__main__':
    app.run()