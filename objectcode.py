### Definitions for the various objects necessary for Community of Practice.

#Since our objects are doubly-linked, Greg and I have created a few conventions for initializing them.
#Initialization order: Account => Group => Project => Revision => File => Comment => Borrow

import pdb

class Account(object):
    ## Object for an individual user's account.

    def __init__(self, accountID, username, password, avatar):
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
    def __init__(self, date_taken, project_from, revision_from_, file_from, line_range, line_offsets):
        self.date_taken = date_taken
        self.project_from = project_from
        self.revision_from = revision_from
        self.file_from = file_from
        #line_range is a tuple of 2 line numbers, or 2 of the same line number for single-line borrows
        self.line_range = line_range
        #line_offsets is a tuple of 2 offsets representing distance from start of line
        self.line_offsets = line_offsets

    def link_borrow(self,project_to,revision_to,file_to):
        self.project_to=project_to
        self.revision_to=revision_to
        self.file_to=file_to

    def get_text(self):
        #returns the borrowed text
        text=''
        codefile = open("testingtk3.py")
        count=0
        while 1:
            line = codefile.readline()
            if not line:
                break
            if count==self.line_range[0]:
                break
            count+=1

        if count==self.line_range[1]:
            text+=line[self.line_offsets[0]:self.line_offsets[1]]
        else:
            text+=line[self.line_offsets[0]:]
            line = codefile.readline()
            while (count+1)<self.line_range[1] and line:
                count+=1
                text+=line
                line = codefile.readline()
            text+=line[:self.line_offsets[1]]
        return text



class Project(object):
    def __init__(self,title,description, projID, parentID, numrevs, groupID):
        self.title=title
        self.description=description
        self.projID = projID
        self.parentID = parentID
        self.groupID = groupID

        self.revisions = [] ##list of revisions
        for i in range(numrevs):
            rev=Revision(self,i,files={})
            self.revisions.append(rev)

        self.children = set()
        self.borrows = set() ##set of borrows

        self.head = None

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

    def create_revision(self):
        nextIndex = len(revisions) + 1
        self.revisions[nextIndex] = self.head

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

    def __init__(self, project, rev_number, file_name, content):
        self.project = project
        self.rev_number = rev_number
        self.file_name = file_name
        self.content = content
        self.project.revisions[rev_number].files[file_name]=self
        self.comments=[]


class Group(object):
    ## Object which defines a user-group.

    def __init__(self,groupID,godID,title,description="",accountIDs=set(),projIDs=set()):
        # groupID is the group's unique hash ID.
        # projIDs and accountIDs are sets of project and account hashes.
        # godID is the account hash of the group god.
        self.title=title
        self.description=description
        self.groupID = groupID
        self.projIDs = projIDs
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


class Comment(object):
    ## Object for comments on users' codes, be they in-line or general.

    def __init__(self,text,time,project,rev,whichfile,account,linenum=-1):
        self.text = text
        self.time = time
        self.last_edited = time #implement later?
        self.project=project
        self.rev=rev
        self.file=whichfile
        self.account = account
        self.linenum=linenum

    def edit(self,new_text,edit_time):
        ## To be called when a user edits a comment.
        self.text = new_text
        self.last_edited = edit_time

    def delete(self):
        ## To be called when a user deletes their comment.
        ## To be implemented.
        pass

class Revision:

    def __init__(self,project,rev_number,files={}):
        self.project=project
        self.rev_number=rev_number
        self.files=files
    def __str__(self):
        return str(self.rev_number)

#Creating a new Head with a previous revision specified copies that revision into the Head for editing
class Head(Revision):

    def __init__(self,project=None,rev_number=None,files={},prevrev=None):
        if not (prevrev is None):
            Revision.__init__(self,prevrev.project,prevrev.rev_number,prevrev.files)
        else:
            Revision.__init__(self,project,rev_number,files)

    def add_file(self,newfile):
        self.files.append(newfile)
