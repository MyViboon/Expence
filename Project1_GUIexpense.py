from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import date, datetime
################# DATABASE ################################
import sqlite3

# สร้าง database
conn = sqlite3.connect('expense.sqlite3')
# สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้ได้เลย)
c = conn.cursor()

# สร้าง table ด้วยภาษาSQL

'''
'รหัส(transectionid)TEXT',
'วันที่-เวลา(datetime)TEXT',
'รายการ(title)TEXT',
'ค่าใช้จ่าย(expense)RAEL(Float)',
'จำนวน(quantity)INTRGER',
'รวม(total)REAL'
'''

c.execute("""CREATE TABLE IF NOT EXISTS expenselist(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                transectionid TEXT,
                datetime TEXT,
                title TEXT,
                expense INTEGER,
                quantity INTEGER,
                total REAL
            )""")

def insert_expense(transectionid,datetime,title,expense,quantity,total):
    ID = None
    with conn:
        c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
            (ID,transectionid,datetime,title,expense,quantity,total))
    conn.commit()# การบันทึกข้อมูลลงฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก
    print('INSERT suscessss!!!')

def show_expense():
    with conn:
        c.execute("SELECT * FROM expenselist")
        expense =  c.fetchall()# คำสั่งให้ดึงข้อมูลเข้ามา
        print(expense)

    return expense
def update_expense(transectionid,title,expense,quantity,total):
    with conn:
        c.execute("""UPDATE expenselist SET title=?, expense=?, quantity=?, total=? WHERE transectionid=?""",
        ([title,expense,quantity,total,transectionid]))
        
    conn.commit()
    print('Data updated')

def delete_expense(transectionid):
    with conn:
        c.execute("DELETE FROM expenselist WHERE transectionid=?",([transectionid]))
    conn.commit()
    print('Data delete')

#################################################
GUI = Tk()
GUI.title('โปรแกรมคำนวนค่าใช้จ่าย By วิบูลย์ V.1.0')
GUI.iconbitmap(r'pig.ico')
#GUI.geometry('720x700+500+50')

w = 720
h = 700

ws = GUI.winfo_screenwidth() # ขนาดหน้าจอกว้าง
hs = GUI.winfo_screenheight() # ขนาดหน้าจอสูง

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')






########################### MENU ####################################################
menubar= Menu(GUI) 
GUI.config(menu=menubar)

#Menu file

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Expot to')

def About():
    messagebox.showinfo('About','สวัสดีครับโปรแกรมนี้ใช้ในการคำนวนเท่านั้น \n ห้ามซื้อขายหรือดัดแปลง \nสนใจบริจาคได้ที่ \n Acount : 1234567')

#About
Donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=Donatemenu)

# Help
Helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=Helpmenu)
Helpmenu.add_command(label='About',command=About)






########################################################################################
#---------โซน Tab-----------------------------------------

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab,bg='pink')
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

i_add = PhotoImage(file='money.png')
i_report = PhotoImage(file='list.png')


Tab.add(T1,text=f'{"เพิ่มค่าใช้จ่าย": ^20s}',image=i_add,compound='top')
Tab.add(T2,text=f'{"แสดงรายการ": ^20s}',image=i_report,compound='top')

#--------------------------------------------------------------------------
F1 =  Frame(T1,background='pink')
#F1.place(x=100,y=40)
F1.pack()




#---------------------------------------------------------------------------


#--------------------โซน funtoin------------------------------------------

days = {'Mon':'จันทร์',
        'Tue' :'อังคาร',
        'Wed' : 'พุธ',
        'Thu' : 'พฤหัส',
        'Fri' : 'ศุกร์',
        'Sat' : 'เสาร์',
        'Sun' : 'อาทิตย์'}

