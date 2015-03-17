import test

import json

import uuid



def index():
    #db.auth_user.drop()
    if auth.user:
        name = auth.user.first_name
        response.flash = T("Logged in as %s"%(name))
    else:
        redirect(URL('default', 'login'))
    return dict()

@auth.requires_login()  # eventually this will probably have to be requires_membership(class.teachers) or something
def create_test():
    """
    Test creation controller
    If form succeeds, creates test and pushes it to test_list

    Future:
    Will be
    Must be a teacher for course
    :return:
    """

    questions = {}

    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY()),
        Field('info', requires=IS_NOT_EMPTY()),
    )


    return dict(form=form, questions=questions)


def new_test():
    import pdb
    data = request.post_vars

    return dict(data=data)

def create_class():
        # used for testing. deletes all data from tables
    #db.classes.drop()
    form = SQLFORM.factory(
                        Field('class_name', requires=IS_NOT_EMPTY()),
                        Field('description', 'text', requires=IS_NOT_EMPTY()),
                        Field('start_date', 'date',requires=IS_NOT_EMPTY()),
                        Field('end_date', 'date',requires=IS_NOT_EMPTY()),
                        Field('teacher_emails', 'list:string',requires=IS_EMAIL()),
                        Field('student_emails', 'list:string',requires=IS_EMAIL())
                        
                        )


    #form.add_button('Cancel', URL('default', 'index', args=[title]))

    if form.process().accepted:
        new_class_token = uuid.uuid4()
        response.flash = T(str(new_class_token))
        class_id = db.classes.insert(name=form.vars.class_name, info=form.vars.description,
                    start_date=form.vars.start_date, end_date=form.vars.end_date,
                    teachers=form.vars.teacher_emails, students=form.vars.student_emails)
                    #class_token = new_class_token)
        
        redirect(URL('default', 'view_class', args=[class_id]))




    return dict(form=form)


def browse_classes():
    return dict()



@auth.requires_login()
def view_class():
    """
    if user == teacher_emails
    info
    Tests
    students

    add/drop students
    create test

    """

    home_button = A('Home', _class='btn', _href=URL('default', 'index'))

    show_all = request.args(0) == 'all'
    if show_all:
        # view all classes
        clase = SQLFORM.grid(db.classes,
                             user_signature=False, deletable=False, csv=False, editable=False,
                             details=False, create=False, searchable=False, sortable=False,
                             fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                     db.classes.teachers, db.classes.test_ids, db.classes.class_avg])
        display_button = A('See My Classes', _class='btn', _href=('default', 'view_class'))
    else:
        # view only my enrolled classes
        clase = SQLFORM.grid(db.classes.students.like("%"+auth.user.email+"%"),
                             user_signature=False, deletable=False, csv=False, editable=False,
                             details=False, create=False, searchable=False, sortable=False,
                             fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                     db.classes.teachers, db.classes.test_ids, db.classes.class_avg])
        display_button = A('See all', _class='btn', _href=URL('default', 'view_class', args=['all']))

    return dict(form = clase, display_button = display_button, home_button=home_button)


def test_list():
    """
    List of Tests

    Future: should be based on the classes you are in
    :return:
    """
    return dict()


# login page
def login():
    response.flash = T("Login Page")
    form = auth.login()
    register_button = A('Register', _class='btn', _href=URL('default', 'register'))
    return dict(form=form, register_button=register_button)


# register page
def register():
    response.flash = T("Register Page")
    form=auth.register()
    back_button = A('Back', _class='btn', _href=URL('default', 'login'))
    return dict(form=form, back_button=back_button)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
