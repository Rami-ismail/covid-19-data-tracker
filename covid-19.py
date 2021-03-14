#imported modules
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import Text
import time
import datetime
import smtplib
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MT1
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import pathlib
import sqlite3



def get_data(country_name):#function that gets the country/global data 
    if  country_name=='World':
        country_name='all' 
        url='https://corona.lmao.ninja/v2/'+country_name
        page=requests.get(url)
        data=page.json()
        results={}
        for i in data.keys():
            if i!='updated' and i!='affectedCountries':
                temp={'country':'World'}
                temp[i]=data[i]
                results.update(temp)
                if results[i]==None:
                   results[i]=0
        return results

    else:
        url='https://corona.lmao.ninja/v2/countries/'+country_name+'?'
        page=requests.get(url)
        data=page.json()
        results={}
        for i in data.keys():
            if i!='countryInfo' and i!='updated':
                results[i]=data[i]
                if results[i]==None:
                    results[i]=0
           
        return results
           
        

def get_countries(): #function that returns a dictionnary with country names as keys and country codes as values
    url='https://corona.lmao.ninja/v2/countries/'
    page=requests.get(url)
    data=page.json()
    database={'World':''}
    temp={}

    for i in range(len(data)):
        for j in data[i].keys():
            if j=='country':
                name=data[i][j]
            if j=='countryInfo':
                temp[name]=data[i][j]['iso2']
            database.update(temp)
    return database
        
            
            
def get_country_code(name):#function that transforms an inputted country name into it's respective country code
    database=get_countries()
    for i in database.keys():
        if name.lower()==i.lower():
            return database[i]
        
def print_(country_data):
    res=''
    for i in country_data.keys():
        res=res+i+':'+str(country_data[i])+'\n'
    return res

def user_registration():
    global NAME,Username
    NAME=Name.get()
    UserName=Username.get()
    emailid=EmailId.get()
    password=Password.get()
    directory2=os.getcwd()+'\\accounts\\'
    

    if NAME!='' and UserName!='' and emailid!='' and password!='':#this is to verify that every entry is filled
        if os.path.isfile(directory2+UserName+'.db'):
            messagebox.showerror('Error','Username in use')
        else:
            user_db=sqlite3.connect(directory2+UserName+'.db')
            cursor=user_db.cursor()
            cursor.execute('CREATE TABLE Credentials(Name text,Username text,Email text,Password text)')
            cursor.execute("CREATE TABLE VirusRequestedData(country text,cases text,todaycases text,death text,todaydeaths text,recovered text,active text,critical text,casesPerOneMillion text,deathsPerOneMillion text,tests text,testsPerOneMillion text,population text,activePerOneMillion text,recoveredPerOneMillion text,criticalPerOneMillion text,Date text)")
                
            
            creds=(NAME,UserName,emailid,password)
            cursor.execute('INSERT INTO Credentials(Name,Username,Email,Password) Values(? ,? ,? ,?)',creds)
            user_db.commit()
            user_db.close()
            messagebox.showinfo("Success!", "Registration Success!")
            Name.set('')
            Username.set('')
            EmailId.set('')
            Password.set('')
    else:
         messagebox.showerror("Error!", "Registration Failed!")
           
    


def register():#creating the register GUI
    global ScreenRegi,UserNameliste,Name,Username,EmailId,Password,user_verify,pass_verify

    ScreenRegi=Toplevel(RegiAndLogin)
    ScreenRegi.title("registration form")
    ScreenRegi.geometry("400x400")
    ScreenRegi.iconbitmap('coronavirus.ico')

    Name=StringVar()
    Username=StringVar()
    EmailId=StringVar()
    Password=StringVar()
    NameLabel=Label(ScreenRegi,text="  Name  ").pack()
    NameEntry=Entry(ScreenRegi,textvariable=Name,width=50).pack()
    UsernameLabel=Label(ScreenRegi,text="   Username   ").pack()
    UsernameEntry=Entry(ScreenRegi,textvariable=Username,width=50).pack()
    EmailIdLabel=Label(ScreenRegi,text="   Email   ").pack()
    EmailIdLabel=Entry(ScreenRegi,textvariable=EmailId,width=50).pack()
    PasswordLabel=Label(ScreenRegi,text="   Password   ").pack()
    PasswordEntry=Entry(ScreenRegi,textvariable=Password,show="*",width=50).pack()
    blank=Label(ScreenRegi,text="  ").pack()
    RegistrationButton=Button(ScreenRegi,text="register",command=user_registration).pack()

 #pack is used here to allign the widgets quickly since not too much is going on 



