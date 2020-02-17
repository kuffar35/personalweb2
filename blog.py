from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,DateField,SelectField
#from wtforms.fields.html5 import DateField
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import os


#admin giriş decoder
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
         return f(*args, **kwargs)
        else :
         return redirect(url_for("index"))

    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "personal"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


#loginForm
class LoginForm(Form):
  username = StringField("",validators=[validators.length(min=4,max=20)])
  password = PasswordField("",validators=[
    validators.DataRequired(message="please enter your password")
  ])





@app.route("/project",methods = ["GET","POST"])
def project():
 pInformation =ProjectForm(request.form)  
 cursor = mysql.connection.cursor()
 projectSorgu = "Select * From project"
 result = cursor.execute(projectSorgu)
 if result > 0:
   pInformation = cursor.fetchall()
   return render_template("project.html",pInformation=pInformation)
 else :  
    return render_template("project.html")
  

@app.route("/contact",methods = ["GET","POST"])
def contact():
 cInformation =ContactForm(request.form)  
 cursor = mysql.connection.cursor()
 contactSorgu = "Select * From contact"
 result = cursor.execute(contactSorgu)
 if result > 0:
   cInformation = cursor.fetchall()
   return render_template("contact.html",cInformation=cInformation)
 else :  
    return render_template("contact.html")
  

@app.route("/controlPanelExit")
def controlPanelExit():
  session.clear()
  return render_template("index.html")

@app.route("/controlPanel",methods = ["GET","POST"])
def controlPanel():
  form = LoginForm(request.form)
  
  username = form.username.data
  password = form.password.data

  cursor=mysql.connection.cursor()
  sorgu = "select * from login where login_name = %s"
  result = cursor.execute(sorgu,(username,))
  if request.method == "POST":
    
    if result > 0 :
      data = cursor.fetchone()
      

      real_password = data["login_pass"]
      

      if password==real_password:
        session["logged_in"] = True
        session["username"]=username

        return redirect(url_for("control_layout"))
      else:
        return redirect(url_for("controlPanel"))  
     
    else:
     return redirect(url_for("controlPanel"))
  else :   
    return render_template("controlPanel/control.html",form=form)    
 
########################################################
#control panel
########################################################

@app.route("/control_layout")
@login_required
def control_layout():

  return render_template("controlPanel/control_layout.html")

#contact form
class ContactForm(Form):
  contactId = StringField("",validators=[validators.length(min=4,max=8)])
  contactHeader = StringField("",validators=[validators.length(min=4,max=80)])
  contactName = StringField("",validators=[validators.length(min=4,max=80)])

#contactControl  
@app.route("/contactControl",methods = ["GET","POST"])
@login_required
def contactControl():
 cInformation = ContactForm(request.form)  
 cursor = mysql.connection.cursor()
 informationSorgu = "Select * From contact"
 result = cursor.execute(informationSorgu)
 if result > 0:
   cInformation = cursor.fetchall()
   return render_template("controlPanel/contact_control.html",cInformation=cInformation)
 else :  
    return render_template("controlPanel/contact_control.html")


#addContact
@app.route("/addControl",methods=["GET","POST"])
@login_required
def addControl():
  form = ContactForm(request.form)
  if request.method == "POST"  :
    contactHeader = form.contactHeader.data
    contactName = form.contactName.data

    cursor = mysql.connection.cursor()
    sorgu = "Insert into 	contact(contactHeader,contactName) VALUES(%s,%s)"
    cursor.execute(sorgu,(contactHeader,contactName))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("contactControl"))
  

  return render_template("controlPanel/addControl.html",form=form)

#deleteContact
@app.route("/deleteContact/<string:id>")
@login_required
def deleteContact(id):
 cursor=mysql.connection.cursor()
 sorgu="Select * From 	contact where contactId  = %s"

 result=cursor.execute(sorgu,(id,))

 if result > 0:
   sorgu2 = "Delete from contact where contactId = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("contactControl"))

