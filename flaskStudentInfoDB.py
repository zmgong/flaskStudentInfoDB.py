from flask import Flask, render_template, url_for, flash, redirect
from forms import StudentInfoForm, StudentInfoSelectForm, StuEmergencyContactForm, GuardianForm, TAInfoForm, \
    TASelectForm, TAEmergencyContactForm, ManagerForm, TutorialMainForm, TutorialInfoForm, AddStudentAttendForm, \
    PriceForm, StudentUnpaidFee, TAUpdateForm, StudentInfoUpdateForm
import sqlite3
from datetime import datetime

conn = sqlite3.connect('blog.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys=ON")
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


# Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/")
@app.route("/home")
def home():
    conn = sqlite3.connect('blog.db')

    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")

    # Aggregation query
    query1 = "SELECT COUNT(*) AS NumOfStuWithUnpaidFee FROM Student WHERE UnpaidFee > 0"
    c.execute(query1)
    NumOfStuWithUnpaidFee = c.fetchall()

    # Aggregation query (functions such as min, max, average or count)
    c.execute("SELECT COUNT(*) AS NumberOFStudent FROM Student")
    """
    Print more statistic information of database at home page.
    """
    posts = c.fetchall()

    # Aggregation with group-by (aggregated value for each group)
    query = "SELECT grade, COUNT(*) AS NumberOFStudent FROM Student GROUP BY grade ORDER BY grade"
    c.execute(query)
    numberOfStudentInEachGrade = c.fetchall()
    print(numberOfStudentInEachGrade)
    return render_template('home.html', posts=posts, numberOfStudentInEachGrade=numberOfStudentInEachGrade,
                           NumOfStuWithUnpaidFee=NumOfStuWithUnpaidFee)


@app.route("/newStudent", methods=['GET', 'POST'])
def newStudent():
    form = StudentInfoForm()
    if form.validate_on_submit():

        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys=ON")

        query = "SELECT * FROM Student where email = '" + form.email.data + "'"
        c.execute(query)
        checkIfStudentEmailDuplicate = c.fetchall()
        if len(checkIfStudentEmailDuplicate) != 0:
            flash("Duplicate email, failed to add new student.")
            return render_template('newStudent.html', title='New student', form=form)

        query = 'insert into Student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        form.UnpaidFee.data = float(form.UnpaidFee.data)

        c.execute(query, (
            form.email.data, form.firstName.data, form.middleName.data, form.lastName.data, form.grade.data,
            form.cellPhone.data, form.address.data, form.DOB.data, form.UnpaidFee.data))

        conn.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('showStudent'))
    return render_template('newStudent.html', title='New student', form=form)


@app.route("/showStudent")
def showStudent():
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT * FROM Student")
    posts = c.fetchall()

    return render_template('showStudent.html', posts=posts)


@app.route("/showStudentUnpaidFee")
def showStudentUnpaidFee():
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT * FROM Student WHERE UnpaidFee > 0")
    posts = c.fetchall()
    return render_template('showStudentUnpaidFee.html', posts=posts)


@app.route(
    "/showSpecificStudentInfo/stuEmergencyContact/deleteStuEmergencyContact/<string:studentEmail>/<string:phone>",
    methods=['GET', 'POST'])
def deleteStuEmergencyContact(studentEmail, phone):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM EmergencyContactsOfStu WHERE studentEmail = '"
    query = query + studentEmail + "' AND phone = '" + phone + "'"
    c.execute(query)
    conn.commit()
    flash(f'Delete!', 'success')
    return redirect(url_for('stuEmergencyContact', email=studentEmail))


@app.route("/showSpecificStudentInfo/stuGuardian/deleteGuardian/<string:studentEmail>/<string:guardianEmail>",
           methods=['GET', 'POST'])
def deleteGuardian(studentEmail, guardianEmail):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM Guardian WHERE studentEmail = '"
    query = query + studentEmail + "' AND guardianEmail = '" + guardianEmail + "'"
    c.execute(query)
    conn.commit()
    flash(f'Delete!', 'success')
    return redirect(url_for('stuGuardian', email=studentEmail))


