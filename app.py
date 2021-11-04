
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shailesh_todo.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
	SerialNo = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	desc = db.Column(db.String(700), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __eper__(self):
		return f"{self.SerialNo}-{self.title}"
	#now to create db file >>>pyton3 , from app import db,  db.create_all() (In Terminal..)
    #https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/


@app.route('/',methods=['GET','POST'])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	if request.method=="POST":
		title_form=request.form['title'] #testing whether we are getting form data OR not.
		desc_form=request.form['desc']
		todo = Todo(title=title_form, desc=desc_form)
		db.session.add(todo)
		db.session.commit()

	alltodos = Todo.query.all()
	return  render_template('index.html',alltodos=alltodos)
	# return 'Hello World Shailesh'

@app.route('/delete_todo/<int:SerialNo>')
def delete_todo(SerialNo):
	todo_delete=Todo.query.filter_by(SerialNo=SerialNo).first()
	db.session.delete(todo_delete)
	db.session.commit()
	return redirect("/")

@app.route('/update_todo/<int:SerialNo>',methods=['GET','POST'])
def update_todo(SerialNo):
	if request.method == "POST":
		title_form = request.form['title']  # testing whether we are getting form data OR not.
		desc_form = request.form['desc']
		todo = Todo.query.filter_by(SerialNo=SerialNo).first()
		todo.title=title_form
		todo.desc=desc_form
		db.session.add(todo)
		db.session.commit()
		return redirect("/")

	todo_update=Todo.query.filter_by(SerialNo=SerialNo).first()
	print("Checking todo_update:",todo_update)
	return render_template('update.html', alltodos=todo_update)




# @app.route('/showall')
# def products():
# 	alltodos=Todo.query.all()
# 	print(alltodos)


# main driver function
if __name__ == '__main__':

	app.run(debug=True,port=8001)
