from flask import Flask, request, render_template, redirect, url_for, flash
import json
import os
from flask_sqlalchemy import SQLAlchemy
from form.Univ import CreateUniv
from form.Studentviewnews import CreateStudentviewnews, EditStudentviewnews
from form.Teacher import CreateTeacher, EditTeacher
import plotly
import plotly.graph_objs as go
from form.News import EditNews, CreateNews
from form.Resources import CreateResources, EditResources
from form.Student import CreateStudent, EditStudent

app = Flask(__name__)
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:56azilos@localhost/Alexey'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://ufcgmyjzehymyf:80c606868723e30e101e0b5f35d220764bb71e2823cebe9020910d5bbd82e910@ec2-54-221-212-126.compute-1.amazonaws.com:5432/d4oo68s9gidr6t'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)


class ormTeacher(db.Model):
    __tablename__ = 'teacher'
    tc_info = db.Column(db.String(40), primary_key=True)
    tc_recomendation = db.Column(db.String(40))
    resources = db.relationship("ormResources", back_populates="teacher")


class ormResources(db.Model):
    __tablename__ = 'resources'
    rs_info = db.Column(db.String(40), primary_key=True)
    tc_info = db.Column(db.String(40), db.ForeignKey('teacher.tc_info'))
    rs_activity = db.Column(db.Integer)
    teacher = db.relationship("ormTeacher", back_populates="resources")
    news = db.relationship("ormNews", back_populates="resources")


class ormNews(db.Model):
    __tablename__ = 'news'
    ns_news_info = db.Column(db.String, primary_key=True)
    rs_info = db.Column(db.String(40), db.ForeignKey('resources.rs_info'))
    ns_likes = db.Column(db.Integer)
    univ_name = db.Column(db.String(40), db.ForeignKey('univer.name'))
    resources = db.relationship("ormResources", back_populates="news")
    univer = db.relationship("ormUniver", back_populates="news")


class ormStudents_view_news(db.Model):
    __tablename__ = 'students_view_news'
    ns_news_info = db.Column(db.String(40))
    st_info = db.Column(db.String(40), primary_key=True)


class ormStudent(db.Model):
    __tablename__ = 'student'
    st_review = db.Column(db.String(40))
    st_info = db.Column(db.String(40), primary_key=True)
    st_document = db.Column(db.String(40))


class ormUniver(db.Model):
    __tablename__ = 'univer'
    city = db.Column(db.String(40))
    name = db.Column(db.String(40), primary_key=True)
    rector = db.Column(db.String(40))
    birthday = db.Column(db.Integer())
    news = db.relationship("ormNews", back_populates="univer")


'''db.session.query(ormStudent).delete()
    db.session.query(ormTeacher).delete()
    db.session.query(ormStudents_view_news).delete()
    db.session.query(ormNews).delete()
    db.session.query(ormResources).delete()
    
    Teacher1 = ormTeacher(tc_info='tc_info1', tc_recomendation='tc_recommedation1')
    Teacher2 = ormTeacher(tc_info='tc_info2', tc_recomendation='tc_recommedation2')
    Teacher3 = ormTeacher(tc_info='tc_info3', tc_recomendation='tc_recommedation3')
    Resources1 = ormResources(rs_info='rs_info1', tc_info='tc_info1', rs_activity='1')
    Resources2 = ormResources(rs_info='rs_info2', tc_info='tc_info2', rs_activity='0')
    Resources3 = ormResources(rs_info='rs_info3', tc_info='tc_info3', rs_activity='1')
    News1 = ormNews(ns_news_info='news_info1', rs_info='rs_info1', ns_likes='15')
    News2 = ormNews(ns_news_info='news_info2', rs_info='rs_info2', ns_likes='89')
    News3 = ormNews(ns_news_info='news_info3', rs_info='rs_info3', ns_likes='93')
    Stviewnews1 = ormStudents_view_news(ns_news_info='news_info1', st_info='st_info1')
    Stviewnews2 = ormStudents_view_news(ns_news_info='news_info2', st_info='st_info2')
    Stviewnews3 = ormStudents_view_news(ns_news_info='news_info3', st_info='st_info3')
    Student1 = ormStudent(st_review='st_review1', st_info='st_info1', st_document='student document 1')
    Student2 = ormStudent(st_review='st_review2', st_info='st_info2', st_document='student document 2')
    Student3 = ormStudent(st_review='st_review3', st_info='st_info3', st_document='student document 3')

    db.session.add_all([Teacher1, Teacher2, Teacher3])
    db.session.add_all([Resources1, Resources2, Resources3])
    db.session.add_all([News1, News2, News3])
    db.session.add_all([Stviewnews1, Stviewnews2, Stviewnews3])
    db.session.add_all([Student1, Student2, Student3])
'''

