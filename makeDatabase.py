
def makeTableStructure(host , password , username, personalpassword) :
	
	import MySQLdb as mdb 
	import sys
	
	con = None
	con = mdb.connect(host, 'root', password)
	cur = con.cursor()
	

	cur.execute("create database oogadaBoogada")
	cur.execute("use oogadaBoogada")
	cur.execute("create table account(account_id int, username tinytext, password tinytext, avatar blob, groups text);")
	cur.execute("create table borrow( borrow_id int, date_taken datetime, project_to_id smallint, project_id smallint, revision_id smallint, file_name tinytext, line_range tinytext);")
	cur.execute("create table comment(all_of_the_text longtext, time_of_post datetime, account_posting_id smallint, project_id smallint, revision_number smallint, file_name tinytext, line_number tinyint);")
	cur.execute("create table file_info( project_id smallint, revision_number smallint, file_name tinytext, file_content blob, checksum tinytext);")
	cur.execute("create table group_info( group_id smallint, group_projects text, account_ids text, god_id int);")
	cur.execute("create table project_info( project_id smallint, parent_id smallint, children_ids text, borrow_ids text, group_id smallint, revisions text, locked tinyint, tags text);")
	cur.execute("create table revision( revision_number tinyint, filenames text, project_id smallint, revision_time datetime);")
	


	cur.execute("grant usage on *.* to " + username + " identified by" + personalpassword + ";")
	cur.execute("grant all privileges on oogadaBoogada.* to " + username + ";")




def update(information , information_type , identifier , identifier_type):

	import MySQLdb as mdb 
	import sys
	
	con = None
	con = mdb.connect(host, 'root', password)
	cur = con.cursor()

	if information_type == "file_content" :
		cur.execute("update file_info set %s =  %s  where  %s = %s" ,(information_type, information , identifier_type , identifier))

	elif information_type == "filenames":
		cur.execute("update revision set %s =  %s  where  %s = %s" ,(information_type, information , identifier_type , identifier))


	elif information_type == "avatar" || information_type == "password" :
		cur.execute("update account set %s =  %s  where  %s = %s" ,(information_type, information , identifier_type , identifier))

	elif information_type == "locked" :
		cur.execute("update project_info set %s =  %s  where  %s = %s" ,(information_type, information , identifier_type , identifier))


	elif information_type == "tags" || information_type == "children_ids" || information_type == "borrow_ids" || information_type == "revisions" :
		con.query("select %s from project_info where %s = %s" , (information_type , identifier_type, identifier))
		current = con.store_result()
		new_info = current + information
		cur.execute("update project_info set %s =  %s  where  %s = %s" ,(information_type, new_info, identifier_type , identifier))


	elif information_type == "group_projects":
		con.query("select %s from group_info where %s = %s" , (information_type , identifier_type, identifier))
		current = con.store_result()
		new_info = current + information
		cur.execute("update group_info set %s =  %s  where  %s = %s" ,(information_type, new_info, identifier_type , identifier))

	elif information_type == "groups" :
		con.query("select %s from account where %s = %s" , (information_type , identifier_type, identifier))
		current = con.store_result()
		new_info = current + information
		cur.execute("update account set %s =  %s  where  %s = %s" ,(information_type, new_info , identifier_type , identifier))
		cur.execute("update group_info set %s =  %s  where  %s = %s" ,(identifier_type , identifier, information_type, information))

	elif information_type == "account_ids":
		con.query("select %s from group_info where %s = %s" , (information_type , identifier_type, identifier))
		current = con.store_result()
		new_info = current + information
		cur.execute("update group_info set %s =  %s  where  %s = %s" ,(information_type, new_info , identifier_type , identifier))
		cur.execute("update account set %s =  %s  where  %s = %s" ,(identifier_type , identifier, information_type, information))
			




def NewEntry(object_type, column_info, column_type):
	for i in range column_info:
		cur.execute("insert into %s ( %s ) values %s", (object_type, colomn_type[i], column_info[i]))


	if object_type = "borrow":
		update(column_info[0], "borrow_ids", column_info[3], "project_id" )

	elif object_type = "project_info":
		update(column_info[0], "group_projects", column_info[4], "group_id" )

	elif object_type = "group_info":
		update(column_info[0], "groups", column_info[3], "account_id" )

	elif object_type = "file_info":
		update(column_info[2], "filenames", column_info[1], "revision_number" )

	elif object_type = "revision":
		update(column_info[0], "revisions", column_info[2], "project_id" )


def SearchAll(search_type, search_value, object_type, fist, last):  # ex: give me all of the object_type who have search_type equal to search_value
	string_of_stuff = ""
	for i in range search_types:
		string_of_stuff = string_of_stuff + 'or' + search_type[i] + 'like "%'  + search_value[i] + '%"'

	con.query("select * from %s where %s limit %s,%s" , (object_type, string_of_stuff, fist, last))
	stuff = con.store_result() 
	return stuff

