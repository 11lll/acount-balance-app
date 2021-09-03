"""The Account Balance Function"""

import pandas as pd
from pandas import *
from datetime import date 

def balance_projection(acc_balance=0, weekly_expenses=0, monthly_income=0, monthly_expenses=0):
    df0=pd.DataFrame()

    today = date.today()
    periods = 48
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
    
    html_start = f"""
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Here's your report!</title>
    <link rel= "stylesheet" type= "text/css" href="static/styles/main.css">
    </head>
    <body>
        <section class="wrapper">
            <div id="stars1"></div>
            <div id="stars2"></div>
            <div id="stars3"></div>
        </section>
        
        <section class="-table-title">
            <div class="table-container">
                <h2 class="subhead">Here's your 1 year report!</h2>
            </div>
        </section>

        """

    html_end = """
        
        <section class="table-help-section">
            <div class="container"> 
                    <a href="https://fundprojector.com/contact">
                        <div class="contact-center">
                            <h1> Need help?</h1>
                        </div>
                    </a>

                    <a href="https://fundprojector.com/">
                        <div class="go-home-btn">
                            <h1>Try again!</h1>
                        </div>
                    </a>                                            
            </div>
        </section>

        <div id="footer">
        Created by Lukass Lappuke
        </div>
    </body>"""
    
    html_body = df0.head(54).to_html(index=False, table_id="tablestyle") #set table_id to your css style name
    html_table = (html_start  + html_body + html_end)

    return html_table