def Banteuk(event=None):
    expense = v_expense.get()
    price = v_price.get()
    cavity = v_cavity.get()
    if expense == '':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกจำนวน')
        return
    elif cavity == '':
        messagebox.showwarning('Error','กรุณากรอกข้อมูลจำนวนที่ต้องการ')
        #return
        cavity = 1
    try:
        total = int(price) * int(cavity)
        v_expense.set('')
        v_price.set('')
        v_cavity.set('')
        today = datetime.now().strftime('%a')
        stamp= datetime.now()
        time = stamp.now().strftime("%d/%m/%Y- %H:%M:%S")
        transectionid = stamp.now().strftime("%Y%m%d%H%M%f")
        time = days[today] + '-'+ time
        print('วันที่ {}\nรายการค่าใช้จ่าย : {} \nราคา :{}'.format(time,expense,price))
        print('จำนวน :{} รวมราคา :{:,d}'.format(cavity,total))

        text = 'วันที่ {}\nรายการค่าใช้จ่าย : {} \nราคา :{} บาท'.format(time,expense,price)
        text = text + 'จำนวน :{} \nรวมราคา :{:,d} บาท'.format(cavity,total)
        v_result.set(text)
        print(today)

        insert_expense(transectionid,time,expense,int(price),cavity,int(total)) # ใส่ใน DB

        with open('savedata.csv','a',encoding='utf-8',newline='')as a:
            wy = csv.writer(a)
            data = [transectionid,time,expense,price,cavity,total]
            wy.writerow(data)
    except:
        # print('ERROR')
        # messagebox.showwarning('Error','กรุณากรอกข้อมูลทุกช่อง')
        v_expense.set('')
        v_price.set('')
        v_cavity.set('')

    E1.focus()
    update_table()
GUI.bind('<Return>',Banteuk)

FONT1 = (None,17)
FONT2 = ('Angsana New',17)
#===========================================================================



#--------------------โซนกรอกข้อมูล-------------------------------------------




Roo = PhotoImage(file='mmm.png').subsample(4)
bg_A = ttk.Label(F1,image=Roo,background='pink')
bg_A.pack()

#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1,background='pink').pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack(pady=5)
#------text2---------
L = ttk.Label(F1,text='ราคา',font=FONT1,background='pink').pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack(pady=5)
#------text3---------
L = ttk.Label(F1,text='จำนวน',font=FONT1,background='pink').pack()
v_cavity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_cavity,font=FONT1)
E3.pack(pady=5)
#==============================================================================

#----------------โซนปุ่ม- buttom------------------
poom = PhotoImage(file='save.png')
B1 = Button(F1,text='กดเพื่อ Save เด้อ!!',bg='#abed9a',image = poom,command=Banteuk,compound='left')
B1.pack(ipadx=30,ipady=10,pady=20)

v_result = StringVar()
v_result.set('------------ผลลัพธ์---------')
result = ttk.Label(F1, textvariable=v_result,font=FONT2,foreground='blue',background='pink')
result.pack(pady=10)

#-------------------------------------------------------================================
#===========================TAB 2==================================================###

######## ฟังชั่น อ่าน CSV##########
def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data
#######################################################################################
# table

L = ttk.Label(T2,text='ตารางแสดงค่าใช้จ่าย',font=FONT1).pack(pady=20)

