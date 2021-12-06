from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import date, datetime

GUI = Tk()
GUI.title('โปรแกรมคำนวนค่าใช้จ่าย By วิบูลย์ V.1.0')
GUI.iconbitmap(r'pig.ico')
GUI.geometry('720x700+500+50')
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
Tab.add(T2,text=f'{"สดงรายการ": ^20s}',image=i_report,compound='top')

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
        
        with open('savedata.csv','a',encoding='utf-8',newline='')as a:
            wy = csv.writer(a)
            data = [transectionid,time,expense,price,cavity,total]
            wy.writerow(data)
    except:
        print('ERROR')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลทุกช่อง')
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

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

# table

L = ttk.Label(T2,text='ตารางแสดงค่าใช้จ่าย',font=FONT1).pack(pady=20)

header = ['รหัส','วันที่-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
kai = ttk.Treeview(T2,columns=header,show='headings',height=10) 
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

################################  ฟังชั่น ลบ ##############################################
def DeleteRecord(event=None):
    check = messagebox.askyesno('Conferm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
    if check == True:
        #print('delete')
        select = kai.selection()
        #print(select)
        data = kai.item(select)
        data = data['values']
        transectionid = data[0]
        #print(transectionid)
        #print(type(transectionid))
        del alltransaction[str(transectionid)]
        #print(alltransaction)
        UpdateCSV()
        update_table()
    else:
        print('cancle')

BDelete = ttk.Button(T2,text='delete',command=DeleteRecord)
BDelete.place(x=50,y=350)

kai.bind('<Delete>',DeleteRecord)




###################### การ เอาลง ตาราง####################################################


def update_table():
    kai.delete(*kai.get_children())
    # for c in kai.get_children():ใช้ * แทน for loop ได้
    #     kai.delete(c)
    try:
        data = read_csv()
        # for i,d in enumerate(data):
        #     print(i+1,d)
        for d in data:
            ## สร้าง transection data
            alltransaction[d[0]] = d # d[0] = transaction
            kai.insert('',0,values=d)
        print(alltransaction)

    except Exception as e:
        print('No File')
        print('ERROR',e)

update_table()

GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()