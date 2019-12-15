def drop_table(table_schema, table_name):
    return ("""
        IF (EXISTS (SELECT *
                            FROM INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = '{table_schema}'
                            AND TABLE_NAME = '{table_name}'))
        BEGIN
            DROP TABLE {table_schema}.{table_name}
        END """).format(table_schema=table_schema, table_name=table_name)


def insert(table_schema, table_name, columns):
    """
    :param table_schema:
    :param table_name:
    :type columns: table key list
    :return: sql string
    """
    key_sql = ", ".join(columns)
    question_mark_sql = ", ".join(['?' for x in range(len(columns))])
    return (""" 
        INSERT INTO {table_schema}.{table_name} ({key_sql})
        VALUES ({question_mark_sql});
        """).format(table_schema=table_schema
                    , table_name=table_name
                    , key_sql=key_sql
                    , question_mark_sql=question_mark_sql)


def copy_table_structure(table_schema, source_table_name, target_table_name):
    return ("""
        SELECT * INTO {table_schema}.{target_table_name} 
        FROM {table_schema}.{source_table_name}
        WHERE 1=2;
        """).format(table_schema=table_schema
                    , target_table_name=target_table_name
                    , source_table_name=source_table_name)


def merge_tables(table_schema, source_table, target_table, primary_keys, columns):
    return ("""
        MERGE {target_table} as tar
         USING {source_table} as src
         ON {key_sql}
         WHEN MATCHED THEN
             UPDATE SET {set_sql}
         WHEN NOT MATCHED THEN
             INSERT ({column_sql})
             VALUES ({value_sql});
         """).format(target_table=table_schema + '.' + target_table
                     , source_table=table_schema + '.' + source_table
                     , key_sql=" and ".join([str('tar.' + x + '=' + 'src.' + x) for x in primary_keys])
                     , set_sql=", ".join([str('tar.' + x + '=' + 'src.' + x) for x in columns])
                     , column_sql=", ".join([str(x) for x in columns])
                     , value_sql=", ".join([str('src.'+x) for x in columns]))


if __name__ == '__main__':
    print('drop:' + drop_table('dbo', 'autoprechr'))
    print('insert: ' + insert('dbo', 'autoprechr', ['Stno', 'ObsTime', 'StnPres', 'Precp']))
    print('copy: ' + copy_table_structure('dbo', 'autoprechr', 'autoprechr_tmp'))
    print('merge: ' + merge_tables('dbo', 'autoprechr_test', 'autoprechr', ['Stno', 'ObsTime'], ['Stno', 'ObsTime', 'StnPres', 'Precp']))