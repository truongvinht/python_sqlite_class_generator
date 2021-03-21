# framework
import logging
import sqlite3

# filling generated data into database
class ModelobjectGenerator:
    def __init__(self, database_path):
        logging.info('init ModelobjectGenerator')
        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()
    def generate_classes(self, local_path):
        logging.debug("generate classes")

        # fetch all tables
        tables = self.fetch_all_tables()
        for table_k in tables:
            table = table_k[0]
            logging.debug("table: " + str(table))

            #fetch all attributes
            attributes = self.fetch_all_attributes(table)
            model_str = self.generate_model(table, attributes)

            # write to file
            text_file = open(local_path + table + ".py", "w")
            text_file.write(model_str)
            text_file.close()
    def generate_model(self, table, attributes):
        logging.debug("generate model: " + table)
            # for attr in attributes:
            #     print(str(attr))
        attr_param_str = ""
        attr_str = ""
        
        for attr in attributes:
            is_required = attr[3]

            # init attributes for object
            attr_value = ""

            # constructor only with required parameter
            if is_required == 1:
                attr_param_str = attr_param_str + ", " + attr[1]
                attr_value = attr[1]
            else:
                if attr[2] in "TEXT":
                    attr_value = "\"\""
                elif attr[2] in "INTEGER":
                    attr_value = "0"
                elif attr[2] in "REAL":
                    attr_value = "0.0"
                elif attr[2] in "BLOB":
                    attr_value = "NULL"

            attr_str = attr_str + "\t\tself." + attr[1] + "=" + attr_value + "\n"

        # persistent name
        persistent_table = "\tpersistent=\"" + table + "\"\n"
        content = "class " + table + ":\n"+persistent_table+"\tdef __init__(self "+attr_param_str+"):\n" + attr_str
        return content


    def fetch_all_tables(self):
        logging.debug("fetch tables")

        # select all tables without sqlite_*
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name ASC"
        self.c.execute(query)
        return self.c.fetchall()

    def fetch_all_attributes(self, table):
        logging.debug("fetch attributes for " + table)

        # select all attributes for table
        query = "PRAGMA table_info('"+table+"')"
        self.c.execute(query)
        return self.c.fetchall()
