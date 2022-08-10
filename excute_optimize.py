import itertools
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.LinkTable import LinkTable
from path_calculate.get_path import GetPath

ConnectDatabase()
original_link = LinkTable().pop_all_link()

sque = ['Mission', 'Mobile', 'Massive', 'normal']
all_Q_sequence = list(itertools.permutations(sque))
ett_list = list()
ett_dict = dict()
not_ett = 0

for Q in all_Q_sequence:
    ett = GetPath().excute_ETT_any_sequency(Q)
    ett_list.append(ett)
    ett_dict[Q] = ett
    if ett > 1:
        not_ett+=1
    LinkTable().delete_all()
    for link in original_link:
        LinkTable().insert_link(start_node=link[0], end_node=link[1],
                                bandwidth=link[2], ETX=link[3])    

nsdar_sdn = ett_list[0]
sorted_ett_list = sorted(ett_list)
print('total path: {}'.format(len(all_Q_sequence)))
print('not available path: {}'.format(not_ett))
print('NSDAR-SDN rank: {}'.format(sorted_ett_list.index(nsdar_sdn)+1))
print('NSDAR-SDN: {}'.format(nsdar_sdn))
print('total ETT small than NSDAR-SDN:')
for k, v in ett_dict.items():
    if v <= nsdar_sdn:
        print('{}: {}'.format(k,v))

print('total ETT greater than NSDAR-SDN:')
for k, v in ett_dict.items():
    if v > nsdar_sdn:
        print('{}: {}'.format(k,v))
