from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField, \
    IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class StudentInfoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First name', validators=[DataRequired(), Length(min=2, max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=20)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(min=2, max=255)])
    grade = IntegerField('Grade', validators=[DataRequired()])
    cellPhone = IntegerField('Cell phone number', validators=[DataRequired()])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    DOB = IntegerField('DOB (Enter 20210329 for 2021/3/29 )', validators=[DataRequired()])
    UnpaidFee = DecimalField('UnpaidFee')
    submit = SubmitField('Submit')


class StudentInfoSelectForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email()])
    firstName = StringField('First name', validators=[Optional(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[Optional(), Length(max=255)])
    grade = IntegerField('Grade', validators=[Optional()])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Submit')


class StudentInfoUpdateForm(FlaskForm):
    firstName = StringField('First name', validators=[DataRequired(), Length(min=2, max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=20)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(min=2, max=255)])
    grade = IntegerField('Grade', validators=[DataRequired()])
    cellPhone = IntegerField('Cell phone number', validators=[DataRequired()])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    DOB = IntegerField('DOB (Enter 20210329 for 2021/3/29 )', validators=[DataRequired()])
    UnpaidFee = DecimalField('UnpaidFee')
    submit = SubmitField('Submit')


class StuEmergencyContactForm(FlaskForm):
    phone = IntegerField('Phone number', validators=[DataRequired()])
    firstName = StringField('First name', validators=[DataRequired(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add new emergency contact')


class GuardianForm(FlaskForm):
    guardianEmail = StringField('Guardian email', validators=[DataRequired(), Email()])
    firstName = StringField('First name', validators=[DataRequired(), Length(max=255)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(max=255)])
    guardianPhoneNumber = IntegerField('Phone number', validators=[DataRequired()])
    submit = SubmitField('Add new guardian for student')


class StudentUnpaidFee(FlaskForm):
    studentUnpaidFee = DecimalField('UnpaidFee')
    submit = SubmitField('Update Unpaid Fee')


class TAInfoForm(FlaskForm):
    typeOfTA = SelectField('Volunteer or paid', choices=[('Paid', 'Paid'), ('Volunteer', 'Volunteer')])
    GPAInPostSec = DecimalField('GPA in post secondary school(Enter any non-zero number if is volunteer TA)',
                                validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    managerEmail = SelectField('Manager email', choices=[])
    firstName = StringField('First name', validators=[DataRequired(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(max=255)])
    DOB = IntegerField('DOB', validators=[DataRequired()])
    homePhoneNum = IntegerField('Home Phone number', validators=[Optional()])
    cellPhoneNum = IntegerField('Cell Phone number', validators=[DataRequired()])
    highSchAvg = IntegerField('High school average', validators=[Optional()])
    collegeName = StringField('College name', validators=[Optional()])
    graduateDate = IntegerField('Graduate date', validators=[Optional()])
    submit = SubmitField('Submit')


class TAUpdateForm(FlaskForm):
    typeOfTA = SelectField('Volunteer or paid', choices=[('Paid', 'Paid'), ('Volunteer', 'Volunteer')])
    GPAInPostSec = DecimalField('GPA in post secondary school(Enter any non-zero number if is volunteer TA)',
                                validators=[DataRequired()])
    managerEmail = SelectField('Manager email', choices=[])
    firstName = StringField('First name', validators=[DataRequired(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(max=255)])
    DOB = IntegerField('DOB', validators=[DataRequired()])
    homePhoneNum = IntegerField('Home Phone number', validators=[Optional()])
    cellPhoneNum = IntegerField('Cell Phone number', validators=[DataRequired()])
    highSchAvg = IntegerField('High school average', validators=[Optional()])
    collegeName = StringField('College name', validators=[Optional()])
    graduateDate = IntegerField('Graduate date', validators=[Optional()])
    submit = SubmitField('Submit')


class TASelectForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email()])
    managerEmail = StringField('Manager', validators=[Optional(), Email()])
    firstName = StringField('First name', validators=[Optional(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Search')


class TAEmergencyContactForm(FlaskForm):
    phone = IntegerField('Phone number', validators=[DataRequired()])
    firstName = StringField('First name', validators=[DataRequired(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add new emergency contact')


class ManagerForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    DOB = IntegerField('DOB (Enter 20210329 for 2021/3/29 )', validators=[DataRequired()])
    firstName = StringField('First name', validators=[DataRequired(), Length(max=255)])
    middleName = StringField('Middle name', validators=[Optional(), Length(max=255)])
    lastName = StringField('Last name', validators=[DataRequired(), Length(max=255)])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    submit = SubmitField('Add new manager')


class TutorialInfoForm(FlaskForm):
    date = IntegerField('Date (Enter 20210329 for 2021/3/29 )', validators=[DataRequired()])
    startTime = IntegerField('Start at (Enter 1800 for 18:00)', validators=[DataRequired()])
    TAEmail = SelectField("Select TA's email", choices=[])
    type = SelectField("Type of tutorial", choices=[('Group', 'Group'), ('One to one', 'One to One')])
    addressOrLink = StringField('Address/Link', validators=[Optional()])
    grade = IntegerField('Grade', validators=[DataRequired()])
    status = SelectField("Status of the tutorial", choices=[('Attend', 'Attend'), ('Not attend', 'Not attend')])
    submit = SubmitField('Create tutorial')


class TutorialMainForm(FlaskForm):
    date = IntegerField('Date (Enter 20210329 for 2021/3/29 )', validators=[Optional()])
    startTime = IntegerField('Start at (Enter 1800 for 18:00)', validators=[Optional()])
    TAEmail = SelectField("Select TA's email", choices=[('N/A', 'N/A')])
    type = SelectField("Type of tutorial", choices=[('N/A', 'N/A'), ('Group', 'Group'), ('One to one', 'One to One')])
    addressOrLink = StringField('Address/Link', validators=[Optional()])
    grade = IntegerField('Grade', validators=[Optional()])
    status = SelectField("Status of the tutorial",
                         choices=[('N/A', 'N/A'), ('Attend', 'Attend'), ('Not attend', 'Not attend')])
    submit = SubmitField('Search tutorial')


class AddStudentAttendForm(FlaskForm):
    studentEmail = StringField('Student email', validators=[DataRequired(), Email()])
    price = DecimalField('Price: ', validators=[Optional()])
    submit = SubmitField('Submit')


class PriceForm(FlaskForm):
    price = DecimalField('Price', validators=[DataRequired()])
    grade = IntegerField('Grade')
    type = SelectField("Type of tutorial", choices=[('N/A', 'N/A'), ('Group', 'Group'), ('One to one', 'One to One')])
    submit = SubmitField('Submit')


'''
class AddStudentAttendForm(FlaskForm):
    date = IntegerField('Date (Enter 20210329 for 2021/3/29 )', validators=[DataRequired()])
    startTime = IntegerField('Start at (Enter 1800 for 18:00)', validators=[DataRequired()])
    TAEmail = SelectField("Select TA's email", choices=[])
    studentEmail = StringField('Please enter the student email correctly', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
'''
