from flask import Flask, render_template, flash, request, redirect, url_for, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, UserForm, PasswordForm, NamerForm, SearchForm, MessagesForm
from flask_ckeditor import CKEditor
from flask_ckeditor import upload_success, upload_fail
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import urllib.request
from flask_mail import Mail, Message
from mailjet_rest import Client
import uuid as uuid
import stripe
import os
import requests

#create a flask instance
app = Flask(__name__)

#add Ckeditor
ckeditor = CKEditor(app)

#Third Sqlite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devtegrate.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://msollesg:rBYN5WygJwPm6gMtBH0Ln81WCSHLJohV@mahmud.db.elephantsql.com/msollesg'

#secret key!
app.config['SECRET_KEY'] = "cairocoders-ednalan"

#saving images to the system files
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'jpeg', 'png', 'JPG', 'gif', 'PNG', 'JPEG']
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

#initializing the database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

app.config['MAX_CONTENT_LENGTH'] = 16 * 900 * 900
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'JPG', 'gif', 'PNG', 'JPEG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set Stripe API key
stripe.api_key = 'your_stripe_api_key_here'

#Search Function
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        
        #Query the Database
        posts = Posts.filter_by(Posts.content.like('%' + post.searched + '%'))
        posts = Posts.order_by(Posts.title.desc()).all()

        return render_template("search.html",
            form=form,
            searched=post.searched,
            posts=posts)

#Website Links
@app.route("/calendly-form")
def calendly():
    return render_template("calendly_form.html", 
        title= 'Consult with us at Devtegrate', 
        meta_description= 'Cloud services, Cloud consulting, Cloud migration, Cloud solutions, Cloud infrastructure, Cloud strategy, Cloud implementation, Cloud security, Cloud optimization, Cloud management, Cloud consulting agency, Cloud expertise, Cloud consulting services, Cloud consulting experts, Cloud optimization services, Cloud cost optimization, Cloud scalability, Cloud modernization, Cloud transformation, Cloud managed services', 
        keywords= 'Cloud services, Cloud consulting, Cloud migration, Cloud solutions, Cloud infrastructure, Cloud strategy, Cloud implementation, Cloud security, Cloud optimization, Cloud management, Cloud consulting agency, Cloud expertise, Cloud consulting services, Cloud consulting experts, Cloud optimization services, Cloud cost optimization, Cloud scalability, Cloud modernization, Cloud transformation, Cloud managed services',
        link= "www.devtegrate.com/calendly-form",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/about-devtegrate")
def about():
    return render_template('about.html', 
        title= 'About Devtegrate Cloud Services', 
        meta_description= "Learn more about Devtegrate, a leading cloud service agency, and how we can help your business transform with our expert services. Contact us today for a consultation.", 
        keywords= "Devtegrate, cloud service agency, expert services, consultation, business transformation.",
        link= "www.devtegrate.com/about-devtegrate",
        revised="Devtegrate, 27th of January, 2023")

@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    form = MessagesForm()
    if form.validate_on_submit():
        sender_email = 'folayemiebire@gmail.com'
        recipient_emails = 'tobi@devtegrate.com'
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        try:
            api_key = '7313cf6592999b69b87e0136ef2d0eea'
            api_secret = '06f5e0d8c5df097b9841e91e8bb51e04'

            mailjet = Client(auth=(api_key, api_secret), version='v3.1')

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": sender_email,
                            "Name": "Devtegrate"
                        },
                        "To": [
                            {
                                "Email": recipient_emails,
                                "Name": "Devtegrate"
                            }
                        ],
                        "Subject": subject,
                        "TextPart": "",
                        "HTMLPart": f'''<h2 style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1.4em; font-weight: 100; color: #000000; text-align: left; padding: 0 0 15px 0;"">You just received a message<br>{message}<br><p @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 0.9em; font-weight: 100; color: #000000; text-align: left; padding: 0 0 15px 0;">Contact phone number:</p>{phone}</p>''',
                        "CustomID": "AppGettingStartedTest"
                    }
                ]
            }

            result = mailjet.send.create(data=data)
            
            # Check if the request was successful (status code 2xx)
            if result.status_code == 200:
                flash("Thank you for reaching out. Your message has been successfully sent. We will promptly review your inquiry and get in touch with you at our earliest convenience.")
                # Send an automated response
                send_message(form)
            else:
                print(f"Failed to send the email. MailJet API response: {result.json()}")
                flash("Failed to send the email.", 'danger')
        except Exception as e:
            print(f"Error occurred while sending the emails: {e}")
            flash("Failed to send the email.", 'danger')

    return render_template("contact.html", title='Contact Devtegrate Cloud Services', meta_description='...', keywords="...", link="...", revised="...")

