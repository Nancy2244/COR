output_file_name = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/output.txt"

def cleaning(request: list) -> list:
    striped_request = []
    for word in request:
        word = word.strip("?")
        word = word.strip(".")
        word = word.strip(",")
        word = word.strip("!")
        word = word.strip(":")
        word = word.strip(";")
        word = word.strip("'")
        word = word.strip('"')
        striped_request.append(word)
    stop_words1 = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/расширенный - вордстат.txt"
    stop_words_list1=[]
    with open (stop_words1, "r", encoding="utf-8") as swl:
        for word in swl:
            stop_words_list1.append(word.strip())
    stop_words2 = "/Volumes/Macintosh HD 1/Users/k1dsporno/PycharmProjects/CORA_search/data/краткий - вордстат.txt"
    stop_words_list2=[]
    with open (stop_words2, "r", encoding="utf-8") as swl2:
        for word in swl2:
            stop_words_list2.append(word.strip())
    stop_words_list1.extend(stop_words_list2)
    union_stop_words = set(stop_words_list1)
    split_request = []
    clean_words=[]
    for word in striped_request:
        split_request.extend(word.split())
    for w in split_request:
        if w not in union_stop_words:
            w=w.lower()
            if w.startswith("орга"):
                clean_words.append("органы")
            else:
                clean_words.append(w)
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("russian")
    clean_words = [stemmer.stem(word) for word in clean_words]
    return clean_words

def popular (clean_words, output_file_name, explain_string, i):
    words_dict ={}
    for word in clean_words:
        if word not in words_dict:
            words_dict[word] = 1
        else:
            words_dict[word] +=1
    new_words_dicts = [(key,value) for key, value in words_dict.items() if value >=i]
    new_words_dicts.sort(key=lambda x:x[1], reverse=True)
    with open(output_file_name, "a", encoding="utf-8") as sr:
        print('', file=sr)
        print(explain_string, file=sr)
        print("*" * 100, file=sr)
        for word, count in new_words_dicts:
            print(f"{word}:{count}", file=sr)
    return new_words_dicts





