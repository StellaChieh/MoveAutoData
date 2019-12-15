# -*- coding: utf-8 -*-

import os
import MyConfig as config
import moveData.Dao
import moveData.MakeSql
import moveData.MyLog
import moveData.ParseXml
import ntpath
import moveData.EmailFunction as EmailFunction
import pyodbc

logger = moveData.MyLog.MyLog(config.get_log_folder()).get_logger()


def process(token_folder):
    error_files = []
    # walk through token_folder to get token xml file
    tokens = []
    for dir_path, dir_names, token_files in os.walk(token_folder):
        for f in token_files:
            tokens.append(os.path.join(dir_path, f))

    if len(tokens) == 0:
        logger.info("Empty token folder.")
        return

    if len(tokens) > 0:
        # try to connect to database
        conn = None
        try:
            db_config = config.get_db_config()
            logger.info('Connect to MsSql Server...')
            conn = moveData.Dao.Connection(db_config.get('ip'), db_config.get('database')
                                           , db_config.get('user'), db_config.get('password'))
        except pyodbc.Error as err:
            logger.warn('Fail to connect to MsSql Server!!!')
            logger.error(err[1])
            logger.warn('Please check again database user, password and internet condition, bye bye!')
            send_connection_error_email()
            return

        # connection is successful, so we can start updating the table
        else:
            logger.info('Connect to MsSql database successfully.')
            make_sql = moveData.MakeSql
            table_schema = 'dbo'

            for token_file in tokens:
                # first parse the xml file, and get table name, columns and values
                logger.info('Parse token ' + ntpath.basename(token_file) + '...')
                token = moveData.ParseXml.parse_xml(token_file)
                logger.info('Finished parsing token ' + ntpath.basename(token_file))

                if len(token.record_list) > 0:
                    table_name = token.get_table_name()
                    tmp_table_name = table_name + '_auto_tmp'
                    columns = token.get_table_columns()
                    # token_name is the token filename stripped off the extension
                    token_name = token.get_token_name()
                    try:
                        logger.info('Begin updating ' + token_name + '...')

                        # drop tmp table
                        sql_droptable = make_sql.drop_table(table_schema, tmp_table_name)
                        logger.debug(sql_droptable)
                        conn.execute(sql_droptable)

                        # create new tmp table
                        sql_createtable = make_sql.copy_table_structure(table_schema, table_name, tmp_table_name)
                        logger.debug(sql_createtable)
                        conn.execute(sql_createtable)

                        # insert records into tmp table
                        # conn.batch_parameterized_insert(make_sql.insert(table_schema, tmp_table_name, columns)
                        #                                 , token.get_table_values_order_by_columns())
                        sql_insert = make_sql.insert(table_schema, tmp_table_name, columns)
                        logger.debug(sql_insert)
                        for record in token.get_table_values_order_by_columns():
                            logger.debug(record)
                            conn.parameterized_execute(sql_insert, record)

                        # merge tmp table and target table
                        sql_merge = make_sql.merge_tables(table_schema, tmp_table_name, table_name, ['Stno', 'ObsTime'],
                                                          columns)
                        logger.debug(sql_merge)
                        conn.execute(sql_merge)

                        # drop tmp table
                        sql_droptable = make_sql.drop_table(table_schema, tmp_table_name)
                        logger.debug(sql_droptable)
                        conn.execute(sql_droptable)

                    except Exception as err:
                        error_files.append(token_file)
                        logger.error(err[1])
                        logger.warn('Fail to update ' + token.get_token_name())

                    else:
                        logger.info('Finished updating ' + token_name)

        finally:
            if conn is not None:
                conn.close()
                logger.info('Close connection to MsSql database.')

        # error processing: 1. send email 2.move the token file to fail folder
        if len(error_files) > 0:
            for token_file in error_files:
                move_folder(token_file, config.get_token_fail_folder())
                logger.info('Move ' + ntpath.basename(token_file) + ' into ' + config.get_token_fail_folder())
            send_token_error_email(error_files)

        # move finished token file into done folder
        for dir_path, dir_names, token_files_ori in os.walk(token_folder):
            for token_file in token_files_ori:
                move_folder(os.path.join(dir_path, token_file), config.get_token_done_folder())
                logger.info('Move ' + token_file + ' into ' + config.get_token_done_folder())


def send_token_error_email(error_files):
    tokens = ', '.join(error_files)
    subject = '197寫入195自動站資料報錯'
    message = '管理員你好:\n\n以下token寫入至195有問題，已移至' + ntpath.basename(config.get_token_fail_folder()) + '資料夾。\n' + tokens
    EmailFunction.Email().send_email(config.get_receivers(), subject, message)
    logger.info("Email sent:\n" + message)


def send_connection_error_email():
    subject = '197寫入195自動站資料報錯'
    message = '管理員你好:\n\n無法連線至197資料庫，請檢查資料庫帳密和網路狀況。'
    EmailFunction.Email().send_email(config.get_receivers(), subject, message)
    logger.info("Email sent:\n" + message)


def move_folder(files_moved, destination):
    cmd = 'move ' + files_moved + ' ' + destination
    os.system(cmd)


if __name__ == '__main__':
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info(' ')
    logger.info('Program starts!')
    process(config.get_token_ori_folder())
    logger.info('Program finished!')
