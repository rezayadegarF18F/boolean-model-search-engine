import os

from pip._vendor.distlib.compat import raw_input
from stemming.porter2 import stem

string_temp = ""
string_temp2 = ""

date_control = False
author_control = False
text_control = False
favorite_control = False

command_index_counter = 1

day_temp = 0
month_temp = 0
year_temp = 0

author = ""
text = ""
favorite = ""

# define lists
word_list = []

day_list = []
month_list = []
year_list = []
author_list = []
text_list = []
favorite_list = []


def Tokenizing(str):
    werb_list1 = []
    werb_temp = ""

    """
        werb_list = str.split()
        return werb_list
        """

    for str_pointer in str:
        if ("A" <= str_pointer <= "Z") or ("a" <= str_pointer <= "z") or (
                "0" <= str_pointer <= "9") or str_pointer == "'":
            werb_temp += str_pointer
        elif str_pointer == "$" or str_pointer == "%" or str_pointer == "@" or str_pointer == "_" or str_pointer == "-":
            if werb_temp != "":
                werb_list1.append(werb_temp)
            werb_temp = ""
            werb_list1.append(str_pointer)
        else:
            if werb_temp != "":
                werb_list1.append(werb_temp)
            werb_temp = ""

    if werb_temp != "":
        werb_list1.append(werb_temp)

    return werb_list1


def Normalizing(werb_list):
    """
    for werb_temp_index, werb_temp_pointer in enumerate(word_list):
        string_temp_for_normalizing = ""
        for inside_werb_temp_pointer in werb_temp_pointer:
            if "A" <= inside_werb_temp_pointer <= "Z":
                string_temp_for_normalizing = chr(ord(inside_werb_temp_pointer) + 32)
            else:
                string_temp_for_normalizing += inside_werb_temp_pointer

        word_list[werb_temp_index] = string_temp_for_normalizing
    """

    for werb_list_pointer, werb_list_index in enumerate(werb_list):
        werb_list[werb_list_pointer] = werb_list_index.lower()

    return werb_list


def Stop_word_remove(werb_list, stop_word_list1):
    werb_list2 = []

    for werb_list_pointer, werb_list_index in enumerate(werb_list):
        exist = False
        for stop_word_pointer, stop_word_index in enumerate(stop_word_list1):
            if werb_list_index == stop_word_index:
                exist = True
                break
        if not exist:
            werb_list2.append(werb_list_index)


    return werb_list2


def Porter_algoritm(werb_list):
    for werb_list_pointer, werb_list_index in enumerate(werb_list):
        werb_list[werb_list_pointer] = stem(werb_list_index)

    return werb_list


def set_docID(werb_list, doc_name, counter):
    for werb_list_pointer, werb_list_index in enumerate(werb_list):
        werb_list[werb_list_pointer] = [werb_list_index, doc_name + "_" + str(counter)]

    return werb_list


def write_list_to_file(file_name, writen_list, directory):
    file_in_writing = open(directory + "\\" + file_name, "w")

    for writen_list_pointer, writen_list_index in enumerate(writen_list):
        file_in_writing.write(writen_list[writen_list_pointer][0])
        file_in_writing.write(" ")
        file_in_writing.write(writen_list[writen_list_pointer][1])
        file_in_writing.write("@@@\n")

    file_in_writing.close()


def read_file_into_list(str):
    temp_list_for_split_files = str.split("@@@\n")
    del temp_list_for_split_files[-1]

    for temp_list_pointer, temp_list_index in enumerate(temp_list_for_split_files):
        temp_list_for_split_files[temp_list_pointer] = temp_list_index.split()

    return temp_list_for_split_files


def create_dictionary(list_for_create):
    temp_list_for_dictionary = []
    for list_for_create_pointer, list_for_create_index in enumerate(list_for_create):
        temp_list_for_dictionary.append(list_for_create_index[0])

    temp_list_for_dictionary.sort()
    for counter5, counter6 in enumerate(temp_list_for_dictionary):
        temp_list_for_dictionary[counter5] = [counter6, "1"]

    temp_list_for_dictionary2 = [[temp_list_for_dictionary[0][0], "0"]]

    for counter1, counter2 in enumerate(temp_list_for_dictionary):
        bool_temp = False
        for counter3, counter4 in enumerate(temp_list_for_dictionary2):

            if counter2[0] == counter4[0]:
                temp_list_for_dictionary2[counter3][1] = str(int(counter4[1]) + 1)
                bool_temp = True

        if not bool_temp:
            temp_list_for_dictionary2.append([counter2[0], "1"])

    return temp_list_for_dictionary2


