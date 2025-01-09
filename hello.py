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

#ทดลอง insert ข้อมูล
'''
with conn:
	command = 'INSERT INTO expense VALUES (?,?,?,?,?)' #sql
	c.execute(command, (None,'breakfast',50.5,'boil eggs with coffee','2024-11-17 08:00:20'))
conn.commit() # save command to database
'''

def insert_expense(title,price,others):
	ts =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with conn:
		command = 'INSERT INTO expense VALUES (?,?,?,?,?)' #sql
		c.execute(command, (None,title,price,others,ts))
	conn.commit() # save command to database, ใช้เมื่อต้องการเปลี่ยนแปลงข้อมูลใน database
	print('saved')

#insert_expense('ค่า grab',100,'ไป รร.')
print('##########โปรแกรมค่าใช้จ่ายประจำวัน########')

'''
for i in range(3):
	print('##########{}########'.format(i+1))
	title = input('รายการ:  ')
	price = float(input('ราคา:  '))
	others = input('หมายเหตุ:   ')
	insert_expense(title,price,others)
'''



def view_expense():
	with conn:
		command ='SELECT * FROM expense'
		c.execute(command)
		result = c.fetchall()
	#print(result)
	return result  #return ค่าที่อยู่ใน function ออกมาเพื่อนำไปใช้ต่อ

def update_expense(ID,field,newvalue):
	with conn:
		command = 'UPDATE expense SET {} = (?) WHERE ID = (?)'.format(field)
		c.execute(command,(newvalue,ID))
	conn.commit()

def delete_expense(ID):
	#การ delect โดยปกติจะ reference กับ ID
	with conn:
		command ='DELETE FROM expense WHERE ID=(?)'
		c.execute(command,([ID])) # สำหรับคำสั่ง Delete จะต้องกำหนดให้ข้อมูล ID เป็นชนิด List
		conn.commit()

############Search function ###########
def search_expense(keyword):
	#การ delect โดยปกติจะ reference กับ ID
	with conn:
		command ='SELECT * FROM expense WHERE ID=(?) OR title LIKE ? OR others LIKE ?'
		text_search = '%{}%'.format(keyword)
		c.execute(command,(keyword,text_search, text_search)) # สำหรับคำสั่ง Delete จะต้องกำหนดให้ข้อมูล ID เป็นชนิด List
		result = c.fetchall()
	return result

#delete_expense(5)

# data = search_expense('7-11')
# print(data)

with conn:
	c.execute('SELECT * FROM expense ORDER BY ID DESC LIMIT 1')
	last_record = c.fetchall()
	print(last_record)
