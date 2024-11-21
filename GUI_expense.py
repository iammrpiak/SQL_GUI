from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import os

############SQL#####################

import sqlite3
from datetime import datetime

conn = sqlite3.connect('expense.sqlite3')
c = conn.cursor()

#สร้างตารางชื่อ expense
c.execute("""CREATE TABLE IF NOT EXISTS expense (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT, 
			price REAL, 
			others TEXT,
			Timestamp TEXT ) """)

def insert_expense(title,price,others):
	ts =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with conn:
		command = 'INSERT INTO expense VALUES (?,?,?,?,?)' #sql
		c.execute(command, (None,title,price,others,ts))
	conn.commit() # save command to database, ใช้เมื่อต้องการเปลี่ยนแปลงข้อมูลใน database
	print('saved')

def view_expense():
	with conn:
		command ='SELECT * FROM expense'
		c.execute(command)
		result = c.fetchall()
	#print(result)
	return result  #return ค่าที่อยู่ใน function ออกมาเพื่อนำไปใช้ต่อ

def update_table():
	table.delete(*table.get_children()) #เป็นการ clear data เก่าที่คงค้างใน table ก่อน
	for row in view_expense():
		#print(row)
		table.insert('','end',values=row)

#####################################################


GUI=Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย')
GUI.geometry('600x500')


FONT1 = ('Angsana New', 20)
FONT2 = ('Angsana New', 16)
FONT3 = ('Angsana New', 12)


####Tab######
PATH = os.getcwd() #check current folder

s= ttk.Style()
s.configure('TNotebook.Tab',font=FONT3)

Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH, expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)

icon_tab1 = os.path.join(PATH,'record.png')
icon_tab2 = os.path.join(PATH,'file.png')
iconimage_tab1 = PhotoImage(file=icon_tab1)
iconimage_tab2 = PhotoImage(file=icon_tab2)

Tab.add(T1, text='บันทึกค่าใช้จ่าย', image=iconimage_tab1, compound='left')
Tab.add(T2, text='ประวัติค่าใช้จ่าย', image=iconimage_tab2, compound='left')

############

icon = os.path.join(PATH,'cat.png')
iconimage = PhotoImage(file= icon)

L=Label(T1,image=iconimage)
L.pack()

L= Label(T1, text='รายการ', font = FONT2)
L.pack()

v_title = StringVar()
E1 = ttk.Entry(T1, textvariable= v_title, width =50, font=FONT2)
E1.pack()

L= Label(T1, text='ราคา', font = FONT2)
L.pack()

v_price = StringVar()
E2 = ttk.Entry(T1, textvariable= v_price, width =50, font=FONT2)
E2.pack()

L= Label(T1, text='หมายเหตุ', font = FONT2)
L.pack()


v_other = StringVar()
E3 = ttk.Entry(T1, textvariable= v_other, width =50, font=FONT2)
E3.pack()


def Save(event = None):

	if v_price.get() == '':
		E2.focus()
		messagebox.showinfo('ข้อมูลไม่ครบ','กรุณากรอกตัวเลขด้วย')
	else:

		title = v_title.get()
		price = float(v_price.get())
		others = v_other.get()

		print(title,price,others)
		insert_expense(title, price, others)

		v_title.set('')
		v_price.set('')
		v_other.set('')

		E1.focus()
		update_table()

E3.bind('<Return>', Save) # ใส่ event=None ใน function ด้วย
#ถ้าหาก user กำลังกรอกข้อมูลในช่อง E3 แล้วมีการกด Enter จะมีการเรียก function นี้มาใช้งาน
# <Return> หมายถึงการกดปุ่ม Enter 
	#messagebox.showinfo('Save', title)



B1 = ttk.Button(GUI, text = 'SAVE', command= Save)
B1.pack(pady=5)

###########Tab2########################

header = ['ID','รายการ','ค่าใช้จ่าย','หมายเหตุ','วัน-เวลา']
hwidth = [50,100,100,200,100]

table = ttk.Treeview(T2, column=header, show='headings', height=20)
table.pack()

for h,w in zip(header, hwidth):
	table.heading(h,text =h)
	table.column(h, width=w)

#table.insert('','end', values=[4])


update_table()
GUI.mainloop()