def create_incidence_matrix(dictionary_list_for_create, doc_werb_list_for_create):
    incidence_matrix = [["start"]]
    # create row of incidence matrix
    for dictionary_list_for_create_pointer, dictionary_list_for_create_index in enumerate(dictionary_list_for_create):
        incidence_matrix.append([dictionary_list_for_create[dictionary_list_for_create_pointer][0]])

    # get list of docID
    docID_temp = []
    for doc_werb_list_for_create_pointer, doc_werb_list_for_create_index in enumerate(doc_werb_list_for_create):
        bool_temp = False
        for counter3, counter4 in enumerate(docID_temp):
            if doc_werb_list_for_create_index[1] == counter4:
                bool_temp = True

        if not bool_temp:
            docID_temp.append(doc_werb_list_for_create_index[1])

    # create column of incidence matrix
    for docID_temp_pointer, docID_temp_index in enumerate(docID_temp):
        incidence_matrix[0].append(docID_temp_index)

    # fill incidence matrix for first time to can work with it
    for incidence_matrix_pointer, incidence_matrix_index in enumerate(incidence_matrix):
        if incidence_matrix_pointer != 0:
            for set_value_pointer, set_value_index in enumerate(incidence_matrix[0]):
                if set_value_pointer != 0:
                    incidence_matrix[incidence_matrix_pointer].append("0")

    # set correct value for incidence matrix
    for doc_werb_list_for_create_pointer, doc_werb_list_for_create_index in enumerate(doc_werb_list_for_create):

        for incidence_matrix_pointer, incidence_matrix_index in enumerate(incidence_matrix):
            if incidence_matrix_pointer != 0:
                if doc_werb_list_for_create_index[0] == incidence_matrix_index[0]:
                    for set_value_pointer, set_value_index in enumerate(incidence_matrix[0]):
                        if set_value_pointer != 0:
                            if doc_werb_list_for_create_index[1] == set_value_index:
                                incidence_matrix[incidence_matrix_pointer][set_value_pointer] = "1"
    """
    for incidence_matrix_pointer, incidence_matrix_index in enumerate(incidence_matrix):

        if incidence_matrix_pointer != 0:

            incidence_matrix_value = 0
            doc_find = ""
            for doc_werb_list_for_create_pointer, doc_werb_list_for_create_index in enumerate(doc_werb_list_for_create):
                
                if incidence_matrix_index[0] == doc_werb_list_for_create_index[0]:
                    incidence_matrix_value = 1
                    doc_find = doc_werb_list_for_create_index[1]

                    for set_value_pointer, set_value_index in enumerate(incidence_matrix_index[0]):
                        if set_value_pointer != 0:
                            if set_value_pointer == doc_find:
                                incidence_matrix[incidence_matrix_pointer][set_value_pointer] = "1"
                            else:
                                incidence_matrix[incidence_matrix_pointer][set_value_pointer] = "0"
    """
    return incidence_matrix


def write_incidence_matrix_to_file(file_name, incidence_for_write, directory):
    file_in_writing = open(directory + "\\" + file_name, "w")

    for incidence_for_write_pointer, incidence_for_write_index in enumerate(incidence_for_write):
        for write_row_pointer, write_row_index in enumerate(incidence_for_write_index):
            file_in_writing.write(write_row_index)
            file_in_writing.write(" ")
        file_in_writing.write("@@@\n")

    file_in_writing.close()


def read_search_index():
    while True:
        print("\nsearch in :")
        print("1. day in month")
        print("2. month")
        print("3. year")
        print("4. comment author")
        print("5. text")
        print("6. favorite")
        print("7. search in all detail of comment")
        print("8. exit from the appp\n\n")

        search_type = raw_input("type here : ")

        if search_type == "8":
            exit()
        elif "1" <= search_type <= "7":
            break
        else:
            print("you have entered undefined number. please try again ")
            continue
    search_case = raw_input("enter your search index : \n")
    return [search_type, search_case]


