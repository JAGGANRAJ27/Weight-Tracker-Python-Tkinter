from tkinter import *
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

def graph_data():
    conn=sqlite3.connect("weightapp.db")
    j=conn.cursor()
    j.execute('SELECT weight,date FROM weightmeasure')
    x=[]
    y=[]
    for row in j.fetchall(): 
        x.append(row[0])
        y.append(row[1])
        plt.plot(x, y)
        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title('Graph based on your Input')
        plt.show() 

def connect():
    conn=sqlite3.connect("sample.db")
    j=conn.cursor()
    j.execute("CREATE TABLE IF NOT EXISTS users(name TEXT,username TEXT,password TEXT)")
    conn.commit()
    conn.close()
connect()

def viewallusers():
    conn=sqlite3.connect("sample.db")
    j=conn.cursor()
    j.execute("SELECT * FROM users")
    rows=j.fetchall()
    conn.commit()
    conn.close()   
    return rows

def adduser(name,username,password):
    conn=sqlite3.connect("sample.db")
    j=conn.cursor()
    j.execute("INSERT INTO users VALUES(?,?,?)",(name,username,password))
    conn.commit()
    conn.close()

def deleteallusers():
    conn=sqlite3.connect("sample.db")
    j=conn.cursor()
    j.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    messagebox.showinfo('Successful', 'All users deleted')

def checkuser(username,password):
    conn=sqlite3.connect("sample.db")
    j=conn.cursor()
    j.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=j.fetchone()
    return result

def getusername(username,password):
    conn=sqlite3.connect("sample.db")
    j=conn.cursor()
    j.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=j.fetchone()
    global profilename
    if result!=None:
        profilename=result[0]

def viewwindow():
    mainpg = Toplevel(root)
    mainpg.title("VIEW ALL USERS")
    mainpg.geometry("800x700")
    Message(mainpg,font=("Arial", 22, "bold"),text = "NAME      USERNAME      PASSWORD",width=700).pack()
    for row in viewallusers():
        a=row[0]
        b=row[1]
        c=row[2]
        d = a + "         " + b + "           " + c
        Message(mainpg,fg='#6680ff',font=("Arial", 25, "bold"),text = d,width=700).pack()
    Button(mainpg,text="Exit Window",font=("Arial",15,"bold"),width=10,command=mainpg.destroy).pack()
    
def register():
    a = register_name.get()
    b = register_username.get()
    c = register_password.get()
    d = register_repassword.get()
    if c==d and c!="" and len(c)>5 and a!="" and b!="":
        adduser(a,b,c)
        messagebox.showinfo('Success', 'Registration Successful')      
    else :
        if(a=="" or b=="" or c=="" or d==""):
            messagebox.showinfo('Error', 'Some Fields are Empty')
        else:
            messagebox.showinfo('Error', 'Both passwords should be same! \nPassword should contain atleast 8 characters')
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)

def login():
    a = login_username.get()
    b = login_password.get()
    getusername(a,b)   
    if (checkuser(a,b))!=None:
        root.destroy()
        appwindow()     
    else:
        e1.delete(0,END)
        e2.delete(0,END)
        messagebox.showinfo('Please Register', 'Invalid Username or Password')

