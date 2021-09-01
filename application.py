from flask import Flask, redirect, url_for, render_template, request
import smtplib
from balance_projection import balance_projection
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email

application = Flask(__name__)
application.config['SECRET_KEY'] = "Don'tTellAnyone!"

class ContactForm(FlaskForm):                    #https://stackoverflow.com/questions/25324113/email-validation-from-wtform-using-flask
  name = StringField("name",  [InputRequired("Please enter your name.")], render_kw={"placeholder": "Name"})
  email = StringField("email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")], render_kw={"placeholder": "Email"})
  message = TextAreaField("message",  [InputRequired("Not including a message would be stupid")], render_kw={"placeholder": "Your message..."})
  submit = SubmitField("Send")


@application.route("/form", methods=["POST", "GET"])
def form(): 
    title = "Thank You!"
    return render_template("form.html", title=title)



@application.route("/", methods=["POST", "GET"])
def home():
    form = ContactForm()

    if form.validate_on_submit():
        req = request.form.get          #https://www.youtube.com/watch?v=lLc_jHkifRc&ab_channel=PrettyPrinted
        name = req("name")
        email = req("email")
        message = req("message")

        msg = f'You have a new message from {name} || {email} \n\n {message}'

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("fundprojector@gmail.com", "DFtJXuL8ir.60aRPGtlOC")
        server.sendmail("fundprojector@gmail.com", "fundprojector@gmail.com", msg)
        return render_template("form.html", form=form)
    
    #return "HE!"
    if request.method == "POST":

        req = request.form                                          #https://stackoverflow.com/questions/53134216/multiple-forms-on-1-page-python-flask
        ab = req["ab"]
        we = req["we"]
        mi = req["mi"]
        me = req["me"]

        if ab == '':
            ab = '0'
        if we == '':
            we = '0'
        if mi == '':
            mi = '0'
        if me == '':
            me = '0'
        #print(acc_balance, weekly_expenses, monthly_income, monthly_expenses)
        return redirect(url_for("dataframe", acc_balance=ab, weekly_expenses=we, monthly_income=mi, monthly_expenses=me))
            
    return render_template("index.html", form=form)


@application.route("/dataframe", methods=["GET"])
def dataframe():
    acc_balance = int(request.args["acc_balance"])
    weekly_expenses = int(request.args["weekly_expenses"])
    monthly_income = int(request.args["monthly_income"])
    monthly_expenses = int(request.args["monthly_expenses"])
    #print(acc_balance, weekly_expenses, monthly_income, monthly_expenses)
    #return render_template("index.html")
    return balance_projection(acc_balance, weekly_expenses, monthly_income, monthly_expenses)



if __name__ == "__main__":
        application.run(debug=True)
        # application.run()