@app.route("/showSpecificStudentInfo/stuEmergencyContact/<string:email>", methods=['GET', 'POST'])
def stuEmergencyContact(email):
    form = StuEmergencyContactForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM EmergencyContactsOfStu WHERE studentEmail = '"
    query = query + email + "';"
    c.execute(query)
    posts = c.fetchall()
    if form.validate_on_submit():

        query = "SELECT * FROM EmergencyContactsOfStu WHERE studentEmail = '" + \
                email + "' AND phone = " + \
                str(form.phone.data) + ";"
        c.execute(query)
        checkIfStudentEmailDuplicate = c.fetchall()
        if len(checkIfStudentEmailDuplicate) != 0:
            flash("Duplicate phone number, failed to add emergence contact.")
            return render_template('stuEmergencyContact.html', posts=posts, form=form)

        query = 'insert into EmergencyContactsOfStu VALUES (?, ?, ?, ?, ?)'
        c.execute(query, (
            form.phone.data, email, form.firstName.data, form.middleName.data, form.lastName.data))
        conn.commit()
        return redirect(url_for('stuEmergencyContact', email=email))
    return render_template('stuEmergencyContact.html', posts=posts, form=form)


@app.route("/showSpecificStudentInfo/stuGuardian/<string:email>", methods=['GET', 'POST'])
def stuGuardian(email):
    form = GuardianForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM Guardian WHERE studentEmail = '"
    query = query + email + "';"
    c.execute(query)
    posts = c.fetchall()
    if form.validate_on_submit():

        query = "SELECT * FROM Guardian WHERE studentEmail = '" + \
                email + "' AND guardianEmail = '" + \
                form.guardianEmail.data + "';"

        c.execute(query)
        checkIfStudentEmailDuplicate = c.fetchall()
        if len(checkIfStudentEmailDuplicate) != 0:
            flash("Duplicate email, failed to add guardian.")
            return render_template('stuGuardian.html', posts=posts, form=form)

        query = 'insert into Guardian VALUES (?, ?, ?, ?, ?)'
        c.execute(query, (
            form.guardianEmail.data, email, form.firstName.data, form.lastName.data, form.guardianPhoneNumber.data))
        conn.commit()
        return redirect(url_for('stuGuardian', email=email))
    return render_template('stuGuardian.html', posts=posts, form=form)


@app.route("/showSpecificStudentInfo/stuUnpaidFee/<string:email>", methods=['GET', 'POST'])
def stuUnpaidFee(email):
    form = StudentUnpaidFee()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM Student WHERE email = '"
    query = query + email + "';"
    c.execute(query)
    posts = c.fetchall()
    if form.validate_on_submit():
        query = "Update Student SET UnpaidFee = '" + \
                str(form.studentUnpaidFee.data) + "' WHERE email = '" + \
                email + "';"

        c.execute(query)
        conn.commit()
        return redirect(url_for('showStudentUnpaidFee', posts=posts))
    return render_template('stuUnpaidFee.html', posts=posts, form=form)


@app.route("/showSpecificStudentInfo/deleteStudent/<string:email>", methods=['GET', 'POST'])
def deleteStudent(email):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM Student WHERE email = '"
    query = query + email + "'"
    c.execute(query)
    conn.commit()
    flash(f'Delete!', 'success')
    return redirect(url_for('showStudent'))