#updateContact
@app.route("/updateContact/<string:id>",methods=["GET","POST"])
@login_required
def updateContact(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From contact where contactId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      information=cursor.fetchone()
      form=ContactForm() 
      
      form.contactHeader.data = information["contactHeader"]
      form.contactName.data = information["contactName"]
      
      
      return render_template("controlPanel/updateContact.html",form=form)  
  #POST    
  else :
    form = ContactForm(request.form)
    
    newcontactHeader=form.contactHeader.data
    newcontactName=form.contactName.data
   

    sorgu2 = "Update contact Set contactHeader = %s , contactName = %s  where contactId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newcontactHeader,newcontactName,id))
    mysql.connection.commit()
    return redirect(url_for("contactControl"))
    

#projectForm
class ProjectForm(Form):
 projectId = StringField("",validators=[validators.length(min=4,max=8)])
 projectName = StringField("",validators=[validators.length(min=4,max=80)])
 projectUrl = StringField("",validators=[validators.length(min=4,max=80)])

#projectControl
@app.route("/projectControl",methods = ["GET","POST"])
@login_required
def projectControl(): 
 pInformation = ProjectForm(request.form)  
 cursor = mysql.connection.cursor()
 informationSorgu = "Select * From project"
 result = cursor.execute(informationSorgu)
 if result > 0:
   pInformation = cursor.fetchall()
   return render_template("controlPanel/project_control.html",pInformation=pInformation)
 else :  
    return render_template("controlPanel/project_control.html")

#addProject
@app.route("/addProject",methods=["GET","POST"])
@login_required
def addProject():
  form = ProjectForm(request.form)
  if request.method == "POST"  :
    projectName = form.projectName.data
    projectUrl = form.projectUrl.data

    cursor = mysql.connection.cursor()
    sorgu = "Insert into 	project(projectName,projectUrl) VALUES(%s,%s)"
    cursor.execute(sorgu,(projectName,projectUrl))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("projectControl"))
  

  return render_template("controlPanel/addProject.html",form=form)

#deleteProject
@app.route("/deleteProject/<string:id>")
@login_required
def deleteProject(id):
 cursor=mysql.connection.cursor()
 sorgu="Select * From 	project where projectId  = %s"

 result=cursor.execute(sorgu,(id,))

 if result > 0:
   sorgu2 = "Delete from project where projectId = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("projectControl"))

#updateProject
@app.route("/updateProject/<string:id>",methods=["GET","POST"])
@login_required
def updateProject(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From project where projectId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("projectControl"))
    else:
      project=cursor.fetchone()
      form=ProjectForm() 
      
      form.projectName.data = project["projectName"]
      form.projectUrl.data = project["projectUrl"]
      
      return render_template("controlPanel/updateProject.html",form=form)  
  #POST    
  else :
    form = ProjectForm(request.form)
    
    newprojectName=form.projectName.data
    newprojectUrl=form.projectUrl.data
   

    sorgu2 = "Update project Set projectName = %s , projectUrl = %s  where projectId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newprojectName,newprojectUrl,id))
    mysql.connection.commit()
    return redirect(url_for("projectControl"))
  

#mainpage_control
class MainpageControl(Form):
  InformationId = StringField("",validators=[validators.length(min=4,max=20)])
  name = StringField("",validators=[validators.length(min=4,max=80)])
  lastname = StringField("",validators=[validators.length(min=4,max=80)])
  adress = StringField("",validators=[validators.length(min=4,max=80)])
  phone = StringField("",validators=[validators.length(min=4,max=80)])
  mail =  StringField("",validators=[validators.length(min=4,max=80)])
  drivinglicence = StringField("",validators=[validators.length(min=4,max=80)])
  bloodgroup = StringField("",validators=[validators.length(min=4,max=80)])
  InformationId = StringField("",validators=[validators.length(min=4,max=80)])

  aboutId = StringField("",validators=[validators.length(min=4,max=20)])
  aboutInformation =StringField("",validators=[validators.length(min=4,max=5000)])
  
  educationId = StringField("",validators=[validators.length(min=4,max=20)])
  firstEducation = StringField("",validators=[validators.length(min=4,max=80)])
  secondEducation = StringField("",validators=[validators.length(min=4,max=80)])
  universityEducation = StringField("",validators=[validators.length(min=4,max=80)])

  certificateId = StringField("",validators=[validators.length(min=4,max=20)])
  certificateName = StringField("",validators=[validators.length(min=4,max=200)])
  certificateTime = StringField("",validators=[validators.length(min=4,max=200)])

  abiltyId = StringField("",validators=[validators.length(min=4,max=20)])
  abiltyName = StringField("",validators=[validators.length(min=4,max=200)])
  abiltyLevel = StringField("",validators=[validators.length(min=4,max=200)])

  languageId = StringField("",validators=[validators.length(min=4,max=20)])
  languageName = StringField("",validators=[validators.length(min=4,max=80)])
  languageLevel = StringField("",validators=[validators.length(min=4,max=80)])

  hobbyId = StringField("",validators=[validators.length(min=4,max=20)])
  hobbyName = StringField("",validators=[validators.length(min=4,max=20)])



