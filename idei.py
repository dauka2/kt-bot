import psycopg2
from db_connect import execute_set_sql_query, execute_get_sql_query

def get_id_from_idea(user_id):
    sql_query = 'SELECT id FROM ideas WHERE user_id = %s ORDER BY id DESC LIMIT 1'
    params = (str(user_id),)
    result = execute_get_sql_query(sql_query, params)
    return result[0][0]

def get_id_from_researches(user_id):
    sql_query = 'SELECT id FROM researches WHERE user_id = %s ORDER BY id DESC LIMIT 1'
    params = (str(user_id),)
    result = execute_get_sql_query(sql_query, params)
    return result[0][0]

def insert_into_idei(user_id):
    sql_query = 'INSERT INTO ideas (user_id) VALUES (%s)'
    params = (str(user_id),)
    execute_set_sql_query(sql_query, params)

def insert_into_researches(user_id):
    sql_query = 'INSERT INTO researches (user_id) VALUES (%s)'
    params = (str(user_id),)
    execute_set_sql_query(sql_query, params)

def set_format(idea_id, format_value):
    sql_query = "UPDATE ideas SET format = %s WHERE id = %s"
    params = (format_value, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)
    
def set_kogo_kasaetsya(idea_id, for_who):
    sql_query = 'UPDATE ideas SET for_who = %s WHERE id = %s'
    params = (for_who, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_perimetr(idea_id, perimetr):
    sql_query = 'UPDATE ideas SET perimetr = %s WHERE id = %s'
    params = (perimetr, str(idea_id),)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_auditory(idea_id, auditory):
    sql_query = 'UPDATE ideas SET auditory = %s WHERE id = %s'
    params = (auditory, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_otrasl_primeneniya(idea_id, otrasl_primeneniya):
    sql_query = 'UPDATE ideas SET otrasl_primeneniya = %s WHERE id = %s'
    params = (otrasl_primeneniya, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_gotovnost_idei(idea_id, gotovnost_idei):
    sql_query = 'UPDATE ideas SET gotovnost_idei = %s WHERE id = %s'
    params = (gotovnost_idei, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_comanda(idea_id, comanda):
    sql_query = 'UPDATE ideas SET comanda = %s WHERE id = %s'
    params = (comanda, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_potential_effect(idea_id, potential_effect):
    sql_query = 'UPDATE ideas SET potential_effect = %s WHERE id = %s'
    params = (potential_effect, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_finance(idea_id, finance):
    sql_query = 'UPDATE ideas SET finance = %s WHERE id = %s'
    params = (finance, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_idea(idea_id, idea):
    sql_query = 'UPDATE ideas SET idea = %s WHERE id = %s'
    params = (idea, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_category(idea_id, idea):
    sql_query = 'UPDATE ideas SET category = %s WHERE id = %s'
    params = (idea, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_city(idea_id, city):
    sql_query = 'UPDATE ideas SET city = %s WHERE id = %s'
    params = (city, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

# ресерчи

def set_format_r(idea_id, format):
    sql_query = 'UPDATE researches SET format = %s WHERE id = %s'
    params = (format, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_kogo_kasaetsya_r(idea_id, for_who):
    sql_query = 'UPDATE researches SET for_who = %s WHERE id = %s'
    params = (for_who, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_perimetr_r(idea_id, perimetr):
    sql_query = 'UPDATE researches SET perimetr = %s WHERE id = %s'
    params = (perimetr, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_auditory_r(idea_id, auditory):
    sql_query = 'UPDATE researches SET auditory = %s WHERE id = %s'
    params = (auditory, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_research_direction(idea_id, research_direction):
    sql_query = 'UPDATE researches SET research_direction = %s WHERE id = %s'
    params = (research_direction, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_stage(idea_id, stage):
    sql_query = 'UPDATE researches SET stage = %s WHERE id = %s'
    params = (stage, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_comanda_r(idea_id, comanda):
    sql_query = 'UPDATE researches SET comanda = %s WHERE id = %s'
    params = (comanda, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_ozhidaemyi_effect(idea_id, ozhidaemyi_effect):
    sql_query = 'UPDATE researches SET ozhidaemyi_effect = %s WHERE id = %s'
    params = (ozhidaemyi_effect, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_finance_r(idea_id, finance):
    sql_query = 'UPDATE researches SET finance = %s WHERE id = %s'
    params = (finance, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_research_idea(idea_id, idea):
    sql_query = 'UPDATE researches SET idea = %s WHERE id = %s'
    params = (idea, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_category_r(idea_id, idea):
    sql_query = 'UPDATE researches SET category = %s WHERE id = %s'
    params = (idea, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def set_city_r(idea_id, idea):
    sql_query = 'UPDATE researches SET city = %s WHERE id = %s'
    params = (idea, idea_id)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)
# Геттеры

def get_format(idea_id):
    sql_query = "SELECT format FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_kogo_kasaetsya(idea_id):
    sql_query = "SELECT for_who FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_perimetr(idea_id):
    sql_query = "SELECT perimetr FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_auditory(idea_id):
    sql_query = "SELECT auditory FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_otrasl_primeneniya(idea_id):
    sql_query = "SELECT otrasl_primeneniya FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_gotovnost_idei(idea_id):
    sql_query = "SELECT gotovnost_idei FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_comanda(idea_id):
    sql_query = "SELECT comanda FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_potential_effect(idea_id):
    sql_query = "SELECT potential_effect FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_finance(idea_id):
    sql_query = "SELECT finance FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_idea(idea_id):
    sql_query = "SELECT idea FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_city(idea_id):
    sql_query = "SELECT city FROM ideas WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

# Аналоги для таблицы researches

def get_format_r(idea_id):
    sql_query = "SELECT format FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_kogo_kasaetsya_r(idea_id):
    sql_query = "SELECT for_who FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_perimetr_r(idea_id):
    sql_query = "SELECT perimetr FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_auditory_r(idea_id):
    sql_query = "SELECT auditory FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_research_direction(idea_id):
    sql_query = "SELECT research_direction FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_stage(idea_id):
    sql_query = "SELECT stage FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_comanda_r(idea_id):
    sql_query = "SELECT comanda FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_ozhidaemyi_effect(idea_id):
    sql_query = "SELECT ozhidaemyi_effect FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_finance_r(idea_id):
    sql_query = "SELECT finance FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_research_idea(idea_id):
    sql_query = "SELECT idea FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_city_r(idea_id):
    sql_query = "SELECT city FROM researches WHERE id = %s"
    params = (idea_id,)
    return execute_get_sql_query(sql_query, params)[0][0]

def delete_idea(idea_id):
    sql_query = "DELETE FROM ideas WHERE id = %s"
    params = (idea_id,)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)

def delete_research(idea_id):
    sql_query = "DELETE FROM researches WHERE id = %s"
    params = (idea_id,)
    result = execute_set_sql_query(sql_query, params)
    return bool(result)
