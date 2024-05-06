from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    complete = title = db.Column(db.Boolean)

@app.route('/')
def index():

    list_of_activities = Todo.query.all()
    return render_template('base.html', list_of_activities=list_of_activities)

@app.route('/add', methods=['POST'])
def add_a_todo_task():

    title = request.form.get('title')
    new_todo_task = Todo(title=title, complete=False)
    db.session.add(new_todo_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update_a_todo_task(todo_id):

    todo_task = Todo.query.filter_by(id = todo_id).first()
    todo_task.complete = not todo_task.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def delete_a_todo_task(todo_id):

    todo_task = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>', methods=["GET", "POST"])
def edit_a_todo_task(todo_id):

    todo_task = Todo.query.get_or_404(todo_id)
    
    if request.method == 'POST':
        new_title = request.form.get('new_title')
        todo_task.title = new_title
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo_task=todo_task)

@app.route('/base')
def base():

    list_of_activities = Todo.query.all()
    return render_template('base.html', list_of_activities=list_of_activities)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)