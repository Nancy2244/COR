from clean_popular import cleaning, popular
from ETS_points import get_ets_points_dict_and_list, split_by_groups
import csv

def find_links ():
    file_name = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/CT_personal_wo_actions.csv"
    link_cell_index = []
    flag = False
    links_dict={}
    id_list=[]
    ets_points_list=[]
    with open(file_name, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if flag == False:
                i=0
                for cell in row:
                    if "LinkText" in cell:
                        link_cell_index.append(i)
                    i+=1
                flag=True
            else:
                if row[3]:
                    id_list.append(row[0])
                if row[3]:
                    ets_points_list.append(row[3])
                for request_cell in link_cell_index:
                    if row[request_cell]:
                        if row[request_cell].startswith("http") == True:
                            if row[3] not in links_dict:
                                links_dict[row[3]] = [row[request_cell]]
                            else:
                                links_dict[row[3]].append(row[request_cell])
        return links_dict, id_list, ets_points_list

def cut_links ():
    links_dict, _id_list, ets_points_list = find_links()
    cut_links_dict={}
    for key, value in links_dict.items():
        cut_links_dict[key] =[]
        for val in value:
            print(val)
            val = val.replace("https://", '')
            print(val)
            domain = "https://"
            for letter in val:
                if letter == "/":
                    break
                else:
                    domain += letter
            cut_links_dict[key].append(domain)
    return cut_links_dict



def popular_links_ets_points ():
    output_file_name = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/output.txt"
    cut_links_dict=cut_links()
    _, _, ets_points_list = find_links()
    ets_points_list = [int(obj) for obj in ets_points_list]
    groups = [(0, 17), (18, 23), (24, 27), (28, None)]
    split=split_by_groups(ets_points_list, cut_links_dict, group_list=groups)
    links_list = []
    for _key, value in cut_links_dict.items():
        links_list.extend(value)
    list_popular=popular(links_list, output_file_name, "test string printing", 5)
    print(split,list_popular)



popular_links_ets_points()