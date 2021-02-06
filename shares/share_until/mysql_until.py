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
        # sql = "select * from user where username=%s and password=%s" %(user,pwd,)
        # cursor.execute(sql,user,pwd) #execute会帮我们做字符串拼接，推荐这种写法
        cursor.execute(sql)
        insert_id = None
        if sql.lower().startswith() == 'insert':
            insert_id = cnn.insert_id()     # 返回插入数据的主键id
        cnn.commit()
        return insert_id
    except Exception as e:
        logger.exception('执行出错\n%s' % e)
        raise e
    finally:
        cursor.close()
        cnn.close()
