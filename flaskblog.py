from flask import Flask, render_template, url_for, flash, redirect, request, send_file, session, send_from_directory
from forms import RegistrationForm, LoginForm, AdminForm, Userprofile, Track, SearchForm
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import pypyodbc
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
bcrypt=Bcrypt(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

conn = pypyodbc.connect('Driver={SQL Server}; Server=LAPTOP-8DPA66RQ; Database=db1; trusted_connection=yes')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        if request.method == 'POST': result = request.form
        cursor = conn.cursor()
        insert = ("INSERT INTO UserInfo2"  
                  "(email, password, username) "  
                  "VALUES(?,?,?)")
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        values = list(result.values())
        values = [values[2], values[3], values[1]]
        cursor.execute(insert, values)
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        if request.method == 'POST':
            cu = conn.cursor()
            username_form = str(form.email.data)
            password_form = str(form.password.data)
            select = ("SELECT email,password "
                      "FROM UserInfo2 "
                      "WHERE email= ?")
            cu.execute(select, [username_form])
            results = cu.fetchone()
            print(results)
            if username_form and password_form in results:
                session['id'] = username_form
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('start'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/AdminLogin", methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():

        if request.method == 'POST':
            cu = conn.cursor()
            admin_form = str(form.AdminID.data)
            password_form = str(form.password.data)
            select = ("SELECT AdminID,password "
                      "FROM AdminInfo1 "
                      "WHERE AdminID= ?")
            cu.execute(select, [admin_form])
            results = cu.fetchone()
            print(results)
            if admin_form and password_form in results:
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('adminhome'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('AdminLogin.html', title='Login', form=form)


@app.route("/start")
def start():
    return render_template('start.html', posts=posts)


@app.route("/createprofile", methods=['GET', 'POST'])
def createprofile():
    form = Userprofile()

    if form.validate_on_submit():
        flash(f'Profile created for {form.CandidateName.data}!', 'success')
        resume = upload()
        print(resume)
        if request.method == 'POST':
            result = request.form
        cursor = conn.cursor()
        insert = ("INSERT INTO UserDash2"  
                  "(name, email, contact, notice_period, Skills, Source, Resume) "  
                  "VALUES(?,?,?,?,?,?,?)")
        values = list(result.values())
        values = [values[1], values[2], values[3], values[4], values[5], values[6], resume]
        cursor.execute(insert, values)
        conn.commit()

        return redirect(url_for('start'))
    return render_template('createpro.html', title='Profile', form=form)


'''@app.route('/uploads', methods=['GET', 'POST'])
def index():
    return render_template('upload1.html')'''


def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    print(request.files.getlist('file'))

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        print(file)

        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        return filename


@app.route('/resume/')
def resume():
    #email = request.args.get('email')
    cus = conn.cursor()
    select = ("SELECT Resume "
              "FROM UserDash2 "
              "WHERE email= ?")
    cus.execute(select, [session['id']])
    result = cus.fetchone()
    print(result)
    return send_file("images/"+result[0],
                     attachment_filename=result[0])


@app.route('/resume1/<result>')
def resume1(result):
    return send_file("images/"+result,
                     attachment_filename=result)

@app.route("/AdminHome", methods=['GET', 'POST'])
def adminhome():
    cursor4 = conn.cursor()
    cursor4.execute("SELECT name, email, contact, notice_period, Skills, Source, Resume FROM UserDash2")
    result = cursor4.fetchall()
    conn.commit()
    return render_template('AdminHome.html', title='Login', data=result)
    '''form = SearchForm()
    print(form.select.data)
    result = None
    if form.validate_on_submit():
        print(form.search.data)`
        curs = conn.cursor()
        choice = form.select.data
        search = form.search.data
        if choice == 'Skills':
            select = ("SELECT name,Skills "
                      "FROM UserProfile3 "
                      "WHERE Skills= ?")
            print(choice)
        elif choice == 'Job ID':
            select = ("SELECT jobTitle,vacancy "
                      "FROM Jobs "
                      "WHERE Job_ID= ?")
        else:
            select = ("SELECT username,noticePeriod "
                      "FROM UserProfile "
                      "WHERE noticePeriod= ?")
        curs.execute(select, [search])
        result = curs.fetchone()
        if not result:
            flash('No Result Found!', 'danger')
        else:
            flash('Filter Applied!', 'success')'''


@app.route("/search", methods=['GET', 'POST'])
def search():
    cursor5 = conn.cursor()
    cursor5.execute("SELECT Job_ID, name, round1, round2, round3, round4, hr, offer, joined FROM UserDash2")
    result = cursor5.fetchall()
    conn.commit()
    return render_template('search1.html', title='progress', data1=result)


@app.route("/log")
def log():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


'''@app.route("/loggedin", methods=['GET', 'POST'])
def loggedin():
    cursor4 = conn.cursor()
    cursor4.execute("SELECT username,email, Source FROM UserProfile3")
    result = cursor4.fetchall()
    conn.commit()
    return render_template('AdminHome.html', title='Login', data=result)'''


@app.route('/stage', methods=['GET', 'POST'])
def stage():
    form = Track()
    if form.validate_on_submit():
        candidate = form.selectC.data
        round = form.selectR.data
        status = form.selectS.data
        jobid = form.selectJ.data
        con = conn.cursor()
        select = ("SELECT email "
                  "FROM UserDash2 "
                  "WHERE name= ?")
        con.execute(select, [candidate])
        result = con.fetchone()
        print(result)
        select = ("SELECT email "
                  "FROM UserDash2 "
                  "WHERE email= ?")
        con.execute(select, [result[0]])
        result2 = con.fetchone()
        print(result2)
        if not result2:
            insert1 = ("INSERT into UserDash2 "
                       "(email) "
                       "VALUES(?)")
            print(str(result[0]))
            con.execute(insert1, [str(result[0])])
            conn.commit()
        insert2 = ("UPDATE UserDash2 "
                   "SET "+round+"= ? "
                   "WHERE email= ?")
        con.execute(insert2, [str(status), str(result[0])])
        insert3 = ("UPDATE UserDash2 "
                   "SET Job_ID = ? "
                   "WHERE email= ?")
        con.execute(insert3, [str(jobid), str(result[0])])
        conn.commit()
        upd = ("UPDATE UserDash2 "
               "SET CurrentRound= ? , Status= ? "
               "WHERE email= ?")
        val1 = [round, status, str(result[0])]
        con.execute(upd, val1)
        conn.commit()
        flash('Success', 'success')
    return render_template('stage.html', title='Track', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    form = SearchForm()

    cursor6 = conn.cursor()
    cursor6.execute(
        "SELECT Job_ID, name, contact, notice_period, Skills, Source, Resume, CurrentRound, Status FROM UserDash2")
    result = cursor6.fetchall()
    conn.commit()
    if request.method == 'POST':
        cursor6 = conn.cursor()
        cursor6.execute("""SELECT Job_ID, name, contact, notice_period, Skills, Source, Resume, CurrentRound, Status FROM UserDash2
                        where Job_ID like '%{}%' and Skills like '%{}%' and notice_period like '%{}%' 
                        and  {} like '%{}%' """.format(form.JobID.data, form.Skills.data, form.NoticePeriod.data,
                                                       form.selectR.data, form.selectS.data))
        result = cursor6.fetchall()
    select = ("SELECT Source,count(source) "
              "FROM UserDash2 "
              "GROUP BY Source "
              "ORDER by count(source) desc ")
    cursor6.execute(select)
    pie = cursor6.fetchall()
    row = []
    for i in pie:
        row.append(list(i))

    select1 = ("SELECT CurrentRound,count(CurrentRound) "
              "FROM UserDash2 "
              "GROUP BY CurrentRound "
              "ORDER by count(CurrentRound) desc ")
    cursor6.execute(select1)
    pie1 = cursor6.fetchall()
    row1 = []
    for i in pie1:
        row1.append(list(i))
    return render_template('dashboard.html', title='DashBoard', data3=result, form=form, data5=row, data6=row1)


if __name__ == '__main__':
    app.run(port=4555, debug=True)