def search(incidence_matrix, search_list):
    print()


# get files directory from user and check it for exist.
print("--- welcome ---" + "\n" + "this programm will work just on the windows OS" + "\n")
while True:
    print("please insert your files directory to load it : ")
    # directory = raw_input()
    files_directory = 'C:\\Users\\rezaa\Downloads\Telegram Desktop\\2009'

    if os.path.isdir(files_directory):
        break
    else:
        print("your address is not a directory . please try again")
        raw_input("Press Enter to continue...")
        os.system('cls')

# Red stop word file
while True:
    print("please insert your stop word file directory to load it : ")
    # directory = raw_input()
    stop_word_directory = "E:\\project\\bazyabi ettelaa'at\\project 1\\stopwords.txt"

    if os.path.isfile(stop_word_directory):
        break
    else:
        print("your address is not a directory . please try again")
        raw_input("Press Enter to continue...")
        os.system('cls')

while True:
    print("please insert your directory that you want to save the document and werb files into it : ")
    # directory = raw_input()
    doc_werb_directory = "E:\\project\\bazyabi ettelaa'at\\project 1\\"

    if os.path.isfile(stop_word_directory):
        break
    else:
        print("your address is not a directory . please try again")
        raw_input("Press Enter to continue...")
        os.system('cls')

while True:
    print("please insert your directory to load the werb_document files load from it : ")
    # directory = raw_input()
    doc_werb_directory_for_load = "E:\\project\\bazyabi ettelaa'at\\project 1\\"

    if os.path.isfile(stop_word_directory):
        break
    else:
        print("your address is not a directory . please try again")
        raw_input("Press Enter to continue...")
        os.system('cls')

while True:
    print("please insert your directory to save dictionarys into it : ")
    # directory = raw_input()
    dictionary_directory_for_save = "E:\\project\\bazyabi ettelaa'at\\project 1\\"

    if os.path.isfile(stop_word_directory):
        break
    else:
        print("your address is not a directory . please try again")
        raw_input("Press Enter to continue...")
        os.system('cls')
# Read stop word file and create list of stop words
stop_word_file = open(stop_word_directory, 'r')
stop_word_list = stop_word_file.read().split()

# assign files to list to work those ile_in_processing
list_of_files = os.listdir(files_directory)