header = ['รหัส','วันที่-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
kai = ttk.Treeview(T2,columns=header,show='headings',height=20) 
kai.pack()
# for i in range(len(header)):
#     kai.heading(header[i],text=header[i])
for h in header:
    kai.heading(h,text=h)
headerwidth = [120,180,100,80,80,80]
for h,w in zip(header,headerwidth):
    kai.column(h,width=w)




alltransaction = {} ## สร้าง ดิชั่นนารี เพื่อ ดึง transaction

################## ฟังชั่น เขียนทับ CSV #######################
def UpdateCSV():
    with open('savedata.csv','w',newline='',encoding='utf-8') as f:
        fw = csv.writer(f)
    ##### เตรียม alltransaction ข้อมูลให้กลายเป็น list 
        data = list(alltransaction.values())
        fw.writerows(data)
        print('กระดานมีการ เปลี่ยนแปลง')
        update_table()

def UpdateSQL():
    data = list(alltransaction.values())
    #print('Update SQL',data[0])
    for d in data:
        #transectionid,title,expense,quantity,total
        #d[0]=02112091625315192', d[1]='พฤหัส-09/12/2021- 16:25:31', d[2]= 'ดาว', d[3]= 25.0, d[4]= 4, d[5]=100.0
        update_expense(d[0],d[2],d[3],d[4],d[5])



################################  ฟังชั่น ลบ ##############################################
def DeleteRecord(event=None):
    check = messagebox.askyesno('Conferm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
    if check == True:
        select = kai.selection()
        data = kai.item(select)
        data = data['values']
        transectionid = data[0]
        del alltransaction[str(transectionid)]
        
        #UpdateCSV()
        delete_expense(str(transectionid)) # delete in DB
        update_table()
    else:
        #print('cancle')
        pass
BDelete = ttk.Button(T2,text='delete',command=DeleteRecord)
BDelete.place(x=35,y=550)

kai.bind('<Delete>',DeleteRecord)




###################### การ เอาลง ตาราง####################################################


def update_table():
    kai.delete(*kai.get_children())
    # for c in kai.get_children():ใช้ * แทน for loop ได้
    #     kai.delete(c)
    try:
        data = show_expense()#read_csv()
        #print('data')
        # for i,d in enumerate(data):
        #     print(i+1,d)
        for d in data:
            ## สร้าง transection data
            alltransaction[d[1]] = d[1:] # d[1] = transaction
            kai.insert('',0,values=d[1:])
            print('TS',alltransaction)
        print(alltransaction)

    except Exception as e:
        print('No File')
        print('ERROR',e)

#################### คลิกขวา เมนู #############
def Editrecord():
    POPUP = Toplevel()# คล้ายๆกับ Tk()
    #POPUP.geometry('500x400')
    
    w = 500
    h = 400

    ws = GUI.winfo_screenwidth() # ขนาดหน้าจอกว้าง
    hs = GUI.winfo_screenheight() # ขนาดหน้าจอสูง

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

    POPUP.title('แก้ใขรายการ')
    L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1,background='pink').pack()
    v_expense = StringVar()
    E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
    E1.pack(pady=5)
    #------text2---------
    L = ttk.Label(POPUP,text='ราคา',font=FONT1,background='pink').pack()
    v_price = StringVar()
    E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
    E2.pack(pady=5)
    #------text3---------
    L = ttk.Label(POPUP,text='จำนวน',font=FONT1,background='pink').pack()
    v_cavity = StringVar()
    E3 = ttk.Entry(POPUP,textvariable=v_cavity,font=FONT1)
    E3.pack(pady=5)
    #==============================================================================

    def Edit():
        #check = messagebox.askyesno('ยืนยันการแก้ไข','คุณต้องการแก้ไขข้อมูลใช่หรือไม่?')
        # print(transectionid)
        # print(alltransaction)
        olddata = alltransaction[str(transectionid)]
        print(olddata)
        v1 = v_expense.get()
        v2 = v_price.get()
        v3 = v_cavity.get()
        totol = int(v2) * int(v3)
        newdata = [olddata[0],olddata[1],v1,v2,v3,totol] 
        alltransaction[str(transectionid)] = newdata 
        #UpdateCSV()
        UpdateSQL()
        update_table()
        POPUP.destroy()# สั่งปิด POPUP

    #----------------โซนปุ่ม- buttom------------------
    poom = PhotoImage(file='save.png')
    B1 = Button(POPUP,text='กดเพื่อ Save เด้อ!!',bg='#abed9a',image = poom,command=Edit,compound='left')
    B1.pack(ipadx=30,ipady=10,pady=20)

############ get data in select record ######
    select = kai.selection()
    #print(select)
    data = kai.item(select)
    data = data['values']
    print(data)
    transectionid = data[0]

    ## สั่ง Set ค่าเก่าไว้ตรงช่องกรอก
    v_expense.set(data[2])
    v_price.set(data[3])
    v_cavity.set(data[4])

    POPUP.mainloop()



rigthclick = Menu(GUI,tearoff=0)
rigthclick.add_command(label='Edit',command=Editrecord)
rigthclick.add_command(label='Delete',command=DeleteRecord)

def menupopup(event):
    #print(event.x_root,event.y_root)
    rigthclick.post(event.x_root,event.y_root)

kai.bind('<Button-3>',menupopup)



update_table()

GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