def send_message(messages_form):
    sender_email = 'folayemiebire@gmail.com'
    subject = messages_form.subject.data
    recipient_emails = messages_form.recipient_emails.data
    message = '''<h1 style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1.6em; font-weight: 100; color: #000000; text-align: left; padding: 15px 0 0 0;" >Hello there,</h1>

        <h2 style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left; ">This is an automated message from Devtegrate LLC. We want to notify you of our prompt response to your request. We will be in touch with you as soon as possible.</h2>

        <p style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left; padding: 0 0 15px 0;">Thank you for considering Devtegrate LLC for your needs. We look forward to assisting you soon!</p>

        <p style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left;">Have any questions? <a style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 700; color: #000000; text-align: left; padding: 0 0 15px 0; text-decoration: none; color: skyblue;" href="mailto:tobi@devtegrate.com">Devtegrate LLC Contact Mail</a></p>

        <img src="https://res.cloudinary.com/quinn-daisies/image/upload/v1695821682/devtegrate/100_zhn6gk.jpg" style="width: 150px; height: 150px; object-fit: cover; justify-content: center; align-items: center; margin: auto;">

        <h3 style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left; padding: 20px 0 0 0;">About Devtegrate LLC:</h3>
        <p style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; color: #000000; text-align: left; font-weight: 100; padding: 0 0 20px 0;">Devtegrate is a prominent professional services provider that specializes in Cloud DevOps. Our team is composed of multinational experts who possess extensive experience in the industry, totaling more than 50 years. We are committed to delivering exceptional services to our clients, addressing their specific needs on a global scale. At Devtegrate, we comprehend the distinct challenges that organizations encounter in managing their workflows, web applications, software development, and other critical requirements. To this end, we provide bespoke solutions that are tailored to streamline processes, enhance productivity, and guarantee seamless operations.</p>

    <span style="display: flex; flex-direction: row;">
        <span style="display: flex; flex-direction: row; width: 100%; padding: 10px; margin: 10px; border-radius: 10px; border: 2px solid skyblue;">
            <span>
                <span style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left;">Cloud Services</span>
                <p style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: flex;">
                    Devtegrate offers comprehensive Cloud Services to enhance your business operations. From scalable infrastructure to secure data storage, we've got you covered. Explore our cloud solutions and elevate your business to new heights.
                </p>
            </span>
            <img style="width: 100px; height: 100px; object-fit: scale-down;" src="https://res.cloudinary.com/quinn-daisies/image/upload/v1696848768/devtegrate-updates/Endpoint-pana_h6uve9.png" alt="Devtegrate Cloud Service">
        </span>

        <span style="display: flex; flex-direction: row; width: 100%; padding: 10px; margin: 10px; border-radius: 10px; border: 2px solid skyblue;">
            <span>
                <span style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left;">Cloud Migration</span>
                <p style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: flex;">
                    Simplify your transition to the cloud with Devtegrate's Cloud Migration services. Our expert team ensures a seamless migration process, minimizing downtime and maximizing efficiency. Trust us to handle your migration journey from start to finish.
                </p>
            </span>
            <img style="width: 100px; height: 100px; object-fit: scale-down;" src="https://res.cloudinary.com/quinn-daisies/image/upload/v1696848769/devtegrate-updates/Endpoint-amico_1_xdnwmn.png" alt="Devtegrate Cloud Service">
        </span>

        <span style="display: flex; flex-direction: row; width: 100%; padding: 10px; margin: 10px; border-radius: 10px; border: 2px solid skyblue;">
            <span>
                <span style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: left;">Cloud DevOps</span>
                <p style="@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'); font-family: 'poppins', sans-serif; font-size: 1em; font-weight: 100; color: #000000; text-align: flex;">
                    Accelerate your development lifecycle with Devtegrate's Cloud DevOps solutions. Our agile approach and cutting-edge tools empower your team to deliver software faster and with higher quality. Experience the benefits of DevOps for your cloud-based projects.
                </p>
            </span>
            <img style="width: 100px; height: 100px; object-fit: scale-down;" src="https://res.cloudinary.com/quinn-daisies/image/upload/v1696848768/devtegrate-updates/Endpoint-bro_dqqdap.png" alt="Devtegrate Cloud Service">
        </span>
    </span>'''

    try:
        api_key = '7313cf6592999b69b87e0136ef2d0eea'
        api_secret = '06f5e0d8c5df097b9841e91e8bb51e04'

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender_email,
                        "Name": "Devtegrate"
                    },
                    "To": [
                        {
                            "Email": recipient_emails,
                            "Name": "Devtegrate"
                        }
                    ],
                    "Subject": subject,
                    "TextPart": "",
                    "HTMLPart": message,
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }

        result = mailjet.send.create(data=data)
        # Check if the request was successful (status code 2xx)
        if result.status_code != 200:
            print(f"Failed to send the email. MailJet API response: {result.json()}")
    except Exception as e:
        print(f"Error occurred while sending the automated response: {e}")