def button_login():

    global olduser,oldpass,user_db,cursor,user
    user_verify=olduser.get()
    pass_verify=oldpass.get()
    directory2=os.getcwd()+'\\accounts\\'

    if not os.path.isfile(directory2+user_verify+'.db'):
        messagebox.showerror("Error!", "User not found")
    else:
    
        
        user_db=sqlite3.connect(directory2+user_verify+'.db')
        cursor=user_db.cursor()
    
        cursor.execute('SELECT Password FROM Credentials')
        password=cursor.fetchall()
        password=password[0][0]

        cursor.execute('SELECT Username FROM Credentials')
        user=cursor.fetchall()
        user=user[0][0]


        if user==user_verify and password==pass_verify:
            messagebox.showinfo("Succes!", "Login success")
            RegiAndLogin.destroy()
            datapage()

        if password!=pass_verify:     
            messagebox.showerror("Error!", "Password doesn't match!")
    
        

def registerAndLogin():#creating the "Welcome" interface

    global RegiAndLogin, ScreenLogIn,olduser,oldpass,Name,Username,EmailId,Password,directory

    RegiAndLogin=Tk()
    RegiAndLogin.geometry("626x392")
    RegiAndLogin.title("Corona Virus Data Tracker")
    RegiAndLogin.resizable(0,0)
    RegiAndLogin.iconbitmap('coronavirus.ico')
    
    olduser=StringVar()
    oldpass=StringVar()

    canvas=Canvas(RegiAndLogin,height=626,width=391)
    canvas.pack(fill=BOTH)#this allows us to create a canvas for a background image
    directory=os.getcwd()+'\\texture\\'
    image=ImageTk.PhotoImage(file=directory+'application background.jpg')
    background_label=ttk.Label(image=image)
    background_label.image=image
    background_label.place(x=-1,y=-1,relwidth=1,relheight=1)



    regi_button=Button(RegiAndLogin,text="Register",command=register)
    welcome_label=ttk.Label(RegiAndLogin,text="Welcome to the Corona Virus Data Tracker!",anchor=CENTER)
    login_label=ttk.Label(RegiAndLogin,text='Login if you have an account:',anchor=CENTER)
    Register_label=ttk.Label(RegiAndLogin,text="Don't have an account? Register:",anchor=CENTER)

    loginuser=Label(RegiAndLogin,text="Username:")
    login_user_entry=Entry(RegiAndLogin,textvariable=olduser,width=40)
    loginpass=Label(RegiAndLogin,text="Password:")
    login_pass_entry=Entry(RegiAndLogin,textvariable=oldpass,show="*",width=40)
    login_Button=Button(RegiAndLogin,text="Login",command=button_login)



    welcome_label.place(x=100,y=10,width=400)
    login_label.place(x=100,y=100,width =200)
    Register_label.place(x=185,y=280,width=200)
    regi_button.place(x=240,y=320,width=100)
    loginuser.place(x=100,y=150)
    login_user_entry.place(x=180,y=150)
    loginpass.place(x=100,y=200)
    login_pass_entry.place(x=180,y=200)
    login_Button.place(x=240,y=240,width=100)



    RegiAndLogin.mainloop()





def get_country_name_list(): #this function returns a list with all the country names gathered from the API to be used for the combobox later
    country_dict=get_countries()
    country_list=[]
    for i in country_dict.keys():
        country_list.append(i)
    return country_list
    

def country_selector(evt): #this function allows an action to trigger in the events of someone clicking an item in the combobox
    country_dict=get_countries()
    country_code.set(country_dict[country_box.get()])
    print_data(get_data(country_name.get()))
    analysepropotion()
    

def print_data(country_data):#displays the country data in form of labels
    global country_result_LBL,widget
    widget=[]
    for i in country_data.keys():
            country_result_LBL=ttk.Label(main_window,text=i+' : '+str(country_data[i]),background='white',width=35)
            widget.append(country_result_LBL)
            for i in range(len(widget)):
                country_result_LBL.place(x=580,y=(i+4)*20)
    if country_name.get()!='World':
        country_box['state']='disabled'



        


def clear():# this function will clear the displayed data in order for it to be replaced when the function print_data is called again
    global widget
    if country_name.get()!='World':
        for i in widget:
            i.destroy()
        country_box['state']='readonly'
        country_code.set('')
        country_name.set('World')
        chartcanvas._tkcanvas.destroy()

    

def tick(): #this function helps refresh the clock every 200 ticks( every second)
    global time
    current_time=time.strftime('%H:%M:%S')#local time from pc
    if current_time != time:#update time if it changes
        time1 = current_time
        clock.config(text=current_time)
    clock.after(200, tick)#refreshes after 200 ticks
    

