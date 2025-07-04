from flask import Flask, render_template, request, redirect, flash, url_for
import smtplib
from email.message import EmailMessage
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

school_email = os.getenv('school_email')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
admin_email = os.getenv('admin_email')


# Create a new client and connect to the server
uri =os.getenv('uri')
client = MongoClient(uri, server_api=ServerApi('1'))


# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)



def send_admission_email(name, email, phone, message):

    # Compose the email
    subject = "New Admission Inquiry Received"
    content = f"""
    You have received a new admission inquiry:

    Name    : {name}
    Email   : {email}
    Phone   : {phone}
    Message : {message}

    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = school_email
    msg['To'] = admin_email
    msg.set_content(content)

    # Send the email securely using SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(school_email, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Admission inquiry sent to school management.")
    except Exception as e:
        print("email not sent")
        print(f"Error sending email: {e}")


# mail Sender
def send_contact_email(name, email, message):
    msg = EmailMessage()
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = school_email
    msg['To'] = admin_email
    msg.set_content(f'''
    New inquiry received:

    Name: {name}
    Email: {email}
    Message: {message}
    ''')
    # Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(school_email, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("contact email sent to school management.")
    except Exception as e:
        print("email not sent")
        print(f"Error sending email: {e}")


app = Flask(__name__)
app.secret_key = os.getenv('secret_key')  # Needed for flashing messages

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/academics')
def academics():
    return render_template('academics.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # print("New Inquiry Received:")
        # print(f"Name: {name}")
        # print(f"Email: {email}")
        # print(f"Phone: {phone}")
        # print(f"Message: {message}")
        send_admission_email(name,email,phone,message)

        flash("Thank you for your inquiry. We will get back to you soon.")
        return redirect('/admission')

    return render_template('admission.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # print("Contact Form Submission:")
        # print(f"Name: {name}")
        # print(f"Email: {email}")
        # print(f"Message: {message}")
        send_contact_email(name,email,message)

        flash("Thanks for reaching out! We'll get back to you soon.")
        # return redirect('/contact')

    return render_template('contact.html')

@app.route('/result', methods =['GET','POST'])
def result():
    if request.method == 'POST':
        roll = request.form['roll']
        class_ = request.form['class']
        unique_id = roll+ class_

        # uri = os.getenv('MONGO_URI')
        # client = MongoClient(uri)
        results = client['school']['result']
        result = results.find_one({'roll': roll, 'class': class_})
        # code to render html file
        if result :
             return render_template('displayresult.html', result=result)
        else :
            flash("result not found check class and roll no. and try again")
            return redirect(url_for('result'))

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
