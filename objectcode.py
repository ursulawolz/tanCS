### Definitions for the various objects necessary for Community of Practice.

#Since our objects are doubly-linked, Greg and I have created a few conventions for initializing them.
#Initialization order: Account => Group => Project => Revision => File => Comment => Borrow

import pdb
import copy
import datetime

class Account(object):
    ## Object for an individual user's account.

    def __init__(self, accountID, username, password, avatar, date_time):
        self.accountID = accountID
        self.username = username
        self.password = password
        self.avatar = avatar
        self.date_time=date_time

        self.group_list = {}

    def add_group(self, new_group):
        ## Adds a new group to the user's list of groups.
        self.group_list[new_group.groupID]=new_group

    def remove_group(self, group):
        ## Removes a group from the user's list of groups.
        del self.project_list[group.groupID]

class Borrow:
    def __init__(self, borrow_id, date_taken, project_from, revision_from, file_from, line_range, line_offsets):
        self.date_taken = date_taken
        self.project_from = project_from
        self.revision_from = revision_from
        self.file_from = file_from
        #line_range is a tuple of 2 line numbers, or 2 of the same line number for single-line borrows
        self.line_range = line_range
        #line_offsets is a tuple of 2 offsets representing distance from start of line
        self.line_offsets = line_offsets
        self.borrow_id=borrow_id

    def link_borrow(self,project_to,revision_to,file_to):
        self.project_to=project_to
        self.revision_to=revision_to
        self.file_to=file_to
        self.project_to.add_borrow(self)

    def get_text(self):
        #returns the borrowed text
        text=''
        codefile = open(self.project_from.revisions[self.revision_from].files[self.file_from].file_name)
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
    def __init__(self,title,description, projID, parentID, numrevs, groupID,times):
        self.title=title
        self.description=description
        self.projID = projID
        self.parentID = parentID
        self.groupID = groupID
        self.times = times

        self.revisions = [] ##list of revisions
        for i in range(numrevs):
            rev=Revision(self,i,datetime.date.today(),files={})
            self.revisions.append(rev)

        self.children = {}
        self.borrows = set() ##set of borrows

        self.locked = 0
        self.tags = set()

    def add_child(self, child):
        self.children[child.projID]=child

    def remove_child(self, child):
        del self.children[child.projID]

    def add_borrow(self, lender):
        self.borrows.add( lender )

    def remove_borrow(self, lender):
        self.borrows.remove( lender )

    def create_revision(self):
        #self.revisions.insert(len(self.revisions)-1,copy.deepcopy(self.revisions[-1]))
        copy.deepcopy(self.revisions[-1])

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

    def __init__(self, project, rev_number, file_name, content, date_created):
        self.project = project
        self.rev_number = rev_number
        self.file_name = file_name
        self.content = content
        self.project.revisions[rev_number].files[file_name]=self
        self.comments=[]
        self.date_created=date_created

    def __deepcopy__(self,memodict):
        newobj=File(self.project,self.rev_number+1,self.file_name,self.content,self.date_created)
        return newobj


class Group(object):
    ## Object which defines a user-group.

    def __init__(self,groupID,godID,title,date_formed,description="",accounts={},projects={}):
        # groupID is the group's unique hash ID.
        # projIDs and accountIDs are sets of project and account hashes.
        # godID is the account hash of the group god.
        self.title=title
        self.description=description
        self.groupID = groupID
        self.projects = projects
        self.accounts = accounts
        self.godID = godID
        self.date_formed=date_formed

    def add_project(self, project):
        self.projects[project.projID]=project

    def remove_project(self, project):
        del self.projects[project.projID]

    def add_user(self, user):
        self.accounts[user.accountID]=user

    def remove_user(self, user):
        del self.accounts[user.accountID]


class Comment(object):
    ## Object for comments on users' codes, be they in-line or general.

    def __init__(self,text,time,project,rev,whichfile,account,linenum=-1):
        self.text = text
        self.time = time
        self.project=project
        self.rev=rev
        self.file=whichfile
        self.account = account
        self.linenum=int(float(linenum))

    def edit(self,new_text,edit_time):
        ## To be called when a user edits a comment.
        self.text = new_text
        self.last_edited = edit_time

    def delete(self):
        ## To be called when a user deletes their comment.
        ## To be implemented.
        pass

    def __deepcopy__(self,memodict):
        return Comment(self.text,self.time,self.project,self.rev+1,self.whichfile,self.account,self.linenum)

class Revision:

    def __init__(self,project,rev_number,time_made,files={}):
        self.project=project
        self.rev_number=rev_number
        self.files=files
        self.time_made=time_made
    def __str__(self):
        return str(self.rev_number)
    def __deepcopy__(self,memodict):
        newobj=Head(self.project,self.rev_number+1,datetime.date.today())
        self.project.revisions.append(newobj)
        newobj.files=copy.deepcopy(self.files,memodict)
        self=Revision(self.project,self.rev_number,datetime.date.today(),self.files)
        self.project.revisions[self.rev_number]=self
        return newobj

#Creating a new Head with a previous revision specified copies that revision into the Head for editing
class Head(Revision):

    def __init__(self,project=None,rev_number=None,time_made=None,files={},prevrev=None):
        if not (prevrev is None):
            Revision.__init__(self,prevrev.project,prevrev.rev_number,prevrev.time_made,prevrev.files)
        else:
            Revision.__init__(self,project,rev_number,time_made,files)

    def add_file(self,newfile):
        self.files.append(newfile)