@app.route("/mainpage_control",methods = ["GET","POST"])
@login_required
def mainpage_control():
  pInformation = MainpageControl(request.form)
  aInformation = MainpageControl(request.form)
  eInformation = MainpageControl(request.form)
  cInformation = MainpageControl(request.form)
  abilityInformation = MainpageControl(request.form)
  lInformation = MainpageControl(request.form)
  hInformation = MainpageControl(request.form)
  

  cursor = mysql.connection.cursor()
  aboutCursor = mysql.connection.cursor()
  eCursor = mysql.connection.cursor()
  cCursor = mysql.connection.cursor()
  abilityCursor = mysql.connection.cursor()
  lCursor = mysql.connection.cursor()
  hCursor = mysql.connection.cursor()


  informationSorgu = "Select * From personal_information"
  aInformationSorgu = "Select * From about"
  eInformationSorgu =  "Select * From education"
  cInformationSorgu =  "Select * From certificate"
  abilityInformationSorgu = "Select * From ability"
  lInformationSorgu = "Select * From language"
  hInformationSorgu = "Select * From hobby"
  
  result = cursor.execute(informationSorgu)
  aResult = aboutCursor.execute(aInformationSorgu)
  eResult =  eCursor.execute(eInformationSorgu)
  cResult =  cCursor.execute(cInformationSorgu)
  abilityResult = abilityCursor.execute(abilityInformationSorgu)
  lResult = lCursor.execute(lInformationSorgu)
  hResult = hCursor.execute(hInformationSorgu)


  if result > 0 :
    pInformation = cursor.fetchall()
    aInformation = aboutCursor.fetchall()
    eInformation = eCursor.fetchall()
    cInformation = cCursor.fetchall()
    abilityInformation = abilityCursor.fetchall()
    lInformation = lCursor.fetchall()
    hInformation = hCursor.fetchall()
    return render_template("controlPanel/mainpage_control.html",pInformation=pInformation,aInformation=aInformation,eInformation=eInformation,cInformation=cInformation,abilityInformation=abilityInformation,lInformation=lInformation,hInformation=hInformation)
  else :  
    return render_template("controlPanel/mainpage_control.html")


@app.route("/project_control")
@login_required
def project_control():
  return render_template("controlPanel/project_control.html")



@app.route("/contact_control")
@login_required
def contact_control():
  return render_template("controlPanel/contact_control.html")  


@app.route("/InformationUpdate/<string:id>",methods=["GET","POST"])
@login_required
def InformationUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From personal_information where InformationId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      information=cursor.fetchone()
      form=MainpageControl() 
      
      form.name.data = information["name"]
      form.lastname.data = information["lastname"]
      form.adress.data = information["adress"]
      form.phone.data = information["phone"]
      form.mail.data = information["mail"]
      form.drivinglicence.data = information["drivinglicence"]
      form.bloodgroup.data = information["bloodgroup"]
      
      return render_template("controlPanel/update.html",form=form)  
  #POST    
  else :
    form = MainpageControl(request.form)
    
    newName=form.name.data
    newlastname=form.lastname.data
    newadress=form.adress.data
    newphone=form.phone.data
    newmail=form.mail.data
    newdrivinglicence=form.drivinglicence.data
    newbloodgroup=form.bloodgroup.data

    sorgu2 = "Update personal_information Set name = %s , lastname = %s , adress = %s , phone = %s , mail = %s , drivinglicence = %s , bloodgroup = %s where InformationId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newlastname,newadress,newphone,newmail,newdrivinglicence,newbloodgroup,id))
    mysql.connection.commit()
    return redirect(url_for("mainpage_control"))
    
@app.route("/aboutUpdate/<string:id>",methods=["GET","POST"])
@login_required
def aboutUpdate(id):
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From about where aboutId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      about=cursor.fetchone()
      form=MainpageControl() 
      
      
      form.aboutInformation.data = about["aboutInformation"]
      
      
      return render_template("controlPanel/aboutUpdate.html",form=form) 
#POST
  else:
    form = MainpageControl(request.form)    
    newAbout=form.aboutInformation.data
   

    sorgu2 = "Update about Set aboutInformation = %s where aboutId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newAbout,id))
    mysql.connection.commit()
    return redirect(url_for("mainpage_control"))