# parse the list of files for load it and parse each file
for files_pointer in list_of_files:
    # open fie with special directory address
    f = open(files_directory + "\\" + files_pointer, 'r')

    # import file into a list
    parse_list = f.read()

    doc_counter = 0
    # define conditions for read the detail of text
    for document_pointer in parse_list:
        string_temp = string_temp + document_pointer

        if document_pointer == "<":
            string_temp = "<"

        if string_temp == "<DATE>":
            doc_counter += 1
            date_control = True
            string_temp = ""

        elif string_temp == "<AUTHOR>":
            author_control = True
            string_temp = ""

        elif string_temp == "<TEXT>":
            text_control = True
            string_temp = ""

        elif string_temp == "<FAVORITE>":
            favorite_control = True
            string_temp = ""

        elif string_temp == "</DATE>":
            date_control = False

        elif string_temp == "</AUTHOR>":
            author_control = False

        elif string_temp == "</TEXT>":
            text_control = False

        elif string_temp == "</FAVORITE>":
            favorite_control = False

        elif string_temp == "</DOC>":
            command_index_counter += 1

        if date_control:
            if document_pointer == "/":
                if month_temp == 0:
                    month_temp = string_temp2
                    month_list.append([month_temp, files_pointer + "_" + str(doc_counter)])
                    string_temp2 = ""
                    string_temp = ""
                elif (day_temp == 0) and (month_temp != 0):
                    day_temp = string_temp2
                    day_list.append([day_temp, files_pointer + "_" + str(doc_counter)])
                    string_temp2 = ""
                    string_temp = ""

            elif document_pointer != "/" and document_pointer != "<":
                string_temp2 = string_temp

            elif document_pointer == "<":
                year_temp = string_temp2
                year_list.append([year_temp, files_pointer + "_" + str(doc_counter)])
                string_temp2 = ""
                string_temp = "<"
                day_temp = 0
                month_temp = 0
                year_temp = 0
                date_control = False


        elif author_control:

            if document_pointer == "<":
                # print(author)

                author_temp_list = Tokenizing(author)
                author_temp_list = Normalizing(author_temp_list)
                author_temp_list = Stop_word_remove(author_temp_list, stop_word_list)
                author_temp_list = Porter_algoritm(author_temp_list)

                author_temp_list = set_docID(author_temp_list, files_pointer, doc_counter)

                author_list += author_temp_list
                string_temp = ""
                author = ""
                author_control = False
            else:
                author = string_temp


        elif text_control:
            if document_pointer == "<":
                # print(text)

                text_temp_list = Tokenizing(text)
                text_temp_list = Normalizing(text_temp_list)
                text_temp_list = Stop_word_remove(text_temp_list, stop_word_list)
                text_temp_list = Porter_algoritm(text_temp_list)

                text_temp_list = set_docID(text_temp_list, files_pointer, doc_counter)

                text_list += text_temp_list
                string_temp = ""
                text = ""
                text_control = False
            else:
                text = string_temp

        elif favorite_control:
            if document_pointer == "<":
                # print(favorite)

                favorite_temp_list = Tokenizing(favorite)
                favorite_temp_list = Normalizing(favorite_temp_list)
                favorite_temp_list = Stop_word_remove(favorite_temp_list, stop_word_list)
                favorite_temp_list = Porter_algoritm(favorite_temp_list)

                favorite_temp_list = set_docID(favorite_temp_list, files_pointer, doc_counter)

                favorite_list += favorite_temp_list
                string_temp = ""
                favorite = ""
                favorite_control = False
            else:
                favorite = string_temp
    """
    for i in range(0, 40):
        print("day temp : ")
        print(day_list[i])
        print("month temp : ")
        print(month_list[i])
        print("year temp : ")
        print(year_list[i])
        print("author temp : ")
        print(author_list[i])
        print("text temp : ")
        print(text_list[i])
        print("favorite temp : ")
        print(favorite_list[i])
        raw_input()
    """

write_list_to_file("day_file", day_list, doc_werb_directory)
write_list_to_file("month_file", month_list, doc_werb_directory)
write_list_to_file("year_file", year_list, doc_werb_directory)
write_list_to_file("author_file", author_list, doc_werb_directory)
write_list_to_file("text_file", text_list, doc_werb_directory)
write_list_to_file("favorite_file", favorite_list, doc_werb_directory)

# this place is end of first step of the project

day_list_after_load_temp = open(doc_werb_directory_for_load + "\\" + "day_file", 'r').read()
month_list_after_load_temp = open(doc_werb_directory_for_load + "\\" + "month_file", 'r').read()
year_list_after_load_temp = open(doc_werb_directory_for_load + "\\" + "year_file", 'r').read()
author_list_after_load_temp = open(doc_werb_directory_for_load + "\\" + "author_file", 'r').read()
text_list_after_load_temp = open(doc_werb_directory_for_load + "\\" + "text_file", 'r').read()
favorite_list_after_load_temp = open(doc_werb_directory_for_load + "\\" + "favorite_file", 'r').read()

day_list_after_load = read_file_into_list(day_list_after_load_temp)
del day_list_after_load_temp
month_list_after_load = read_file_into_list(month_list_after_load_temp)
del month_list_after_load_temp
year_list_after_load = read_file_into_list(year_list_after_load_temp)
del year_list_after_load_temp
author_list_after_load = read_file_into_list(author_list_after_load_temp)
del author_list_after_load_temp
text_list_after_load = read_file_into_list(text_list_after_load_temp)
del text_list_after_load_temp
favorite_list_after_load = read_file_into_list(favorite_list_after_load_temp)
del favorite_list_after_load_temp

day_dictionary = create_dictionary(day_list_after_load)
del day_list_after_load
month_dictionary = create_dictionary(month_list_after_load)
del month_list_after_load
year_dictionary = create_dictionary(year_list_after_load)
del year_list_after_load
author_dictionary = create_dictionary(author_list_after_load)
del author_list_after_load
text_dictionary = create_dictionary(text_list_after_load)
del text_list_after_load
favorite_dictionary = create_dictionary(favorite_list_after_load)
del favorite_list_after_load

