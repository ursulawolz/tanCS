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
