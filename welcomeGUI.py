import tkinter as tk
import pymysql
from tkinter import IntVar
from tkinter import messagebox
import heartdisease

pymysql.install_as_MySQLdb()

tkinter = tk

class App(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.welcome_gui()

    def welcome_gui(self):
        self.grid()
        width=545
        height=350

        # calculate current window screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y)) #positions the window to the center of the screen

        self.label_welcome = tkinter.Label(self.parent, text = "Welcome to Heart Disease Predication System",font="Helvetica 16 bold")
        self.label_welcome.grid(row=0,column=1,sticky="news",ipadx=30,ipady=50)

        self.b1 = tkinter.Button(self.parent,text= "Doctor Login")
        self.b1.grid(row=3,column=1,pady=30)
        self.b1.bind("<Button-1>", self.doctor_window)

        self.b2 = tkinter.Button(self.parent,text= "Patient Login")
        self.b2.grid(row=4,column=1)
        self.b2.bind("<Button-1>", self.patient_window)

    def doctor_window(self, Event):
        self.after(500, self.doctor_login_window)

    def patient_window(self, Event):
        self.after(500, self.patient_login_window)

    def doctor_login_window(self):
        self.withdraw()

        self.login_w = tkinter.Toplevel(self)

        width=545
        height=350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.login_w.geometry('%dx%d+%d+%d' % (width, height, x, y))


        self.label_welcome = tkinter.Label(self.login_w, text="Please Enter your login details",
                                           font="Helvetica 16 bold")
        self.label_welcome.grid(row=0, column=0,columnspan=4,sticky="news",padx=90,pady=50)

        self.label_duser = tkinter.Label(self.login_w,text="Username: ", anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_dpassword=tkinter.Label(self.login_w,text="Password:", anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")

        self.label_duser.grid(row=3,column=1,sticky=tkinter.E+tkinter.W)
        self.label_dpassword.grid(row=4,column=1,sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)

        self.d_user_login=tkinter.Entry(self.login_w)
        self.d_pwd_login=tkinter.Entry(self.login_w,show="*")

        self.d_user_login.grid(row=3,column=2,sticky=tkinter.E+tkinter.W)
        self.d_pwd_login.grid(row=4,column=2,sticky=tkinter.E+tkinter.W)

        self.connectb=tkinter.Button(self.login_w,text="Log in",font="Helvetica 10 bold",command=self.dbconnection_doctor)
        self.cancelb=tkinter.Button(self.login_w,text="Cancel",command=self.login_w.quit,font="Helvetica 10 bold")

        self.connectb.grid(row=5,column=1,sticky=tkinter.E,pady=20)
        self.cancelb.grid(row=5,column=2,pady=20)

        self.registerb = tkinter.Button(self.login_w, text="Register", font="Helvetica 10 bold",command=self.doctor_register_window)
        self.registerb.grid(row=7,column=1,columnspan=2)

    def dbconnection_doctor(self):

        login_dname = self.d_user_login.get()
        login_pwd  = self.d_pwd_login.get()

        sql = "SELECT d_uname,d_pwd from doctor_login WHERE d_uname=%s AND d_pwd=%s"
        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_d = self.conn.cursor()
            self.cursor_d.execute("USE heartdisease")
            self.cursor_d.execute(sql, (login_dname,login_pwd))
            self.cursor_d.execute("select * from doctor_login")
            exists = False

            for row in self.cursor_d:
                if row["d_uname"] == login_dname and row["d_pwd"] == login_pwd:
                    exists = True
                    global docname
                    docname = row["d_uname"]

            if exists:
                self.initialize_dw()
                self.login_w.withdraw()
            else:
                messagebox.showinfo("Info","User doesn't exists, Please Register")

        finally:
            print("")


    def patient_login_window(self):
        self.withdraw()
        self.login_p=tkinter.Toplevel(self)
        width=545
        height=350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.login_p.geometry('%dx%d+%d+%d' % (width, height, x, y))


        self.label_welcome = tkinter.Label(self.login_p, text="Please Enter your login details",
                                           font="Helvetica 16 bold")
        self.label_welcome.grid(row=0, column=0,columnspan=4,sticky="news",padx=90,pady=50)

        self.label_user=tkinter.Label(self.login_p,text="Username: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_password=tkinter.Label(self.login_p,text="Password:", anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")

        self.label_user.grid(row=3,column=1,sticky=tkinter.E+tkinter.W)
        self.label_password.grid(row=4,column=1,sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)

        self.p_user_login=tkinter.Entry(self.login_p)
        self.p_pwd_login=tkinter.Entry(self.login_p,show="*")

        self.p_user_login.grid(row=3,column=2,sticky=tkinter.E+tkinter.W)
        self.p_pwd_login.grid(row=4,column=2,sticky=tkinter.E+tkinter.W)

        self.connectb=tkinter.Button(self.login_p,text="Log in",font="Helvetica 10 bold",command=self.dbconnection_patient)
        self.cancelb=tkinter.Button(self.login_p,text="Cancel",command=self.login_p.quit,font="Helvetica 10 bold")

        self.connectb.grid(row=5,column=1,sticky=tkinter.E,pady=20)
        self.cancelb.grid(row=5,column=2,pady=20)

        self.registerb = tkinter.Button(self.login_p, text="Register", font="Helvetica 10 bold",command=self.patient_register_window)
        self.registerb.grid(row=7,column=1,columnspan=2)

    def dbconnection_patient(self):

        login_pname = self.p_user_login.get()
        login_pwd  = self.p_pwd_login.get()

        sql = "SELECT p_uname,p_pwd from patient_login WHERE p_uname=%s AND p_pwd=%s"
        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_p = self.conn.cursor()
            self.cursor_p.execute("USE heartdisease")
            self.cursor_p.execute(sql, (login_pname,login_pwd))
            self.cursor_p.execute("select * from patient_login")
            exists = False
            for row in self.cursor_p:
                if row["p_uname"] == login_pname and row["p_pwd"] == login_pwd:
                    exists = True
                    global patient_name
                    patient_name = row["p_uname"]

            if exists:
                self.records()
                self.login_p.withdraw()
            else:
                messagebox.showinfo("Info","User doesn't exists, Please Register")
                self.conn.close()
        except pymysql.DatabaseError as e:
            messagebox.showwarning("Error",e)

    def doctor_register_window(self):
        self.login_w.withdraw()
        self.register_d=tkinter.Toplevel(self)
        width=545
        height=350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.register_d.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.label_welcome = tkinter.Label(self.register_d, text="Enter your details to Register",
                                           font="Helvetica 16 bold")
        self.label_welcome.grid(row=0, column=0,columnspan=4,sticky="news",padx=90,pady=50)

        self.label_user=tkinter.Label(self.register_d,text="Username: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_password=tkinter.Label(self.register_d,text="Password:", anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_phno=tkinter.Label(self.register_d,text="Phone No: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_email=tkinter.Label(self.register_d,text="E-Mail ID: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")

        self.label_user.grid(row=3,column=1,sticky=tkinter.E+tkinter.W)
        self.label_password.grid(row=4,column=1,sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
        self.label_phno.grid(row=5,column=1,sticky=tkinter.E+tkinter.W)
        self.label_email.grid(row=6,column=1,sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)

        self.dbuser_d=tkinter.Entry(self.register_d)
        self.dbpassword_d=tkinter.Entry(self.register_d,show="*")
        self.dbphno_d=tkinter.Entry(self.register_d)
        self.dbemail_d=tkinter.Entry(self.register_d)


        self.dbuser_d.grid(row=3,column=2,sticky=tkinter.E+tkinter.W)
        self.dbpassword_d.grid(row=4,column=2,sticky=tkinter.E+tkinter.W)
        self.dbphno_d.grid(row=5,column=2,sticky=tkinter.E+tkinter.W)
        self.dbemail_d.grid(row=6,column=2,sticky=tkinter.E+tkinter.W)


        self.connectb=tkinter.Button(self.register_d,text="Submit",font="Helvetica 10 bold",command=self.insert_doctor)
        self.cancelb=tkinter.Button(self.register_d,text="Reset",font="Helvetica 10 bold",command=self.clear_register_field_d)

        self.connectb.grid(row=7,column=1,sticky=tkinter.E,pady=20)
        self.cancelb.grid(row=7,column=2,pady=20)

        self.login_back = tkinter.Button(self.register_d, text="Login Here", font="Helvetica 10 bold",command=self.login_back_d)
        self.login_back.grid(row=8,column=1,columnspan=2)

    def login_back_d(self):
        self.register_d.withdraw()
        self.doctor_login_window()

    def clear_register_field_d(self):
        self.dbuser_d.delete(0, 'end')
        self.dbpassword_d.delete(0, 'end')
        self.dbphno_d.delete(0, 'end')
        self.dbemail_d.delete(0, 'end')

    def insert_doctor(self):
        uname = self.dbuser_d.get()
        pwd  = self.dbpassword_d.get()
        phno = self.dbphno_d.get()
        email = self.dbemail_d.get()

        sql_uname = "SELECT d_uname from doctor_login"

        sql = "INSERT INTO doctor_login(d_uname,d_pwd,d_phno,d_email) VALUES(%s,%s,%s,%s)"
        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_d = self.conn.cursor()
            self.cursor_d.execute("USE heartdisease")
            self.cursor_d.execute(sql_uname)
            exists = False
            for row in self.cursor_d:
                if row["d_uname"] == uname:
                    exists = True

            if exists:
                messagebox.showwarning("Warnikng!", "Please choose different username")
            else:
                self.cursor_d.execute(sql,(uname , pwd , phno , email))
                self.conn.commit()
                messagebox.showinfo("Info","Registration Successful,Pleases Login to Continue")

        except pymysql.Error:
            messagebox.showerror("Error","Registration error")

        finally:
            self.conn.close()
            print("db closed")

    def patient_register_window(self):
        self.login_p.withdraw()
        self.register_p=tkinter.Toplevel(self)
        width=545
        height=350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.register_p.geometry('%dx%d+%d+%d' % (width, height, x, y))


        self.label_welcome = tkinter.Label(self.register_p, text="Enter your details to Register",
                                           font="Helvetica 16 bold")
        self.label_welcome.grid(row=0, column=0,columnspan=4,sticky="news",padx=90,pady=50)

        self.label_user=tkinter.Label(self.register_p,text="Username: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_password=tkinter.Label(self.register_p,text="Password:", anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_phno=tkinter.Label(self.register_p,text="Phone No: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.label_email=tkinter.Label(self.register_p,text="E-Mail ID: ",anchor=tkinter.W,background="dark slate gray",foreground="white", font="Helvetica 8  bold")


        self.label_user.grid(row=3,column=1,sticky=tkinter.E+tkinter.W)
        self.label_password.grid(row=4,column=1,sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
        self.label_phno.grid(row=5,column=1,sticky=tkinter.E+tkinter.W)
        self.label_email.grid(row=6,column=1,sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)

        self.dbuser_p=tkinter.Entry(self.register_p)
        self.dbpassword_p=tkinter.Entry(self.register_p,show="*")
        self.dbphno_p=tkinter.Entry(self.register_p)
        self.dbemail_p=tkinter.Entry(self.register_p)

        self.dbuser_p.grid(row=3,column=2,sticky=tkinter.E+tkinter.W)
        self.dbpassword_p.grid(row=4,column=2,sticky=tkinter.E+tkinter.W)
        self.dbphno_p.grid(row=5,column=2,sticky=tkinter.E+tkinter.W)
        self.dbemail_p.grid(row=6,column=2,sticky=tkinter.E+tkinter.W)

        self.connectb_p=tkinter.Button(self.register_p,text="Submit",font="Helvetica 10 bold",command=self.insert_patient)
        self.cancelb_p=tkinter.Button(self.register_p,text="Reset",font="Helvetica 10 bold",command=self.clear_register_field_p)

        self.connectb_p.grid(row=7,column=1,sticky=tkinter.E,pady=20)
        self.cancelb_p.grid(row=7,column=2,pady=20)

        self.login_back = tkinter.Button(self.register_p, text="Login Here", font="Helvetica 10 bold",command=self.login_back_p)
        self.login_back.grid(row=8,column=1,columnspan=2)

    def login_back_p(self):
        self.register_p.withdraw()
        self.patient_login_window()

    def clear_register_field_p(self):
        self.dbuser_p.delete(0, 'end')
        self.dbpassword_p.delete(0, 'end')
        self.dbphno_p.delete(0, 'end')
        self.dbemail_p.delete(0, 'end')

    def insert_patient(self):
        uname = self.dbuser_p.get()
        pwd  = self.dbpassword_p.get()
        phno = self.dbphno_p.get()
        email = self.dbemail_p.get()

        sql_uname = "SELECT p_uname from patient_login"

        sql = "INSERT INTO patient_login(p_uname,p_pwd,p_phno,p_email) VALUES(%s,%s,%s,%s)"
        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_p = self.conn.cursor()
            self.cursor_p.execute("USE heartdisease")
            self.cursor_p.execute(sql_uname)
            exists = False
            for row in self.cursor_p:
                if row["p_uname"] == uname:
                    exists = True

            if exists:
                messagebox.showwarning("Warning!", "Please choose different username")
            else:
                self.cursor_p.execute(sql,(uname , pwd , phno , email))
                self.conn.commit()
                messagebox.showinfo("Info","Registration Successful,Pleases Login to Continue")

        except pymysql.Error:
            messagebox.showerror("Error","Registration error")

        finally:
            self.conn.close()
            print("db closed")


    def initialize_dw(self):
        self.withdraw()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.center_window(screen_w, screen_h)
        self.dw.grid()

        self.label_space1 = tk.Label(self.dw,text="                  ")
        self.label_space1.grid(row=0,column=0,rowspan=12,columnspan = 6,sticky="news",ipadx=45,padx=12)

        self.label_head = tk.Label(self.dw,text = 'Heart Disease Prediction System',font="helvetica 20 bold")
        self.label_head.grid(row=0,column=4,columnspan=10,sticky="news",ipady=25)

        self.img = tk.PhotoImage(file="bg.png")
        self.img = self.img.zoom(8)
        self.img = self.img.subsample(15)

        self.label_image = tk.Label(self.dw,image=self.img)
        self.label_image.image= self.img
        self.label_image.grid(row=1, column=8,ipady=5,pady=10)

        self.label_head = self.create_label("Patient Name :")
        self.label_head.grid(row=3,column=6,sticky="w",ipadx=30,pady=12)
        self.entry_pname = self.create_entry(20)
        self.entry_pname.grid(row=3, column=7)

        self.label_age = self.create_label("Age :")
        self.label_age.grid(row=4,column=6,sticky="w",ipadx=30,pady=12)
        self.entry_age = self.create_entry(20)
        self.entry_age.grid(row=4, column=7)

        self.label_sex = self.create_label("Sex:")
        self.label_sex.grid(row=5,column=6,sticky="w",ipadx=30,pady=12)
        OPTIONS = ["Male","Female"]

        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.sex_option= "Male"

        self.option_sex = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_sex)
        print(self.option_sex.getvar)
        self.option_sex.grid(row=5, column=7,ipadx=30)

        self.label_cp = self.create_label("Chest pain:")
        self.label_cp.grid(row=6,column=6,sticky="w",ipadx=30,pady=12)
        OPTIONS = [
            "Typical angina",
            "atypical angina",
            "Non-angina pain",
            "Asymptomatic"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.cp_option = "Typical angina"
        self.option_cp = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_cp)
        self.option_cp.config(width = 15)
        self.option_cp.grid(row=6, column=7)

        self.label_bp = self.create_label("Resting blood pressure \n (in mm Hg)")
        self.label_bp.grid(row=7,column=6,sticky="w",ipadx=30,pady=12)
        self.entry_bp = self.create_entry(20)
        self.entry_bp.grid(row=7, column=7)

        self.label_chol = self.create_label("cholesterol(mg/dl):")
        self.label_chol.grid(row=8,column=6,sticky="w",ipadx=30,pady=12)
        self.entry_chol = self.create_entry(20)
        self.entry_chol.grid(row=8, column=7)

        self.label_fbs = self.create_label("Fasting blood sugar\n(fbs>120 mg/dl):")
        self.label_fbs.grid(row=9,column=6,sticky="w",ipadx=30,pady=12)
        OPTIONS = [
            "True",
            "False"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.fsb_option="True"
        self.option_fbs = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_fsb)
        self.option_fbs.config(width = 15)
        self.option_fbs.grid(row=9, column=7)

        self.label_ecg = self.create_label("Resting ECG:")
        self.label_ecg.grid(row=3,column=9,sticky="w",ipadx=30)
        OPTIONS = [
            "Normal",
            "ST-T wave abnormality",
            "Left ventricular hypertrophy"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.ecg_option = "Normal"
        self.option_ecg = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_ecg)
        self.option_ecg.config(width = 15)
        self.option_ecg.grid(row=3, column=10)

        self.label_thalach = self.create_label("Maximum heart rate achieved:")
        self.label_thalach.grid(row=4,column=9,sticky="w",ipadx=30)
        self.entry_thalach = self.create_entry(20)
        self.entry_thalach.grid(row=4, column=10)

        self.label_exang = self.create_label("Exercise induced angina/n (yes/No):")
        self.label_exang.grid(row=5,column=9,sticky="w",ipadx=30)
        OPTIONS = [
            "Yes",
            "No"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.exang_option = "Yes"
        self.option_exang = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_exang)
        self.option_exang.config(width=15)
        self.option_exang.grid(row=5, column=10)

        self.label_oldpeak = self.create_label("ST depression(oldpeak):")
        self.label_oldpeak.grid(row=6,column=9,sticky="w",ipadx=30)
        self.entry_oldpeak = self.create_entry(20)
        self.entry_oldpeak.grid(row=6, column=10)

        self.label_slope = self.create_label("Slope of ST segment:")
        self.label_slope.grid(row=7,column=9,sticky="w",ipadx=30)
        OPTIONS = [
            "unsloping",
            "flat",
            "Down sloping"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.slope_option = "unsloping"
        self.option_slope = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_slope)
        self.option_slope.config(width=15)
        self.option_slope.grid(row=7, column=10)

        self.label_ca = self.create_label("CA \n (0-3) colored by flourosopy")
        self.label_ca.grid(row=8,column=9,sticky="w",ipadx=30)
        OPTIONS = [
            "0",
            "1",
            "2",
            "3"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.ca_option = "0"
        self.option_ca = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_ca)
        self.option_ca.config(width=15)
        self.option_ca.grid(row=8, column=10)

        self.label_thal = self.create_label("thal:")
        self.label_thal.grid(row=9,column=9,sticky="w",ipadx=30)
        OPTIONS = [
            "Normal",
            "Fixed defect",
            "Reversible defect"
        ]
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.thal_option = "Normal"
        self.option_thal = tk.OptionMenu(self.dw, self.variable, *OPTIONS,command=self.getOption_thal)
        self.option_thal.config(width=15)
        self.option_thal.grid(row=9, column=10)

        self.b1 = tk.Button(self.dw,text='Submit',command=self.insert_patient_attributes)
        self.b1.grid(row=10,column=8)

        self.b2 = tk.Button(self.dw,text='Cancel',command=self.dw.quit)
        self.b2.grid(row=10,column=9)

    def center_window(self,width, height):
        # get screen width and height
        self.dw = tk.Toplevel(self)
        screen_width = self.dw.winfo_screenwidth()
        screen_height = self.dw.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.dw.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def getOption_sex(self,value):
        self.sex_option = value
    def getOption_cp(self,value):
        self.cp_option = value
    def getOption_fsb(self,value):
        self.fsb_option = value
    def getOption_ecg(self,value):
        self.ecg_option = value
    def getOption_exang(self,value):
        self.exang_option = value
    def getOption_slope(self,value):
        self.slope_option = value
    def getOption_ca(self,value):
        self.ca_option = value
    def getOption_thal(self,value):
        self.thal_option = value


    def insert_patient_attributes(self):
        uname = self.entry_pname.get()
        age = self.entry_age.get()
        sex = self.sex_option
        cp = self.cp_option
        bp = self.entry_bp.get()
        chol = self.entry_chol.get()
        fsb = self.fsb_option
        ecg = self.ecg_option
        thalach = self.entry_thalach.get()
        exang = self.exang_option
        oldpeak = self.entry_oldpeak.get()
        slope = self.slope_option
        ca = self.ca_option
        thal = self.thal_option
        dname = docname

        sql = "INSERT INTO patient_attribute(p_uname,p_age,p_sex,p_cp,p_bp,p_chol,p_fsb,p_ecg,p_thalach,p_exang,p_oldpeak,p_slope,p_ca,p_thal,p_docname) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_pa = self.conn.cursor()
            self.cursor_pa.execute("USE heartdisease")
            self.cursor_pa.execute(sql,
                                   (uname, age, sex, cp, bp, chol, fsb, ecg, thalach, exang, oldpeak, slope, ca, thal,dname))
            f = open('u', 'w')
            f.write(uname)
            f.close()
            self.conn.commit()

            heartdisease.main()

            global patient_name_d
            patient_name_d = self.entry_pname.get()
            self.records_d()
        except pymysql.DatabaseError as e:
            messagebox.showerror("Error", e)


    def records(self):
        self.login_p.withdraw()
        self.rec_window = tk.Toplevel(self)
        width=835
        height=365
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.rec_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.rec_window.resizable(width=False,height=False)
        self.r_label_head = tk.Label(self.rec_window, text="Diagnosis Details", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_label_head.grid(row=0,column=0,columnspan=2, sticky='ew')
        self.records_w = tk.Frame(self.rec_window,relief='groove',bd=5,colormap="new")
        self.records_w.grid(padx=250)
        self.r_labels_uname = tk.Label(self.records_w, text="Patient Name", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_uname.grid(row=0,column=0, sticky='ew')

        self.r_labels_age = tk.Label(self.records_w, text="Age",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_age.grid(row=1,column=0,sticky='ew')

        self.r_labels_gender = tk.Label(self.records_w, text="Gender", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_gender.grid(row=2,column=0,sticky='ew')

        self.r_labels_cp = tk.Label(self.records_w, text="Chest Pain", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_cp.grid(row=3,column=0,sticky='ew')

        self.r_labels_bp = tk.Label(self.records_w, text="Blood Pressure", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_bp.grid(row=4,column=0,sticky='ew')

        self.r_labels_chol = tk.Label(self.records_w, text="Cholesterol (mg/dl", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_chol.grid(row=5,column=0,sticky='ew')

        self.r_labels_fbs = tk.Label(self.records_w, text="Fasting blood sugar(fbs>120 mg/dl)", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_fbs.grid(row=6,column=0,sticky='ew')

        self.r_labels_ecg = tk.Label(self.records_w, text="Resting ECG",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_ecg.grid(row=7,column=0,sticky='ew')

        self.r_labels_rate = tk.Label(self.records_w, text="Max heart rate",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_rate.grid(row=8,column=0,sticky='ew')

        self.r_labels_ex = tk.Label(self.records_w, text="Exercise induced angina",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_ex.grid(row=9,column=0,sticky='ew')

        self.r_labels_st = tk.Label(self.records_w, text="ST depression", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_st.grid(row=10,column=0,sticky='ew')

        self.r_labels_slope = tk.Label(self.records_w, text="Slope", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_slope.grid(row=11,column=0,sticky='ew')

        self.r_labels_ca = tk.Label(self.records_w, text="CA",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_ca.grid(row=12,column=0,sticky='ew')

        self.r_labels_thal = tk.Label(self.records_w, text="thal", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_thal.grid(row=13,column=0,sticky='ew')

        self.r_labels_res = tk.Label(self.records_w, text="Result",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_res.grid(row=14,column=0,sticky='ew')

        self.r_labels_docname = tk.Label(self.records_w, text="Doctor Name", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_docname.grid(row=15,column=0,sticky='ew')

        self.showallrecords()

    def showallrecords(self):
        data ,dat = self.readfromdatabase()

        for index, dat in enumerate(data):
            tk.Label(self.records_w, text=dat['p_uname']).grid(column=index+1, row=0,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_age']).grid(column=index+1, row=1,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_sex']).grid(column=index+1, row=2,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_cp']).grid(column=index+1, row=3,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_bp']).grid(column=index+1, row=4,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_chol']).grid(column=index + 1, row=5,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_fsb']).grid(column=index + 1, row=6,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_ecg']).grid(column=index + 1, row=7,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_thalach']).grid(column=index + 1, row=8,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_exang']).grid(column=index + 1, row=9,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_oldpeak']).grid(column=index + 1, row=10,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_slope']).grid(column=index + 1, row=11,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_ca']).grid(column=index + 1, row=12,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_thal']).grid(column=index + 1, row=13,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_result']).grid(column=index + 1, row=14,sticky='ew',padx=20)
            tk.Label(self.records_w, text=dat['p_docname']).grid(column=index + 1, row=15,sticky='ew',padx=20)


    def readfromdatabase(self):
        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_rec = self.conn.cursor()
            self.cursor_rec.execute("USE heartdisease")
            self.cursor_rec.execute("select * from patient_attribute where p_uname=%s",patient_name)
            names = [description[0] for description in self.cursor_rec.description]
            return self.cursor_rec.fetchall() , names

        except pymysql.DatabaseError as e:
            messagebox.showerror("Error", e)

        finally:
            self.conn.close()
            print("db closed")

    def records_d(self):
        self.dw.withdraw()
        self.rec_window_d = tk.Toplevel(self)
        width=835
        height=379
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.rec_window_d.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.rec_window_d.resizable(width=False,height=False)
        self.r_label_head = tk.Label(self.rec_window_d, text="Diagnosis Details", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_label_head.grid(row=0,column=0,columnspan=2, sticky='ew')
        self.rec_doc_frame = tk.Frame(self.rec_window_d,relief='groove',bd=5,colormap="new")
        self.rec_doc_frame.grid(padx=250)
        self.r_labels_uname = tk.Label(self.rec_doc_frame, text="Patient Name", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_uname.grid(row=0,column=0, sticky='ew')

        self.r_labels_age = tk.Label(self.rec_doc_frame, text="Age",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_age.grid(row=1,column=0,sticky='ew')

        self.r_labels_gender = tk.Label(self.rec_doc_frame, text="Gender", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_gender.grid(row=2,column=0,sticky='ew')

        self.r_labels_cp = tk.Label(self.rec_doc_frame, text="Chest Pain", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_cp.grid(row=3,column=0,sticky='ew')

        self.r_labels_bp = tk.Label(self.rec_doc_frame, text="Blood Pressure", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_bp.grid(row=4,column=0,sticky='ew')

        self.r_labels_chol = tk.Label(self.rec_doc_frame, text="Cholesterol (mg/dl", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_chol.grid(row=5,column=0,sticky='ew')

        self.r_labels_fbs = tk.Label(self.rec_doc_frame, text="Fasting blood sugar(fbs>120 mg/dl)", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_fbs.grid(row=6,column=0,sticky='ew')

        self.r_labels_ecg = tk.Label(self.rec_doc_frame, text="Resting ECG",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_ecg.grid(row=7,column=0,sticky='ew')

        self.r_labels_rate = tk.Label(self.rec_doc_frame, text="Max heart rate",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_rate.grid(row=8,column=0,sticky='ew')

        self.r_labels_ex = tk.Label(self.rec_doc_frame, text="Exercise induced angina",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_ex.grid(row=9,column=0,sticky='ew')

        self.r_labels_st = tk.Label(self.rec_doc_frame, text="ST depression", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_st.grid(row=10,column=0,sticky='ew')

        self.r_labels_slope = tk.Label(self.rec_doc_frame, text="Slope", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_slope.grid(row=11,column=0,sticky='ew')

        self.r_labels_ca = tk.Label(self.rec_doc_frame, text="CA",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_ca.grid(row=12,column=0,sticky='ew')

        self.r_labels_thal = tk.Label(self.rec_doc_frame, text="thal", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_thal.grid(row=13,column=0,sticky='ew')

        self.r_labels_res = tk.Label(self.rec_doc_frame, text="Result",background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_res.grid(row=14,column=0,sticky='ew')

        self.r_labels_docname = tk.Label(self.rec_doc_frame, text="Support Vector Machine (Accuracy)", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_docname.grid(row=15,column=0,sticky='ew')

        self.r_labels_docname = tk.Label(self.rec_doc_frame, text="Random Forest (Accuracy)", background="dark slate gray",foreground="white", font="Helvetica 8  bold")
        self.r_labels_docname.grid(row=16,column=0,sticky='ew')

        self.showallrecords_d()

    def showallrecords_d(self):
        data ,dat = self.readfromdatabase_d()

        for index, dat in enumerate(data):
            tk.Label(self.rec_doc_frame, text=dat['p_uname']).grid(column=index+1, row=0,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_age']).grid(column=index+1, row=1,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_sex']).grid(column=index+1, row=2,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_cp']).grid(column=index+1, row=3,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_bp']).grid(column=index+1, row=4,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_chol']).grid(column=index + 1, row=5,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_fsb']).grid(column=index + 1, row=6,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_ecg']).grid(column=index + 1, row=7,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_thalach']).grid(column=index + 1, row=8,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_exang']).grid(column=index + 1, row=9,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_oldpeak']).grid(column=index + 1, row=10,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_slope']).grid(column=index + 1, row=11,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_ca']).grid(column=index + 1, row=12,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_thal']).grid(column=index + 1, row=13,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_result']).grid(column=index + 1, row=14,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_svm']).grid(column=index + 1, row=15,sticky='ew',padx=20)
            tk.Label(self.rec_doc_frame, text=dat['p_rf']).grid(column=index + 1, row=16,sticky='ew',padx=20)


    def readfromdatabase_d(self):
        try:
            self.conn = self.getConnection()  # connect to db and returns cursor
            self.cursor_rec = self.conn.cursor()
            self.cursor_rec.execute("USE heartdisease")
            self.cursor_rec.execute("select * from patient_attribute where p_uname=%s",patient_name_d)
            names = [description[0] for description in self.cursor_rec.description]
            return self.cursor_rec.fetchall() , names

        except pymysql.DatabaseError as e:
            messagebox.showerror("Error", e)

        finally:
            self.conn.close()


    def getUsername(self):
        with open('u', 'w') as the_file:
            the_file.write(self.entry_pname.get())

    def create_label(self,txt):
        return tk.Label(self.dw,text = txt,font="helvetica 12 bold")

    def create_entry(self,width):
        return tk.Entry(self.dw,width=width)


    def getConnection(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='root',
                                     db='heartdisease',
                                     cursorclass=pymysql.cursors.DictCursor) # A cursor which returns results as a dictionary
            print("connection to Database ok")
            return self.conn

        except pymysql.Error:
            messagebox.showerror("Error","Connection to database Error")



if __name__ == "__main__":
    app = App(None)
    app.title('Heart Disease Prediction System')
    app.mainloop()





