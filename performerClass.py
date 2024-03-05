from db_connect import execute_get_sql_query


def get_performers():
    sql_query = 'SELECT performer_id FROM performers order by id'
    return execute_get_sql_query(sql_query)


def get_performer_by_category(category):
    sql_query = 'SELECT * FROM performers where category = %s'
    params = (category,)
    return execute_get_sql_query(sql_query, params)[0]


def get_performer_by_id(id):
    sql_query = 'SELECT * FROM performers where id = %s'
    params = (id,)
    return execute_get_sql_query(sql_query, params)


def list_categories():
    sql_query = 'SELECT category FROM performers'
    categories = execute_get_sql_query(sql_query)
    categories_result = []
    for category in categories:
        categories_result.append(category[0])
    return categories_result


def get_all_anonymous_appeals_by_id_performer(id_performer, status_1, status_2):
    sql_query = (
        'SELECT * from appeals WHERE is_appeal_anon=TRUE and id_performer=%s and (status=%s or status=%s)  order by id'
    )
    params = (str(id_performer), status_1, status_2,)
    appeals = execute_get_sql_query(sql_query, params)
    if appeals:
        return appeals
    return None


def get_performers_id():
    sql_query = "SELECT DISTINCT performer_id from performers"
    performers_id_result = execute_get_sql_query(sql_query)
    performers_id = []
    for id in performers_id_result:
        performers_id.append(id[0])
    return performers_id


def get_email_by_category(category):
    sql_query = "SELECT email from performers where category = %s"
    params = (category,)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_performer_id_by_category(performer_id):
    sql_query = "SELECT id from performers where category = %s"
    params = (performer_id,)
    performer_id = execute_get_sql_query(sql_query, params)
    if performer_id:
        return performer_id[0][0]
    else:
        return None


def get_performer_id(category):
    sql_query = "SELECT id from performers where category = %s"
    params = (category,)
    category = execute_get_sql_query(sql_query, params)
    if category:
        return category[0][0]
    else:
        return None


def get_performer_id_by_id(id):
    sql_query = "SELECT performer_id from performers where id=%s"
    params = (id,)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_categories_by_parentcategory(parent_category):
    sql_query = "SELECT category from performers where parent_category = %s"
    params = (parent_category,)
    categories = execute_get_sql_query(sql_query, params)
    categories_ = []
    for category in categories:
        categories_.append(category[0])
    return categories_


def get_subcategories(category):
    sql_query = "SELECT subcategory from performers where category = %s"
    params = (category,)
    subcategories = execute_get_sql_query(sql_query, params)
    subcategories_ = []
    for subcategory in subcategories:
        subcategories_.append(subcategory[0])
    return subcategories_


def get_subsubcategories_by_subcategory(subcategory):
    sql_query = "SELECT subsubcategory from performers where subcategory = %s"
    params = (subcategory,)
    subsubcategories = execute_get_sql_query(sql_query, params)
    subsubcategories_ = []
    for subcategory in subsubcategories:
        subsubcategories_.append(str(subcategory[0]).strip())
    return subsubcategories_


def get_regions():
    sql_query = "SELECT category from performers where id > 12 and id < 30"
    regions = execute_get_sql_query(sql_query)
    regions_ = []
    for region in regions:
        regions_.append(region[0])
    return regions_


def get_performer_by_category_and_subcategory(category, subcategory):
    sql_query = "select * from performers where category = %s and subcategory = %s"
    params = (category, subcategory,)
    return execute_get_sql_query(sql_query, params)


def get_performer_by_subsubcategory(subsubcategory):
    sql_query = "select * from performers where subsubcategory = %s"
    params = (subsubcategory,)
    return execute_get_sql_query(sql_query, params)


def get_performers_():
    sql_query = "select id, category, subcategory, subsubcategory from performers"
    return execute_get_sql_query(sql_query)


def get_subcategories_():
    sql_query = "select subcategory from performers"
    return execute_get_sql_query(sql_query)


def get_performer_ids(performer_id):
    sql_query = "SELECT id FROM performers WHERE performer_id = %s"
    params = (performer_id,)
    ids = execute_get_sql_query(sql_query, params)
    ids_ = []
    for id in ids:
        ids_.append(str(id[0]))
    return ids_