def Share(): #creating the interface that will allow the user to share the data that he/she requested
    global email,password,receiver,Subject,message,share_window,message_Entry
    
    share_window=Toplevel(main_window)
    share_window.geometry('850x400')
    share_window.title('Sharing')
    share_window.iconbitmap('coronavirus.ico')

    
    receiver=StringVar()
    Subject=StringVar()
    message=StringVar()

    
    To_Label=ttk.Label(share_window,text='Recipient email').pack()
    To_Entry=ttk.Entry(share_window,textvariable=receiver,width=50).pack()

    Sub_Label=ttk.Label(share_window,text='Subject').pack()
    subject_Entry=ttk.Entry(share_window,textvariable=Subject,width=50).pack()

    Msg_Label=ttk.LabelFrame(share_window,text='Message : ')
    Msg_Label.pack()
    message_Entry=Text(Msg_Label,width=100,height=16)
    message_Entry.pack()
    
    Send_button=ttk.Button(share_window,command=mail,text='Send',width=25).pack()



    if country_name.get()=='' or country_name.get()=='World':
        Subject.set('Global Corona Statistics')
        country_name.set('World')
    else:
        Subject.set('Corona Statistics for '+country_name.get())
        
    

    data=get_data(country_name.get())
    
    message.set('Here are the statistics of covid-19 recorded on '+str(date.strftime('%A'))+' '+str(date.strftime('%B'))+' '+str(date.strftime('%d'))+' '+str(date.strftime('%Y'))+' in '+country_name.get()+' at '+str(time.strftime('%H:%M:%S'))+' (GMT+3):\n'+print_(get_data(country_name.get()))+'\n\n                                                           Stay Safe, Your Dear Friend: '+user.upper())
    message_Entry.insert(INSERT,message.get())

def mail(): # this function is responsible of sending an email via the messaging server (gmail ---> to any email)
    email_user='covid19datatracker@gmail.com'
    password_user='Ramichko123'
    send_to = receiver.get()
    subject = Subject.get()
    message_content= message_Entry.get('1.0','end')

    if send_to=='':
        messagebox.showerror('Error',"You can't email the wind")
    else:

        msg=MT1()
        msg['From']=email_user
        msg['To']=send_to
        msg['Subject']=subject

        msg.attach(MT(message_content,'plain'))

        server=smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_user,password_user)
        text=msg.as_string()
        server.sendmail(email_user, send_to,text)
        server.quit()

        messagebox.showinfo('Success!','The data you requested was sent succesfully')
        share_window.destroy()

        
        


def plotnormal(): #ploting the results of the selected criteria
    fig=plt.figure()
    plt.bar(x,y,color='blue')
    plt.title('Requested chart for '+country_name.get(),fontsize=16)
    plt.ylabel('Values',fontsize=14)
    plt.xlabel('Criteria',fontsize=14)
    fig.show()
  
    


def plotevo():#total cases total recovered total deaths

    axis=cursor.fetchall()
    xaxis=[]
    yaxis=[]
    for i in range(len(axis)):
            xaxis.append(axis[i][1])
            yaxis.append(float(axis[i][0]))

    if len(xaxis)<=1:
         messagebox.showerror('Error','Insufficent Data')
         fixgui() 


    else:
        fig=plt.figure()
        plt.plot(xaxis,yaxis,color='blue')
        plt.title('Requested plot for '+country_name.get(),fontsize=16)
        plt.xlabel('Months',fontsize=14)
    fig.show()

        
        

#creates x and y axis for each stat variable
x=[]
y=[]
def createaxis0(): 
        temp=stat0.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat0_check_button['state']=DISABLED
def createaxis1():
        temp=stat1.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat1_check_button.config(state=DISABLED)
def createaxis2():
        temp=stat2.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat2_check_button.config(state=DISABLED)

def createaxis3():
        temp=stat3.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat3_check_button.config(state=DISABLED)
def createaxis4():
        temp=stat4.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat4_check_button.config(state=DISABLED)

def createaxis5():
        temp=stat5.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat5_check_button.config(state=DISABLED)
def createaxis6():
        temp=stat6.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat6_check_button.config(state=DISABLED)
def createaxis7():
        temp=stat7.get()
        if data[temp]==None:
            data[temp]=0
        x.append(temp)
        y.append(data[temp])
        stat7_check_button.config(state=DISABLED)

