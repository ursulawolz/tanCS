def makeTableStructure1(host1 , password , username, personalpassword) :
	
	import MySQLdb as mdb 
	import sys
	con = None
	con = mdb.connect(host = host1, user = "root", passwd = password)
	cur = con.cursor()
	

	cur.execute("create database oogadaBoogada")
	cur.execute("use oogadaBoogada")
	cur.execute("grant usage on *.* to " + username + " identified by '" + personalpassword + "' ;")
	cur.execute("grant all privileges on oogadaBoogada.* to " + username + ";")
	cur.execute("create table account(account_id int, username tinytext, password tinytext, avatar blob, groups text, creation_time datetime);")
	cur.execute("create table borrow( borrow_id int, project_to_id smallint, project_id smallint, revision_id smallint, file_name tinytext, line_range tinytext, line_offset tinytext, revision_to_id smallint, file_to_name tinytext, creation_time datetime);")
	cur.execute("create table comment(all_of_the_text longtext, account_posting_id smallint, project_id smallint, revision_number smallint, file_name tinytext, line_number tinyint, creation_time datetime);")
	cur.execute("create table file_info( project_id smallint, revision_number smallint, file_name tinytext, file_content blob, creation_time datetime);")
	cur.execute("create table group_info( group_id smallint, group_projects text, account_ids text, god_id int, title tinytext, description longtext, creation_time datetime);")
	cur.execute("create table project_info( project_id smallint, parent_id smallint, children_ids text, borrow_ids text, group_id smallint, revisions text, locked tinyint, tags text, head tinyint, title tinytext, description longtext, creation_time datetime);")
	cur.execute("create table revision( revision_number tinyint, filenames text, project_id smallint, head tinyint, creation_time datetime);")



makeTableStructure1('localhost', 'olinhasnotrees' , 'clinet_yay' , 'password') 