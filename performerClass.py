from db_connect import execute_get_sql_query


def get_performers():
    sql_query = 'SELECT performer_id FROM performers order by id'
    return execute_get_sql_query(sql_query)


def get_performer_by_category(category):
    sql_query = 'SELECT * FROM performers where category = %s'
    params = (category,)
    return execute_get_sql_query(sql_query, params)[0]


def list_categories():
    sql_query = 'SELECT category FROM performers WHERE id <> 5'
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


def get_performer_id_by_category(category):
    sql_query = "SELECT performer_id from performers where category = %s"
    params = (category,)
    category = execute_get_sql_query(sql_query, params)
    if category:
        return category[0][0]
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


def get_subcategories(parent_category):
    sql_query = "SELECT category from performers where parent_category = %s"
    params = (parent_category,)
    categories = execute_get_sql_query(sql_query, params)
    categories_ = []
    for category in categories:
        categories_.append(category[0])
    return categories_


def get_regions():
    sql_query = "SELECT category from performers where id > 12"
    regions = execute_get_sql_query(sql_query)
    regions_ = []
    for region in regions:
        regions_.append(region[0])
    return regions_