profilename=""
t = 11
def appwindow():

    def connect1():
        conn=sqlite3.connect("weightapp.db")
        j=conn.cursor()
        j.execute("CREATE TABLE IF NOT EXISTS weightmeasure(id INTEGER PRIMARY KEY,weight TEXT,date DATE,sample TEXT)")
        conn.commit()
        conn.close()
    connect1()

    def insert(weight,date,sample):
        conn=sqlite3.connect("weightapp.db")
        j=conn.cursor()
        j.execute("INSERT INTO weightmeasure VALUES(NULL,?,?,?)",(weight,date,sample))
        conn.commit()
        conn.close()

    def view():
        conn=sqlite3.connect("weightapp.db")
        j=conn.cursor()
        j.execute("SELECT * FROM weightmeasure")
        rows=j.fetchall()
        conn.commit()
        conn.close()
        return rows

    def deletealldata():
        conn=sqlite3.connect("weightapp.db")
        j=conn.cursor()
        j.execute("DELETE FROM weightmeasure")
        conn.commit()
        conn.close()
        list1.delete(0,END)
        messagebox.showinfo('Successful', 'All data deleted')
    
    def insertitems():
        a=Weightval.get()
        b=dateent.get()
        c=reference1.get()
        d=c.replace('.', '', 1)
        e=b.count('-')      

        if a=="" or b=="":
            messagebox.showinfo("Error","Some Fields are empty")
        elif len(b)!=10 or e!=2:
            messagebox.showinfo("Error","DATE should be in format dd-mm-yyyy")
        else:
            insert(a,b,c)
            e1.delete(0,END)
            e2.delete(0,END)
        list1.delete(0,END)

    def viewallitems():
        list1.delete(0,END)
        list1.insert(END,"SI.No     Weight    Date")
        for row in view():
            a=str(row[0])
            b=str(row[1])
            c=str(row[2])
            f= a + "        " + b + "       " + c + "" 
            list1.insert(END,f)
    
    mainpg = Tk()
    mainpg.title("Weight tracker")
    mainpg.geometry("900x700")
    mainpg.config(bg="lightblue")
    kg=Label(mainpg,font=("Arial",17),text="Enter Your Weight",bg="lightblue").place(x=10,y=150)
    Weightval=StringVar()
    e1=Entry(mainpg,font=("Arial",15),textvariable=Weightval)
    e1.place(x=220,y=155,height=27,width=165)
    date=Label(mainpg,font=("Arial",17),text="Date(dd-mm-yyyy)",bg="lightblue").place(x=10,y=200)
    dateent=StringVar()
    e2=Entry(mainpg,font=("Arial",15),textvariable=dateent)
    e2.place(x=220,y=205,height=27,width=165)
    reference1=StringVar()

    scroll_bar=Scrollbar(mainpg)
    scroll_bar.place(x=651,y=410,height=277,width=20)  
    list1=Listbox(mainpg,height=7,width=30,font=("Arial",20),yscrollcommand = scroll_bar.set)
    list1.place(x=168,y=410)
    scroll_bar.config( command = list1.yview )
    Add=Button(mainpg,text="Add Item",font=("Arial",17),bg="cyan",width=10,command=insertitems).place(x=110,y=300)
    View=Button(mainpg,text="View all Entries",font=("Arial",17),bg="cyan",width=12,command=viewallitems).place(x=110,y=355)
    Delete=Button(mainpg,text="Delete all Entries",font=("Arial",17),bg="cyan",width=15,command=deletealldata).place(x=550,y=280)
    Delete=Button(mainpg,text="Show Graph",font=("Arial",17),bg="cyan",width=15,command=graph_data).place(x=550,y=335)
    hd=Label(mainpg,width=60,font=("Arial",35),text="Weight Tracker",bg="yellow").place(x=-350,y=0)
    name = "Welcome, " + "'"+profilename+"'"
    greet=Label(mainpg,width=60,font=("Arial",30),text=name,bg="salmon").place(x=-250,y=60)
    mainpg.resizable(False, False)
    mainpg.mainloop()
   
root = Tk()
root.title("Want To Track Your Weight Regularly?Login (or) Register")
root.geometry("1000x700")
root.config(bg="lightblue")
l1=Label(root,font=("Arial",19),text="Username",bg="lightblue").place(x=80,y=230)
l2=Label(root,font=("Arial",19),text="Password",bg="lightblue").place(x=80,y=280)
b1=Button(root,text="Login",bg="cyan",font=("Arial",19),width=12,command=login).place(x=110,y=360)
l6=Label(root,font=("Arial",19),text="Name",bg="lightblue").place(x=653,y=195)
l3=Label(root,font=("Arial",19),text="Username",bg="lightblue").place(x=604,y=243)
l4=Label(root,font=("Arial",19),text="Password",bg="lightblue").place(x=610,y=293)
l5=Label(root,font=("Arial",17),text="Confirm password",bg="lightblue").place(x=532,y=342)
b2=Button(root,bg="cyan",text="Register",font=("Arial",19),width=12,command=register).place(x=630,y=400)
login_username=StringVar()
e1=Entry(root,font=("Arial",15),textvariable=login_username)
e1.place(x=205,y=238,height=25,width=165)
login_password=StringVar()
e2=Entry(root,font=("Arial",15),textvariable=login_password,show="*")
e2.place(x=205,y=287,height=25,width=165)
register_name=StringVar()
e6=Entry(root,font=("Arial",15),textvariable=register_name)
e6.place(x=740,y=200,height=25,width=165)
register_username=StringVar()
e3=Entry(root,font=("Arial",15),textvariable=register_username)
e3.place(x=740,y=250,height=25,width=165)
register_password=StringVar()
e4=Entry(root,font=("Arial",15),textvariable=register_password, show="*")
e4.place(x=740,y=300,height=25,width=165)
register_repassword=StringVar()
e5=Entry(root,font=("Arial",15),textvariable=register_repassword, show="*")
e5.place(x=740,y=350,height=25,width=165)
Label(root,width=60,font=("Arial",35),text="Weight Tracker",bg="yellow").place(x=-295,y=0)
b3=Button(root,text="Exit Window",font=("Arial",15,"bold"),bg="red",width=10,command=root.destroy).place(x=410,y=580)
b4=Button(root,text="Delete all users",font=("Arial",15,"bold"),width=12,command=deleteallusers).place(x=130,y=520)
b5=Button(root,text="View all users",font=("Arial",15,"bold"),width=12,command=viewwindow).place(x=130,y=480)
root.resizable(False, False)
root.mainloop()
