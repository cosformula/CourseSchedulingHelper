from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import os
import json
from datetime import datetime
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Courses(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    courseno = db.Column(db.String(30))
    coursename = db.Column(db.String(30))
    credit = db.Column(db.String(30))
    teachno = db.Column(db.String(30))
    teachname = db.Column(db.String(30))
    coursetime = db.Column(db.String(30))
    courseplace = db.Column(db.String(30))
    capacity = db.Column(db.Integer)
    enroll = db.Column(db.Integer)
    campus = db.Column(db.String(30))
    status = db.Column(db.String(30))
    qtime = db.Column(db.String(30))
    qplace = db.Column(db.String(30))
    school = db.Column(db.String(30))
    tag = db.Column(db.String(30))

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    courseno = db.Column(db.String(30))
    coursename = db.Column(db.String(30))
    coursetime = db.Column(db.String(30))
    teachname = db.Column(db.String(30))
    credit = db.Column(db.String(30))
    campus = db.Column(db.String(30))
    page = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())

@app.route('/')
def index():
    return 'it works!'
@app.route('/getcourse')
def query():
    courseno = request.args.get('courseno')
    coursename = request.args.get('coursename')
    teachname = request.args.get('teachname')
    coursetime = request.args.get('coursetime')
    credit = request.args.get('credit')
    campus = request.args.get('campus')
    page = int(request.args.get('page'))
    record = Record(courseno=courseno,
                    coursename=coursename,
                    coursetime = coursetime,
                    teachname = teachname,
                    credit = credit,
                    campus = campus,
                    page = page,
                    time=datetime.now())
    db.session.add(record)
    db.session.commit()
    print('record',courseno,coursename,teachname,coursetime,credit,campus,page)
    coursesquery = Courses.query.filter(Courses.courseno.like('%%%s%%'%courseno))\
    .filter(Courses.coursename.like('%%%s%%'%coursename))\
    .filter(Courses.teachname.like('%%%s%%'%teachname))\
    .filter(Courses.coursetime.like('%%%s%%'%coursetime))
    if credit != '':
        coursesquery = coursesquery.filter(Courses.credit.like('%s'%credit))
    if campus != '':
        coursesquery = coursesquery.filter(Courses.campus.like('%s'%campus))
    courses = coursesquery.paginate(page,per_page=50,error_out=False)
    coursedata = {}
    coursedatalist = []
    for course in courses.items:
        coursedatalist.append({'courseno':course.courseno,
        'coursename':course.coursename,
        'teachname':course.teachname,
        'teachno':course.teachno,
        'coursetime':course.coursetime,
        'campus':course.campus,
        'capacity':course.capacity,
        'school':course.school,
        'enroll':course.enroll,
        'tag':course.tag,
        'credit':course.credit})
    coursedata['total'] = courses.total
    coursedata['list'] = coursedatalist
    json_str = json.dumps(coursedata)
    return json_str
    
if __name__ == '__main__':
    app.run('127.0.0.1', '8080')