def clearaxis():#clears the criteria chosen for the x axis
    global x,y
    x=[]
    y=[]
    stat0.set('')
    stat1.set('')
    stat2.set('')
    stat3.set('')
    stat4.set('')
    stat5.set('')
    stat6.set('')
    stat7.set('')
    
    stat0_check_button.config(state=NORMAL)
    stat1_check_button.config(state=NORMAL)
    stat2_check_button.config(state=NORMAL)
    stat3_check_button.config(state=NORMAL)
    stat4_check_button.config(state=NORMAL)
    stat5_check_button.config(state=NORMAL)
    stat6_check_button.config(state=NORMAL)
    stat7_check_button.config(state=NORMAL)
  

def logout():#logout function returns to main window
    main_window.destroy()
    user_db.close()
    registerAndLogin()  

def save():
   
    data=get_data((country_name.get()))
    entities=[]

    for i in data.values():
        entities.append(i)
    
    if country_name.get()!='World':
        del entities[13]
    entities.append(str(date.strftime('%B'))+' '+str(date.strftime('%d')+' '+str(date.strftime('%Y'))))
    cursor.execute("INSERT INTO VirusRequestedData(country,cases,todaycases,death,todaydeaths,recovered,active,critical,casesPerOneMillion,deathsPerOneMillion,tests,testsPerOneMillion,Population,activePerOneMillion,recoveredPerOneMillion,criticalPerOneMillion,Date) Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",entities)
    messagebox.showinfo('Success!','Data Saved Succesfully')
    user_db.commit()



    
    
    
    

def history():
    global history_gui,mylist

    def clear_history():
        for i in history_labels:
            i.destroy()
        cursor.execute('DELETE FROM VirusRequestedData')
        user_db.commit()
        mylist.delete(0,END)





    history_gui=Toplevel(main_window)
    history_gui.title('History')
    history_gui.geometry('1100x800')
    history_gui.iconbitmap('coronavirus.ico')
    
    mylist=Listbox(history_gui)
    scrollbar=Scrollbar(mylist)
    scrollbar.pack(side=RIGHT,fill=Y)
    mylist['yscrollcommand']=scrollbar.set


    cursor.execute('SELECT DISTINCT * FROM VirusRequestedData')
    data=cursor.fetchall()
    history_labels=[]
    for row in data:
        display=str(row).strip("()")
        display="     ".join(display.split(','))
        history_LBL=ttk.Label(history_gui,text=display,background='white',width=100)
        history_labels.append(history_LBL)
        mylist.insert(END,history_LBL.cget("text"))
        
    mylist.pack(side=LEFT,fill=BOTH)
    mylist.place(y=25,width=1100,height=800)
    scrollbar.config(command=mylist.yview)

    clearbutton=ttk.Button(history_gui,text='Clear History',command=clear_history,width=180).place(x=5,y=0)
   
    history_gui.mainloop()

def analysepropotion():
            global chartcanvas
            data=get_data(country_name.get())
            critical=(data['critical']/data['cases'])*100
            active=(data['active']/data['cases'])*100
            recoveries=(data['recovered']/data['cases'])*100
            dead=(data['deaths']/data['cases'])*100
            labels='active','critical','recovered','dead'
            sizes=[active,critical,recoveries,dead]
            explode=(0,0,0.1,0)
            fig1,ax1=plt.subplots(figsize=(5,4))
            ax1.pie(sizes,explode=explode,labels=labels,autopct="%1.1f%%",shadow=True,startangle=90)
            ax1.axis('equal')
            ax1.set_title('Requested Pie Chart for '+country_name.get())
            chartcanvas = FigureCanvasTkAgg(fig1,main_window)
            chartcanvas.get_tk_widget().place(x=10,y=280)   

    
def Analyse():
    global analysewindow,analyze_criteria,analyze_box

    button_analyze['state']=DISABLED
    analyze_criteria=StringVar()
    analyze_box=ttk.Combobox(main_window,textvariable=analyze_criteria,values=['Analyse Current Data','Analyse Saved Data',],state='readonly')
    analyze_box.bind('<<ComboboxSelected>>',analyse_methods)
    analyze_box.place(x=720,y=480)



