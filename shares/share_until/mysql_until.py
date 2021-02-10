import pymysql


def get_connect(conf):
    cnn = pymysql.connect(**conf)
    cursor = cnn.cursor()
    return cnn, cursor


def execute_select_sql(conf, sql, logger, *args):
    cnn = pymysql.connect(**conf)
    cursor = cnn.cursor()
    try:
        cursor.execute(sql, args)
        return cursor.fetchall()
    except Exception as e:
        logger.exception('查询出错\n%s' % e)
        raise e
    finally:
        cursor.close()
        cnn.close()


def execute_change_sql(con, sql, logger, *args):
    cnn, cursor = con
    try:
        cursor.execute(sql, args)
        insert_id = None
        if sql.strip().lower().startswith('insert'):
            insert_id = cnn.insert_id()     # 返回插入数据的主键id
        return insert_id
    except Exception as e:
        logger.exception('执行出错\n%s' % e)
        raise e


def commit_close(con):
    cnn, cursor = con
    cnn.commit()
    cursor.close()
    cnn.close()


def mysql_rollback(con):
    cnn, cursor = con
    cnn.rollback()
    cursor.close()
    cnn.close()
