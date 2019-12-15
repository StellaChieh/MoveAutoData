import os.path
try:
    import xml.etree.cElementTree as Et
except ImportError:
    import xml.etree.ElementTree as Et


class Token:

    def __init__(self, file_path, sent_time, count, record_list):
        self.file_path = file_path
        self.sent_time = sent_time
        self.count = count
        self.record_list = record_list
        self.keys = []

    def get_table_columns(self):
        """  Return  the list of  database table keys. """
        if len(self.keys) == 0:
            self.keys = list(self.record_list[0])
        return self.keys

    def get_table_values_order_by_columns(self):
        """ Return the values of a record in get_table_keys key order. """
        records = []
        keys = self.get_table_columns()
        for record in self.record_list:
            records.append([record[key] for key in keys])
        return records

    def get_token_name(self):
        """  Get the token name, basically it is the xml file name without extension. """
        base = os.path.basename(self.file_path)
        return os.path.splitext(base)[0]

    def get_record_num(self):
        """  Return the record number in a token ."""
        # Update 10000 records
        return self.count.split(' ')[1]

    def get_table_name(self):
        """  Return what database table this token manipulate . """
        filename = self.get_token_name()
        table = 'autoprec'
        filename_ary = filename.split('_')
        if 'His' in filename_ary or 'his' in filename_ary:
            table = 'his_' + table

        if 'HR' in filename_ary:
            table += 'hr'
        elif 'DY' in filename_ary:
            table += 'dy'
        else:
            table += 'mn'

        return table + "_test"


def parse_xml(txt_absolute_path):
    """ Parse XML file into Token class. """
    root = Et.parse(txt_absolute_path).getroot()
    sent_time = root.find('sent').text
    count = root.find('count').text
    info = root.find('info')
    record_list = []
    for element in info.findall('columnvalue'):
        dict_column_value = {}
        for sub_element in element:
            if sub_element.tag == 'name':
                key = sub_element.text
            else:
                dict_column_value[key] = sub_element.text
        record_list.append(dict_column_value)
    return Token(txt_absolute_path, sent_time, count, record_list)


if __name__ == '__main__':
    # xml = parse_xml('../Token/CMT_Auto_HR_20190702080020_2.xml')
    xml = parse_xml('../Token/CMT_Auto_his_DY_20190702080106_1.xml')
    print('token name: ' + xml.get_token_name())
    print('sent time: ' + xml.sent_time)
    print('record num: ' + xml.get_record_num())
    print('table name: ' + xml.get_table_name())
    print('table columns: ' + ', '.join(xml.get_table_columns()))
    # for record in xml.get_table_values_order_by_columns():
    #     print(', '.join(str(x) for x in record))