def analyse_methods(method):
    analyze_box['state']=DISABLED
    def fix_gui():
        button_analyze['state']=NORMAL
        analyze_box.destroy()
    
    def Analyseevo():
        global analyseevo_window,fixgui

        def case():
            name=country_name.get()
            cursor.execute('SELECT DISTINCT cases,Date FROM VirusRequestedData WHERE Country=?',(name,))
            fig=plt.figure()
            plt.ylabel('total number of cases',fontsize=16)
            plotevo()
        
        def todayCases():
            name=country_name.get()
            cursor.execute('SELECT DISTINCT todaycases,Date FROM VirusRequestedData WHERE Country=?',(name,))
            fig=plt.figure()
            plt.ylabel('number of cases day by day',fontsize=16)
            plotevo()

        

        def totalrecovered():
            name=country_name.get()
            cursor.execute('SELECT DISTINCT recovered,Date FROM VirusRequestedData WHERE Country=?',(name,))
            fig=plt.figure()
            plt.ylabel('total number of recoveries',fontsize=16)
            plotevo()
            
        def todaydeath():
            name=country_name.get()
            cursor.execute('SELECT DISTINCT todaydeaths,Date FROM VirusRequestedData WHERE Country=?',(name,))
            fig=plt.figure()
            plt.ylabel('number of deaths day by day',fontsize=16)
            plotevo()    

        def totaldeath():
            name=country_name.get()
            cursor.execute('SELECT DISTINCT death,Date FROM VirusRequestedData WHERE Country=?',(name,))
            fig=plt.figure()
            plt.ylabel('total number of deaths',fontsize=16)
            plotevo()
        
        def fixgui():
            analyseevo_window.destroy()
            button_analyze['state']=NORMAL
            analyze_box.destroy()

    

        analyseevo_window=Toplevel(main_window)
        analyseevo_window.geometry('200x200')
        analyseevo_window.title('Analyse Saved Data')
        analyseevo_window.iconbitmap('coronavirus.ico')
        analyseevoFrame=ttk.LabelFrame(analyseevo_window,text='Criteria to Analyse')
        totalcasesB=ttk.Button(analyseevoFrame,text='total cases evolution',command=case)
        todaycasesB=ttk.Button(analyseevoFrame,text='day by day cases evolution',command=todayCases)
        totalrecoveredB=ttk.Button(analyseevoFrame,text='total recovery evolution',command=totalrecovered)
        totalDeathB=ttk.Button(analyseevoFrame,text='total death evolution',command=totaldeath)
        todayDeathB=ttk.Button(analyseevoFrame,text='day by day death evolution',command=todaydeath)
        
        analyseevoFrame.pack()
        totalcasesB.pack()
        todaycasesB.pack()
        totalrecoveredB.pack()
        totalDeathB.pack()
        todayDeathB.pack()
        
        
      
        analyseevo_window.protocol("WM_DELETE_WINDOW",fixgui)


    def Analysecurrent(): #create the analyse interface

        global stat0,stat1,stat2,stat3,stat4,stat5,stat6,stat7,data,analyse_window
        global stat0_check_button,stat1_check_button,stat2_check_button,stat3_check_button,stat4_check_button,stat5_check_button,stat6_check_button,stat7_check_button
        
    
        
        
        data=get_data(country_name.get())
        analyse_window=Toplevel(main_window)
        analyse_window.geometry('300x300')
        analyse_window.iconbitmap('coronavirus.ico')
        analyse_window.title('Analyse Current Data')
        analyseFrame=ttk.Labelframe(analyse_window,text='Criteria to Analyse')
        analyseFrame.pack()

        def fixgui():
            analyse_window.destroy()
            button_analyze['state']=NORMAL
            analyze_box.destroy()
        

        stat0=StringVar()
        stat1=StringVar()
        stat2=StringVar()
        stat3=StringVar()
        stat4=StringVar()
        stat5=StringVar()
        stat6=StringVar()
        stat7=StringVar()



        stat0_check_button=ttk.Checkbutton(analyseFrame,text='total cases',onvalue='cases',variable=stat0,command=createaxis0)
        stat0_check_button.pack()
        stat1_check_button=ttk.Checkbutton(analyseFrame,text='today cases',onvalue='todayCases',variable=stat1,command=createaxis1)
        stat1_check_button.pack()
        stat2_check_button=ttk.Checkbutton(analyseFrame,text='death',onvalue='deaths',variable=stat2,command=createaxis2)
        stat2_check_button.pack()
        stat3_check_button=ttk.Checkbutton(analyseFrame,text='today deaths',onvalue='todayDeaths',variable=stat3,command=createaxis3)
        stat3_check_button.pack()
        stat4_check_button=ttk.Checkbutton(analyseFrame,text='recovered',onvalue='recovered',variable=stat4,command=createaxis4)
        stat4_check_button.pack()
        stat5_check_button=ttk.Checkbutton(analyseFrame,text='active',onvalue='active',variable=stat5,command=createaxis5)
        stat5_check_button.pack()
        stat6_check_button=ttk.Checkbutton(analyseFrame,text='critical',onvalue='critical',variable=stat6,command=createaxis6)
        stat6_check_button.pack()
        stat7_check_button=ttk.Checkbutton(analyseFrame,text='test',onvalue='tests',variable=stat7,command=createaxis7)
        stat7_check_button.pack()

            
        plot_button=ttk.Button(analyse_window,text='Plot',command=plotnormal).pack()
        clearBTN=ttk.Button(analyse_window,text='clear',command=clearaxis).pack()
        analyse_window.protocol("WM_DELETE_WINDOW",fixgui)
    
   
       
        
        


    if analyze_criteria.get()=='Analyse Current Data':
         Analysecurrent()
    
       
    else:
         Analyseevo()
        
    



