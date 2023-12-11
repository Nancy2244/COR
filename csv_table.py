file_name = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/CT_personal_wo_actions.csv"
from clean_popular import cleaning
import csv
import requests
from pprint import pprint
def get_csv_table():
    with open(file_name, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        flag = False
        request_cell_index=[]
        id_list=[]
        link_cell_index=[]
        all_data = []
        all_words = []
        ets_points_list = []
        for row in reader:
            #обрабатываю первую строку и нахожу номера колонок
            if flag == False:
                i = 0
                for cell in row:
                    if "LinkText" in cell:
                        link_cell_index.append(i)
                    if "RequestText" in cell:
                        request_cell_index.append(i)
                    i += 1
                flag = True
            else:
                if row[0]:
                    search_dict = {}

                    #добавляю id студента в словарь; записываю все id
                    if row[0]:
                        search_dict["id"] = row[0]
                        id_list.append(row[0])
                    #добавляю баллы в словарь; записываю все баллы
                    if row[3]:
                        search_dict["ets_points"] = row[3]
                        ets_points_list.append(row[3])

                    #добавляю слова в словарь и чищу их
                    iteration_search_words = []
                    search_dict["clean_request"] = []
                    for request_cell in request_cell_index:
                        if row[request_cell]:
                            if row[request_cell].startswith("http") == False:
                                all_words.append(row[request_cell])
                                clean=(row[request_cell]).split()
                                clean=cleaning(clean)
                                iteration_search_words.append(clean)
                                search_dict["clean_request"].append(' '.join(clean))


                    # добавляю линки в словарь и чищу их
                    search_dict["links"] = []
                    search_dict["domain"] = []
                    search_dict["N="] = 0
                    for link_cell in link_cell_index:
                        if row[link_cell]:
                            if row[link_cell].startswith("http"):
                                search_dict["links"].append(row[link_cell])
                                search_dict["N="] +=1
                                to_clean = row[link_cell]
                                domain = ''
                                if "https://" in to_clean:
                                    to_clean = to_clean.replace("https://", '')
                                    domain = "https://"
                                elif "http://" in to_clean:
                                    to_clean = to_clean.replace("http://", '')
                                    domain = "http://"
                                for letter in to_clean:
                                    if letter == "/":
                                        break
                                    else:
                                        domain += letter
                                search_dict["domain"].append(domain)
                    all_data.append(search_dict)
                    print(search_dict["N="], search_dict["id"])

    return all_data
get_csv_table()

#пишу таблицу из поучившегося списка словарей

from OpenSSL.SSL import SSLeay_version, SSLEAY_VERSION
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl

def page_text():
    all_data = get_csv_table()
    links_text={}
    for data in all_data:
        link_parse_result = {}
        # TODO: тут не нужен цикл по элементам словаря, просто проверь, есть ли ключ if "links" in data.keys()
        # TODO: и обратись по ключу data["links"]
        #for key,value in data.items():
        if "links" in data.keys() and data["links"]:
            i = 1
            for val in data["links"]:
                print(f" val_type: {type(val)} | val: {val}")
                if len(val) == 0:
                    link_parse_result["error"] = "no links found"
                else:
                    print(f"Handling link_{i}. url: {val}")
                    try:
                        page =requests.get(val, verify=False, timeout=2)
                    except requests.exceptions.ConnectionError:
                        link_parse_result[f"link_{i}"] = "error"
                    except requests.exceptions.Timeout:
                        link_parse_result[f"link_{i}"] = "timeout"
                    else:
                        soup = BeautifulSoup(page.text, 'html.parser')
                        # kill all script and style elements
                        for script in soup(["script", "style"]):
                            script.extract()  # rip it out
                        # get text
                        text = soup.get_text()
                        # break into lines and remove leading and trailing space on each
                        lines = (line.strip("\n").replace(u'\xa0',' ') for line in text.splitlines())
                        # break multi-headlines into a line each
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        # drop blank lines
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        links_text[val]=text
                        link_parse_result[f"link_{i}"] = text[:500]
                        print(text[:500])
                    i+=1
        else:
            link_parse_result["error"] = "no links presented"
        data["links_text"] = link_parse_result

    return all_data






def write_csv_table():
    all_data_modified = page_text()
    output_file = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/table_id_ets_search_link_domain.csv"
    with open (output_file, "w", encoding="utf-8") as table:
        spamwriter = csv.writer(table, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["id", "ets_points", "clean_request", "links", "domain", "links_text"])
        for d in all_data_modified:
            row_list = [d["id"],
                        d["ets_points"],
                        '; '.join(d["clean_request"]),
                        '; '.join(d["links"]),
                        '; '.join(d["domain"]),
                        d["links_text"]]
            # for key, value in l.items():
            #     if type(value) == list:
            #         row_list.append('; '.join(value))
            #     else:
            #         row_list.append(value)
            pprint(row_list)
            spamwriter.writerow(row_list)

#write_csv_table()

with open(file_name, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    flag = False
    request_cell_index = []
    id_list = []
    link_cell_index = []
    all_data = []
    for row in reader:
        # обрабатываю первую строку и нахожу номера колонок
        if flag == False:
            i = 0
            for cell in row:
                if "EssayLinks__LinkText" in cell:
                    link_cell_index.append(i)
                i += 1
            flag = True
        else:
            search_dict = {"essay_links": 0}
            if row[3]:
                search_dict["ets_points"] = int(row[3])
            else:
                search_dict["ets_points"] = 0
            for i in link_cell_index:
                if row[i] and "http" in row[i]:
                    search_dict["essay_links"] +=1
            all_data.append(search_dict)
    #pprint(all_data)
    all_data.sort(key=lambda x: x["ets_points"], reverse=True)
    # pprint(all_data)

#print(all_data)