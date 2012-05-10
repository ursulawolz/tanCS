#convert lists
#convert date time
#convert terminology
#convert from head pobject to id
#convert head shit



def convertForSearch(infos_to_be_updated, info_types_being_updated, object_that_is_being_updated):
	host = 'calvin.olin.edu'
	port = 3306
	username ='clinet_yay'
	password = 'password'

	object_type = type(object_that_is_being_updated)
	database_object_type = converter[object_type]
	
	for i in range(len(info_types_being_updated)) :
		info_types_being_updated[i] = converter[info_types_being_updated[i]]
		update(infos_to_be_updated[i], info_types_being_updated[i] , )



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