def answerbot(evt):
        answer['state']=NORMAL
        for i in range(len(questions)):
           temp=question.get()
           if temp==questions[i]:
                answer.delete('1.0','end')
                answer.insert(INSERT,answers[i])
                answer['state']=DISABLED
        



def show_info ():
    global answer,question,questions,answers

    info_window=Toplevel(main_window)
    info_window.geometry('700x600')
    info_window.title('Information and FAQ')
    info_window.iconbitmap('coronavirus.ico')
    questionframe=ttk.LabelFrame(info_window,text='Questions')
    answerframe=ttk.LabelFrame(info_window,text='Answer')

    question=StringVar()
    questions=['What are the symptoms of coronavirus vs the flu?','What should I stock up on in case of an outbreak?','Is coronavirus worse that the flu?','Do masks actually work?','Does the flu vaccine protect against the coronavirus?','Who gets sick from the coronavirus and why?','Can you get the coronavirus from a cat or a dog?','Can you get coronavirus from a package?','Can you get the coronavirus from food?','Given that the virus thrives in cold environments, is it likely to fizzle out as warm weather approaches?','Can you get the coronavirus twice?','Can you get the coronavirus from sex?','Is a comparison to the Spanish Flu relevant in the US, in the developing world, or not at all?',"Will washing my hands help and is it safe to shake someone else's?","Will spraying my body with alcohol or chlorine help? Can hand dryers kill the virus?","Should I rinse my nose with saline and eat garlic?"]
    answers=[
    'Coronavirus may include: fever, hack, brevity of breath. Side effects may show up between 2 to 14 days after introduction. Influenza may include: fever or feeling hot/chills, hack, sore throat, runny or stuffy nose, muscle of body, muscle of body throbs, migraines, weakness, regurgitating or looseness of the bowels, hurts. Flu frequently goes ahead abruptly. Indications for coronavirus and influenza may begin mellow however the two diseases can be lethal.',
    "Store network specialists state there's no compelling reason to reserve past the prescribed 14-day crisis supply of nourishment and necessities. In any case, here are some fundamental supplies to keep at home for any crisis: A gallon of water for each individual every day, in addition to some extra in the event that you have pets. Canned and dry nourishments. Your preferred nourishments like chips or chocolate might be encouraging as well. Cleanser, hand sanitizers, clothing cleanser. Tissue and diapers if necessary. A 30-day supply of solutions and over-the-counter medications you use consistently. It additionally assists with having some amusement like books, cards and tabletop games.",
    "Coronavirus has a higher death rate than influenza. Over 3%' of COVID-19 patients bite the dust versus under 1%' for flu starting at early March. Those numbers will change as coronavirus spreads and more cases are identified. A great many individuals get seasonal influenza every year. Coronavirus is less normal in youngsters as per the CDC. Most contaminations are in grown-ups. Youngsters and seniors are at high hazard for this season's cold virus.",
    "There is no advantage to wearing a veil at this moment, except if you are debilitated yourself and indicating side effects of the infection. The veil itself can get defiled and fill in as a wellspring of disease, really accomplishing more damage than anything else. The CDC additionally doesn't prescribe to the overall population utilizing face covers as a technique for security from coronavirus or other respiratory diseases. You should possibly wear a cover if a medicinal services proficient suggests it. A face veil ought to be utilized by individuals who have COVID-19 and are demonstrating manifestations. This is to shield others from the danger of getting contaminated. Veils are not prescribed for general security in the event that you are not sick. Social insurance experts treating and managing those influenced must wear defensive covers, explicitly N95 clinical respirator covers. On the off chance that you do utilize a cover, discard it after one use. They can't be reused. The CDC likewise says individuals in everybody don't have to wear respirators which are selling out in numerous spots.",
    "'It's an alternate sort of infection,' says Brandon Brown, a disease transmission specialist and partner educator at the University of California. 'Take human papillomavirus for instance. There's a lot of sorts of HPV, and you can get tainted by numerous kinds, so on the off chance that you get one, it's not defensive against others. That is somewhat of a comparative method to consider it with seasonal influenza and coronavirus, on the grounds that they're both so various kinds of infections that it's not expected that since you've had this season's cold virus antibody or you've had influenza, that you'd be secured against the different infection.",
    "The individuals that are getting the most broken down from coronavirus are grown-ups over age 65,' says Brown to Mother Jones. 'This is somewhat not quite the same as seasonal influenza, in light of the fact that this season's flu virus arrives at that populace yet in addition kids younger than 2, likewise pregnant ladies and individuals with constant wellbeing conditions.",
    "A great deal of the infections that we know including a ton of the coronaviruses, started in creatures. It could be bats, pigs, chickens, contingent upon the infection. Be that as it may, there's been no report of any transmission from our local creatures to people right now,' says. CDC doesn't have any proof to propose that creatures or creature items imported from China represent a hazard for spreading COVID-19 in the United States.",
    "'The infection can get by on different surfaces. It will in general live better when it's on colder surfaces. Infections on surfaces could stay irresistible somewhere in the range of two hours to nine days. Since the infection can live on surfaces for a more drawn out timeframe, is to rehearse legitimate hand washing,' says Dr Brown. 'In an office setting, in the event that somebody has contacted a surface and they're unmistakably wiped out, and they're wheezing or hacking, and we contact that surface-it could be a door handle, it could be a work area and afterward we continue to contact our eyes, nose, or mouth, this is another way that the infection can be transmitted. So it's not just about things that individuals are stressed over, however it's about our regular daily existences too. The single direction that we can shield ourselves from that is with legitimate hand washing.",
    "This is a chance if the individual who is setting up the nourishment, shipping the nourishment, or sharing the nourishment is irresistible. As far as the nourishment beginning from a creature that is wiped out and afterward getting another person wiped out who's eating the creature, I don't believe that is as normal, in light of the fact that the infection can endure for two to nine days in the ideal conditions, which is cold conditions, and typically a great deal of the nourishment that we're eating that others are planning is warm nourishment,' Brown recommends. There have been 257 instances of coronavirus determined so far to have 14 passings announced There have been 257 instances of coronavirus determined so far to have 14 passings detailed The CDC notes: 'It might be conceivable that an individual can get COVID-19 by contacting a surface or article that has the infection on it and afterward contacting their own mouth, nose, or perhaps their eyes, yet this isn't believed to be the principle way the infection spreads.",
    "The CDC states: 'It isn't yet realized whether climate and temperature sway the spread of the infection. Some different infections, similar to the basic cold and influenza, spread more during chilly climate months yet that doesn't mean it is difficult to get wiped out with these infections during different months. Right now, it isn't known whether the spread will diminish when climate gets hotter. There is significantly more to find out about the transmissibility, seriousness, and different highlights related with COVID-19 and examinations are progressing.",
    "'We would envision that in the wake of being tainted with the coronavirus, you would be less inclined to be contaminated once more. We could see something like the influenza infection for instance to find out about that. We know so minimal about COVID-19, the novel coronavirus, that we don't know precisely if there's a lot of subtypes, as there are for this season's flu virus, and if it's conceivable to be contaminated by two distinctive subtypes.'",
    "'There is no sign that coronavirus is explicitly transmitted at the same time, on the off chance that we are in close contact with somebody who has side effects of influenza or coronavirus (hacking, wheezing, runny nose, fever, cerebral pain) as we may be during sex, the probability of transmission for non-sexual reasons would be high.'",
    "'No. The Spanish Flu tainted as much as 500 million individuals and slaughtered 50 million individuals. We're seeing the all out passings currently appearing to climb gradually for the coronavirus as more individuals are recuperating, and it's sort of having a tendency to back off. Fifty million individuals on the planet is a great deal. We took in a ton about the Spanish influenza. We took in a ton from H1N1, we took in a great deal from SARS and Ebola, so ideally we've taken in our exercise from all these different flare-ups that have occurred before the coronavirus. We realize that the casualty rate for the present novel coronavirus is around 2 percent, just among the cases that we're seeing. What's more, this may be an overestimation. We additionally realize that the casualty rate for seasonal influenza is .01 percent, or around there. So I would state that, on the off chance that we need to contrast coronavirus with something, we ought to most likely contrast it with this season's flu virus,' says Brown, a disease transmission expert at the University of California, Riverside.",
    "So, yes. WHO says you can murder infections on your hands by washing them altogether and normally with cleanser and water - or with a liquor based hand rub. You ought to wash your hands in any event, when they are not unmistakably filthy and particularly in the wake of hacking or wheezing.",
    "One of the more peculiar - and conceivably risky - legends encompassing the infection is that liquor and chlorine can murder it. In any case, the WHO has cautioned that such advances will have no effect on infections that have just entered your body. Actually, splashing yourself with such substances can harm your mucous films, for example, your eyes and mouth. With respect to hand dryers, there is no proof to recommend they are successful in slaughtering the infection. In any case, warm air dryers - or paper towels - ought to be utilized to dry your hands after you have washed them completely.",
    "While there is some proof that shows consistently flushing your nose with saline can assist you with recouping snappier from the basic cool, the equivalent can't be said for the coronavirus. The WHO said washing your nose has not been appeared to forestall respiratory issues. In the interim, notwithstanding garlic having some antimicrobial properties, there is no proof from the present episode which shows it can shield individuals from the infection."
    ]

    questionbox=ttk.Combobox(questionframe,textvariable=question,values=questions,state='readonly',width=100)
    questionbox.bind('<<ComboboxSelected>>',answerbot)

    answer=Text(answerframe,state=NORMAL,wrap=WORD,width=100,height=70)

    questionframe.pack()
    answerframe.pack()
    questionbox.pack()
    answer.pack()


    info_window.mainloop()












            
