from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:qwerty@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods =['GET'])
def blog():
    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id = id).first()
        return render_template('singlepost.html', blog=blog)
    else:    
        blogs = Blog.query.order_by(desc(Blog.id)).all()
        print(blogs)
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods =['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title,body)
        
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