#addCertificate

@app.route("/addCertificate",methods=["GET","POST"])
@login_required
def addCertificate():
  form = MainpageControl(request.form)
  if request.method == "POST"  :
    certificateName = form.certificateName.data
    certificateTime = form.certificateTime.data

    cursor = mysql.connection.cursor()
    sorgu = "Insert into 	certificate(certificateName,certificateTime) VALUES(%s,%s)"
    cursor.execute(sorgu,(certificateName,certificateTime))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("mainpage_control"))
  

  return render_template("controlPanel/addCertificate.html",form=form)



#deleteCertificate

@app.route("/delCertificate/<string:id>")
@login_required
def delCertificate(id):
 cursor=mysql.connection.cursor()
 sorgu="Select * From 	certificate where certificateId  = %s"

 result=cursor.execute(sorgu,(id,))

 if result > 0:
   sorgu2 = "Delete from certificate where certificateId = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("mainpage_control"))

#updateCertificate
@app.route("/updateCertificate/<string:id>",methods=["GET","POST"])
@login_required
def updateCertificate(id):

 if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From certificate where certificateId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      certificate=cursor.fetchone()
      form=MainpageControl() 
      
      
      form.certificateName.data = certificate["certificateName"]
      form.certificateTime.data = certificate["certificateTime"]

      return render_template("controlPanel/certificateUpdate.html",form=form) 
#POST
 else:
    form = MainpageControl(request.form)    
    newCname=form.certificateName.data
    newCtime=form.certificateTime.data
   

    sorgu2 = "Update certificate Set certificateName = %s , certificateTime = %s where certificateId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newCname,newCtime,id))
    mysql.connection.commit()
    return redirect(url_for("mainpage_control"))
 
 
#abilityadd
@app.route("/addAbility",methods=["GET","POST"])
@login_required
def addAbility():
  form = MainpageControl(request.form)
  if request.method == "POST"  :
    abiltyName = form.abiltyName.data
    abiltyLevel = form.abiltyLevel.data

    cursor = mysql.connection.cursor()
    sorgu = "Insert into 	ability(abiltyName,abiltyLevel) VALUES(%s,%s)"
    cursor.execute(sorgu,(abiltyName,abiltyLevel))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("mainpage_control"))
  

  return render_template("controlPanel/addAbility.html",form=form)

#abilitydelete
@app.route("/delAbility/<string:id>")
@login_required
def delAbility(id):
 cursor=mysql.connection.cursor()
 sorgu="Select * From ability where abiltyId = %s"

 result=cursor.execute(sorgu,(id,))

 if result > 0:
   sorgu2 = "Delete from ability where abiltyId = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("mainpage_control"))

#abilityupdate
@app.route("/updateAbility/<string:id>",methods=["GET","POST"])
@login_required
def updateAbility(id):
 if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From ability where abiltyId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      abilty=cursor.fetchone()
      form=MainpageControl() 
      
      
      form.abiltyName.data = abilty["abiltyName"]
      form.abiltyLevel.data = abilty["abiltyLevel"]
      
      return render_template("controlPanel/abilityUpdate.html",form=form) 
#POST
 else:
    form = MainpageControl(request.form)    
    newAname=form.abiltyName.data
    newAlevel=form.abiltyLevel.data
   

    sorgu2 = "Update ability Set abiltyName = %s , abiltyLevel = %s where abiltyId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newAname,newAlevel,id))
    mysql.connection.commit()
    return redirect(url_for("mainpage_control"))
 
#addlanguage
@app.route("/addlanguage",methods=["GET","POST"])
@login_required
def addlanguage():
  form = MainpageControl(request.form)
  if request.method == "POST"  :
    languageName = form.languageName.data
    languageLevel = form.languageName.data

    cursor = mysql.connection.cursor()
    sorgu = "Insert into 	language(languageName,languageLevel) VALUES(%s,%s)"
    cursor.execute(sorgu,(languageName,languageLevel))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("mainpage_control"))
  

  return render_template("controlPanel/addlanguage.html",form=form)

#dellanguage
@app.route("/dellanguage/<string:id>",methods=["GET","POST"])
@login_required
def dellanguage(id):
 cursor=mysql.connection.cursor()
 sorgu="Select * From language where languageId = %s"

 result=cursor.execute(sorgu,(id,))

 if result > 0:
   sorgu2 = "Delete from language where languageId = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("mainpage_control"))

