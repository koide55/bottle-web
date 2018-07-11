import sqlite3
import datetime
from bottle import *
from peewee import *

PORT=8086
DBFILE = "./data.db"

db = SqliteDatabase(DBFILE)

# Modles class #####################################################################
class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    userid = PrimaryKeyField()
    username = CharField(null=True)
    password = CharField(null=True)
    cookie = CharField(null=True)
    session = CharField(null=True)

class Comments(BaseModel):
    commentid = PrimaryKeyField()
    user = ForeignKeyField(Users, related_name='comments')
    comment = CharField(null=False)
    datetime = CharField(null=False)

try:
    db.connect()
    db.create_tables([Users, Comments])
except:
    pass

# Controller #######################################################################
@get('/')
@get('/signup')
def index():
    return '''
        <form action="/register" method="post">
            Username: <input name="username" type="text"/>
            Password: <input name="password" type="password"/><br>
            <input value="Signup" type="submit"/>
        </form>
         <a href="/login"><button>Go to Login Page</botton></a>
    '''

@post('/register')
def register():
    username = request.forms.decode().get('username')
    password = request.forms.decode().get('password')
    try:
        user = Users.get(Users.username==username)
        return('''
            <b>Error.</b><br>
            <a href="/login"><button>Login</botton></a>
            <a href="/signup"><button>Signup</button></a>
        ''')
    except:
        pass
    user = Users.create(username=username, password=password)
    user.save()
    return('''
        <b>Registered</b><br>
        <a href="/login"><button>Go to Login</botton></a>
        <a href="/signup"><button>Go to SignUp</button></a>
    ''')

@get('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>', name=name)

@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text"/>
            Password: <input name="password" type="password"/><br>
            <input value="Login" type="submit"/>
        </form>
        <a href="/signup"><button>Go to Signup Page</botton></a>
    '''

@post('/login')
def login():
    username=request.forms.decode().get('username')
    password=request.forms.decode().get('password')

    # query SQLite directly !! for SQL injection
#    import sqlite3
#    conn = sqlite3.connect(DBFILE)
#    c = conn.cursor()
#    sql = "SELECT * FROM users WHERE username='"+username+"' and password='"+password+"';"
#    try :
#        records = c.execute(sql)
#    except Users.DoesNotExit:
#        return('''
#            <b>Error.</b>'
#            <a href="/login"><button>Login</botton></a>
#            <a href="/signup"><button>Signup</button></a>
#            <a href="/logout"><button>Logout</button></a>
#        ''')
#    else:
#        record=records.fetchone()
#        cookie = 'user'+str(record[0])
#        response.set_cookie('cookie_id', cookie, secret='key')
#        update = "UPDATE users SET cookie='"+cookie+"' WHERE userid="+str(record[0])
#        c.execute(update)
#        conn.commit()
#        conn.close()
#        return '''
#            <b>Login Sucess. Hello, '''+username+'''..</b><br>
#            <a href="/mypage"><button>MyPage</botton></a>
#            <a href="/login"><button>Login</botton></a>
#            <a href="/signup"><button>Signup</botton></a>
#            <a href="/logout"><button>Logout</botton></a>
#        '''
#    return
    try:
        user = Users.get(Users.username==username, Users.password==password)
        cookie_id = 'user'+str(user.userid)
        response.set_cookie('cookie_id', cookie_id, secret='key')
        user.cookie = cookie_id
        user.save()
        return '''
            <b>Login Sucess. Hello, '''+username+'''..</b><br>
            <a href="/mypage"><button>MyPage</botton></a>
            <a href="/login"><button>Login</botton></a>
            <a href="/signup"><button>Signup</botton></a>
            <a href="/logout"><button>Logout</botton></a>
        '''
    except Users.DoesNotExist:
        return('''
            <b>Error.</b>'
            <a href="/login"><button>Login</botton></a>
            <a href="/signup"><button>Signup</button></a>
            <a href="/logout"><button>Logout</button></a>
        ''')

@get('/logout')
def logout():
    response.delete_cookie('cookie_id')
    response.delete_cookie('username')
    redirect('/login')

@get('/mypage')
def mypage():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    if cookie_id != None:
        try:
            user = Users.get(Users.cookie==cookie_id)
        except Users.DoesNotExist:
            return('''
                <b>Error.</b><br>
                <a href="/login"><button>Login</botton></a>
                <a href="/signup"><button>Signup</button></a>
            ''')
    return '''
        <b>Hello, '''+user.username+'''..</b>
        <a href="/bbs"><button>Go to BBS</button></a>
        <a href="/login"><button>Go to Login</botton></a>
        <a href="/signup"><button>Go to Signup</botton></a>
    '''

@get('/bbs')
def bbs():
    cookie_id=request.get_cookie('cookie_id', secret='key')
    if cookie_id!=None:
        try:
            user = Users.get(Users.cookie==cookie_id)
            username = user.username
            comments = Comments.select()
        except Users.DoesNotExist:
            return('''
                <b>Error.</b>'
                <a href="/login"><button>Login</botton></a>
                <a href="/signup"><button>Signup</button></a> 
                <a href="/logout"><button>Logout</button></a>
            ''')
    else:
        return('''
                <b>Error.</b>'
                <a href="/login"><button>Login</botton></a>
                <a href="/signup"><button>Signup</button></a>
                <a href="/logout"><button>Logout</button></a>
            ''')
    return template('bbs', username=username, comments=comments)

@post('/bbs')
def bbs():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    if cookie_id != None:
        try:
            user = Users.get(Users.cookie==cookie_id)
        except Users.DoesNotExist:
            return('''
                <b>Error.</b>'
                <a href="/login"><button>Login</botton></a>
                <a href="/signup"><button>Signup</button></a> 
                <a href="/logout"><button>Logout</button></a>
            ''')
    else:
        return('''
                <b>Error.</b>'
                <a href="/login"><button>Go to Login</botton></a>
                <a href="/signup"><button>Go to Signup</button></a>      
            ''')
    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    comment = request.forms.decode().get('comment')
    Comments.create(user=user, comment=comment, datetime=now)

@get('/contact')
def contact():
    return '''
        <form action="/contact" method="post">
        貴方のメールアドレス: <input name="address" type="text"/><br>
        <textarea name="comment" rows="5" cols="70" placeholder="連絡事項を書いてください">
        </textarea>
        <button type="submit">書き込む</button>
        </form>
    '''
@post('/contact')
def contact():
    address = request.forms.decode().get('address')
    comment = request.forms.decode().get('comment')
    import os
    os.system('/bin/echo "'+comment+'" | /usr/sbin/sendmail -f '+address+' pi@localhost')
    return ('''
        <b>正常に送信されました</b>
        <a href="/mypage"><button>Go to MyPage</button></a>
    ''')

# Main routines #####################################################################
run(host='0.0.0.0', port=PORT)
