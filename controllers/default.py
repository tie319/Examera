import test

import json

import uuid

import ast


def index():
    #db.auth_user.drop()
    if auth.user:
        name = auth.user.first_name
        response.flash = T("Logged in as %s"%(name))
        home_button = A('Home', _class='btn', _href=URL('default', 'index'))
        classes_taught = ""

        show_all = request.args(0) == 'all'
        if show_all:
            # view all classes
            clase = SQLFORM.grid(db.classes,
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, sortable=False,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.teachers, db.classes.test_ids, db.classes.class_avg])
            clase.element('.web2py_counter',replace=None)
            display_button = A('See My Classes', _class='btn', _href=('default', 'view_class'))
        else:
            # view only my enrolled classes
            def edit_button(row):
                b = ''
                b = A('Edit', _class='btn', _href=URL('default', 'edit_class', args=[row.id], user_signature=True))
                return b
            links = [dict(header='', body=edit_button)]

            clase = SQLFORM.grid(db.classes.students.like("%"+auth.user.email+"%"),
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, searchable=False, sortable=False,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.teachers, db.classes.test_ids, db.classes.class_avg])
            clase.element('.web2py_counter',replace=None)
            classes_taught = SQLFORM.grid(db.classes.teachers.like("%"+auth.user.email+"%"),
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, searchable=False, sortable=False,
                                 links=links,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.students, db.classes.test_ids, db.classes.class_avg])
            classes_taught.element('.web2py_counter',replace=None)
            display_button = A('See All Classes', _class='btn', _href=URL('default', 'view_class', args=['all']))

        return dict(classes_taught = classes_taught, form = clase, display_button = display_button, home_button=home_button)
    else:
        redirect(URL('default', 'login'))
    return dict()

@auth.requires_login()
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
    post_data = request.post_vars

    for key in post_data.keys():
        test_string = key

    test_data = json.loads(test_string)

    old_test = "undefined"

    name = test_data['test_name']

    creator = auth.user.email

    query = db.tests.id > 0
    query &= db.tests.creator == creator
    query &= db.tests.name == name

    old_tests = db(query).count()

    if old_tests > 0:
        old_test = db(query).select().first()

    update = False
    if old_test == "undefined":
        db.tests.insert(name=name, creator=creator, test_data=test_data)
    else:
        old_test.update(test_data=test_data)
        update = True

    return dict(update=update)


def take_test():
    # creator = "schfiftysix@yahoo.com"
    # name = "This is a test"
    # query = db.tests.id > 0
    # query &= db.tests.creator == creator
    # query &= db.tests.name == name

    class_id = 5

    query = db.tests.id == 3

    old_tests = db(query).count()

    test_data = "undefined"
    test_id = "undefined"
    if old_tests > 0:
        mytest = db(query).select().first()
        test_unparsed = mytest.test_data
        test_id = mytest.id
        test_data = ast.literal_eval(test_unparsed)
    return dict(test_data=test_data, test_id=test_id, class_id=class_id)


def new_test_submission():
    post_data = request.post_vars

    for key in post_data.keys():
        test_string = key

    test_data = json.loads(test_string)

    old_test = "undefined"

    test_id = test_data['test_id']

    class_id = test_data['class_id']

    answers = test_data['questions']

    test_taker = auth.user.email

    db.test_submissions.insert(test_taker=test_taker, answers=answers, test_id=test_id, class_id=class_id)

    # query = db.classes.id == class_id
    #
    # submitted_tests = db(query).select().first()
    #
    # submitted_tests_unparsed = submitted_tests.submitted_tests
    #
    # if submitted_tests_unparsed is None:
    #     new_dict = dict(test_id=test_id, test_taker=test_taker, questions=questions)
    #     submitted_array = [new_dict]
    #
    # else:
    #     new_dict = dict(test_id=test_id, test_taker=test_taker, questions=questions)
    #     submitted_array = submitted_tests_unparsed
    #     submitted_array.append(new_dict)
    #
    # submitted_tests.update(submitted_tests=submitted_array)

    return dict()


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
        teach_list = []
        teach_list.append(form.vars.teacher_emails)
        teach_list.append(auth.user.email)
        class_id = db.classes.insert(name=form.vars.class_name, info=form.vars.description,
                    start_date=form.vars.start_date, end_date=form.vars.end_date,
                    teachers=teach_list, students=form.vars.student_emails)
                    #class_token = new_class_token)
        
        redirect(URL('default', 'view_class', args=[class_id]))




    return dict(form=form)


def browse_classes():
    return dict()

@auth.requires_login()
def edit_class():
    clase = db(db.classes.id==request.args(0)).select().first()

    if auth.user.email in clase.teachers:
        form = SQLFORM.factory(
                    Field('class_name', default=clase.name, requires=IS_NOT_EMPTY()),
                    Field('description', 'text', default=clase.info, requires=IS_NOT_EMPTY()),
                    Field('start_date', 'date', default=clase.start_date, requires=IS_NOT_EMPTY()),
                    Field('end_date', 'date', default=clase.end_date, requires=IS_NOT_EMPTY()),
                    Field('teacher_emails', default=clase.teachers),
                    Field('student_emails', default=clase.students)

                    )
        if form.process().accepted:
            clase.update_record(name=form.vars.class_name, info=form.vars.description,
                    start_date=form.vars.start_date, end_date=form.vars.end_date,
                    teachers=form.vars.teacher_emails, students=form.vars.student_emails)

            redirect(URL('default', 'view_class', args=[class_id]))
    return dict(form=form)

@auth.requires_login()
def edit_class():
    clase = db(db.classes.id==request.args(0)).select().first()

    if auth.user.email in clase.teachers:
        form = SQLFORM.factory(
                    Field('class_name', default=clase.name, requires=IS_NOT_EMPTY()),
                    Field('description', 'text', default=clase.info, requires=IS_NOT_EMPTY()),
                    Field('start_date', 'date', default=clase.start_date, requires=IS_NOT_EMPTY()),
                    Field('end_date', 'date', default=clase.end_date, requires=IS_NOT_EMPTY()),
                    Field('teacher_emails', 'list:string'),
                    Field('student_emails', 'list:string')
                    
                    )
        if form.process().accepted:
            clase.update_record(name=form.vars.class_name, info=form.vars.description,
                    start_date=form.vars.start_date, end_date=form.vars.end_date,
                    teachers=form.vars.teacher_emails, students=form.vars.student_emails)

            redirect(URL('default', 'view_class', args=[class_id]))

        return dict(form=form)
    return dict(form=form)

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
