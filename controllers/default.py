import test

import json

import uuid

import ast


def index():
    #db.tests.drop()
    if auth.user:
        classes_taught = ""

        add = request.args(0) == 'add'
        if add:
            test_name = request.args(1)
            class_name = request.args(2)
            response.flash = T(str(test_name + ' was added to ' + class_name))

        #db.test_submissions.insert(test_taker='tmarshik@gmail.com', class_id=5,
         #           test_id=1, answers=['one', 'two'],
          #          grade=.90)

        show_all = request.args(0) == 'all'
        if show_all:
            # view all classes
            clase = SQLFORM.grid(db.classes,
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, searchable=False, sortable=False,
                                 maxtextlength=1000,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.teachers, db.classes.students])
            clase.element('.web2py_counter',replace=None)
            display_button = A('See My Classes', _class='btn', _href=('default', 'view_class'))
        else:
            # view only my enrolled classes
            def edit_button(row):
                b = A('Edit', _class='btn', _href=URL('default', 'edit_class', args=[row.id]))
                return b
            def take_test_button(row):
                b = A('Tests', _class='btn', _href=URL('default', 'test_page', args=[row.id]))
                return b
            links = [dict(header='', body=edit_button)]
            links_student = [dict(header='', body=take_test_button)]

            clase = SQLFORM.grid(db.classes.students.like("%"+auth.user.email+"%"),
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, searchable=False, sortable=False,
                                 links=links_student, maxtextlength=1000,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.teachers])
            clase.element('.web2py_counter',replace=None)
            classes_taught = SQLFORM.grid(db.classes.teachers.like("%"+auth.user.email+"%"),
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, searchable=False, sortable=False,
                                 links=links, maxtextlength=1000,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.students])
            classes_taught.element('.web2py_counter',replace=None)
            display_button = A('See All Classes', _class='btn', _href=URL('index', args=['all']))

        return dict(classes_taught = classes_taught, form = clase, display_button = display_button)
    else:
        redirect(URL('default', 'login'))
    return dict()


def test_page():
    class_id = request.args(0)
    selected_class = db(db.classes.id == class_id).select().first()
    test_name_list = selected_class.test_names
    test_id_list = selected_class.test_ids
    class_name = selected_class.name
    query = db.test_submissions.test_taker == auth.user.email
    query &= db.test_submissions.class_id == class_id
    scores = db(query).select()
    scores_list = []
    if test_id_list is not None:
        for test_id in test_id_list:
            this_score = 0.0
            for score in scores:
                if test_id == int(score.test_id):
                    if score.grade > this_score:
                        this_score = score.grade
            scores_list.append(this_score*100)

    return dict(test_name_list=test_name_list, test_id_list=test_id_list, class_id=class_id, class_name=class_name, scores_list=scores_list)

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

    post_url = URL('default', 'new_test')

    questions = {}

    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY()),
        Field('info', requires=IS_NOT_EMPTY()),
    )

    return dict(form=form, questions=questions, post_url=post_url)


def edit_test():
    post_url = URL('default', 'new_test')
    test_id = request.args(0)
    mytest = db(db.tests.id == test_id).select().first()
    test_name = mytest.name
    test_unparsed = mytest.test_data
    test_data = ast.literal_eval(test_unparsed)
    return dict(test_data=test_data, test_name=test_name, post_url=post_url)


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
        old_test.update_record(test_data=test_data)
        update = True

    return dict(update=update)


def take_test():

    class_id = request.args(1)

    post_url = URL('default', 'new_test_submission')

    query = db.tests.id == request.args(0)

    old_tests = db(query).count()

    test_data = "undefined"
    test_id = "undefined"
    load_page = False
    if old_tests > 0:
        load_page = True
        mytest = db(query).select().first()
        test_unparsed = mytest.test_data
        test_id = mytest.id
        test_data = ast.literal_eval(test_unparsed)
    return dict(test_data=test_data, test_id=test_id, class_id=class_id, post_url=post_url, load_page=load_page)


def new_test_submission():
    post_data = request.post_vars

    test_string = "undefined"

    for key in post_data.keys():
        test_string = key

    test_data = json.loads(test_string)

    old_test = "undefined"

    test_id = test_data['test_id']

    class_id = test_data['class_id']

    answers = test_data['questions']

    test_taker = auth.user.email

    sub_id = db.test_submissions.insert(test_taker=test_taker, answers=answers, test_id=test_id, class_id=class_id)

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

    grade_sub(sub_id, test_id)

    return dict()


