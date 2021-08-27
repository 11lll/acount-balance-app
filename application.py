import pandas as pd
from pandas import *
from datetime import date
from flask import Flask, redirect, url_for, render_template, request

application = Flask(__name__)

"""The Account Balance Function"""

df0=pd.DataFrame()

today = date.today()
#today = '30/08/2021' 

def balance_projection(periods, acc_balance, weekly_expenses, monthly_income, monthly_expenses):

    df0 = pd.DataFrame()
    df0['Date'] = pd.date_range(start=today, periods=periods, freq='W-MON')
    df0['Week Number'] = df0['Date'].dt.isocalendar().week
    df0['Month'] = df0['Date'].dt.month    
    
    duplicate_list = []
    duplicate_list = df0.duplicated(subset=['Month'], keep='last')

    df0['Weekly Expenses'] = weekly_expenses
    
    monthly_exp_list = []
    for n in duplicate_list:
        if n == False:
            monthly_exp_list.append(monthly_expenses)
        else:
            monthly_exp_list.append(0)
    df0['Monthly Expenses'] = monthly_exp_list

    monthly_inc_list = []
    for n in duplicate_list:
        if n == False:
            monthly_inc_list.append(monthly_income)
        else:
            monthly_inc_list.append(0)
    df0['Monthly Income'] = monthly_inc_list

    acc_balance_list = []
    for n in range(periods):
        if n == 0:
            acc_balance_list.append(acc_balance)
        else:
            acc_balance_list.append(0)
    
    rows_list = []
    new_acc_balance = 0
    for i in range(periods):
        dict1 = {}
        new_acc_balance += acc_balance_list[i] - weekly_expenses - monthly_exp_list[i] + monthly_inc_list[i]
        dict1.update(Account_Balance = new_acc_balance)
        rows_list.append(dict1) 
    
    df00 = pd.DataFrame(rows_list)
    df0 = df0.join(df00)
    df0 = df0.rename({"Account_Balance":"Account Balance"}, axis=1)
    
    #print(duplicate_list)
    #print(monthly_exp_list)
    #print(salary_list)

    html_start = f"""
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Here's your report!</title>
    <link rel= "stylesheet" type= "text/css" href="static/styles/df_style.css">
    </head>
    <body>
        <section class="wrapper">
            <div id="stars1"></div>
            <div id="stars2"></div>
            <div id="stars3"></div>
        </section>
        
        <section class="title">
            <div class="container">
                <h2 class="subhead">Here's your 1 year report!</h2>
            </div>
        </section>
        """
    # css_style = """
    # <style type="text/css" media="screen">
    #     #balance {
    #     font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    #     font-size: 12px;
    #     border-collapse: collapse;
    #     width: 100%;
    #     }

    #     #customers td, #customers th {
    #     border: 1px solid #ddd;
    #     padding: 8px;
    #     }

    #     #customers tr:nth-child(even){background-color: #f2f2f2;}

    #     #customers tr:hover {background-color: #ddd;}

    #     #customers th {
    #     padding-top: 12px;
    #     padding-bottom: 12px;
    #     text-align: left;
    #     background-color: #4CAF50;
    #     color: white;
    #     }
    # </style>
    # </head>
    # <body>
    # """
    html_body = df0.head(54).to_html(index=False, table_id="tablestyle") #set table_id to your css style name
    html_end = """
        <div id="footer">
        Created by Lukass Lappuke
        </div>
    </body>"""
    html_table = (html_start  + html_body + html_end)

    return html_table


periods = 48


    
@application.route("/", methods=["POST", "GET"])
def home():
    #return "HE!"
    if request.method == "POST":
        req = request.form

        ab = req["ab"]
        we = req["we"]
        mi = req["mi"]
        me = req["me"]

        #print(acc_balance, weekly_expenses, monthly_income, monthly_expenses)
        return redirect(url_for("dataframe", acc_balance=ab, weekly_expenses=we, monthly_income=mi, monthly_expenses=me))

    return render_template("index2.html")



@application.route("/dataframe", methods=["GET"])
def dataframe():
    acc_balance = int(request.args["acc_balance"])
    weekly_expenses = int(request.args["weekly_expenses"])
    monthly_income = int(request.args["monthly_income"])
    monthly_expenses = int(request.args["monthly_expenses"])
    #print(acc_balance, weekly_expenses, monthly_income, monthly_expenses)
    #return render_template("index.html")
    return balance_projection(periods, acc_balance, weekly_expenses, monthly_income, monthly_expenses)



if __name__ == "__main__":
        # application.run(debug=True)
        application.run_server(host="0.0.0.0")