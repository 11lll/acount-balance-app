from flask import Flask, redirect, url_for, render_template, request
import smtplib
from balance_projection import balance_projection
from forms import ContactForm
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = "Don'tTellAnyone!"

email_psw = os.environ.get("FLASK_EMAIL_PSW")


@application.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()

    if form.is_submitted():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        msg = f'You have a new message from {name} || {email} \n\n {message}'

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("fundprojector@gmail.com", email_psw)
        server.sendmail("fundprojector@gmail.com", "fundprojector@gmail.com", msg)
        return render_template("form.html", form=form, name=name, email=email, message=message)
    else:
        return render_template("contact.html", form=form)


@application.route("/", methods=["POST", "GET"])
def home():
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
        return redirect(url_for("dataframe", acc_balance=ab, weekly_expenses=we, monthly_income=mi, monthly_expenses=me))
            
    return render_template("index.html")


@application.route("/dataframe", methods=["GET"])
def dataframe():
    acc_balance = int(request.args["acc_balance"])
    weekly_expenses = int(request.args["weekly_expenses"])
    monthly_income = int(request.args["monthly_income"])
    monthly_expenses = int(request.args["monthly_expenses"])
    return balance_projection(acc_balance, weekly_expenses, monthly_income, monthly_expenses)



if __name__ == "__main__":
        application.run(debug=True)
        # application.run()