@app.route('/showSpecificStudentInfo/<string:email>', methods=['GET', 'POST'])
def showSpecificStudentInfo(email):
    form = StudentInfoUpdateForm()
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM Student WHERE email = '"
    query = query + email + "';"
    c.execute(query)
    posts = c.fetchall()
    try:
        for i in posts:
            i['dobToShow'] = datetime.strptime(str(i['DOB']), '%Y%m%d').strftime('%m/%d/%Y')
    except:
        #prevent crash if datetime format isn't correct
        for i in posts:
            i['dobToShow'] = str(i['DOB'])

    if form.validate_on_submit():
        query = "UPDATE Student SET firstName = '" + form.firstName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET middleName = '" + form.middleName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET lastName = '" + form.lastName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET grade = " + str(form.grade.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET cellPhone = " + str(form.cellPhone.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET address = '" + form.address.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET DOB = " + str(form.DOB.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE Student SET UnpaidFee = " + str(form.UnpaidFee.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        return redirect(url_for('showSpecificStudentInfo', email = email))
    return render_template('showSpecificStudentInfo.html', posts=posts, form=form)


@app.route("/studentMain", methods=['GET', 'POST'])
def studentMain():
    form = StudentInfoSelectForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('blog.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys=ON")
        query = "SELECT email, firstName, middleName, lastName, UnpaidFee FROM Student"
        if len(form.email.data) != 0 or len(form.firstName.data) != 0 or len(form.middleName.data) != 0 or len(
                form.lastName.data) != 0 \
                or form.grade.data is not None:
            query = query + " WHERE"
            secondPart = []
            if len(form.email.data) != 0:
                secondPart.append("email = '" + form.email.data + "'")
            if len(form.firstName.data) != 0:
                secondPart.append("firstName = '" + form.firstName.data + "'")
            if len(form.middleName.data) != 0:
                secondPart.append("middleName = '" + form.middleName.data + "'")
            if len(form.lastName.data) != 0:
                secondPart.append("lastName = '" + form.lastName.data + "'")
            if form.grade.data is not None:
                secondPart.append("grade = " + str(form.grade.data))
            query = query + " " + secondPart[0]
            secondPart.pop(0)
            for i in secondPart:
                query = query + " AND " + i
        c.execute(query)
        posts = c.fetchall()
        return render_template('showStudent.html', posts=posts)
    return render_template('studentMain.html', title='Select student', form=form)


@app.route("/TAMain", methods=['GET', 'POST'])
def TAMain():
    form = TASelectForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('blog.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys=ON")
        query = "SELECT email, cellPhoneNum, firstName, middleName, lastName FROM TA"
        if len(form.email.data) != 0 or len(form.managerEmail.data) != 0 or len(form.firstName.data) != 0 or len(
                form.middleName.data) != 0 or len(
            form.lastName.data) != 0:
            query = query + " WHERE"
            secondPart = []
            if len(form.email.data) != 0:
                secondPart.append("email = '" + form.email.data + "'")
            if len(form.managerEmail.data) != 0:
                secondPart.append("managerEmail = '" + form.email.data + "'")
            if len(form.firstName.data) != 0:
                secondPart.append("firstName = '" + form.firstName.data + "'")
            if len(form.middleName.data) != 0:
                secondPart.append("middleName = '" + form.middleName.data + "'")
            if len(form.lastName.data) != 0:
                secondPart.append("lastName = '" + form.lastName.data + "'")
            query = query + " " + secondPart[0]
            secondPart.pop(0)
            for i in secondPart:
                query = query + " AND " + i

        c.execute(query)
        posts = c.fetchall()

        return render_template('showTA.html', posts=posts)
    return render_template('TAMain.html', title='Select TA', form=form)


@app.route("/newTA", methods=['GET', 'POST'])
def newTA():
    form = TAInfoForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT firstName, lastName, email FROM Manager WHERE email <> 'NAnobody@gmail.com'")
    posts = c.fetchall()
    choices = [('NAnobody@gmail.com', 'N/A')]
    for post in posts:
        choices.append((post['email'], post['firstName'] + " " + post['lastName']))
    form.managerEmail.choices = choices
    if form.validate_on_submit():

        query = "SELECT * FROM TA where email = '" + form.email.data + "'"
        c.execute(query)
        checkIfTADuplicate = c.fetchall()
        if len(checkIfTADuplicate) != 0:
            flash("Duplicate email, failed to add new TA.")
            return render_template('newTA.html', title='Add New TA', form=form)

        query = 'insert into TA VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        c.execute(query, (
            form.email.data, form.managerEmail.data, form.firstName.data, form.middleName.data, form.lastName.data,
            form.DOB.data, form.homePhoneNum.data, form.cellPhoneNum.data, form.highSchAvg.data, form.collegeName.data,
            form.graduateDate.data))
        if form.typeOfTA.data == 'VolunteerTA':
            query = 'insert into VolunteerTA VALUES (?)'
            c.execute(query, (form.email.data,))
        else:
            query = 'insert into PaidTA VALUES (?, ?)'

            c.execute(query, (form.email.data, float(form.GPAInPostSec.data)))
        conn.commit()
        query = "SELECT email, cellPhoneNum, firstName, middleName, lastName FROM TA WHERE email = '" + form.email.data + "'"
        c.execute(query)
        posts = c.fetchall()
        flash(f'Account created for {form.email.data}!', 'success')
        return render_template('showTA.html', posts=posts)
    return render_template('newTA.html', title='Add New TA', form=form)


@app.route("/showTA")
def showTA():
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT * FROM TA")
    posts = c.fetchall()
    return render_template('showTA.html', posts=posts)


@app.route('/showSpecificTAInfo/<string:email>', methods=['GET', 'POST'])
def showSpecificTAInfo(email):
    isPaidTA = None
    form = TAUpdateForm()
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")

    c.execute("SELECT firstName, lastName, email FROM Manager WHERE email <> 'NAnobody@gmail.com'")
    posts = c.fetchall()
    choices = [('NAnobody@gmail.com', 'N/A')]
    for post in posts:
        choices.append((post['email'], post['firstName'] + " " + post['lastName']))
    form.managerEmail.choices = choices

    query = "SELECT * FROM TA WHERE email = '"
    query = query + email + "';"
    c.execute(query)
    posts = c.fetchall()
    for i in posts:
        query = "SELECT * FROM PaidTA WHERE TAEmail = '"
        query = query + email + "';"
        c.execute(query)
        paidTAInfo = c.fetchall()
        if len(paidTAInfo) != 0:
            isPaidTA = True
            i['GPAInPostSec'] = paidTAInfo[0]['GPAInPostSec']
        else:
            isPaidTA = False
    print('!')
    try:
        for i in posts:
            i['dobToShow'] = datetime.strptime(str(i['DOB']), '%Y%m%d').strftime('%m/%d/%Y')
    except:
        #prevent crash if datetime format isn't correct
        for i in posts:
            i['dobToShow'] = str(i['DOB'])
    if form.validate_on_submit():
        '''
        query = "UPDATE TA SET typeOfTA = '" + form.typeOfTA.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()
'''
        query = "UPDATE TA SET managerEmail = '" + form.managerEmail.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET firstName = '" + form.firstName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET middleName = '" + form.middleName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET lastName = '" + form.lastName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET DOB = " + str(form.DOB.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET homePhoneNum = " + str(form.homePhoneNum.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET cellPhoneNum = " + str(form.cellPhoneNum.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET highSchAvg = " + str(form.highSchAvg.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET collegeName = '" + form.collegeName.data + "' WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        query = "UPDATE TA SET graduateDate = " + str(form.graduateDate.data) + " WHERE email = '" + email + "'"
        c.execute(query)
        conn.commit()

        if form.typeOfTA.data == 'Paid':
            if isPaidTA:
                query = "UPDATE PaidTA SET GPAInPostSec = " \
                        + str(float(form.GPAInPostSec.data)) + " WHERE TAEmail = '" + email + "'"
                c.execute(query)
                conn.commit()
            else:
                query = 'insert into PaidTA VALUES (?, ?)'
                c.execute(query, (email, float(form.GPAInPostSec.data)))
                conn.commit()
        else:
            query = "DELETE FROM PaidTA WHERE TAEmail = '" + email + "'"
            c.execute(query)
            conn.commit()

        return redirect(url_for('showTA', email=email))
    return render_template('showSpecificTAInfo.html', posts=posts, form=form)


@app.route("/showSpecificTAInfo/deleteTA/<string:email>", methods=['GET', 'POST'])
def deleteTA(email):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM TA WHERE email = '"
    query = query + email + "'"
    c.execute(query)

    query = "DELETE FROM VolunteerTA WHERE TAEmail = '"
    query = query + email + "'"
    c.execute(query)

    query = "DELETE FROM PaidTA WHERE TAEmail = '"
    query = query + email + "'"
    c.execute(query)

    conn.commit()
    flash(f'Delete!', 'success')
    '''
    query = "SELECT email, cellPhoneNum, firstName, middleName, lastName FROM TA"
    c.execute(query)
    posts = c.fetchall()
    '''
    return redirect(url_for('showTA', email=email))


@app.route("/showSpecificTAInfo/TAEmergencyContact/<string:email>", methods=['GET', 'POST'])
def TAEmergencyContact(email):
    form = TAEmergencyContactForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM EmergencyContactsOfTA WHERE TAEmail = '"
    query = query + email + "';"
    c.execute(query)
    posts = c.fetchall()

    if form.validate_on_submit():

        query = "SELECT * FROM EmergencyContactsOfTA where TAEmail = '" + email + "' AND phoneNum = " + str(
            form.phone.data) + ";"
        c.execute(query)
        checkIfDuplicate = c.fetchall()
        if len(checkIfDuplicate) != 0:
            flash("Duplicate email, failed to add new emergency contact.")
            return render_template('TAEmergencyContacts.html', posts=posts, form=form)

        query = 'insert into EmergencyContactsOfTA VALUES (?, ?, ?, ?, ?)'
        c.execute(query, (email, form.phone.data, form.firstName.data,
                          form.middleName.data, form.lastName.data))
        conn.commit()
        return redirect(url_for('TAEmergencyContact', email=email))
    return render_template('TAEmergencyContacts.html', posts=posts, form=form)


@app.route(
    "/showSpecificTAInfo/TAEmergencyContact/deleteTAEmergencyContact/<string:TAEmail>/<string:phoneNum>",
    methods=['GET', 'POST'])
def deleteTAEmergencyContact(TAEmail, phoneNum):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM EmergencyContactsOfTA WHERE TAEmail = '"
    query = query + TAEmail + "' AND phoneNum = '" + phoneNum + "'"
    c.execute(query)
    conn.commit()
    flash(f'Delete!', 'success')
    return redirect(url_for('TAEmergencyContact', email=TAEmail))


@app.route("/managerMain", methods=['GET', 'POST'])
def managerMain():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM Manager WHERE email <> 'NAnobody@gmail.com'"
    c.execute(query)
    posts = c.fetchall()
    try:
        for i in posts:
            i['dobToShow'] = datetime.strptime(str(i['DOB']), '%Y%m%d').strftime('%m/%d/%Y')
    except:
        #prevent crash if datetime format isn't correct
        for i in posts:
            i['dobToShow'] = str(i['DOB'])
    return render_template('managerMain.html', posts=posts)


@app.route("/newManager", methods=['GET', 'POST'])
def newManager():
    form = ManagerForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('blog.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys=ON")

        query = "SELECT * FROM Manager where email = '" + form.email.data + "'"
        c.execute(query)
        checkIfDuplicate = c.fetchall()
        if len(checkIfDuplicate) != 0:
            flash("Duplicate email, failed to add new manager.")
            return render_template('newManager.html', title='Add New Manager', form=form)

        query = 'insert into Manager VALUES (?, ?, ?, ?, ?, ?)'

        c.execute(query, (
            form.email.data, form.DOB.data, form.firstName.data,
            form.middleName.data, form.lastName.data,
            form.phone.data))

        conn.commit()
        query = "SELECT * FROM Manager WHERE email = '" + form.email.data + "'"
        c.execute(query)
        posts = c.fetchall()
        flash(f'Account created for {form.email.data}!', 'success')
        return render_template('managerMain.html', posts=posts)
    return render_template('newManager.html', title='Add New Manager', form=form)


@app.route("/deleteManager/<string:email>", methods=['GET', 'POST'])
def deleteManager(email):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM Manager WHERE email = '"
    query = query + email + "'"
    c.execute(query)
    conn.commit()
    flash(f'Delete!', 'success')
    return redirect(url_for('managerMain'))


@app.route("/tutorialMain", methods=['GET', 'POST'])
def tutorialMain():
    form = TutorialMainForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT email FROM TA")
    posts = c.fetchall()
    for post in posts:
        form.TAEmail.choices.append((post['email'], post['email']))
    if form.validate_on_submit():

        query = "SELECT * FROM Tutorial"
        if form.date.data is not None \
                or form.startTime.data is not None \
                or form.TAEmail.data != 'N/A' \
                or form.type.data != 'N/A' \
                or len(form.addressOrLink.data) != 0 \
                or form.grade.data is not None \
                or form.status.data != 'N/A':
            query = query + " WHERE"
            secondPart = []
            if form.date.data is not None:
                secondPart.append("date = '" + str(form.date.data) + "'")
            if form.startTime.data is not None:
                secondPart.append("startTime = '" + str(form.startTime.data) + "'")
            if form.TAEmail.data != 'N/A':
                secondPart.append("TAEmail = '" + form.TAEmail.data + "'")
            if form.type.data != 'N/A':
                secondPart.append("type = '" + form.type.data + "'")
            if len(form.addressOrLink.data) != 0:
                secondPart.append("addressOrLink = '" + form.addressOrLink.data + "'")
            if form.grade.data is not None:
                secondPart.append("grade = '" + str(form.grade.data) + "'")
            if form.status.data != "N/A":
                secondPart.append("status = '" + form.status.data + "'")
            query = query + " " + secondPart[0]
            secondPart.pop(0)
            for i in secondPart:
                query = query + " AND " + i
        c.execute(query)
        posts = c.fetchall()
        return render_template('showTutorial.html', posts=posts)
    return render_template('tutorialMain.html', title='Search tutorial', form=form)


@app.route("/newTutorial", methods=['GET', 'POST'])
def newTutorial():
    form = TutorialInfoForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT email FROM TA")
    posts = c.fetchall()
    for post in posts:
        form.TAEmail.choices.append((post['email'], post['email']))
    if form.validate_on_submit():

        query = "SELECT * FROM Tutorial where date = " + str(form.date.data) + " AND startTime = " + \
                str(form.startTime.data) + " AND TAEmail = '" + form.TAEmail.data + "' "
        c.execute(query)
        checkIfDuplicate = c.fetchall()
        if len(checkIfDuplicate) != 0:
            flash("TA have a tutorial at this time already, please change data, start time or TA's email.")
            return render_template('newTutorial.html', title='New tutorial', form=form)

        query = 'insert into Tutorial VALUES (?, ?, ?, ?, ?, ?, ?)'

        c.execute(query, (
            form.date.data, form.startTime.data, form.TAEmail.data, form.type.data, form.addressOrLink.data,
            form.grade.data,
            form.status.data))

        conn.commit()
        flash(f'Tutorial is created!', 'success')
        return redirect(url_for('showTutorial'))
    return render_template('newTutorial.html', title='New tutorial', form=form)


@app.route("/showTutorial")
def showTutorial():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("SELECT * FROM Tutorial")
    posts = c.fetchall()
    for i in posts:
        i['dateToShow'] = datetime.strptime(str(i['date']), '%Y%m%d').strftime('%m/%d/%Y')
        i['startTimeToShow'] = datetime.strptime(str(i['startTime']), '%H%M').strftime('%H:%M')

    return render_template('showTutorial.html', posts=posts)


@app.route('/showSpecificTutorialInfo/<string:TAEmail>/<string:date>/<string:startTime>', methods=['GET', 'POST'])
def showSpecificTutorialInfo(TAEmail, date, startTime):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")

    query = "SELECT * FROM Tutorial WHERE TAEmail = '" + \
            TAEmail + "' AND date = " + \
            date + " AND startTime = " + \
            startTime + ";"
    c.execute(query)
    posts = c.fetchall()
    #Some more error catching for invalid date types
    try:
        for i in posts:
            i['dateToShow'] = datetime.strptime(str(i['date']), '%Y%m%d').strftime('%m/%d/%Y')
            i['startTimeToShow'] = datetime.strptime(str(i['startTime']), '%H%M').strftime('%H:%M')
    except:
        for i in posts:
            i['dateToShow'] = str(i['date'])
            i['startTimeToShow'] = str(i['startTime'])

    query = "SELECT firstName, middleName, lastName FROM TA WHERE email = '" + TAEmail + "'"
    c.execute(query)
    TAName = c.fetchall()[0]
    return render_template('showSpecificTutorialInfo.html', posts=posts, TAName=TAName)


@app.route(
    "/home/deleteTutorial/<string:TAEmail>/<string:date>/<string:startTime>",
    methods=['GET', 'POST'])
def deleteTutorial(TAEmail, date, startTime):
    conn = sqlite3.connect('blog.db')
    # Display all blogs from the 'blogs' table
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM Tutorial WHERE TAEmail = '" + \
            TAEmail + "' AND date = " + \
            date + " AND startTime = " + \
            startTime + ";"
    c.execute(query)
    conn.commit()
    flash(f'Delete!', 'success')
    return redirect(url_for('showTutorial'))


@app.route("/home/manageStudentForTutorial/<string:TAEmail>/<string:date>/<string:startTime>", methods=['GET', 'POST'])
def manageStudentForTutorial(TAEmail, date, startTime):
    form = AddStudentAttendForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    # Division query
    query = "SELECT studentEmail AS email FROM studentAttendTutorial WHERE TAEmail = '" + \
            TAEmail + "' AND date = " + \
            date + " AND startTime = " + \
            startTime
    query = "SELECT * FROM Student WHERE email in (" + query + ")"
    c.execute(query)
    studentNameAndEmail = c.fetchall()

    # Join query
    if len(studentNameAndEmail) != 0:
        for i in studentNameAndEmail:
            query = "SELECT price FROM studentAttendTutorial, Student WHERE TAEmail = '" + \
                    TAEmail + "' AND date = " + \
                    date + " AND startTime = " + \
                    startTime + " AND studentEmail = '" + \
                    i['email'] + "' AND grade = " + i['grade']

            c.execute(query)
            i['price'] = c.fetchall()[0]['price']

    if form.validate_on_submit():
        # check if student exist
        query1 = "SELECT * FROM STUDENT WHERE email = '" + form.studentEmail.data + "'"
        c.execute(query1)
        if len(c.fetchall()) == 0:
            flash(f'No such student.', 'fail')
            return redirect(url_for('manageStudentForTutorial', TAEmail=TAEmail, date=date, startTime=startTime))

        # check if student in the tutorial already
        query = "SELECT * FROM studentAttendTutorial WHERE TAEmail = '" + \
                TAEmail + "' AND date = " + \
                date + " AND startTime = " + \
                startTime + " AND studentEmail = '" + form.studentEmail.data + "'"
        c.execute(query)
        if len(c.fetchall()) != 0:
            flash(f'Student already in the tutorial.', 'fail')
            return redirect(url_for('manageStudentForTutorial', TAEmail=TAEmail, date=date, startTime=startTime))

        # base on grade of student and the type of the tutorial, find price, then add to student's unpaid fee.
        query = "SELECT grade FROM Student WHERE email = '" + form.studentEmail.data + "'"
        c.execute(query)
        studentGrade = c.fetchall()[0]['grade']

        query = "SELECT type FROM tutorial WHERE date = " + date + " AND startTime = " + startTime + " AND TAEmail = '" + TAEmail + "'"
        c.execute(query)
        typeOfTutorial = c.fetchall()[0]['type']

        # Join query
        query = "SELECT price FROM Price, Student, Tutorial WHERE Tutorial.TAEmail = '" + \
                TAEmail + "' AND Tutorial.date = " + \
                date + " AND Tutorial.startTime = " + \
                startTime + " AND Student.email = '" + \
                form.studentEmail.data + "' AND Price.grade = Student.grade AND Price.type = Tutorial.type"
        c.execute(query)
        priceList = c.fetchall()

        price = None
        if form.price.data is None:
            if len(priceList) == 0:
                flash(f"Correlated price is not found. Please add price manually.", 'fail')
                return redirect(url_for('manageStudentForTutorial', TAEmail=TAEmail, date=date, startTime=startTime))
            else:
                price = priceList[0]['price']

        else:
            price = form.price.data

        query = 'insert into studentAttendTutorial VALUES (?, ?, ?, ?, ?)'
        c.execute(query, (
            date, startTime, TAEmail, form.studentEmail.data, float(price)))
        conn.commit()

        query = "UPDATE Student SET UnpaidFee = UnpaidFee + " + str(
            price) + " WHERE email = '" + form.studentEmail.data + "'"
        c.execute(query)
        conn.commit()
        flash(f"Success, {price} is added to student's unpaid fee.")
        return redirect(url_for('manageStudentForTutorial', TAEmail=TAEmail, date=date, startTime=startTime))
    return render_template('manageStudentForTutorial.html', studentNameAndEmail=studentNameAndEmail, form=form,
                           TAEmail=TAEmail, date=date, startTime=startTime)


@app.route("/home/removeStudentFromTutorial/<string:TAEmail>/<string:date>/<string:startTime>/<string:email>",
           methods=['GET', 'POST'])
def removeStudentFromTutorial(TAEmail, date, startTime, email):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "SELECT * FROM studentAttendTutorial WHERE studentEmail = '" + \
            email + "' AND TAEmail = '" + \
            TAEmail + "' AND date = '" + \
            date + "' AND startTime = '" + \
            startTime + "' "
    c.execute(query)
    info = c.fetchall()

    query = "DELETE FROM studentAttendTutorial WHERE studentEmail = '" + \
            email + "' AND TAEmail = '" + \
            TAEmail + "' AND date = '" + \
            date + "' AND startTime = '" + \
            startTime + "' "
    c.execute(query)

    flash(f"Student is removed, but the unpaid fee of the student is unchanged, "
          f"please mines {info[0]['price']} from {email}'s unpaid fee if you want.", 'Success')

    conn.commit()
    return redirect(url_for('manageStudentForTutorial', TAEmail=TAEmail, date=date, startTime=startTime))


@app.route("/managePriceTable", methods=['GET', 'POST'])
def managePriceTable():
    form = PriceForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")

    c.execute("SELECT * FROM Price")
    posts = c.fetchall()
    if form.validate_on_submit():
        print("Submit")
        query = "SELECT * FROM Price where type = '" + form.type.data + "' AND grade = " + str(form.grade.data) + ";"
        c.execute(query)
        checkIfDuplicate = c.fetchall()
        if len(checkIfDuplicate) != 0:
            flash("TA have a tutorial at this time already, please change data, start time or TA's email.")
            return render_template('managePriceTable.html', title='Price table', form=form, posts=posts)

        c.execute("PRAGMA foreign_keys=ON")
        query = 'insert into Price VALUES (?, ?, ?)'
        c.execute(query, (
            float(form.price.data), form.grade.data, form.type.data))
        conn.commit()
        return redirect(url_for('managePriceTable'))
    return render_template('managePriceTable.html', title='Price table', form=form, posts=posts)


@app.route("/deletePrice/<string:grade>/<string:type>/<string:price>/", methods=['GET', 'POST'])
def deletePrice(grade, type, price):
    form = PriceForm()
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    query = "DELETE FROM Price WHERE price = '" + price + "' AND grade = '" \
            + grade + "' AND type = '" + type + "'"
    c.execute(query)
    conn.commit()
    c.execute("SELECT * FROM Price")
    posts = c.fetchall()
    return redirect(url_for('managePriceTable'))


if __name__ == '__main__':
    app.run(debug=True)
