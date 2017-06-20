import json
import pickle


# line = "INSERT INTO TOXIC VALUES "

def pickle2sql(file):
    with open(file, 'rb') as test_file:
        with open("dump.sql", 'w') as result_file:
            test_pickle = pickle.load(test_file)
            counter = 1
            index = 1
            sql_line = "INSERT INTO twitchtoxicity.messages ('message_data') VALUES \n"

            for line in test_pickle:

                if index is test_pickle.__len__():
                    line = json.dumps(line)
                    line = line.replace("'", "\\'")
                    sql_line += "('{}')\n".format(line)
                    result_file.writelines(sql_line)

                elif counter is 100:
                    line = json.dumps(line)
                    line = line.replace("'", "\\'")
                    sql_line += "('{}')\n".format(line)
                    result_file.writelines(sql_line)
                    counter = 1
                    sql_line = "INSERT INTO twitchtoxicity.messages ('message_data') VALUES \n"

                else:
                    line = json.dumps(line)
                    line = line.replace("'", "\\'")
                    sql_line += "('{}'),\n".format(line)

                    counter += 1
                    index += 1


if __name__ == "__main__":
    test_pickle = "D:\\twitchtoxicity\\data\\videos\\MLG\\NiP celebration after mouse-v57849574.rechat-filtered.pickle"
    pickle2sql(test_pickle)