write_list_to_file("day_dictionary_file", day_dictionary, dictionary_directory_for_save)
del day_dictionary
write_list_to_file("month_dictionary_file", month_dictionary, dictionary_directory_for_save)
del month_dictionary
write_list_to_file("year_dictionary_file", year_dictionary, dictionary_directory_for_save)
del year_dictionary
write_list_to_file("author_dictionary_file", author_dictionary, dictionary_directory_for_save)
del author_dictionary
write_list_to_file("text_dictionary_file", text_dictionary, dictionary_directory_for_save)
del text_dictionary
write_list_to_file("favorite_dictionary_file", favorite_dictionary, dictionary_directory_for_save)
del favorite_dictionary

# this place is end of second step of the project

day_dictionary_after_load_temp = open(doc_werb_directory_for_load + "\\" + "day_dictionary_file", 'r').read()
month_dictionary_after_load_temp = open(doc_werb_directory_for_load + "\\" + "month_dictionary_file", 'r').read()
year_dictionary_after_load_temp = open(doc_werb_directory_for_load + "\\" + "year_dictionary_file", 'r').read()
author_dictionary_after_load_temp = open(doc_werb_directory_for_load + "\\" + "author_dictionary_file", 'r').read()
text_dictionary_after_load_temp = open(doc_werb_directory_for_load + "\\" + "text_dictionary_file", 'r').read()
favorite_dictionary_after_load_temp = open(doc_werb_directory_for_load + "\\" + "favorite_dictionary_file", 'r').read()

day_dictionary_after_load = read_file_into_list(day_dictionary_after_load_temp)
month_dictionary_after_load = read_file_into_list(month_dictionary_after_load_temp)
year_dictionary_after_load = read_file_into_list(year_dictionary_after_load_temp)
author_dictionary_after_load = read_file_into_list(author_dictionary_after_load_temp)
text_dictionary_after_load = read_file_into_list(text_dictionary_after_load_temp)
favorite_dictionary_after_load = read_file_into_list(favorite_dictionary_after_load_temp)

day_list_after_load_temp2 = open(doc_werb_directory_for_load + "\\" + "day_file", 'r').read()
month_list_after_load_temp2 = open(doc_werb_directory_for_load + "\\" + "month_file", 'r').read()
year_list_after_load_temp2 = open(doc_werb_directory_for_load + "\\" + "year_file", 'r').read()
author_list_after_load_temp2 = open(doc_werb_directory_for_load + "\\" + "author_file", 'r').read()
text_list_after_load_temp2 = open(doc_werb_directory_for_load + "\\" + "text_file", 'r').read()
favorite_list_after_load_temp2 = open(doc_werb_directory_for_load + "\\" + "favorite_file", 'r').read()

day_list_after_load2 = read_file_into_list(day_list_after_load_temp2)
month_list_after_load2 = read_file_into_list(month_list_after_load_temp2)
year_list_after_load2 = read_file_into_list(year_list_after_load_temp2)
author_list_after_load2 = read_file_into_list(author_list_after_load_temp2)
text_list_after_load2 = read_file_into_list(text_list_after_load_temp2)
favorite_list_after_load2 = read_file_into_list(favorite_list_after_load_temp2)

day_incidence_matrix = create_incidence_matrix(day_dictionary_after_load, day_list_after_load2)
month_incidence_matrix = create_incidence_matrix(month_dictionary_after_load, month_list_after_load2)
year_incidence_matrix = create_incidence_matrix(year_dictionary_after_load, year_list_after_load2)
author_incidence_matrix = create_incidence_matrix(author_dictionary_after_load, author_list_after_load2)
text_incidence_matrix = create_incidence_matrix(text_dictionary_after_load, text_list_after_load2)
favorite_incidence_matrix = create_incidence_matrix(favorite_dictionary_after_load, favorite_list_after_load2)

