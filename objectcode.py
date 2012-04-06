### Definitions for the various objects necessary for Community of Practice.

class Account:
    ## Object for an individual user's account.

    def __init__(self,hashID,username,password,avatar):
        self.hashID = hashID
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


class Project:
    def __init__(self, projID, parentID, groupID):
        self.projID = projID
        self.parentID = parentID
        self.groupID = groupID

        self.children = set()
        self.borrows = set()

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


class Group:
    ## Object which defines a user-group.

    def __init__(self, groupID, projIDs, accountIDs, godID):
        # groupID is the group's unique hash ID.
        # projIDs and accountIDs are each sets of project and account hashes.
        # godID is the account hash of the group god.
        self.groupID = groupID
        self.projIDs = projIDs
        self.accountIDs = accountIDs
        self.godID = godID



class Comment:
    ## Object for comments on users' codes, be they in-line or general.

    def __init__(self,text,time,hashID,which_file,which_line=-1):
        self.text = text
        self.time = time
        self.hashID = hashID
        self.which_file = which_file
        if which_line != -1:
            self.which_line == which_line
        self.lastEdited = -1

    def edit(self,new_text,edit_time):
        ## To be called when a user edits a comment.
        self.text = new_text
        self.lastEdited = edit_time

    def delete(self):
        ## To be called when a user deletes their comment.
        ## To be implemented.
        pass
