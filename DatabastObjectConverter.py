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
	 	values = [object_thing.accountID, object_thing.username, object_thing.password, object_thing.password, object_thing.avatar]
	 	types = ['account_id', 'username', 'password', 'avatar', 'groups', 'creation_time']



	elif type(object_thing) == Borrow:
		values = [object_thing.date_taken , object_thing.borrow_id]
		types = ['borrow_id', 'project_to_id', 'project_id', 'revision_id', 'file_name', 'line_range', 'line_offset', 'revision_to_id', 'file_to_name', 'creation_time']

		self.date_taken = date_taken
        self.borrow_id = borrow_id
        self.project_from = project_from
        self.revision_from = revision_from
        self.project_to = project_to
        self.file_from = file_from
        #line_range is a tuple of 2 line numbers, or 2 of the same line number for single-line borrows
        self.line_range = line_range
        #line_offsets is a tuple of 2 offsets representing distance from start of line
        self.line_offsets = line_offsets






	elif type(object_thing) == Project:
		values =
		types =	

	elif type(object_thing) == File:
		values =
		types =

	elif type(object_that_is_being_updated) == Group:
		values =
		types =

	elif type(object_that_is_being_updated) == Comment:
		values =
		types =

	elif type(object_that_is_being_updated) == Revision:
		values =
		types =


def convertForSearchAll():

