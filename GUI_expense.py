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

c.execute(""" CREATE TABLE IF NOT EXISTS expense_status (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			expense_id INTEGER,
			checkstatus TEXT,
			comment TEXT)""")


def insert_expense(title,price,others):
	ts =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with conn:
		command = 'INSERT INTO expense VALUES (?,?,?,?,?)' #sql
		c.execute(command, (None,title,price,others,ts))
	conn.commit() # save command to database, ใช้เมื่อต้องการเปลี่ยนแปลงข้อมูลใน database
	print('saved')

	#ทุกครั้งที่มีการ insert จะให้มีการเลือก last record มาด้วย
	with conn:
		c.execute('SELECT * FROM expense ORDER BY ID DESC LIMIT 1')
		last_record = c.fetchone()
		print(last_record)
		last_id = last_record[0]
		insert_expense_status(last_id,'ยังไม่ตรวจสอบ','')


def view_expense():
	with conn:
		command ='SELECT * FROM expense'
		c.execute(command)
		result = c.fetchall()
	#print(result)
	return result  #return ค่าที่อยู่ใน function ออกมาเพื่อนำไปใช้ต่อ

def delete_expense(ID):
	with conn:
		command = 'DELETE FROM expense WHERE ID=(?)'
		c.execute(command,([ID]))
	conn.commit()

def update_expense(ID, field, newvalue):
	with conn:()
	command = 'UPDATE expense SET {} = (?) WHERE ID =(?)'.format(field)
	c.execute(command,(newvalue,ID))
	conn.commit()

def update_table(event=None):
	table.delete(*table.get_children()) #เป็นการ clear data เก่าที่คงค้างใน table ก่อน
	for row in view_expense():
		#print(row)
		table.insert('','end',values=row)


def search_expense(keyword):
	#การ delect โดยปกติจะ reference กับ ID
	with conn:
		command ='SELECT * FROM expense WHERE ID=(?) OR title LIKE ? OR others LIKE ?'
		text_search = '%{}%'.format(keyword)
		c.execute(command,(keyword,text_search, text_search)) # สำหรับคำสั่ง Delete จะต้องกำหนดให้ข้อมูล ID เป็นชนิด List
		result = c.fetchall()
	return result

##############EXPENSE STATUS ##########################

def insert_expense_status(expense_id,checkstatus,comment):
	ts =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with conn:
		command = 'INSERT INTO expense_status VALUES (?,?,?,?)' #sql
		c.execute(command, (None,expense_id,checkstatus,comment))
	conn.commit() # save command to database, ใช้เมื่อต้องการเปลี่ยนแปลงข้อมูลใน database
	print('saved')

def view_expense_status():
	with conn:
		command ='SELECT * FROM expense_status'
		c.execute(command)
		result = c.fetchall()
	#print(result)
	return result  #return ค่าที่อยู่ใน function ออกมาเพื่อนำไปใช้ต่อ

def delete_expense_status(ID):
	with conn:
		command = 'DELETE FROM expense_status WHERE expense_id=(?)'
		c.execute(command,([ID]))
	conn.commit()

def update_expense_status(expense_id, field, newvalue):
	with conn:()
	command = 'UPDATE expense_status SET {} = (?) WHERE expense_id =(?)'.format(field)
	c.execute(command,(newvalue,expense_id))
	conn.commit()

#####################################################


GUI=Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย')
GUI.geometry('700x600')


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
		update_table() # เมื่อกด save ข้อมูล โปรแกรมจะทำการ update table ทันทีเพื่อให้มีข้อมูลชุดใหม่เข้าไปอยู่ใน table

E3.bind('<Return>', Save) # ใส่ event=None ใน function ด้วย
#ถ้าหาก user กำลังกรอกข้อมูลในช่อง E3 แล้วมีการกด Enter จะมีการเรียก function นี้มาใช้งาน
# <Return> หมายถึงการกดปุ่ม Enter 
	#messagebox.showinfo('Save', title)



B1 = ttk.Button(T1, text = 'SAVE', command= Save)
B1.place(x=250,y= 350)

###########Tab2########################
F1 = Frame(T2)
F1.pack(pady=20)

v_search =StringVar()
ESearch = ttk.Entry(F1, textvariable=v_search, font= FONT1, width=30)
ESearch.grid(row=0, column=0)


def searchdata(event=None):
	search =v_search.get()	
	data = search_expense(search)
	print(data)
	table.delete(*table.get_children()) #เป็นการ clear data เก่าที่คงค้างใน table ก่อน
	for row in data:
		table.insert('','end',values=row)

ESearch.bind('<Return>', searchdata) #ถ้าใช้ Bind ด้วยปุ่ม Return (Enter) จะต้องใส่ event=None ใน function ที่เรียกใช้งานด้วย