@app.route('/')
def main_page():
    return render_template('index.html', action="/")


@app.route('/g', methods=['GET'])
def query():
    db.session.query(ormUniver).delete()
    Univ1 = ormUniver(city='Kyiv', name='name1', rector='rector1', birthday='1985')
    Univ2 = ormUniver(city='Lviv', name='name2', rector='rector2', birthday='1956')
    Univ3 = ormUniver(city='Kyiv', name='name3', rector='rector3', birthday='1925')
    db.session.add_all([Univ1, Univ2, Univ3])
    db.session.commit()
    return redirect('/show')



@app.route('/show')
def all_univ():
    name = "Univ"

    univ_db = db.session.query(ormUniver).all()
    univ = []
    for row in univ_db:
        univ.append({"city": row.city, "name": row.name, "rector": row.rector, "birthday": row.birthday})
        print(univ)
    return render_template('allUniv.html', name=name, univ=univ, action="/show")


@app.route('/insert', methods=['GET', 'POST'])
def create_Univ():
    form = CreateUniv()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateUniv.html', form=form, form_name="New Univ", action="/createUniv")
        else:

            ids = db.session.query(ormUniver).all()
            check = True
            for row in ids:
                if row.name.data == form.name.data:
                    check = False

            new_var = ormUniver(
                city=form.city.data,
                name=form.name.data,
                rector=form.rector.data,
                birthday=form.birthday.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Univ'))

    return render_template('CreateUniv.html', form=form, form_name="New Univ", action="/createUniv")


@app.route('/plot')
def dashboard():
    query3 = (
        db.session.query(
            ormUniver.city,
            ormUniver.name
        )
    ).all()

    city, name = zip(*query3)
    bar = go.Bar(
        x=city,
        y=name
    )

    data = {
        "bar": [bar],
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('Dashboard.html', graphsJSON=graphsJSON)


@app.route('/News')
def all_news():
    name = "News"

    news_db = db.session.query(ormNews).all()
    news = []
    for row in news_db:
        news.append({"ns_news_info": row.ns_news_info, "rs_info": row.rs_info, "ns_like": row.ns_likes})
        print(news)
    return render_template('allNews.html', name=name, news=news, action="/News")


@app.route('/Studentsviewnews')
def all_Studentviewnews():
    name = "Studenstviewnews"

    Studentsviewnews_db = db.session.query(ormStudents_view_news).all()
    Studentsviewnews = []
    for row in Studentsviewnews_db:
        Studentsviewnews.append(
            {"ns_news_info": row.ns_news_info, "st_info": row.st_info})
    return render_template('allStudentsviewnews.html', name=name, Studentsviewnews=Studentsviewnews,
                           action="/Studentsviewnews")


@app.route('/Teacher')
def all_Teacher():
    name = "Teacher"

    Teacher_db = db.session.query(ormTeacher).all()
    Teacher = []
    for row in Teacher_db:
        Teacher.append({"tc_info": row.tc_info, "tc_recomendation": row.tc_recomendation})
    return render_template('allTeacher.html', name=name, Teacher=Teacher, action="/Teacher")


@app.route('/Student')
def all_Student():
    name = "Student"

    Student_db = db.session.query(ormStudent).all()
    Student = []
    for row in Student_db:
        Student.append({"st_info": row.st_info, "st_review": row.st_review, "st_document": row.st_document})
    return render_template('allStudent.html', name=name, Student=Student, action="/Student")


@app.route('/Resources')
def all_Resources():
    name = "Resources"

    Resources_db = db.session.query(ormResources).all()
    Resources = []
    for row in Resources_db:
        Resources.append({"rs_info": row.rs_info, "tc_info": row.tc_info, "rs_activity": row.rs_activity})
    return render_template('allResources.html', name=name, Resources=Resources, action="/Resources")


@app.route('/createResources', methods=['GET', 'POST'])
def create_Resources():
    form = CreateResources()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateResources.html', form=form, form_name="New Resources",
                                   action="createResources")
        else:

            ids = db.session.query(ormResources).all()
            check = True
            for row in ids:
                if row.rs_info == form.rs_info.data:
                    check = False

            new_var = ormResources(
                rs_info=form.rs_info.data,
                tc_info=form.tc_info.data,
                rs_activity=int(form.rs_activity.data),
            )
            teacher_insertion = ormTeacher(
                tc_info=form.tc_info.data,
            )
            if check:
                db.session.add(teacher_insertion)
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Resources'))

    return render_template('CreateResources.html', form=form, form_name="New variable", action="createResources")


@app.route('/createStudent', methods=['GET', 'POST'])
def create_Student():
    form = CreateStudent()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateStudent.html', form=form, form_name="New Student", action="createStudent")
        else:

            ids = db.session.query(ormStudent).all()
            check = True
            for row in ids:
                if row.st_info == form.st_info.data:
                    check = False

            new_var = ormStudent(
                st_info=form.st_info.data,
                st_review=form.st_review.data,
                st_document=form.st_document.data,
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Student'))
            if not check:
                flash('You are trying to insert duplicate primary key')
                return redirect(url_for('all_Student'))

    return render_template('CreateStudent.html', form=form, form_name="New student", action="createStudent")


@app.route('/createTeacher', methods=['GET', 'POST'])
def create_Teacher():
    form = CreateTeacher()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateTeacher.html', form=form, form_name="New Teacher", action="createTeacher")
        else:

            ids = db.session.query(ormTeacher).all()
            check = True
            for row in ids:
                if row.tc_info == form.tc_info.data:
                    check = False

            new_var = ormTeacher(
                tc_info=form.tc_info.data,
                tc_recomendation=form.tc_recomendation.data,
            )

            db.session.add(new_var)
            db.session.commit()
            return redirect(url_for('all_Teacher'))

    return render_template('CreateTeacher.html', form=form, form_name="New Teacher", action="createTeacher")


@app.route('/createNews', methods=['GET', 'POST'])
def create_News():
    form = CreateNews()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateNews.html', form=form, form_name="New News", action="createNews")
        else:

            ids = db.session.query(ormNews).all()
            check = True
            for row in ids:
                if row.ns_news_info == form.ns_news_info.data:
                    check = False

            new_var = ormNews(
                ns_news_info=form.ns_news_info.data,
                rs_info=form.rs_info.data,
                ns_likes=form.ns_likes.data
            )
            resource_var = ormResources(
                rs_info=form.rs_info.data,
                rs_activity=1
            )
            if check:
                db.session.add(resource_var)
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_news'))

    return render_template('CreateNews.html', form=form, form_name="New News", action="createNews")


@app.route('/createStudentsviewnews', methods=['GET', 'POST'])
def create_Studentviewnews():
    form = CreateStudentviewnews()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateStudentviewnews.html', form=form, form_name="New Student view news",
                                   action="createStudentsviewnews")
        else:

            ids = db.session.query(ormStudents_view_news).all()
            check = True
            for row in ids:
                if row.ns_news_info == form.ns_news_info.data:
                    check = False

            new_var = ormStudents_view_news(
                ns_news_info=form.ns_news_info.data,
                st_info=form.st_info.data
            )
            news_var = ormNews(
                ns_news_info=form.ns_news_info.data,
                ns_likes=0
            )
            student_var = ormStudent(
                st_info=form.st_info.data
            )
            if check:
                db.session.add(student_var)
                db.session.add(news_var)
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Studentsviewnews'))

    return render_template('CreateStudentviewnews.html', form=form, form_name="New Student views news",
                           action="createStudentsviewnews")


@app.route('/delete/News', methods=['GET'])
def delete_News():
    ns_news_info = request.args.get('ns_news_info')

    result = db.session.query(ormNews).filter(ormNews.ns_news_info == ns_news_info).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_news'))


@app.route('/delete/Studentviewnews', methods=['GET'])
def delete_Studentviewnews():
    st_info = request.args.get('st_info')

    result = db.session.query(ormStudents_view_news).filter(ormStudents_view_news.st_info == st_info).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Studentsviewnews'))


@app.route('/delete/Resources', methods=['GET'])
def delete_Resources():
    rs_info = request.args.get('rs_info')

    result = db.session.query(ormResources).filter(ormResources.rs_info == rs_info).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Resources'))


@app.route('/delete/Student', methods=['GET'])
def delete_Student():
    st_info = request.args.get('st_info')

    result = db.session.query(ormStudent).filter(ormStudent.st_info == st_info).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Student'))


@app.route('/delete/Teacher', methods=['GET'])
def delete_Teacher():
    tc_info = request.args.get('tc_info')

    result = db.session.query(ormTeacher).filter(ormTeacher.tc_info == tc_info).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Teacher'))


@app.route('/editNews', methods=['GET', 'POST'])
def edit_News():
    form = EditNews()
    ns_news_info = request.args.get('ns_news_info')
    if request.method == 'GET':
        News = db.session.query(ormNews).filter(ormNews.ns_news_info == ns_news_info).one()
        form.ns_news_info.data = News.ns_news_info
        form.ns_likes.data = News.ns_likes
        form.rs_info.data = News.rs_info

        return render_template('EditNews.html', form=form, form_name="Edit news",
                               action="editNews?ns_news_info=" + News.ns_news_info)


    else:

        if not form.validate():
            return render_template('allNews.html', form=form, form_name="Edit News", action="editNews")
        else:

            # find user
            var = db.session.query(ormNews).filter(ormNews.ns_news_info == ns_news_info).one()
            print(var)

            # update fields from form data

            var.ns_news_info = form.ns_news_info.data
            var.ns_likes = form.ns_likes.data
            var.rs_info = form.rs_info.data

            db.session.commit()

            return redirect(url_for('all_news'))


@app.route('/editResources', methods=['GET', 'POST'])
def edit_Resources():
    form = EditResources()
    rs_info = request.args.get('rs_info')
    if request.method == 'GET':

        Resources = db.session.query(ormResources).filter(ormResources.rs_info == rs_info).one()

        form.rs_info.data = Resources.rs_info
        form.tc_info.data = Resources.tc_info
        form.rs_activity.data = Resources.rs_activity

        return render_template('EditResources.html', form=form, form_name="Edit Resourses",
                               action="editResources?rs_info=" + Resources.rs_info)
    else:

        if not form.validate():
            return render_template('EditResources.html', form=form, form_name="Edit Resourses", action="editResources")
        else:

            var = db.session.query(ormResources).filter(ormResources.rs_info == rs_info).one()
            print(var)

            # update fields from form data
            var.rs_info = form.rs_info.data
            var.tc_info = form.tc_info.data
            var.rs_activity = int(form.rs_activity.data)

            db.session.commit()

            return redirect(url_for('all_Resources'))


@app.route('/editStudent', methods=['GET', 'POST'])
def edit_Student():
    form = EditStudent()
    st_info = request.args.get('st_info')
    if request.method == 'GET':

        st = db.session.query(ormStudent).filter(ormStudent.st_info == st_info).one()

        # fill form and send to user

        form.st_info.data = st.st_info
        form.st_review.data = st.st_review
        form.st_document.data = st.st_document

        return render_template('EditStudent.html', form=form, form_name="Edit Student",
                               action="editStudent?st_info=" + st.st_info)


    else:

        if not form.validate():
            return render_template('EditStudent.html', form=form, form_name="Edit Student", action="editStudent")
        else:

            var = db.session.query(ormStudent).filter(ormStudent.st_info == st_info).one()
            print(var)

            # update fields from form data

            var.st_info = form.st_info.data
            var.st_review = form.st_review.data
            var.st_document = form.st_document.data
            db.session.commit()

            return redirect(url_for('all_Student'))


@app.route('/editTeacher', methods=['GET', 'POST'])
def edit_Teacher():
    form = EditTeacher()
    tc_info = request.args.get('tc_info')
    if request.method == 'GET':

        tc = db.session.query(ormTeacher).filter(ormTeacher.tc_info == tc_info).one()
        form.tc_info.data = tc.tc_info
        form.tc_recomendation.data = tc.tc_recomendation
        return render_template('EditTeacher.html', form=form, form_name="Edit Teacher",
                               action="editTeacher?tc_info=" + tc.tc_info)
    else:
        if not form.validate():
            return render_template('EditTeacher.html', form=form, form_name="Edit Teacher", action="editTeacher")
        else:
            var = db.session.query(ormTeacher).filter(ormTeacher.tc_info == tc_info).one()
            print(var)

            var.tc_info = form.tc_info.data
            var.tc_recomendation = form.tc_recomendation.data

            db.session.commit()

            return redirect(url_for('all_Teacher'))


@app.route('/editStudentviewnews', methods=['GET', 'POST'])
def edit_Studentviewnews():
    form = EditStudentviewnews()
    st_info = request.args.get('st_info')
    if request.method == 'GET':

        stn = db.session.query(ormStudents_view_news).filter(ormStudents_view_news.st_info == st_info).one()

        form.ns_news_info.data = stn.ns_news_info
        form.st_info.data = stn.st_info
        return render_template('EditStudentviewnews.html', form=form, form_name="Edit Student view news",
                               action="editStudentviewnews?st_info=" + stn.st_info)
    else:
        if not form.validate():
            return render_template('EditStudentviewnews.html', form=form, form_name="Edit Student view news",
                                   action="editStudentviewnews")
        else:
            var = db.session.query(ormStudents_view_news).filter(ormStudents_view_news.st_info == st_info).one()
            print(var)

            var.ns_news_info = form.ns_news_info.data
            var.st_info = form.st_info.data

            db.session.commit()

            return redirect(url_for('all_Studentsviewnews'))


if __name__ == '__main__':
    app.run()