def grade_sub(sub_id, test_id):
    sub = db(db.test_submissions.id==sub_id).select().first()
    test = db(db.tests.id==test_id).select().first()

    test_data = ast.literal_eval(test['test_data'])

    correct_list = []

    for question in test_data['questions']:
        correct_list += question['correct_answer']

    num_ques = len(correct_list)

    total_correct = 0
    for i in range(0, num_ques):
        if sub.answers[i] == correct_list[i]:
            total_correct += 1

    grade = float(total_correct)/float(num_ques)
    sub.update_record(grade=grade)
    return


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

    if form.process().accepted:
        teach_list = []
        teach_list.append(form.vars.teacher_emails)
        teach_list.append(auth.user.email)
        class_id = db.classes.insert(name=form.vars.class_name, info=form.vars.description,
                    start_date=form.vars.start_date, end_date=form.vars.end_date,
                    teachers=teach_list, students=form.vars.student_emails)
                    #class_token = new_class_token)
        
        redirect(URL('index'))
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
                    Field('teacher_emails', 'list:string'),
                    Field('student_emails', 'list:string')

                    )
        if form.process().accepted:
            clase.update_record(name=form.vars.class_name, info=form.vars.description,
                    start_date=form.vars.start_date, end_date=form.vars.end_date,
                    teachers=form.vars.teacher_emails, students=form.vars.student_emails)

            redirect(URL('index'))
    return dict(form=form)

def test_list():
    """
    List of Tests

    Future: should be based on the classes you are in
    :return:
    """
    def add_test_button(row):
        b = A('Add Test to Class', _class='btn', _href=URL('default', 'add_test_to_class', args=[row.id, row.name]))
        return b
    def edit_button(row):
        b = A('Edit Test', _class='btn', _href=URL('default', 'edit_test', args=[row.id]))
        return b
    links = [dict(header='', body=add_test_button),
             dict(header='', body=edit_button)]
    form = SQLFORM.grid(db.tests.creator == auth.user.email,
                        user_signature=False, csv=False, editable=False,
                        details=False, create=False, searchable=False, sortable=False,
                        links=links,
                        fields=[db.tests.name])
    form.element('.web2py_counter',replace=None)
    return dict(form=form)


def add_test_to_class():
    test_id = request.args(0)
    test_name = request.args(1)
    def select_button(row):
        b = A('Select', _class='btn', _href=URL('default', 'backend_add_test', args=[row.id, test_id, test_name]))
        return b
    links = [dict(header='', body=select_button)]
    classes_taught = SQLFORM.grid(db.classes.teachers.like("%"+auth.user.email+"%"),
                                 user_signature=False, deletable=False, csv=False, editable=False,
                                 details=False, create=False, searchable=False, sortable=False,
                                 links=links, maxtextlength=1000,
                                 fields=[db.classes.name, db.classes.info, db.classes.start_date, db.classes.end_date,
                                         db.classes.test_names])
    classes_taught.element('.web2py_counter', replace=None)
    return dict(classes_taught=classes_taught)

def backend_add_test():
    class_id = request.args(0)
    test_id = request.args(1)
    test_name = request.args(2)
    selected_class = db(db.classes.id == class_id).select().first()
    class_name = selected_class.name
    if selected_class.test_ids is None:
        test_id_list = []
    else:
        test_id_list = selected_class.test_ids
    test_id_list.append(test_id)
    selected_class.update_record(test_ids=test_id_list)
    if selected_class.test_names is None:
        test_name_list = []
    else:
        test_name_list = selected_class.test_names
    test_name_list.append(str(test_name))
    selected_class.update_record(test_names=test_name_list)
    redirect(URL('default', 'index', args=['add', test_name, class_name]))

# login page
def login():
    message = "log in as 'tyler@gmail.com' with password 'tyler' to demo this site"
    form = auth.login()
    register_button = A('Register', _class='btn', _href=URL('default', 'register'))
    return dict(form=form, register_button=register_button, message = message)


# register page
def register():
    form = auth.register()
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
