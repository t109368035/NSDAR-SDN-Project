import re
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.LinkTable import LinkTable
from DBControll.PathTable import PathTable
from path_calculate.dikstra_graph import Graph


class GetPath:
    def __init__(self):
        ConnectDatabase()
        self.vlan_dict = self.dict_of_vlan()

    def get_normal_path(self):
        for ap in ['map15', 'map5']:
            btype = 'normal'
            graph = Graph(LinkTable().pop_ETT())
            path = graph.dijkstra(ap, 'out')
            print('start from {}, type is {}\n{}\n\n'.format(ap, 'normal', path))
            PathTable().insert_path(AP=ap.replace('\'','"'), app_type=btype.replace('\'','"'),
                                    path=str(path).replace('\'','"'), vlan=self.vlan_dict[ap][btype])

    def get_APP_path(self):
        for btype in ['Mission', 'Mobile', 'Massive']:
            for ap in ['map15', 'map5']:
                graph = Graph(LinkTable().pop_ETT())
                path = graph.dijkstra(ap, 'out')
                self.minus_use_bandwidth(path, btype)
                print('start from {}, type is {}\n{}\n\n'.format(ap, btype, path))
                PathTable().insert_path(AP=ap.replace('\'','"'), app_type=btype.replace('\'','"'),
                                        path=str(path).replace('\'','"'), vlan=self.vlan_dict[ap][btype])

    def minus_use_bandwidth(self,path,btype):
        for i in range(0,len(path)-1): #拿出目前節點以及下一個節點
            c_node = int(re.search('\d+$',path[i]).group())
            n_node = int(re.search('\d+$',path[i+1]).group())
            if not abs(n_node - c_node) == 1: #取出無線link
                for link in self.get_link_have_minus(path[i], path[i+1]): #取出受到影響所有link                    
                        original_bandwidth = LinkTable().pop_bandwidth(start_node=link[0], end_node=link[1])
                        bandwidth=original_bandwidth-self.get_btype_bandwidth(btype)
                        if bandwidth<=0:
                            LinkTable().delete_link(start_node=link[0],end_node=link[1])
                        else:
                            LinkTable().modify_bandwidth(start_node=link[0], end_node=link[1], bandwidth=bandwidth)
    
    def get_link_have_minus(self, c_node, n_node):
        all_link = LinkTable().pop_link_end_with(end_node=c_node) + LinkTable().pop_link_start_with(start_node=c_node) + LinkTable().pop_link_end_with(end_node=n_node) + LinkTable().pop_link_start_with(start_node=n_node)
        all_link.remove([c_node,n_node])
        print(all_link)
        return all_link

    def get_btype_bandwidth(self, btype):
        if btype is 'Mission':#設定每種應用類型使用的頻寬
            use = 25000000
        elif btype is 'Mobile':
            use = 15000000
        elif btype is 'Massive':
            use = 5000000
        return use
    
    def dict_of_vlan(self):
        v = {'map15':{'normal':15 ,'Mission':18, 'Mobile':17, 'Massive':16},
             'map5':{'normal':5 ,'Mission':8, 'Mobile':7, 'Massive':6}}
        return v