@app.route("/make-that-great-leap-in-your-career-path")
def career():
    return render_template("career.html", 
        title= 'Careers at Devtegrate Cloud Services', 
        meta_description= 'Explore the opportunities for growth and development in the field of cloud technology with Devtegrate. Browse our job openings and apply today.',
        keywords= "Devtegrate, Cloud Services, Careers, Job Opportunities, IT Careers, Cloud Technology Careers, IT Job Openings, Cloud Jobs, Devtegrate Job Openings, Cloud Engineering Careers, Cloud Infrastructure Careers, Cloud Consultant Careers, Cloud Solutions Careers, Cloud Operations Careers, Cloud Support Careers, Cloud Professional Services Careers, Cloud Sales Careers, Cloud Marketing Careers, Cloud Administration Careers",
        link= "www.devtegrate.com/make-that-great-leap-in-your-career-path",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/explore-our-world")
def explore():
    return render_template("explore.html", 
        title= 'Explore Devtegrate Cloud Services',
        meta_description= "Discover the world of cloud technology with Devtegrate - a leading cloud service agency. Explore our range of solutions and services for your business today.",
        keywords= "Devtegrate, cloud service agency, cloud solutions, cloud services, explore, business, technology, innovation, growth",
        link= "www.devtegrate.com/explore-our-world",
        revised="Devtegrate, 27th of January, 2023")

#Attention Needed
@app.route("/devtegrate-partner/cloud-services")
def partner():
    return render_template("partner.html", 
        title= 'Explore Devtegrate Cloud Services and partner',
        meta_description= "Discover the world of cloud technology with Devtegrate - a leading cloud service agency. Explore our range of solutions and services for your business today.",
        keywords= "Devtegrate, cloud service agency, cloud solutions, cloud services, explore, business, technology, innovation, growth",
        link= "www.devtegrate.com/explore-our-world",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/frequently-asked-questions")
def faq():
    return render_template("faq.html", 
        title= 'Frequently Asked Questions - Devtegrate Cloud Services',
        meta_description= 'Get your questions answered and learn more about Devtegrate services on our FAQ page. Discover solutions to common issues and find out how to get in touch with our team.',
        keywords= 'Devtegrate, FAQ, Questions, Answers, Services, Solutions, Common issues, Contact, Team, Support, Help, Information, Cloud services, Technology, Career, Opportunities',
        link= "www.devtegrate.com/frequently-asked-questions",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/get-in-touch", methods=['GET', 'POST'])
def get_in_touch():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        email = request.form['email']
        message = request.form['message']

        body = f"Name: {name}\n\nCompany: {company}\n\nEmail: {email}\n\nMessage:\n{message}"
        mailto_url = f"mailto:tobi@devtegrate.com?subject=New Contact Form Submission&body={body}"

        return redirect(mailto_url)
    return render_template("get-in-touch.html",
        title=  "Get in Touch with Devtegrate Cloud Services",
        meta_description=  "Connect with Devtegrate and learn how our expert cloud services can benefit your business. Contact us today to schedule a consultation and take the first step towards innovation and growth.",
        keywords=  "Devtegrate, Cloud Services, Contact, Agency, Consulting, Business, Innovation, Growth, Expertise, Solutions, Support, Cloud Computing, Get in Touch, Consultation, Schedule, Connect",
        link="www.devtegrate.com/get-in-touch",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/explore-our-services")
def services():
    return render_template("services.html", 
        title=  "Explore Our Services at Devtegrate Cloud Services",
        meta_description=  "Discover the full range of cloud services offered by Devtegrate, a leading cloud service agency. From cloud consulting to cloud migration, explore our solutions and find out how we can help your business transform.",
        keywords=  "Devtegrate, cloud services, cloud consulting, cloud migration, solutions, business transformation, cloud infrastructure, cloud strategy, cloud implementation, cloud security, cloud optimization, cloud management, cloud consulting agency, cloud expertise, cloud consulting services, cloud consulting experts, cloud optimization services, cloud cost optimization, cloud scalability, cloud modernization, cloud transformation, cloud managed services.",
        link="www.devtegrate.com/explore-our-services",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/devtegrate-help-center")
def help_center():
    return render_template("help_center.html", 
        title= "Devtegrate Help Center - Get Support and Solutions",
        meta_description= "Find answers to your questions and get the support you need at the Devtegrate Help Center. Discover solutions to common issues and learn more about our services. Contact our team for further assistance.",
        keywords= "Devtegrate, Help Center, Support, Solutions, Questions, Answers, Services, Common issues, Contact, Team, Assistance, Cloud services, Technology, Career, Opportunities",
        link="www.devtegrate.com/devtegrate-help-center",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/devtegrate-privacy-policy")
def privacy_policy():
    return render_template("privacy.html",
        title= "Devtegrate Privacy Policy",
        meta_description= "Learn about Devtegrate's commitment to protecting your privacy and data. Read our privacy policy to understand how we collect, use, and share your information.",
        keywords= "Devtegrate, Privacy Policy, Data Protection, Data Privacy, Privacy Commitment, Information Collection, Data Use, Data Sharing, Privacy Statement",
        link="www.devtegrate.com/devtegrate-privacy-policy",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/inspiration")
def inspiration():
    return render_template("inspiration.html", 
        title= "Inspiration from Devtegrate Cloud Services",
        meta_description= "Find inspiration for your business and technology journey with Devtegrate. Discover success stories and learn how others have transformed their operations with our cloud services.",
        keywords= "Devtegrate, Cloud Services, Inspiration, Business, Technology, Journey, Success stories, Transformation, Operations, Cloud technology, Innovation, Growth",
        link="www.devtegrate.com/inspiration",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/amazon-web-service")
def aws():
    return render_template("aws.html",
        title= "Amazon Web Services Solutions by Devtegrate",
        meta_description= "Discover the full range of Amazon Web Services solutions offered by Devtegrate. From AWS migration to optimization and management, our expert team can help your business maximize the potential of AWS.",
        keywords= "Devtegrate, Amazon Web Services, AWS, Cloud Solutions, Cloud Migration, Cloud Optimization, Cloud Management, Cloud Consulting, Cloud Expertise, Business Solutions, AWS Solutions Provider.",
        link="www.devtegrate.com/amazon-web-service",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/microsoft-azure")
def azure():
    return render_template("azure.html", 
        title= 'Microsoft Azure Cloud Services by Devtegrate',
        meta_description= 'Explore the benefits of Microsoft Azure for your business with Devtegrates expert guidance and implementation services. Contact us to learn more.',
        keywords= 'Microsoft Azure, Devtegrate, Cloud Services, Business Solutions, Cloud Computing, Cloud Infrastructure, Cloud Migration, Cloud Security, Cloud Management, Cloud Consulting, Cloud Implementation, Cloud Strategy, Cloud Optimization, Cloud Modernization, Cloud Transformation, Cloud Expertise, Cloud Service Provider',
        link="www.devtegrate.com/microsoft-azure",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/google-cloud-platform")
def gcp():
    return render_template("gcp.html", 
        title= "Explore the Power of Google Cloud Platform with Devtegrate",
        meta_description= "Unlock the full potential of Google Cloud Platform with Devtegrate's expert services and solutions. Discover the benefits of GCP and contact us today to schedule a consultation.",
        keywords= "Devtegrate, Google Cloud Platform, GCP, Cloud Services, Solutions, Consultation, Expert Services, Cloud Computing, Technology, Business Solutions, Cloud Infrastructure, Cloud Development, Cloud Operations, Cloud Support, Cloud Professional Services, Cloud Integration",
        link="www.devtegrate.com/google-cloud-platform",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/integration", methods=['GET', 'POST'])
def integration():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        email = request.form['email']
        message = request.form['message']

        body = f"Name: {name}\n\nCompany: {company}\n\nEmail: {email}\n\nMessage:\n{message}"
        mailto_url = f"mailto:tobi@devtegrate.com?subject=New Contact Form Submission&body={body}"
        return redirect(mailto_url)
    return render_template("integration.html", 
        title= "Integration Services - Devtegrate Cloud Solutions",
        meta_description= "Streamline your business operations with Devtegrate's integration services. From cloud to on-premise and everything in between, our experts can help you achieve seamless integration. Contact us today for a consultation.",
        keywords= "Devtegrate, Integration services, Cloud solutions, On-premise, Seamless integration, Business operations, Contact, Consultation, Cloud integration, IT integration, Technical integration, Cloud services provider, Cloud strategy",
        link="www.devtegrate.com/integration",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/devtegrate-team-page")
def team():
    return render_template("team.html", 
        title= "Meet the Devtegrate Team - Cloud Experts",
        meta_description= "Get to know the talented and experienced team behind Devtegrate's cloud services. Learn about our team members' skills and expertise in the field of cloud technology. ",
        keywords= "Devtegrate, Team, Cloud Experts, Cloud Technology, Skills, Expertise, Cloud Services, Team Members, Cloud Professionals, Cloud Solutions, Cloud Infrastructure, Cloud Strategy, Cloud Implementation, Cloud Optimization, Cloud Management, Cloud Consulting, Cloud Migration, Cloud Security.",
        link="www.devtegrate.com/devtegrate-team-page",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/")
def index():
    return render_template('index.html', 
        title= 'DevOps | Software Development Cycle | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/cloud-infrastructure")
def cloud_infrastructure():
    return render_template('cloud-infrastructure.html', 
        title= 'DevOps | Cloud Infrastructure | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-infrastructure",
        revised="Devtegrate, 27th of January, 2023")

#########Update Needed############
#@app.route("/devtegrate-articles")
#def blog():
    #return render_template('blog.html', 
        #title= 'DevOps | Software Development Cycle | Cloud Service', 
        #meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        #keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        #link="www.devtegrate.com/",
        #revised="Devtegrate, 27th of January, 2023")

#@app.route("/devtegrate-articles-read")
#def article():
    #return render_template('article.html', 
        #title= 'DevOps | Software Development Cycle | Cloud Service', 
        #meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        #keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        #link="www.devtegrate.com/",
        #revised="Devtegrate, 27th of January, 2023")

@app.route("/Monitoring-and-Metrics-for-Cloud-Services-and-Cloud-DevOps")
def monitoring():
    return render_template('monitoring-and-etrics.html', 
        title= 'DevOps | Cloud Infrastructure | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-infrastructure",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/cloud-migration")
def cloud_migration():
    return render_template('cloud-migration.html', 
        title= 'DevOps | Cloud Infrastructure | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-migration",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/cloud-devops-and-devsecops")
def cloud_devops():
    return render_template('cloud-devops.html', 
        title= 'DevOps | Cloud Infrastructure | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-migration",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/devtegrate-cloud-computing")
def cloud_computing():
    return render_template('cloud-computing.html', 
        title= 'DevOps | Cloud Infrastructure | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-migration",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/cloud-integration")
def cloud_integration():
    return render_template('cloud-integration.html', 
        title= 'DevOps | Cloud Integration | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-integration",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/cloud-automation")
def cloud_automation():
    return render_template('cloud-automation.html', 
        title= 'DevOps | Cloud Automation | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/cloud-automation",
        revised="Devtegrate, 27th of January, 2023")

@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.xml",
        title= 'DevOps | Software Development Cycle | Cloud Service', 
        meta_description= 'Software Development Life Cycle | Cloud Service | Server Side Programming | Oracle Corporation  Computer software company |  SQL Server Management Studio.',
        keywords= "Software, Development, Server, Programming, Oracle, Corporation, Computer, software, Server, Management, Studio, DevOps, Devtegrate, Cloud Service, DevOpsSec, Azure, AWS, Amazon Web Service, Microsoft Azure, Google Cloud Platform, GCP",
        link="www.devtegrate.com/",
        revised="Devtegrate, 27th of January, 2023")

#Pass Stuff to NavBar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/payment-page')
def payment_page():
    return render_template('payment.html',
                           title='Explore Devtegrate Cloud Services',
                           meta_description='Discover the world of cloud technology with Devtegrate - a leading cloud service agency. Explore our range of solutions and services for your business today.',
                           keywords='Devtegrate, cloud service agency, cloud solutions, cloud services, explore, business, technology, innovation, growth',
                           link='www.devtegrate.com/explore-our-world',
                           revised='Devtegrate, 27th of January, 2023')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # If form is submitted, process payment
    if request.method == 'POST':
        # Get payment amount from form
        amount = int(request.form['amount'])

        # Create a Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount * 100,
            currency='usd'
        )

        # Return success message and redirect to dashboard
        flash('Payment was successful', 'success')
        return redirect(url_for('dashboard'))

    # Render payment page
    return render_template('payment.html')

#create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data, email=form.email.data).first()
        if user:
            
            #cHECK THE HASH
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password Please... Try Again!")
        else:
            flash(" That User Doesn't Exist... Try Again!")

    return render_template('login.html', form=form)

#Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Successfully Logged Out! ")
    return redirect(url_for('login'))

#create dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id or 1
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        
        #check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            #Grab Image name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)

            #set the uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            
            #save the image
            saver = request.files['profile_pic']

            #change it to a String to save to db
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully !")
                return render_template("dashboard.html",
                    form=form,
                    name_to_update = name_to_update)
            except:
                flash("Error! Looks Like There Was a Problem... Try Again!")
                return render_template("dashboard.html",
                    form=form,
                    name_to_update = name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully !")
            return render_template("dashboard.html",
                form=form,
                name_to_update = name_to_update)

    else:
        return render_template("dashboard.html",
                form=form,
                name_to_update = name_to_update, 
                id = id or 1)


    return render_template('dashboard.html')

#Json Thing
@app.route('/date')
def get_current_date():
    return {"Date": date.today()}

#Delete DataBase
@app .route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!!")

            our_users = Users.query.order_by(Users.date_added)
            return render_template("add_user.html",
                form=form,
                name=name,
                our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, Try Again... ")
            return render_template("add_user.html",
                form=form,
                name=name,
                our_users=our_users)

    else:
        flash("Sorry, You can delete this User")
        return redirect(url_for('dashboard'))


#Create New DataBase Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        
        #check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            #Grab Image name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)

            #set the uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            
            #save the image
            saver = request.files['profile_pic']

            #change it to a String to save to db
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully !")
                return render_template("update.html",
                    form=form,
                    name_to_update = name_to_update)
            except:
                flash("Error! Looks Like There Was a Problem... Try Again!")
                return render_template("update.html",
                    form=form,
                    name_to_update = name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully !")
            return render_template("update.html",
                form=form,
                name_to_update = name_to_update)

    else:
        return render_template("update.html",
                form=form,
                name_to_update = name_to_update, 
                id = id or 1)

@app.route('/register-an-account', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #Hash Password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

            flash("User Added Successfully")

        else:
            flash("This User Already Exist")
            return render_template("add_user.html",
                form=form)

        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash = ''

    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)

@app.route('/files/<path:filename>')
def uploaded_files(filename):
    app = current_app._get_current_object()
    path = (app.config['UPLOAD_FOLDER'])
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    app = current_app._get_current_object()
    f = request.files.get('upload')

    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    saver.save(os.path.join((app.config['UPLOAD_FOLDER']), f.filename))
    url = url_for('main.uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)


#localhost:5000/user/john
@app.route("/user")
@login_required
def user():
    poster = current_user.id
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("user.html",
        posts=posts)

#create custom error page
#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successful")

    return render_template("name.html",
        name = name,
        form = form)

#create password Testing page
@app.route('/test_pw', methods=['GET', 'POST'])
@login_required
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    #validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ""

        #Look up User by Email Address
        pw_to_check = Users.query.filter_by(email=email).first()

        #check hash password
        passed = check_password_hash(pw_to_check.password_hash, password)

        #flash("Form Submitted Successful")

    return render_template("test_pw.html",
        email = email,
        password = password,
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)

#create a model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    about_author = db.Column(db.Text(), nullable=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(), nullable=True)
    #Do Some Password Stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(' Password Not A Readable Attribute !!! ')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #create string
    def __repr__(self):
        return '<Name %r>' % self.name