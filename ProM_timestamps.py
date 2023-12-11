file_name="/Volumes/Macintosh HD 1/Users/k1dsporno/Desktop/Postgraduate/prom-lite-1.3-all-platforms/ProM_file/Actions_long.csv"
output_file = "/Volumes/Macintosh HD 1/Users/k1dsporno/Desktop/Postgraduate/prom-lite-1.3-all-platforms/ProM_file/actions_ready.csv"
median_file = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/actions_3_new.csv"
cluster_file= "/Volumes/Macintosh HD 1/Users/k1dsporno/Desktop/Postgraduate/prom-lite-1.3-all-platforms/ProM_file/clusters.csv"
import csv
import datetime
from datetime import datetime



def function_to_convert_timestamp(cell):
    try:
        timestamp_sting = int(cell)
    except ValueError:
        return cell
    datetime_obj = datetime.fromtimestamp(timestamp_sting)
    return datetime_obj.strftime('%m/%d/%Y %H:%M:%S')

def zone_duration_table ():
    with open (file_name, "r", encoding="utf-8") as table:
        median_table = open(median_file, "w", encoding="utf-8")
        writer = csv.writer(median_table, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        reader= csv.reader(table, delimiter=",",  quotechar='"')
        reader_list = list(reader)
        wr=["ID", "Zone", "TimeStart", "TimeEnd", "class"]
        writer.writerow(wr)
        k=-1
        for i, row in enumerate(reader_list):
            if i < k:
                continue
            if row [1]:
                new_row = []

                if row[1] == "1":
                    new_row.extend([row[0], "Start", int(row[4])-2, (int(row[4])-2)])
                    writer.writerow(new_row)
                    new_row=[]

                if row [2].startswith("ZoneApp") and row[3].startswith("Pause"):
                    new_row.extend([row[0],"OutApp", row[4], int(row[5])+int(row[4])])
                    writer.writerow(new_row)


                elif row[2].startswith ("ZoneApp") and row[3].startswith("Resume"):
                    new_row.extend([row[0],"InApp", row[4],int(row[4])+int(row[5])])
                    writer.writerow(new_row)


                elif row[2].startswith("ZoneEndButton"):
                    new_row.extend([row[0], "End", row[4], int(row[4])+int(row[5])])
                    writer.writerow(new_row)

                elif row[2].startswith("ZoneEssaySource"):
                    new_row.extend([row[0], "EssaySource", row[4], int(row[4])+int(row[5])])
                    writer.writerow(new_row)

                elif row[2].startswith("ZoneArgMinus"):
                    current_row=row[2]
                    current_num=current_row[-1]
                    new_row.extend([row[0], f"ArgMinus{row[2][-1]}", row[4], int(row[4])+int(row[5])])
                    writer.writerow(new_row)
                    print(new_row)

                elif row[2].startswith("ZoneArgSource"):
                    current= row[2]
                    current_num=current[-1]
                    duration_arg_source = int(row[5])
                    k = i+1
                    while True:
                        current_row = reader_list[k]
                        if current_row[2].startswith("ZoneArgSource") or current_row[2].startswith("ZoneArgRadio"):
                            duration_arg_source += int(current_row[5])
                            k += 1
                        else:
                            new_row.extend([row[0], f"ArgumentSource{current_num}", row[4], int(row[4])+int(duration_arg_source)])
                            writer.writerow(new_row)
                            break

                elif row[2].startswith("ZoneArgText"):
                    current= row[2]
                    current_num=current[-1]
                    duration_arg = int(row[5])
                    k = i + 1
                    while True:
                        current_row=reader_list[k]
                        if current_row[2].startswith("ZoneArgText"): #and current_row[2].endswith(current_num):
                            duration_arg += int(current_row[5])
                            k += 1
                        else:
                            new_row.extend([row[0],f"Argument{current_num}", row[4], int(row[4])+int(duration_arg)])
                            writer.writerow(new_row)
                            break

                elif row[2].startswith("ZoneEssayText"):
                    duration_essay = int(row[5])
                    k = i + 1
                    while True:
                        current_row=reader_list[k]
                        if current_row[2].startswith("ZoneEssayText"):
                            duration_essay += int(current_row[5])
                            k += 1
                        else:
                            new_row.extend([row[0],"Essay", row[4], int(row[4])+int(duration_essay)])
                            writer.writerow(new_row)
                            break
                else:
                    continue


zone_duration_table()


data = []
with open(cluster_file, "r", encoding="utf-8") as clusters:
    reader_clusters = csv.reader(clusters, delimiter=",", quotechar='"')
    reader_list_clusters = list(reader_clusters)
    cluster_dict={}
    for row in reader_list_clusters:
        cluster_dict[row[0]]=row[4]

with open(median_file, "r", encoding="utf-8") as csvfile:

    with open(output_file, "w", encoding="utf8") as csv_writer:
        writer = csv.writer(csv_writer, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            if row[0] not in cluster_dict.keys():
                cluster_dict[row[0]] = 0
            new_row = [row[0], row[1], function_to_convert_timestamp(row[2]), function_to_convert_timestamp(row[3]),
                       cluster_dict[row[0]]]
            writer.writerow(new_row)