######################################   MAIN  ##################################################:


def datapage():#creating the GUI that will display the data requested
    global country_box,country_code,country_name,country_results,main_window,result_frame,clock,date,calendar,button_analyze
    
    
    def close():
        user_db.close()
        main_window.destroy()
    
    main_window=Tk()
    main_window.geometry('900x750')
    main_window.title('Corona Virus Data Tracker')
    main_window.resizable(0,0)
    main_window.iconbitmap('coronavirus.ico')
    canvas=Canvas(main_window,height=900,width=700).pack()
    image=ImageTk.PhotoImage(file=directory+'application background title.jpg')
    background_label=ttk.Label(canvas,image=image)
    background_label.image=image
    background_label.place(x=-1,y=-1,relwidth=1,relheight=1)

    clear_button=ttk.Button(main_window,text='Clear',command=clear,width=15)

    logout_icon = PhotoImage(file = directory+'logout.png')
    logout_button=ttk.Button(main_window,image=logout_icon,command=logout,width=15)

    info_icon= PhotoImage(file=directory+'info.png')
    info_button=ttk.Button(main_window,image=info_icon,command=show_info)

    history_icon= PhotoImage(file=directory+'history.png')
    history_button=ttk.Button(main_window,image=history_icon,command=history,width=15)

    save_button=ttk.Button(main_window,text='Save',command=save,width=15)
    

    country_list=get_country_name_list()
    country_list.sort()
    

    country_code=StringVar()
    country_name=StringVar()
    
    
    
    country_name_LBL=ttk.Label(main_window,text='Country Name',background='white',width=20,anchor=CENTER)
    country_code_LBL=ttk.Label(main_window,text='Country Code',background='white',width=20,anchor=CENTER)
    country__code_Show_LBL=ttk.Label(main_window,background='white',textvariable=country_code)
    


    country_box=ttk.Combobox(main_window,textvariable=country_name,values=country_list,state='readonly')
    country_box.bind('<<ComboboxSelected>>',country_selector)
   
    
   
    clear_button.place(x=730,y=530,width =120)
    logout_button.place(x=750,y=8)
    country_box.place(x=150,y=149,width=160)
    country_name_LBL.place(x=20,y=150)
    country_code_LBL.place(x=20,y=200)
    country__code_Show_LBL.place(x=200,y=200)
    save_button.place(x=580,y=530,width=120)
    history_button.place(x=630,y=8)
    info_button.place(x=570,y=8)



#create a clock and a calendar:
    time=''
    clock=ttk.Label(main_window,background='white')
    clock.place(x=180,y=100)
    tick()

    date=datetime.datetime.now()
    calendar=ttk.Label(main_window,background='white',text=str(date.strftime('%A'))+' '+str(date.strftime('%B'))+' '+str(date.strftime('%d'))+' '+str(date.strftime('%Y')))
    calendar.place(x=20,y=100)

    share_icon=PhotoImage(file=directory+'share.png')
    button_share=ttk.Button(main_window,image=share_icon,command=Share,width=50)
    button_share.place(x=690,y=8)


    button_analyze=ttk.Button(text='Analyse',command=Analyse,width=18)
    button_analyze.place(x=580,y=480)
    
    main_window.protocol("WM_DELETE_WINDOW",close)

    country_name.set('World')
    print_data(get_data(country_name.get()))
    analysepropotion()
    country_box['state']='readonly'


    main_window.mainloop()
    
##############################   Main Program   #################################################################################################################################################
registerAndLogin()