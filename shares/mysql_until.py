import pymysql


def execute_select_sql(conf, sql, logger):
    cnn = pymysql.connect(**conf)
    cursor = cnn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        logger.exception('查询出错\n%s' % e)
        raise e
    finally:
        cursor.close()
        cnn.close()


def execute_change_sql(conf, sql, logger):
    cnn = pymysql.connect(**conf)
    cursor = cnn.cursor()
    try:
        cursor.execute(sql)
        cnn.commit()
    except Exception as e:
        logger.exception('执行出错\n%s' % e)
        raise e
    finally:
        cursor.close()
        cnn.close()