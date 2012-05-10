#Example: update('fileContent','File','revision','Revision',etc....)
def update(information , information_type , identifier , identifier_type,  host1, port1, username, password): #creations come before updates. ie an update doesnt create a NEW but a NEW can create an update

	con = None
	con = mdb.connect(host=host1, port= port1, user=username, passwd=password)
	cur = con.cursor()
	cur.execute("use oogadaBoogada")

	if type(information) == str:
		information = "'" + information + "'"
	else:
		information = str(information)
	if type(identifier) == str:
		identifier = "'" + identifier + "'"
	else:
		identifier= str(identifier)

	if information_type == "file_content" :
		cur.execute("update file_info set " + information_type + " = " + information + " where " + identifier_type + " = " + identifier)

	elif information_type == "filenames":  #only called when a new file is created
		cur.execute("update revision set " + information_type + " = " + information + " where " + identifier_type + " = " + identifier)


	elif information_type == "avatar" or information_type == "password" :   
		cur.execute('update account set ' + information_type + ' = ' + information + ' where ' + identifier_type + ' = ' + identifier)

	elif information_type == "locked" :
		cur.execute("update project_info set " + information_type + " = " + information + " where " + identifier_type + " = " + identifier)


	elif information_type == "tags" or information_type == "children_ids" or information_type == "borrow_ids" or information_type == "revisions" :
		con.query("select " + information_type +  " from project_info where " + identifier_type + ' = ' + identifier)
		results = con.store_result()
		current = results.fetch_row(0,1)
		if len(current) == 0:
			new_info = information
		else:
			current = current[0]
			current = current[information_type]
			current = str(current)
			information = information.strip("'")
			information = information.lstrip("'")
			new_info = "'" + current + '$$$$' + information + "'"
		cur.execute("update project_info set " + information_type + " = " + new_info + " where " + identifier_type + " = " + identifier)


	elif information_type == "group_projects":
		con.query("select " + information_type +  " from group_info where " + identifier_type + ' = ' + identifier)
		results = con.store_result()
		current = results.fetch_row(0,1)
		if len(current) == 0:
			new_info = information
		else:
			current = current[0]
			current = current[information_type]
			information = information.strip("'")
			information = information.lstrip("'")
			new_info = "'" + current + '$$$$' + information + "'"
		cur.execute("update group_info set " + information_type + " = " + new_info + " where " + identifier_type + " = " + identifier)

	elif information_type == "groups" :
		con.query("select " + information_type + " from account where " + identifier_type + ' = ' + identifier)
		results = con.store_result()
		current = results.fetch_row(0,1)
		if len(current) == 0:
			new_info = information
		else:
			current = current[0]
			current = current[information_type]
			information = information.strip("'")
			information = information.lstrip("'")
			new_info = "'" + current + '$$$$' + information + "'"
		cur.execute("update account set " + information_type + " = " + new_info + " where " + identifier_type + " = " + identifier)
		cur.execute("update group_info set " + information_type + " = " + information + " where " + identifier_type + " = " + identifier)

	elif information_type == "account_ids":
		con.query("select " + information_type +  " from group_info where " + identifier_type + ' = ' + identifier)
		results = con.store_result()
		current = results.fetch_row(0,1)
		if len(current) == 0:
			new_info = information
		else:
			current = current[0]
			current = current[information_type]
			information = information.strip("'")
			information = information.lstrip("'")
			new_info = "'" + current + '$$$$' + information + "'"
		cur.execute("update group_info set " + information_type + " = " + new_info + " where " + identifier_type + " = " + identifier)
		cur.execute("update account set " + information_type + " = " + information + " where " + identifier_type + " = " + identifier)

	con.commit()
			




def NewEntry(object_type, column_info, column_type, host1, port1, username, password):  #if a person creates a new revision they must also provide the changes made
	
	con = None
	con = mdb.connect(host=host1, port= port1, user=username, passwd=password)
	cur = con.cursor()
	cur.execute("use oogadaBoogada")

	infos = ''
	types = ''
	for i in range(len(column_info)):
		if not type(column_info[i]) == str:
			column_info[i] = str(column_info[i])
		if i == len(column_info) - 1: 
			types = types + column_type[i] + ', ' + column_type[i+1]
			infos = infos + "'" + column_info[i] + "' , NOW()"
		else:
			infos = infos + "'" + column_info[i] + "' ,"
			types = types + column_type[i] + ',' 



	cur.execute('insert into ' + object_type + '(' + types + ')' + 'values (' + infos +  ');')
	con.commit()


	if object_type == "borrow":
		update(column_info[0], "borrow_ids", column_info[1], "project_id", host,password )

	elif object_type == "project_info":
		update(column_info[0], "group_projects", column_info[4], "group_id" , host,password)
		if not column_info[1] == None :
			update(column_info[0],'children_ids',column_info[1], 'project_id', host, password)

	elif object_type == "group_info":
		update(column_info[0], "groups", column_info[3], "account_id", host,password )

	elif object_type == "file_info":
		update(column_info[2], "filenames", column_info[1], "revision_number" , host,password)

	elif object_type == "revision":
		update(column_info[0], "revisions", column_info[2], "project_id" , host,password)
		if column_info[0] != 1:
			update(0, "head", column_info[0]-1, "revision_number")
		string = column_info[1]
		list_of_files = string[3:].split('$$$$')
		new_types = ['project_id', 'revision_number', 'file_name', 'file_content']
		for i in list_of_files:
			new_info = [column_info[2], column_info[0], i, column_info[4]]
			NewEntry('file_info', new_info, new_types, host, password)
 


def SearchAll(search_type, search_value, object_type, fist, last, host1, port1, username, password):  # ex: give me all of the object_type who have search_type equal to search_value
	

	
	con = None
	con = mdb.connect(host=host1, port= port1, user=username, passwd=password)
	cur = con.cursor()
	cur.execute("use oogadaBoogada")

	string_of_stuff = ""
	for i in range(len(search_value)):

			if not type(search_value[i]) == str:
				search_value[i] = str(search_value[i])
			if i == len(search_value) - 1:
				string_of_stuff = string_of_stuff + search_type[i] + ' like "%'  + search_value[i] + '%"'
			else:
				string_of_stuff = string_of_stuff + search_type[i] + ' like "%'  + search_value[i] + '%" or '
	
	con.query(" select * from " + object_type + " where " + string_of_stuff + ' limit ' + fist+ ' ,' + last)
	results = con.store_result() 
	stuff = results.fetch_row()

	return stuff


import MySQLdb as mdb 
import sys
	


meep = [123, 'FearBisquick', 'weee', 'NULL', 'groups and things']
moop = ['account_id', 'username' , 'password', 'avatar', 'groups', 'creation_time' ]
NewEntry('account', meep, moop, 'calvin.olin.edu', 3306, 'clinet_yay', 'password')
print SearchAll(['groups', 'account_id'] , ['and', 12], 'account', '0' , '1',  'calvin.olin.edu', 3306, 'clinet_yay', 'password')
	
	
	
