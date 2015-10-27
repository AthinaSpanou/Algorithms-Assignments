# STABLE MATCH BETWEEN MEN AND WOMEN

import json
import copy
import sys

f = open(sys.argv[2], 'r') #sys.argv[2] shows the input file
j = json.load(f)
f.close()

men_rankings = copy.deepcopy(j['men_rankings']) #a dict of the men with their preferences
women_rankings = copy.deepcopy(j['women_rankings']) #a dict of the women with their preferences

engaged={} #a dict that shows the pairs of the marriage

men_free = copy.deepcopy(sorted(men_rankings.keys())) #a list of the names of the men who are free
women_free = copy.deepcopy(sorted(women_rankings.keys())) #a list of the names of the women who are free

if sys.argv[1] == '-m':
    while men_free : #while there is a name in the list men_free
        man = men_free.pop(0) #first man of list
        man_list = men_rankings[man] #list of preferences of the selected man
        woman = man_list.pop(0) #the first woman in preference list
        if woman in women_free: #if the selected woman is free
            engaged[man] = woman
            women_free.remove(woman)
        else: ##if the selected woman is not free
            woman_list = women_rankings[woman]
            for key in engaged.keys():
                if engaged[key] == woman:
                    current_man = key #current pair for woman
            if woman_list.index(current_man) > woman_list.index(man): #if current man is less in preference than the man that proposes to her
                del engaged[current_man] #delete existing pair
                men_free.append(current_man) 
                engaged[man] = woman #new pair
            else:
                men_free.append(man)  

if sys.argv[1] == '-w':
    while women_free : #while there is a name in the list women_free
        woman = women_free.pop(0) #first woman of list
        woman_list = women_rankings[woman] #list of preferences of the selected woman
        man = woman_list.pop(0) #the first man in preference list
        if man in men_free: #if the selected man is free
            engaged[woman] = man
            men_free.remove(man)
        else: #if the selected man is not free
            man_list = men_rankings[man]
            for key in engaged.keys():
                if engaged[key] == man:
                    current_woman = key #current pair for man
            if man_list.index(current_woman) > man_list.index(woman): #if current woman is less in preference than the woman that proposes to him
                del engaged[current_woman] #delete existing pair
                women_free.append(current_woman)
                engaged[woman] = man  #new pair
            else:
                women_free.append(woman)

j_string = json.dumps(engaged, sort_keys=True) #turn engaged dict into a json representation
print(j_string)

if len(sys.argv)>4:
    f=open(sys.argv[4],'w')
    json.dump(engaged, f, sort_keys=True, indent=4) #the output file
    f.close()
# END OF THE PROGRAM