def cleardata(event=None):
	update_table()
	v_search.set('')
	ESearch.focus()

GUI.bind('<F12>', update_table) #กดปุ่ม F12 แล้วคืนค่าข้อมูลทั้งหมด


BSearch = ttk.Button(F1, text='Search', command=searchdata)
BSearch.grid(row=0, column=1)


header = ['ID','รายการ','ค่าใช้จ่าย','หมายเหตุ','วัน-เวลา']
hwidth = [50,100,100,200,100]

table = ttk.Treeview(T2, column=header, show='headings', height=20)
table.pack()

for h,w in zip(header, hwidth):
	table.heading(h,text =h)
	table.column(h, width=w)

#table.insert('','end', values=[4])

########Delete##################
def delete_table(event=None):
	try:
		print ('delete...')
		select = table.selection()
		ID = table.item(select)['values'][0]
		choice = messagebox.askyesno('ลบข้อมูล','คุณต้องการลบข้อมูลใช่หรือไม่')
		if choice == True:
			delete_expense(ID)

			#DELETE STATUS
			delete_expense_status(ID)
			update_table()
	except Exception as e:
		print(e)
		messagebox.showwarning('เลือกรายการ','กรุณาเลือกรายการที่ต้องการลบ')

table.bind('<Delete>', delete_table)

###################
def updatedata(event=None):
	try:
		select = table.selection()
		data = table.item(select)['values']
		print(data)

		GUI2= Toplevel()
		GUI2.title('แก้ไขข้อมูลการบันทึก')
		GUI2.geometry('500x400')
		
		L= Label(GUI2, text='รายการ', font = FONT2)
		L.pack()

		v_title_e = StringVar()
		v_title_e.set(data[1])
		E1 = ttk.Entry(GUI2, textvariable= v_title_e, width =50, font=FONT2)
		E1.pack()

		L= Label(GUI2, text='ราคา', font = FONT2)
		L.pack()

		v_price_e = StringVar()
		v_price_e.set(data[2])
		E2 = ttk.Entry(GUI2, textvariable= v_price_e, width =50, font=FONT2)
		E2.pack()

		L= Label(GUI2, text='หมายเหตุ', font = FONT2)
		L.pack()

		v_other_e = StringVar()
		v_other_e.set(data[3])
		E3 = ttk.Entry(GUI2, textvariable= v_other_e, width =50, font=FONT2)
		E3.pack()

		expenseid = data[0] #นำไปใช้ค้นหาสถานะ
		with conn:
			command = 'SELECT * FROM expense_status WHERE expense_id =(?)'
			c.execute(command,([expenseid]))
			d = c.fetchone()


		v_check = StringVar()
		FR1 = Frame(GUI2)
		FR1.pack(pady=20)
		R1 = ttk.Radiobutton(FR1, text = 'ตรวจสอบแล้ว', value='ตรวจสอบแล้ว',variable=v_check)
		R1.grid(row=0,column=0)

		R2 = ttk.Radiobutton(FR1, text = 'ยังไม่ตรวจสอบ', value='ยังไม่ตรวจสอบ',variable=v_check)
		R2.grid(row=0, column=1)

		print('Data:',d)
		if d[2] =='ยังไม่ตรวจสอบ':
			R2.invoke() # เลือกค่า default ให้ปุ่ม
		else:
			R1.invoke()



		L = Label(GUI2, text = 'เพิ่มเติม', font = FONT2)
		L.pack()
		v_comment= StringVar()
		v_comment.set(d[3])
		E4 = ttk.Entry(GUI2, textvariable=v_comment, font=FONT2, width = 30)
		E4.pack()




		def Edit():
			ID = data[0]

			title_e = v_title_e.get()
			price_e = float(v_price_e.get())
			other_e = v_other_e.get()
			update_expense(ID,'title',title_e)
			update_expense(ID,'price',price_e)
			update_expense(ID,'others',other_e)

			check = v_check.get()
			comment =v_comment.get()

			update_expense_status(ID, 'checkstatus',check)
			update_expense_status(ID, 'comment',comment)


			update_table() #update ข้อมูลใหม่หลังจาก edit

			GUI2.destroy()


		B1 = ttk.Button(GUI2, text = 'SAVE', command= Edit)
		B1.pack(pady=10)

		GUI2.mainloop()



	except Exception as e:
		print(e)
		messagebox.showwarning('เลือกรายการ','กรุณาเลือกรายการที่ต้องการลบ')

table.bind('<Double-1>', updatedata)




update_table()  # run program ทุกครั้งให้มีการ update data
GUI.mainloop()