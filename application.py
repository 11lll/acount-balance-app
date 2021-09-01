from flask import Flask, redirect, url_for, render_template, request
import smtplib
from balance_projection import balance_projection

application = Flask(__name__)
    
@application.route("/", methods=["POST", "GET"])
def home():
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
            
    return render_template("index.html")

@application.route("/form", methods=["POST", "GET"])
def form():
    title = "Thank You!"
    if request.method == "POST":
        req = request.form.get          #https://www.youtube.com/watch?v=lLc_jHkifRc&ab_channel=PrettyPrinted
        name = req("name")
        email = req("email")
        message = req("message")

        msg = f'You have a new message from {name} || {email} \n\n {message}'

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("fundprojector@gmail.com", "DFtJXuL8ir.60aRPGtlOC")
        server.sendmail("fundprojector@gmail.com", "fundprojector@gmail.com", msg)

        return render_template("form.html", title=title, name=name)
    return render_template("form.html", title=title)



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