write_incidence_matrix_to_file("day_incidence_matrix", day_incidence_matrix, dictionary_directory_for_save)
del day_incidence_matrix
write_incidence_matrix_to_file("month_incidence_matrix", month_incidence_matrix, dictionary_directory_for_save)
del month_incidence_matrix
write_incidence_matrix_to_file("year_incidence_matrix", year_incidence_matrix, dictionary_directory_for_save)
del year_incidence_matrix
write_incidence_matrix_to_file("author_incidence_matrix", author_incidence_matrix, dictionary_directory_for_save)
del author_incidence_matrix
write_incidence_matrix_to_file("text_incidence_matrix", text_incidence_matrix, dictionary_directory_for_save)
del text_incidence_matrix
write_incidence_matrix_to_file("favorite_incidence_matrix", favorite_incidence_matrix, dictionary_directory_for_save)
del favorite_incidence_matrix

# this place is end of third step

day_incidence_matrix_after_load_temp = open(doc_werb_directory_for_load + "\\" + "day_incidence_matrix", 'r').read()
month_incidence_matrix_after_load_temp = open(doc_werb_directory_for_load + "\\" + "month_incidence_matrix", 'r').read()
year_incidence_matrix_after_load_temp = open(doc_werb_directory_for_load + "\\" + "year_incidence_matrix", 'r').read()
author_incidence_matrix_after_load_temp = open(doc_werb_directory_for_load + "\\" + "author_incidence_matrix",
                                               'r').read()
text_incidence_matrix_after_load_temp = open(doc_werb_directory_for_load + "\\" + "text_incidence_matrix", 'r').read()
favorite_incidence_matrix_after_load_temp = open(doc_werb_directory_for_load + "\\" + "favorite_incidence_matrix",
                                                 'r').read()

day_incidence_matrix_after_load = read_file_into_list(day_incidence_matrix_after_load_temp)
del day_incidence_matrix_after_load_temp
month_incidence_matrix_after_load = read_file_into_list(month_incidence_matrix_after_load_temp)
del month_incidence_matrix_after_load_temp
year_incidence_matrix_after_load = read_file_into_list(year_incidence_matrix_after_load_temp)
del year_incidence_matrix_after_load_temp
author_incidence_matrix_after_load = read_file_into_list(author_incidence_matrix_after_load_temp)
del author_incidence_matrix_after_load_temp
text_incidence_matrix_after_load = read_file_into_list(text_incidence_matrix_after_load_temp)
del text_incidence_matrix_after_load_temp
favorite_incidence_matrix_after_load = read_file_into_list(favorite_incidence_matrix_after_load_temp)
del favorite_incidence_matrix_after_load_temp

search_index = read_search_index()
search_case_list = Tokenizing(search_index[1])
search_case_list = Normalizing(search_case_list)
search_case_list = Stop_word_remove(search_case_list, stop_word_list)
search_case_list = Porter_algoritm(search_case_list)

#print(search_case_list)
#print(stop_word_list)

if int(search_index[0]) == 1:
    search(day_incidence_matrix_after_load, search_case_list)
elif int(search_index[0]) == 2:
    search(month_incidence_matrix_after_load, search_case_list)
elif int(search_index[0]) == 3:
    search(year_incidence_matrix_after_load, search_case_list)
elif int(search_index[0]) == 4:
    search(author_incidence_matrix_after_load, search_case_list)
elif int(search_index[0]) == 5:
    search(text_incidence_matrix_after_load, search_case_list)
elif int(search_index[0]) == 6:
    search(favorite_incidence_matrix_after_load, search_case_list)
elif int(search_index[0]) == 7:
    search(day_incidence_matrix_after_load, search_case_list)
    search(month_incidence_matrix_after_load, search_case_list)
    search(year_incidence_matrix_after_load, search_case_list)
    search(author_incidence_matrix_after_load, search_case_list)
    search(text_incidence_matrix_after_load, search_case_list)
    search(favorite_incidence_matrix_after_load, search_case_list)

"""
print(day_list_after_load[0])
print(month_list_after_load[0])
print(year_list_after_load[0])
print(author_list_after_load[0])
print(text_list_after_load[0])
print(favorite_list_after_load[0])
"""

"""
for po in range(0, 1000):
    print(day_list[po])
    print(month_list[po])
    print(year_list[po])
    print(author_list[po])
    print(text_list[po])
    print(favorite_list[po])
    raw_input()
"""
print("\n" + "files is loaded." + "\n")
