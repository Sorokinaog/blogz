from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:blogzblogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
app.secret_key = "y217kGcys&zP3B"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref = 'owner')
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/')
def index():
    users = User.query.order_by(asc(User.username)).all()
    return render_template('index.html', users = users)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost',)
        if user and user.password != password:
            flash ("Incorrect Password!")  
            return redirect('/login') 
        if not user:
            flash ("The Username does not exist")
            return redirect('/login')
    return render_template('login.html') 


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        user = User.query.filter_by(username=username).first()
        new_user = User(username, password)
        if username =="" or password =="" or verify_password =="":
            flash("One or more fields are empty")
            return render_template('signup.html')
        if user:
            flash("That username already exists")
            return render_template('signup.html')
        if len(username)<3 or len(password)<3:
            flash("Username or password less than 3 characters long")
            return render_template('signup.html')
        if password != verify_password:
            flash("The passwords do not match")
            return render_template('signup.html')
        db.session.add(new_user)
        db.session.commit()
        #new_user_id =new_user.id
        session['username'] = username
        return redirect('/newpost')      
    return render_template('signup.html') 


@app.route('/logout')
def logout():
    del session['username']
    flash("You logged out")
    return redirect('/blog')


@app.route('/blog', methods =['GET'])
def blog():
    #owner = User.query.filter_by(username=session['username']).first()
    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id = id).first()
        return render_template('singlepost.html', blog=blog)
    else:    
        blogs = Blog.query.order_by(desc(Blog.id)).all()
        return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods =['POST','GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(title,body,owner)
        
        if title =='' and body =='':
            error = 'empty entries'
            return render_template('newpost.html', error=error, title=title, body=body)
        if title =='':
            error = 'empty title'
            return render_template('newpost.html', error=error, title=title, body=body)
        if body == '':
            error = 'empty body'
            return render_template('newpost.html', error=error, title=title, body=body)

        db.session.add(new_blog)
        db.session.commit()
        id = new_blog.id
        return redirect('/blog?id={0}'.format(id))
    error = request.args.get('error')
    return render_template('newpost.html', error = error) 




if __name__ == '__main__':
    app.run()




