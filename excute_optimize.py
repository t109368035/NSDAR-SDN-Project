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

for Q in all_Q_sequence:
    ett = GetPath().excute_ETT_all_sequency(Q)
    #print('{}: {}'.format(Q, ett))
    LinkTable().delete_all()
    for link in original_link:
        LinkTable().insert_link(start_node=link[0], end_node=link[1],
                                bandwidth=link[2], ETX=link[3])
    if ett < 1:
        ett_list.append(ett)
        ett_dict[Q] = ett

nsdar_sdn = ett_list[0]
sorted_ett_list = sorted(ett_list)
print('total path: {}'.format(len(all_Q_sequence)))
print('available path: {}'.format(len(ett_list)))
print('NSDAR-SDN rank: {}'.format(sorted_ett_list.index(nsdar_sdn)+1))
print('NSDAR-SDN: {}'.format(nsdar_sdn))
print('total ETT small than NSDAR-SDN:')
for k, v in ett_dict.items():
    if v < nsdar_sdn:
        print('{}: {}'.format(k,v))

#ett = GetPath().excute_ETT_NSR_SDN()
#print('{}: {}'.format('NSRSDN', ett))
#LinkTable().delete_all()
#for link in original_link:
#    LinkTable().insert_link(start_node=link[0], end_node=link[1],
#                            bandwidth=link[2], ETX=link[3])
