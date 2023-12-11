from clean_popular import cleaning, popular
import csv
import matplotlib.pyplot as plt

def get_ets_points_dict_and_list():
    file_name = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/CT_personal_wo_actions.csv"
    request_cell_index = []
    flag = False
    ets_points_dict={}
    ets_points_list=[]
    with open(file_name, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if flag == False:
                i=0
                for cell in row:
                    if "RequestText" in cell:
                        request_cell_index.append(i)
                    i+=1
                flag=True
            else:
                if row[3]:
                    ets_points_list.append(row[3])
                for request_cell in request_cell_index:
                    if row[request_cell]:
                        if row[request_cell].startswith("http") == False:
                            if row[3] not in ets_points_dict:
                                ets_points_dict[row[3]] = [row[request_cell]]
                            else:
                                ets_points_dict[row[3]].append(row[request_cell])
    return ets_points_dict, ets_points_list

#get_ets_points_dict_and_list()
def split_by_groups(ets_points_list, ets_points_dict, group_list: list) -> None:
    for frm ,till in group_list:
        count = 0
        group_list = []
        if till is None: # обрабатываем крайний случай конца
            till = int(max(ets_points_list))
        for i in ets_points_list:
            if int(i) >= frm and int(i) <= till:
                count+=1
        for key, value in ets_points_dict.items():
            if int(key) > frm and int(key) <= till:
                group_list.extend(value)
        print(f"from {frm} till {till} values: {group_list}")
        output_file_name = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/ets_points.txt"
        popular(cleaning(group_list), output_file_name,
                f"Количество слов в запросе при ETS от {frm} до {till} ({count} чел.)", 2)


def main():
    ets_points_dict, ets_points_list = get_ets_points_dict_and_list()
    groups = [(0,17), (18,23), (24,27), (28, None)]
    ets_points_list = [int(obj) for obj in ets_points_list]
    split_by_groups(ets_points_list, ets_points_dict, groups)


if __name__ == "__main__":
    main()

# points = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/points.txt"
# sorted_points_list=[]
#
# with open (points, "r", encoding="utf-8") as pt:
#     for line in pt:
#         sorted_points_list = line.split("', '")
# sorted_points_list = [int(obj) for obj in sorted_points_list]
# points_stat={}
# for point in sorted_points_list:
#     if point not in points_stat:
#         points_stat[point] = 1
#     else:
#         points_stat[point] +=1



# x=points_stat.keys()          # график
# y = points_stat.values()
# plt.plot(x,y)
# plt.show()