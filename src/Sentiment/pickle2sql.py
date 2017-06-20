try:
    import ujson as json
except:
    import json
import pickle
import sys
import lzma as compressor
COMPRESSOR_EXTENSION = 'xz'

# line = "INSERT INTO TOXIC VALUES "

def pickle2sql(file):
    with compressor.open(file, 'rb') as test_file:
        with open("dump.sql", 'w') as result_file:
            result_file.write('START TRANSACTION;\n\n')
            test_pickle = pickle.load(test_file)
            counter = 0
            index = 0
            result_file.write("INSERT INTO twitchtoxicity.messages (`message_data`) VALUES \n");

            for line in test_pickle:
                
                if index == len(test_pickle)-1:
                    sys.stdout.write("Done. Processed {} from {} ({:.1%})                     \r".format(index,len(test_pickle),index/len(test_pickle)))
                    line = json.dumps(line)
                    line = line.replace("\\", "\\\\").replace("'", "\\'")
                    result_file.write("('")
                    result_file.write(line)
                    result_file.write("');\n")
                    index += 1

                elif counter == 100:
                    sys.stdout.write("Processed {} from {} ({:.1%})                     \r".format(index,len(test_pickle),index/len(test_pickle)))
                    line = json.dumps(line)
                    line = line.replace("\\", "\\\\").replace("'", "\\'")
                    result_file.write("('")
                    result_file.write(line)
                    result_file.write("');\n")
                    counter = 0
                    result_file.write("\nINSERT INTO twitchtoxicity.messages (`message_data`) VALUES \n");
                    index += 1
                    #sql_line = "INSERT INTO twitchtoxicity.messages ('message_data') VALUES \n"

                else:
                    line = json.dumps(line)
                    line = line.replace("\\", "\\\\").replace("'", "\\'")
                    result_file.write("('")
                    result_file.write(line)
                    result_file.write("'),\n")

                    counter += 1
                    index += 1
            result_file.write('\nCOMMIT;\n')

    print("\nDone.")

if __name__ == "__main__":
    test_pickle = "./data/videos/MLG/Luminosity Gaming vs Virtus Pro - Quarter Finals - MLG CSGO Major-v58219102.rechat-filtered.pickle.xz"
    pickle2sql(test_pickle)
