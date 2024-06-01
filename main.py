from flask import Flask, render_template,url_for, request, redirect, Response 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user, login_required, current_user
from User_Login import UserLogin
from werkzeug.utils import secure_filename

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text,  nullable=False)
    psw = db.Column(db.Text, nullable=False)
class Notes(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String(100), nullable =False)
    text = db.Column (db.String(200), nullable =False) 
    status = db.Column (db.Text , nullable = False )
    
@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id,User)

   
@app.route('/reg/', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        login = request.form['login']
        users = User.query.all()
        users_true = {}
        for user in users:
            users_true[user.login] = user.psw
        if login not in users_true:
            psw = request.form['psw']
            user = User(login=login, psw=psw)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/')
            except:
                return "При добавлении пользователя произошла ошибка!"
        else:
            return 'Вы уже были зарегистрированы'
    return render_template("reg.html")
        
    

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = User.query.all()
        login = request.form['login']
        psw = request.form['psw']
        users_true = {}
        for user in users:
            
            if login == user.login:
                if psw == user.psw:
                    userlogin = UserLogin().create(user)
                    login_user(userlogin)
                    return redirect('/'+str(login))
    return render_template("login.html")
    


@app.route('/home')#url
@app.route('/')
def home():
    notes = Notes.query.all() 
    return render_template('home.html' , notes=notes)#подключение HTML

@app.route('/create' , methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']
        status = request.form['status'] 
        note = Notes (name=name ,  text=text , status=status)
        
        try:
            print(1)
            db.session.add(note)
            print(2)
            db.session.commit()
            print(3)
            return redirect('/home')
        except Exception as e:
            print(e)
            return 'ошибка'
    else:
        return render_template('Create_Notes.html')
    return render_template('Create_Notes.html') 

@app.route('/notes/<int:id>/')
def settings(id):
    notes = Notes.query.get(id)
    return render_template('settings.html', notes=notes)

@app.route('/notes/<int:id>/del/')
def delNotes(id):
        notes = Notes.query.get_or_404(id)
        try:
            db.session.delete(notes)
            db.session.commit()
            return redirect('/home')
        except Exception as e:
            print(e)
            return 'ошибка'
        


@app.route('/profile')
def profile():
    d
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)