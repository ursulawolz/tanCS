### Definitions for the various objects necessary for Community of Practice.

class Account:
    ## Object for an individual user's account.

    def __init__(self, userID, username, password, avatar):
        self.accountID = accountID
        self.username = username
        self.password = password
        self.avatar = avatar

        # User's projects and groups will be stored as sets,
        # for the sake of memory.
        self.project_list = set()
        self.group_list = set()

    def add_project(self,new_project):
        ## Adds a new project to the user's list of projects.
        self.project_list.add( new_project )

    def remove_project(self,project):
        ## Removes a project from the user's list of projects.
        self.project_list.remove( project )

    def add_group(self, new_group):
        ## Adds a new group to the user's list of groups.
        self.group_list.add( new_group )

    def remove_group(self, group):
        ## Removes a group from the user's list of groups.
        self.group_list.remove( group )

class Borrow:
    def __init(self, date_taken, projectID, revisionID, file_name, line_range):
        self.date_taken = date_taken
        self.projectID = projectID
        self.revisionID = revisionID
        self.file_name = file_name
        self.line_range = line_range


class Project:
    def __init__(self, projID, parentID, groupID, borrows):
        self.projID = projID
        self.parentID = parentID
        self.groupID = groupID

        self.children = set()
        self.borrows = borrows

        ## Revisions is a dict, for which each key is a datetime,
        ## and the values are the revisions.
        self.revisions = {}

        self.locked = 0
        self.tags = set()

    def add_child(self, child):
        self.children.add( child )

    def remove_child(self, child):
        self.children.remove( child )

    def add_borrow(self, lender):
        self.borrows.add( lender )

    def remove_borrow(self, lender):
        self.borrows.remove( lender )

    def add_revision(self, revision_text, revision_datetime):
        nextIndex = len(revisions) + 1
        self.revisions[nextIndex] = [revision_text, revision_datetime]

    def lock_proj(self):
        self.locked = 1
    
    def unlock_proj(self):
        self.locked = 0

    def add_tag(self, new_tag):
        self.tags.add( new_tag )

    def remove_tag(self, tag):
        self.tags.remove( tag )


class File:
    ## Object for a revision file.

    def __init__(self, projectID, revision_number, file_name, content)
        self.projectID = projectID
        self.revision_number = revision_number
        self.file_name = file_name
        self.content = content


class Group:
    ## Object which defines a user-group.

    def __init__(self, groupID, accountIDs, godID):
        # groupID is the group's unique hash ID.
        # projIDs and accountIDs are sets of project and account hashes.
        # godID is the account hash of the group god.
        self.groupID = groupID
        self.projIDs = set()
        self.accountIDs = accountIDs
        self.godID = godID

    def add_project(self, projectID):
        self.projIDs.add(projectID)

    def remove_project(self, projectID):
        self.projIDs.remove(projectID)

    def add_user(self, userID):
        self.accountIDs.add(userID)

    def remove_user(self, userID):
        self.accountIDs.remove(userID)


class Comment:
    ## Object for comments on users' codes, be they in-line or general.

    def __init__(self,text,time,hashID,which_file,which_line=-1):
        self.text = text
        self.time = time
        self.last_edited = time

        self.accountID = accountID
        self.projectID = projectID
        self.revisionID = revisionID

        self.file_name = file_name
        self.line_number = line_number

    def edit(self,new_text,edit_time):
        ## To be called when a user edits a comment.
        self.text = new_text
        self.last_edited = edit_time

    def delete(self):
        ## To be called when a user deletes their comment.
        ## To be implemented.
        pass
