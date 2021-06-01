from flask import Flask, redirect, url_for, session, render_template, request, jsonify, Response, send_file, send_from_directory, abort
from flask_mail import Mail, Message
from flask_pymongo import pymongo
import os
import gevent
from threading import Thread
from utils import *
from forms import *
from database import Database
from payee import *
from client import *
from chat import *
from report import *
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms
import json
import uuid
import datetime

#instantiation and configuration
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'SECRET KEY'
app.config['MAIL_SERVER'] = 'MAIL SERVER HERE'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'EMAIL HERE'
app.config['MAIL_PASSWORD'] = 'PASSWORD HERE'
app.config['PDF_FILES'] = 'PDF FOLDER'
app.config['EXCEL_FILES'] = 'EXCEL FOLDER'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'

mail = Mail(app)
socketio = SocketIO(app, logger=True)
Database.initialize()

''' Email '''
class Email:
    def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)

    def send_passcode(email):
        passcode = Generator.generate_code(8)
        msg = Message(f'Your PayeePro passcode is: {passcode}', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.html = render_template('email.html', passcode=passcode)
        session['email'] = email
        session['generated_passcode'] =  passcode
        print('from send_passcode function: ' + session['generated_passcode'])
        Thread(target=Email.send_async_email, args=(app, msg)).start()

    def send_contact_email(name, email, subject, message):
        contact_email = Message(f'Contact form', sender=app.config['MAIL_USERNAME'], recipients=['EMAIL HERE'])
        contact_email.html = render_template('contact.html', name=name, email=email, subject=subject, message=message)
        Thread(target=Email.send_async_email, args=(app, contact_email)).start()    

    def send_registration_email(email):
        #send email with link to dashboard
        registration_email = Message(f'Registration', sender=app.config['MAIL_USERNAME'], recipients=[email])
        registration_link = Generator.generate_code(16)
        registration_email.html = render_template('registration.html', email=email, registration_link=registration_link)
        Thread(target=Email.send_async_email, args=(app, )).start()

    def send_payee_form_email(email, subject, message):
        payee_form_email = Message(f'{subject}', sender=app.config['MAIL_USERNAME'], recipients=[email]) 
        payee_form_email.html = render_template('email.html', email=email, subject=subject, message=message)
        Thread(target=Email.send_async_email, args=(app, payee_form_email)).start()
        
    def send_invitation_code(email):
        invitation_code_email = Message(f'Invitation code', sender=app.config['MAIL_USERNAME'], recipients=[email]) 
        invitation_code = Generator.generate_code(8)
        invitation_code_email.html = render_template('email.html', email=email, invitation_code=invitation_code)
        Thread(target=Email.send_async_email, args=(app, invitation_code_email)).start()

'''  END  '''

''' Authenticate '''

#general authentication functionality for all users

class Authenticate:
    def verify_account(email):
        payee_email =  Database.get_record('payee', {'email' : email})
        if payee_email is None:
            print('Unauthorized')
        else:
            Email.send_passcode(email) 
''' END '''

''' User '''

#generic functionality for all users

''' END '''

''' Client '''

#functionality for clients only

class Client:
    def get_client(id):
        client = Database.get_record('client',{'_id' : ObjectId(id)})
        return client

    def get_all_clients(client_ids):
        clients = []
        if client_ids is not None:
            for client_id in client_ids:
                c = Database.get_record('client',{'_id' : ObjectId(client_id)})
                clients.append(c) 
        return clients

    def get_client_by_payee(id):
        client = Database.get_record('client', {'payee_id' : id})
        return client    

    def budget_calculator(value_list):
        return sum(value_list)


''' END '''


''' Payee '''

#functionality for payees only

class Payee:
    def get_all_payees():
        pass

    def get_payee(email):
        pass

''' END '''

def get_user_account(email):
    payee = Database.get_record('payee', {'email' : email})
    if payee is None:
        print('No account')
    else:
        return payee

def cached_accounts(id):
    #once a person logs in get there account info and cache it to persist it across the site  
    pass         

def check_messages(id):
    pass
    #when users logs in, get all their messages
    
''' END '''

#routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact/')
@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.get_json().get('name')
        email = request.get_json().get('email')
        subject = request.get_json().get('subject')
        message = request.get_json().get('message')
        Email.send_contact_email(name, email, subject, message)
    return Response("{'message' : 'message sent'}", status=200, mimetype='application/json')     

@app.route('/email_verification/')
@app.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    user_email = request.get_json().get('email')
    Authenticate.verify_account(user_email)
    return jsonify({'success' : 200})


@app.route('/passcode/', methods=['GET', 'POST'])
@app.route('/passcode', methods=['GET', 'POST'])
def passcode():
    user_entered_passcode = request.get_json().get('passcode')
    if request.method == 'POST':
        if user_entered_passcode == session['generated_passcode']: 
            return jsonify({'passcode' : user_entered_passcode, 'redirect' : '/dashboard/'})
    return jsonify({'passcode' : user_entered_passcode})    


@app.route('/dashboard/')    
@app.route('/dashboard', methods=['GET', 'POST'])
# @cache.cached(timeout=99999)
def dashboard():
    form = ChatMessageForm()   
    room = Generator.generate_code(16)  
    account = get_user_account(session['email'])
    if account['clients'] is not None:   
       ids = account['clients']
       clients = Client.get_all_clients(ids) 
    else:
       clients = 'You have no clients. Be sure to add some in the future.'                  
    return render_template('dashboard.html', account=account, clients=clients, room=room)

  
@app.route('/dashboard/budget/')
@app.route('/dashboard/budget')
def budget():
    clients = Database.get_records('client', {'payee_id' : 'ID HERE'})
    client_list = []
    for client in clients:
        client_list.append(client)              
    return render_template('budget.html', client_list=client_list)
    

@app.route('/dashboard/notifications/')
@app.route('/dashboard/notifications')
def notifications():
    pass

@app.route('/register/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.get_json().get('first_name')
        middle_name = request.get_json().get('middle_name')
        last_name = request.get_json().get('last_name')
        email = request.get_json().get('email')
        user = {
            'first_name' : first_name,
            'middle_name' : middle_name,
            'last_name' : last_name,
            'email' : email,
            'clients' : []
        }
        payee_collection.insert_one(user)
        Authenticate.verify_account(email)
    return Response({'status' : 'OK'})    


@app.route('/registration/')
@app.route('/registration')
def registration():
    return render_template('registration.html')

''' Print '''

@app.route('/dashboard/print/record', methods=['GET', 'POST'])
def dashboard_print_record():
    id = request.get_json().get('id')
    clients = Database.get_records('client',{'_id' : ObjectId(id) })
    client_list = []
    for client in clients:
        client_list.append(client) 
    return redirect(url_for('print_result', id=str(id)))
    
@app.route('/dashboard/print/<id>', methods=['GET', 'POST'])
def print_result(id):
    if id != 'null':
        client = Database.get_record('client',{'_id' : ObjectId(id) })
        return render_template('print-doc.html', client=client)
    else:
        return Response({'ok' : 200})
 
@app.route('/dashboard/print/chat-history/<id>', methods=['GET', 'POST'])
def print_chat_history(id):
    if id != 'null':
        result = Database.get_records('chat', {'client_id': id})
        chat_history = []
        for row in result:
            chat_history.append(row['messages'])  
        print(chat_history)     
        return render_template('print-chat.html', chat_history=chat_history) 
    else:
        return Response({'ok' : 200})     

@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    try:
        print(filename)
        return send_from_directory(app.config['PDF_FILES'], f"report-{filename}.pdf", as_attachment=True)
    except FileNotFoundError:
        abort(404) 

# this one, only generates PDFs
@app.route('/dashboard/print/pdf/<type>/<id>', methods=['GET', 'POST'])
def generate_report_pdf(type, id):
    if id != 'null':
        data = Database.get_record('client',{'_id' : ObjectId(id) })
        print(data['first_name'])
        name = data['first_name'] + " " + data['last_name']
        client = [{'name' : name, 'ssn' : data['ssn'], 'email' : data['email'] }]
        filename_uuid = uuid.uuid4().hex
        path = f"{app.config['PDF_FILES']}/report-{filename_uuid}.pdf"
        if type == 'monthly-statement':
            budget_report = Report.generate_budget_report(render_template('report.html', data = data, client=client), path)
            return send_from_directory(app.config['PDF_FILES'], f"report-{filename_uuid}.pdf", as_attachment=True)

        elif type == 'annual-statement':
            reports = Report.retrieve_annual_report(id)
            budget_report = Thread(Report.generate_budget_report(render_template('report.html', data = reports, client=client), path)).start()
            return send_from_directory(app.config['PDF_FILES'], f"report-{filename_uuid}.pdf", as_attachment=True)

        elif type == 'chat-history':
            return render_template('report.html', type='chat history')
  

@app.route('/dashboard/spreadsheet/<type>/<id>', methods=['GET', 'POST'])
def generate_report_spreadsheet(type, id):
    if id != 'null':
        data = Database.get_record('client',{'_id' : ObjectId(id) })
        name = data['first_name'] + " " + data['last_name']
        client = [{'name' : name, 'ssn' : data['ssn'], 'email' : data['email'] }]
        budget = data['expenses']
        filename = uuid.uuid4().hex
        spreadsheet = Report.generate_spreadsheet(data, filename)
        return send_from_directory(app.config['EXCEL_FILES'], f"{filename}.xslx", as_attachment=True)
    
''' END '''
'''  client area '''

@app.route('/client/dashboard')
@app.route('/client/dashboard/')
def client_dashboard():
    id = request.args['id']
    client = Database.get_records('client', {'_id' : ObjectId(id)})
    expenses = []
    client_item = []
    for c in client:
        client_item.append(c)
        for expense in c['expenses']:  
            for key, value in expense.items():
                if key != 'income_source' and key != 'budget_amount' and key != 'budget_date':
                    expenses.append(value) 
    return render_template('client.html', client=client_item, budget=Client.budget_calculator(expenses))

 
@app.route('/client/dashboard/chat/', methods=['GET', 'POST'])
def client_chat():
    id = request.args['id']
    messages = Database.get_record('chat', {'client_id' : id})
    client = Database.get_record('client', {'_id' : ObjectId(id) })
    payee = Database.get_record('payee', {'_id' : ObjectId(messages['payee_id'])})
    return render_template('client/chat.html', chat_messages=messages, client=client, payee=payee)

'''

 Chat

 get the admin_id from client db
 then start a chatroom with admin
 send messages between them
 then save messages to database every 20 mins or so (in the background)

'''
@socketio.on('join-room')
def on_join_room(data, methods=['GET', 'POST']):
    room = data['room']
    join_room(room)
    if 'client' in data:
        # get chat history when join 
        result = Database.get_records('chat', {'client_id': room})
        # fetch data
        chat_history = []
        total = 0
        for row in result:
            msg = json.dumps(row, default=str)
            total += len(row['messages'])
            chat_history.append(msg)
            print(rooms())   
            message_count = total
            emit('chat-history', [chat_history, message_count], room=room) 


@socketio.on('notification-alert')
def notification_alert(data, methods=['GET', 'POST']):
    #get client name and message count
    message_count = data['messageCount']
    user = ''
    role = ''
    print(message_count)
    if 'client' in data:
        client = data['client']
        print(f'to client: {client}')
        user = client
        role = 'client'
        print(user)
    elif 'payee' in data:
        payee = data['payee']
        print(f'to payee: {payee}') 
        user = payee   
        role = 'payee'
        print(user)     
    emit('notifications', [message_count, role, user])

@socketio.on('notifications')
def notifications(data, methods=['GET', 'POST']):
    #get client name and message count
    emit('notification-alert', data)
    
@socketio.on('payeepro-chat')
def on_join(data, methods=['GET', 'POST']):
    username = data['username']
    room = data['room']
    payee = data['payee']
    payee_id = data['payee_id']
    message = data['message']

    client = Database.get_record('chat', {'client_id' : room})
    if client == None:
        Database.save_record('chat', {
            'payee_id' : payee_id,
            'client_id' : room,
            'messages' : [{
                'date' : datetime.datetime.now(),
                'sender' : payee,
                'message' : message
            }] 
        })
    else:
        get_client = Database.get_record('chat', {'client_id' : data['room']})
        Database.update_record('chat', get_client, 
            { '$push':  {
                 "messages" : {
                   'date' : datetime.datetime.now(),
                   'sender' : data['payee'],
                   'message' : data['message']
                 }

            } }
        ) 
    emit('response', data, room=room)  

@socketio.on('payeepro-client-chat')
def on_client_join(data, methods=['GET', 'POST']):
    username = data['username']
    room = data['room']
    payee = data['payee']
    payee_id = data['payee_id']
    message = data['message']
    
    client = Database.get_record('chat', {'client_id' : room})
    if client == None:
        Database.save_record('chat', {
            'payee_id' : payee_id,
            'client_id' : room,
            'messages' : [{
                'date' : datetime.datetime.now(),
                'sender' : username,
                'message' : message
            }] 
        })
    else:
        get_client = Database.get_record('chat', {'client_id' : data['room']})
        Database.update_record('chat', get_client, 
            { '$push':  {
                 "messages" : {
                   'date' : datetime.datetime.now(),
                   'sender' : data['username'],
                   'message' : data['message']
                 }

            } }
        )
    emit('client-response', data, room=room)  

''' END '''

@app.route('/dashboard/email', methods=['GET', 'POST'])
def email():
    return render_template('email.html')

@app.route('/dashboard/send/email', methods=['GET', 'POST'])
def send_email():
    email = request.get_json().get('email')
    subject = request.get_json().get('subject')    
    message = request.get_json().get('message')
    if request.method == 'POST':
        Email.send_payee_form_email(email, subject, message)
    return Response("{'message' : 'message sent'}", status=200, mimetype='application/json')  

@app.route('/dashboard/additional-expense-items', methods=['GET', 'POST'])   
def additional_expense_items():
    income_sources_name = request.get_json().get('income_sources_name')
    income_sources = request.get_json().get('income_sources')
    expenses = request.get_json().get('expenses')
    amounts = request.get_json().get('amounts')
    print(amounts)
    return Response("{'message' : 'message sent'}", status=200, mimetype='application/json') 


@app.route('/save_budget/')
@app.route('/save_budget', methods=['GET', 'POST'])
def save_budget():
    if request.method == 'POST':
        budget = {
            'first_name' : request.get_json().get('first_name'),
            'middle_name' : request.get_json().get('middle_name'),
            'last_name' : request.get_json().get('last_name'),
            'email' : request.get_json().get('email'),
            'ssn' : request.get_json().get('ssn'),
            'dob' : request.get_json().get('dob'),
            'image' : 'null',
            'payee_id' : 'ID HERE',
            'expenses' :[{
             'income_source' : 'SSA',   
             'budget_amount' : request.get_json().get('budget_amount'),   
             request.get_json().get('first_expense') : request.get_json().get('first_expense_amount'),
             request.get_json().get('second_expense') : request.get_json().get('second_expense_amount'),
             request.get_json().get('third_expense') : request.get_json().get('third_expense_amount'),
             request.get_json().get('fourth_expense') : request.get_json().get('fourth_expense_amount'),
             request.get_json().get('fifth_expense') : request.get_json().get('fifth_expense_amount'),
             'additional expenses' :  request.get_json().get('additional_expenses')
            }]
        }
        Thread(target=None, args=(Database.save_record('client', budget))).start()
    return render_template('payee/chat.html', budget=budget)


'''' TESTING.... '''

@app.route('/dashboard/test-expense-items', methods=['GET', 'POST'])   
def test_additional_expense_items():
    income_sources_name = request.get_json().get('income_sources_name')
    income_sources = request.get_json().get('income_sources')
    expenses = request.get_json().get('expenses')
    amounts = request.get_json().get('amounts')
    print(amounts)
    return Response("{'message' : 'message sent'}", status=200, mimetype='application/json') 


@app.route('/test/save_budget/')
@app.route('/test/save_budget', methods=['GET', 'POST'])
def test_save_budget():
    if request.method == 'POST':
        budget = {
            'first_name' : request.get_json().get('first_name'),
            'middle_name' : request.get_json().get('middle_name'),
            'last_name' : request.get_json().get('last_name'),
            'email' : request.get_json().get('email'),
            'ssn' : request.get_json().get('ssn'),
            'dob' : request.get_json().get('dob'),
            'image' : 'null',
            'payee_id' : 'ID HERE',
            'expenses' :[{
                'income_source' : 'Social Security',   
                'budget_amount' : request.get_json().get('budget_amount'),   
                request.get_json().get('first_expense') : request.get_json().get('first_expense_amount'),
                request.get_json().get('second_expense') : request.get_json().get('second_expense_amount'),
                request.get_json().get('third_expense') : request.get_json().get('third_expense_amount'),
                request.get_json().get('fourth_expense') : request.get_json().get('fourth_expense_amount'),
                request.get_json().get('fifth_expense') : request.get_json().get('fifth_expense_amount')
            }],
        }
    return render_template('payee/chat.html', budget=budget)

''' END '''

if __name__ == '__main__':
    socketio.run(app, debug = True)