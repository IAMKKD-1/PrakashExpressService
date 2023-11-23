from flask import Flask, render_template, request, redirect
from datetime import datetime
import inflect
import os

app = Flask(__name__)
p = inflect.engine()
os.makedirs(r"C:\Bills", exist_ok=True)
metadata = []
data = []
Bill_Date=datetime.now().strftime("%Y-%m-%d")
Bill_Month=datetime.now().strftime("%Y-%m")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['companyName']
        bill_date = request.form['billDate']
        bill_month = request.form['billMonth']
        airway_bill = request.form['airwayBill']
        date = request.form['date']
        weight = request.form['weight']
        destination_city = request.form['destinationCity']
        amount = request.form['amount']
        try:
            bill_date_fix = datetime.strptime(bill_date, '%Y-%m-%d').strftime('%d-%m-%Y')
            bill_month_fix = datetime.strptime(bill_month, '%Y-%m').strftime('%B-%Y')
            date_fix = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        except:
            bill_date_fix = bill_date
            bill_month_fix = bill_month
            date_fix = date
        if not metadata:
            metadata.append([company_name, bill_date_fix, bill_month_fix])   
        data.append([airway_bill, date_fix, weight, destination_city, amount])
        if data:
            for i in data:
                if '' in i:
                    data.pop(data.index(i))
        if metadata:
            for i in metadata:
                if '' in i:
                    metadata.pop(metadata.index(i))
        if 'add_row' in request.form:
            if not metadata or not data:
                return render_template('website.html', Bill_Date=Bill_Date, Bill_Month=Bill_Month, Date=Bill_Date)
            else:
                return render_template('website.html', Company_Name=metadata[0][0], Bill_Date=bill_date, Bill_Month=bill_month, Date=date)
        if 'print_pdf' in request.form:
            return redirect('/print-pdf')
    return render_template('website.html', Bill_Date=Bill_Date, Bill_Month=Bill_Month, Date=Bill_Date)

@app.route('/print-pdf')
def print_pdf():
    if not metadata or not data:
        return render_template('template.html')
    total_amount = sum([int(i[4]) for i in data])
    template = render_template('template.html', Company_Name=metadata[0][0], Bill_Date=metadata[0][1], Bill_Month=metadata[0][2], data=data, total_amount_words=p.number_to_words(total_amount).title(), total_amount=total_amount)
    data.clear()
    metadata.clear()
    return template

if __name__ == '__main__':
    app.run(debug=True)
