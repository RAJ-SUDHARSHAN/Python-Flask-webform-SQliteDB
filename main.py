from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import Length, Email, InputRequired, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=2)])
    mobile = IntegerField("Phone Number", validators=[InputRequired(),
                                                      NumberRange(min=10,
                                                                  message="Please enter a valid Phone number")])
    email = StringField("E-Mail", validators=[InputRequired(), Email()])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Any", "Any")])
    subject = SelectMultipleField("Subject",
                                  choices=[("IOT Conference", "IOT Conference"), ("Blockchain Bootcamp", "Blockchain Bootcamp"),
                                           ("AI and ML conference", "AI and ML conference")],
                                  validators=[InputRequired()])
    submit_field = SubmitField("Register")


app = Flask(__name__)
app.config["SECRET_KEY"] = '127sd3455ffg34434'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guests.db'
Bootstrap(app)

db = SQLAlchemy(app)


class Forms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)

db.create_all()


@app.route("/")
@app.route("/forms", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        existing_email = Forms.query.filter_by(email=form.email.data).first()
        existing_mobile = Forms.query.filter_by(mobile=form.mobile.data).first()
        if existing_email is None:
            new_form = Forms(name=request.form["name"], mobile=request.form["mobile"], email=request.form["email"],
                             gender=request.form["gender"], subject=request.form["subject"])
            db.session.add(new_form)
            db.session.commit()
            return "Registered Successfully"
        elif existing_mobile is None:
            new_form = Forms(name=request.form["name"], mobile=request.form["mobile"], email=request.form["email"],
                             gender=request.form["gender"], subject=request.form["subject"])
            db.session.add(new_form)
            db.session.commit()
            return "Registered Successfully"
        else:
            flash("Email or Phone number already exists")
            return redirect(url_for("register"))
    return render_template("register.html", title="Register", form=form)


@app.route("/enquiries")
def index():
    all_guests = db.session.query(Forms).all()
    return render_template("enquiries.html", guests=all_guests)


@app.route("/forms/<int:form_id>", methods=["GET", "POST"])
def update(form_id):
    update_form = Forms.query.get(form_id)
    edit_form = RegistrationForm(
        name=update_form.name,
        mobile=update_form.mobile,
        email=update_form.email,
        gender=update_form.gender,
        subject=update_form.subject
    )
    if edit_form.validate_on_submit():
        update_form.name = edit_form.name.data
        update_form.mobile = edit_form.mobile.data
        update_form.email = edit_form.email.data
        update_form.gender = edit_form.gender.data
        update_form.subject = edit_form.subject.data
        db.session.add(update_form)
        db.session.commit()
        return redirect(url_for('index', form_id=form_id))
    return render_template("register.html", form=edit_form, is_edit=True)


if __name__ == "__main__":
    app.run(debug=True)
