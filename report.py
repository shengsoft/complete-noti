from openpyxl import Workbook
import reportlab
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from threading import Thread
from flask import render_template
from database import Database
from datetime import datetime, date, timedelta
from bson.objectid import ObjectId
from flask_pymongo import pymongo
import json
import random

class Report:
    def generate_budget_report(html, filename): #report_type as an argument
        #get clients budget and generate PDF for download
        font_config = FontConfiguration()
        Thread(HTML(string=html).write_pdf(filename, stylesheets=['static/stylesheets/report.css'], font_config=font_config))
                              
    def generate_spreadsheet(budget, filename):
        #generate a spreadsheet of a clients budget for download
        filename = f'reports/xslx/{filename}.xslx'
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Budget'
        for data in budget['expenses']:
            for key, value in data.items():
                sheet.insert_cols(idx=1)
                sheet['A1'] = key
                sheet['A2'] = value
            workbook.save(filename=filename)
        return 'created excel file'

    def retrieve_monthly_report(id):
        #get budget of client for the prior month
        Database.initialize()
        previous_month = datetime.now().date() - timedelta(30) #datetime.date
        previous_year = datetime.now() #datetime.date        
        record = Database.get_record('client', {'_id' : ObjectId(str(id)) })
        values = []
        for date in record['additional_expenses']:
            for key, value in date.items():
                if key == 'budget_date':
                    budget_date = datetime.strftime(value, "%B %d, %Y")
                    month = datetime.strftime(previous_month, "%B %d, %Y")
                    budget_year = datetime.strftime(value, "%Y")
                    year = datetime.strftime(previous_year, "%Y")
                    if budget_date < month and budget_year == year:
                        values.append(value) 
        return values                

    def retrieve_annual_report(client_id): 
        #get budget of client for the year to date 
        Database.initialize()
        client_records = Database.get_record('client', { '_id' : ObjectId(str(client_id)) })
        previous_year = datetime.now().date() - timedelta(365)
        items = []
        for record in client_records['additional_expenses']:
            for key, value in record.items():
                 if key == 'budget_date':
                     budget_year = datetime.strftime(value, "%Y")
                     year = datetime.strftime(previous_year, "%Y")
                     if budget_year >= year: #previous year to date
                         items.append(value)
        return items                 


    def fake_annual_report(client, number_of_reports):
        Database.initialize()
        c = Database.get_record('client', {'_id' : client })
        additional_expenses = []
        reports = range(1, number_of_reports + 1)
        for data in reports:
            source = random.choice(['inheritance', 'lottery', 'annunity', 'savings'])
            start_date = datetime.now().strptime('1/1/2019 8:30 AM', '%m/%d/%Y %I:%M %p')
            end_date = datetime.now().strptime('5/20/2021 1:30 PM', '%m/%d/%Y %I:%M %p')
            time_between = end_date - start_date
            days = time_between.days
            random_day = random.randrange(days)
            random_amount_numbers = random.choice([
                    10000, 55000, 654357, 9674567, 23500, 2500, 1500, 456000, 55600, 125000,
                    987678, 54000, 5500, 12500, 55600, 789000, 7500, 550, 560, 350, 355000, 
                    5236, 768900, 65789, 34500, 2150, 6500, 8500, 66545, 12345678, 98000, 12345
                ])
            random_expense_numbers = random.choice([
                    10000, 55000, 654357, 9674567, 23500, 2500, 1500, 456000, 55600, 125000,
                    987678, 54000, 5500, 12500, 55600, 789000, 7500, 550, 560, 350, 355000, 
                    5236, 768900, 65789, 34500, 2150, 6500, 8500, 66545, 12345678, 98000, 12345
                ]) 
            random_expense_amount_numbers = random.choice([
                    10000, 55000, 654357, 9674567, 23500, 2500, 1500, 456000, 55600, 125000,
                    987678, 54000, 5500, 12500, 55600, 789000, 7500, 550, 560, 350, 355000, 
                    5236, 768900, 65789, 34500, 2150, 6500, 8500, 66545, 12345678, 98000, 12345
                ])
            random_budget_date = random.choice([
                start_date + timedelta(days=random_day),
                start_date + timedelta(days=random_day),
                start_date + timedelta(days=random_day),
                start_date + timedelta(days=random_day),
                start_date + timedelta(days=random_day),
                start_date + timedelta(days=random_day),
                start_date + timedelta(days=random_day)
            ])      
            additional_expenses.append({
                'income_source' : source,
                'amount' :  random_amount_numbers,
                'expense' : random_expense_numbers,
                'expense_amount' : random_expense_amount_numbers,
                'budget_date' : random_budget_date 
            })
            Database.update_records('client', {'_id': client}, {"$set": { 'additional_expenses': additional_expenses}})
        print(client)
    
    def generate_annual_report(payee_id):
        Database.initialize()
        client_records = Database.get_records('client', { 'payee_id' : payee_id })
        client_list = []
        for client in client_records:
            client_list.append(client)
            r = random.choice(client_list)
            id = r['_id']
        Report.fake_annual_report(id, 100)

