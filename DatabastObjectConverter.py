#convert lists
#convert date time
#convert terminology
#convert from head pobject to id
#convert head shit

	converter['Account'] = 'account'
	converter['accountID'] = 'account_id'
	converter['username'] = 'username'
	converter['password'] = 'password'
	converter['avatar'] = 'avatar'
	converter['group_list'] = 'groups'
	converter['date_time'] = 'creation_time'

	converter['Borrow'] = 'borrow'
	converter['date_taken'] = 'creation_time'
	converter['project_from'] = 'project_id'
	converter['project_to'] = 'project_to_id'
	converter['revision_from'] = 'revision_id'
	converter['file_from'] = 'file_name'
	converter['line_range'] = 'line_range'
	converter['line_offsets'] = 'line_offset'
	converter['borrow_id'] = 'borrow_id'
	converter['project_to'] = 'project_to_id'
	converter['revision_to'] = 'revision_id'
	converter['file_to'] = 'file_to_name'

	converter['Project'] = 'project_info'
	converter['title'] = 'title'
	converter['description'] = 'description'
	converter['projID'] = 'project_id'
	converter['parentID'] = 'parent_id'
	converter['groupID'] = 'group_id'
	converter['revisions'] = 'revisions'
	converter['children'] = 'children_ids'
	converter['borrows'] = 'borrow_ids'
	converter['head'] = 'head'
	converter['locked'] = 'locked'
	converter['tags'] = 'tags'
	converter['times'] = 'creation_time'

	converter['File'] = 'file_info'
	converter['rev_number'] = 'revision_number'
	converter['file_name'] = 'file_name'
	converter['content'] = 'file_content'
	converter['revision'] = 'revision_number'
	converter['comments'] = 'comments'
	converter['date_created'] = 'creation_time'

	converter['Group'] = 'group_info'
	converter['title'] = 'title'
	converter['description'] = 'description'
	converter['groupID'] = 'group_id'
	converter['projects'] = 'group_projects'
	converter['godID'] = 'god_id'
	converter['accounts'] = 'account_ids'
	converter['date_formed'] = 'creation_time'
	
	converter['Comment'] = 'comment'
	converter['text'] = 'all_of_the_text'
	converter['time'] = 'creation_time'
	converter['project'] = 'project_id'
	converter['rev'] = 'revision_number'
	converter['file'] = 'file_name'
	converter['account'] = 'account_posting_id'
	converter['linenum'] = 'line_number'
	converter['commentID'] = 'comment_id'
	
	converter['Revision'] = 'revision'
	converter['project'] = 'project_id'
	converter['rev_number'] = 'revision_number'
	converter['files'] = 'filenames'
	converter['time_made'] = 'creation_time'




def convertForUpdate(infos_to_be_updated, info_types_being_updated, object_that_is_being_updated):
	host = 'calvin.olin.edu'
	port = 3306
	username ='clinet_yay'
	password = 'password'

	if type(object_that_is_being_updated) == Account :
	 	identifier = object_that_is_being_updated.accountID
	 	identifier_type = converter['accountID']

	elif type(object_that_is_being_updated) == Borrow :
	 	identifier = object_that_is_being_updated.borrow_id
	 	identifier_type = converter['borrow_id']

	elif type(object_that_is_being_updated) == Project :
	 	identifier = object_that_is_being_updated.projID
	 	identifier_type = converter['projID']

	elif type(object_that_is_being_updated) == File:
	 	identifier = object_that_is_being_updated.file_name
	 	identifier_type = converter['file_name']

	elif type(object_that_is_being_updated) == Group:
	 	identifier = object_that_is_being_updated.groupID
	 	identifier_type = converter['groupID']

	elif type(object_that_is_being_updated) == Comment:
	 	identifier = object_that_is_being_updated.project
	 	identifier_type = converter['project']

	elif type(object_that_is_being_updated) == Revision:
	 	identifier = object_that_is_being_updated.rev_number
	 	identifier_type = converter['rev_number']

	if info_types_being_updated = 'head':
		info_types_being_updated = infos_to_be_updated.rev_number


	database_object_type = converter[object_type]
	object_that_is_being_updated
	
	for i in range(len(info_types_being_updated)) :
		info_types_being_updated[i] = converter[info_types_being_updated[i]]
		update(str(infos_to_be_updated[i]), info_types_being_updated[i], str(identifier), identifier_type, host, port, username, password )

