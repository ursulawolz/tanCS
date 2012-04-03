
def makeTableStructure(host , password , username, personalpassword) :
	
	import MySQLdb as mdb 
	import sys
	
	con = None
	con = mdb.connect(host, 'root', password)
	cur = con.cursor()
	

	cur.execute("create database oogadaBoogada")
	cur.execute("use oogadaBoogada")
	cur.execute("create table account(account_id int, username tinytext, password tinytext, avatar blob, projects text, groups text);")
	cur.execute("create table borrow(date_taken datetime, project_id smallint, revision_id smallint, file_name tinytext, line_range tinytext);")
	cur.execute("create table comment(all_of_the_text longtext, time_of_post datetime, account_posting_id smallint, project_id smallint, revision_number smallint, file_name tinytext, line_number tinyint);")
	cur.execute("create table file_info( project_id smallint, revision_number smallint, file_name tinytext, file_content blob, checksum tinytext);")
	cur.execute("create table group_info( group_id smallint, group_projects text, account_ids text, god_id int);")
	cur.execute("create table project_info( project_id smallint, parent_id smallint, children_ids text, borrow_ids text, group_id smallint, revisions text, locked tinyint, tags text);")
	cur.execute("create table revision( revision_number tinyint, filenames text, project_id smallint);")
	


	cur.execute("grant usage on *.* to " + username + " identified by" + personalpassword + ";")
	cur.execute("grant all privileges on oogadaBoogada.* to " + username + ";")




def update(information , information_type , identifier , identifier_type):

	import MySQLdb as mdb 
	import sys
	
	con = None
	con = mdb.connect(host, 'root', password)
	cur = con.cursor()

	if information_type == "file_content" :
		cur.execute("update file_info set " + information_type " = " + information + " where " + identifier_type + " = " + identifier)
	
	elif information_type == "avatar" || information_type == "password" || information_type == "projects":	
		cur.execute("update account set " + information_type " = " + information + " where " + identifier_type + " = " + identifier)

	elif information_type == "tags" || information_type == "locked" || information_type == "children_ids" || information_type == "borrow_ids" || information_type == "revisions" :
		cur.execute("update project_info set " + information_type " = " + information + " where " + identifier_type + " = " + identifier)

	elif information_type == "group_projects":
				cur.execute("update group_info set " + information_type " = " + information + " where " + identifier_type + " = " + identifier)

	elif information_type == "groups" || information_type == "account_ids":
		cur.execute("update account set " + information_type " = " + information + " where " + identifier_type + " = " + identifier)
		cur.execute("update group_info set " + information_type " = " + information + " where " + identifier_type + " = " + identifier)

			




def NewEntry(object_type, column_info_list, column_type_list):


def SearchEntries():