#updateLanguage
@app.route("/updateLanguage/<string:id>",methods=["GET","POST"])
@login_required
def updateLanguage(id):
 if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From language where languageId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      language=cursor.fetchone()
      form=MainpageControl() 
      
      
      form.languageName.data = language["languageName"]
      form.languageLevel.data = language["languageLevel"]
      
      return render_template("controlPanel/updateLanguage.html",form=form) 
#POST
 else:
    form = MainpageControl(request.form)    
    newLname=form.languageName.data
    newLlevel=form.languageLevel.data
   

    sorgu2 = "Update language Set languageName = %s , languageLevel = %s where languageId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newLname,newLlevel,id))
    mysql.connection.commit()
    return redirect(url_for("mainpage_control"))
 


#addhobby
@app.route("/addhobby",methods=["GET","POST"])
@login_required
def addhobby():
  form = MainpageControl(request.form)
  if request.method == "POST"  :
    hobbyName = form.hobbyName.data
  

    cursor = mysql.connection.cursor()
    sorgu = "Insert into 	hobby(hobbyName) VALUES(%s)"
    cursor.execute(sorgu,(hobbyName,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("mainpage_control"))
  

  return render_template("controlPanel/addhobby.html",form=form)

#deletehobby
@app.route("/deletehobby/<string:id>",methods=["GET","POST"])
@login_required
def deletehobby(id):
 cursor=mysql.connection.cursor()
 sorgu="Select * From hobby where hobbyId = %s"

 result=cursor.execute(sorgu,(id,))

 if result > 0:
   sorgu2 = "Delete from hobby where hobbyId = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("mainpage_control"))

#updatehobby
@app.route("/updatehobby/<string:id>",methods=["GET","POST"])
@login_required
def updatehobby(id):
 if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From hobby where hobbyId  = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      hobby=cursor.fetchone()
      form=MainpageControl() 
            
      form.hobbyName.data = hobby["hobbyName"]
      
      return render_template("controlPanel/updatehobby.html",form=form) 
#POST
 else:
    form = MainpageControl(request.form)    
    newHname=form.hobbyName.data 

    sorgu2 = "Update hobby Set hobbyName = %s where hobbyId = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newHname,id))
    mysql.connection.commit()
    return redirect(url_for("mainpage_control"))

#cvSelect
@app.route("/",methods=["GET","POST"])
def personalInfprmationCv(): 
 pInformation = MainpageControl(request.form)
 aInformation = MainpageControl(request.form)
 eInformation = MainpageControl(request.form)
 cInformation = MainpageControl(request.form)
 abilityInformation = MainpageControl(request.form)
 lInformation = MainpageControl(request.form)
 hInformation = MainpageControl(request.form)

 cursor = mysql.connection.cursor()
 aboutCursor = mysql.connection.cursor()
 eCursor = mysql.connection.cursor()
 cCursor = mysql.connection.cursor()
 abilityCursor = mysql.connection.cursor()
 lCursor = mysql.connection.cursor()
 hCursor = mysql.connection.cursor()


 informationSorgu = "Select * From personal_information"
 aInformationSorgu = "Select * From about"
 eInformationSorgu =  "Select * From education"
 cInformationSorgu =  "Select * From certificate"
 abilityInformationSorgu = "Select * From ability"
 lInformationSorgu = "Select * From language"
 hInformationSorgu = "Select * From hobby"
  
 result = cursor.execute(informationSorgu)
 aResult = aboutCursor.execute(aInformationSorgu)
 eResult =  eCursor.execute(eInformationSorgu)
 cResult =  cCursor.execute(cInformationSorgu)
 abilityResult = abilityCursor.execute(abilityInformationSorgu)
 lResult = lCursor.execute(lInformationSorgu)
 hResult = hCursor.execute(hInformationSorgu)
 if result > 0:
   pInformation = cursor.fetchall()
   aInformation = aboutCursor.fetchall()
   eInformation = eCursor.fetchall()
   cInformation = cCursor.fetchall()
   abilityInformation = abilityCursor.fetchall()
   lInformation = lCursor.fetchall()
   hInformation = hCursor.fetchall()

   return render_template("index.html",pInformation=pInformation,aInformation=aInformation,eInformation=eInformation,cInformation=cInformation,abilityInformation=abilityInformation,lInformation=lInformation,hInformation=hInformation)
 else :  
    return render_template("index.html")


if __name__ == "__main__":
  app.run(debug=True) 