def convertForNewEntry(object_thing):
	host = 'calvin.olin.edu'
	port = 3306
	username ='clinet_yay'
	password = 'password'


	if type(object_thing) == Account :
		for i in range object_thing.group_list:
			groups_and_things = '$$$$' + i
	 	values = [object_thing.accountID, object_thing.username, object_thing.password, object_thing.avatar, groups_and_things , object_thing.date_time]
	 	types = ['account_id', 'username', 'password', 'avatar', 'groups', 'creation_time']

	elif type(object_thing) == Borrow:
		values = [object_thing.borrow_id, object_thing.project_to, object_thing.project_from, object_thing.revision_from, object_thing.file_from, object_thing.line_range, object_thing.line_offsets, object_thing.revision_to, object_thing.file_to, object_thing.date_taken]
		types = ['borrow_id', 'project_to_id', 'project_id', 'revision_id', 'file_name', 'line_range', 'line_offset', 'revision_to_id', 'file_to_name', 'creation_time']

	elif type(object_thing) == Project:
		for i in range object_thing.children:
			list_o_children = '$$$$' + i
		for j in range object_thing.borrows:
			rawr_borrows_rawr = '$$$$' + j
		for k in range object_thing.revisions:
			kiwi = '$$$$' + k
		head_thing = object_thing.head.rev_number
		values =[object_thing.projID, object_thing.parentID, list_o_children, rawr_borrows_rawr, object_thing.groupID, kiwi, object_thing.locked, object_thing.tags, head_thing, object_thing.title, object_thing.description, object_thing.times ]
		types = ['project_id', 'parent_id', 'children_ids', 'borrow_ids', 'group_id', 'revisions', 'locked', 'tags', 'head', 'title', 'description', 'creation_time']

	elif type(object_thing) == File:
		for i in range object_thing.comments:
			i_say_words = '$$$$' + i
		values = [object_thing.project, object_thing.rev_number, object_thing.file_name, object_thing.content, i_say_words, object_thing.date_created]
		types = ['project_id', 'revision_number', 'file_name', 'file_content', 'comments', 'creation_time']

	elif type(object_thing) == Group:
		for i in range object_thing.projects:
			what_are_we_working_on = '$$$$' + i
		for j in range object_thing.accounts:
			whos_working = '$$$$' + j
		values =[object_thing.groupID, what_are_we_working_on, whos_working, object_thing.godID, object_thing.title, object_thing.description, object_thing.date_formed]
		types =	['group_id', 'group_projects', 'account_ids', 'god_id', 'title', 'description', 'creation_time']

	elif type(object_thing) == Comment:
		values = [object_thing.text, object_thing.account, object_thing.project, object_thing.rev, object_thing.whichfile, object_thing.linenum, object_thing.commentID, object_thing.time]
		types =	['all_of_the_text', 'account_posting_id', 'project_id', 'revision_number', 'file_name', 'line_number', 'comment_id', 'creation_time']

	elif type(object_thing) == Revision:
		for i in range object_thing.files:
			flying_flies = '$$$$' + i
		if type(object_thing) == Revision:
			head = 1 
		values =[object_thing.rev_number, flying_flies, object_thing.project, head, object_thing.creation_time]
		types =	['revision_number', 'filenames', 'project_id', 'head', 'creation_time']

	NewEntry(converter(object_thing), values, types, host1, port1, username, password)


def convertForSearchAll(search_type, search_value, object_type, first, last):
	host = 'calvin.olin.edu'
	port = 3306
	username ='clinet_yay'
	password = 'password'




	SearchAll(converter(search_type), search_value, converter(object_type), fist, last, host1, port1, username, password)


