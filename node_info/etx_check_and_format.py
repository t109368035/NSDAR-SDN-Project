'''
this python script is to change etx_information format 
from dict({'start': '10.10.1.15', 'end': '10.10.1.55', 'cost': 1.202}) 
to nametuple(Edge(start='10.10.1.15', end='10.10.1.55', cost=1.202))

and

check the etx is continue renew

'''
from collections import namedtuple

def change_format(collect_etx_value):
    Edge = namedtuple('Edge', 'start, end, cost')
    information_format = [Edge(**edge) for edge in collect_etx_value.values()]

    return information_format

def check_etx(collect_etx_member, collect_etx_value, etx_information):
    if next(iter(etx_information)) not in collect_etx_member: # => 利用iter將dict()變成跌帶物件，再用next取得第一個值(key)
        collect_etx_member.append(next(iter(etx_information)))
    collect_etx_value[next(iter(etx_information))] = etx_information[next(iter(etx_information))]


        
