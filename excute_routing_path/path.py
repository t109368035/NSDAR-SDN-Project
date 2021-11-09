from alg import Graph

class Printdis_topo():
  def __init__(self, dis_topo):
    self.dis_topo = dis_topo

  def path(self, dis_topo):
    dp_to_mac = [('10.10.1.25', '145234203392259', '84:16:f9:1a:39:03'),
                 ('10.10.1.45', '27310741594218', '18:d6:c7:0d:20:6a'),
                 ('10.10.1.15', '27310741590990', '18:d6:c7:0d:13:ce'),
                 ('10.10.1.55', '145234203657311', '84:16:f9:1e:44:5f'),
                 ('10.10.3.55', '27310741570752', '18:d6:c7:0c:c4:c0'),
                 ('10.10.3.25', '145234203662428', '84:16:f9:1e:58:5c'),
                 ('10.10.3.15', '145234203695054', '84:16:f9:1e:d7:ce'),
                 ('10.10.3.45', '145234203391803', '84:16:f9:1a:37:3b'),
                 ('10.10.1.98', '27310741608024', '18:d6:c7:0d:56:a5'),
                 ('10.10.1.99', '145234203673937', '84:16:f9:1e:85:51'),
                 ('10.10.3.98', '145234203695083', '84:16:f9:1a:17:f4'),
                 ('10.10.3.99', '145234203662402', '84:16:f9:1e:58:42')]

    node_change_channel = {
        "10.10.1.15cost": "10.10.3.15cost",
        "10.10.1.45": "10.10.3.45",
        "10.10.1.45cost": "10.10.3.45cost",
        "10.10.1.98": "10.10.3.98",
        "10.10.1.25cost": "10.10.3.25cost",
        "10.10.1.55": "10.10.3.55",
        "10.10.1.55cost": "10.10.3.55cost",
        "10.10.1.99": "10.10.3.99",

        "10.10.3.15cost": "10.10.1.15cost",
        "10.10.3.45": "10.10.1.45",
        "10.10.3.45cost": "10.10.1.45cost",
        "10.10.3.98": "10.10.1.98",
        "10.10.3.25cost": "10.10.1.25cost",
        "10.10.3.55": "10.10.1.55",
        "10.10.3.55cost": "10.10.1.55cost",
        "10.10.3.99": "10.10.1.99",
    }
    total_topo = []
    totaluser = ["slice_1","slice_3","slice_2","slice_4"]
    #totaluser = ["slice_3","slice_4"]
    #totaluser = ["sta","sta2","sta3"]
    i=0
    for user in totaluser:
        print(user)
        print("############################################################")
        ShortestPath = Graph(dis_topo)
        Throughdis_topo = []
        Throughdis_topo = list(ShortestPath.dijkstra(user, "net"))
        print(Throughdis_topo)
        result = []
        path = []
        new_topo = []
        # for search link
        for j in dis_topo:
            for found_node in range(len(Throughdis_topo) - 1):
                if Throughdis_topo[found_node] in j and Throughdis_topo[found_node + 1] in j:
                    path.append(j)
      
        for p in path:
            if 0 not in p :
               result.append(p)
        print("result", result)
        totalweight=0
        for resultweight in result:
           totalweight= totalweight+resultweight[2]
        print("totalweight", totalweight)
        #print "###"
        for ddaa in dis_topo:
            if 0 not in ddaa:
                new_topo.append(ddaa)

        for Mod_result in result:
            #print list(Mod_result)
            modweight = list(Mod_result)
            modip = modweight
            #print "modip", modip
            #print(Mod_result[0])
            for cal in new_topo:
                if  cal[2]<1 :
                   continue
                if cal[0] == node_change_channel[Mod_result[0]] and cal[1] == Mod_result[0] :
                    continue
                if cal[0] == Mod_result[0] and cal[1] ==node_change_channel[Mod_result[0]] :
                    continue
                if cal[0] ==Mod_result[0] and cal[1] == Mod_result[1] :
                    #print "case1"
                    #print "cal", cal
                    modweight_cal = list(cal)
                    modweight_cal[2] = modweight_cal[2] + .5
                    #print modweight_cal
                    modweight_tuple = tuple(modweight_cal)
                    dis_topo.pop(dis_topo.index(cal))
                    dis_topo.append(modweight_tuple)
                if cal[0] ==Mod_result[0] and cal[1] != Mod_result[1] :
                    #print "cal", cal
                    #print "case2"
                    modweight_cal = list(cal)
                    modweight_cal[2] = modweight_cal[2] + .3
                    #print modweight_cal
                    modweight_tuple = tuple(modweight_cal)
                    dis_topo.pop(dis_topo.index(cal))
                    dis_topo.append(modweight_tuple)
                if cal[0] !=Mod_result[0] and cal[1] == Mod_result[1] :
                     #print "cal", cal
                     #print "case3"
                     modweight_cal = list(cal)
                     modweight_cal[2]=modweight_cal[2]+.3
                     #print modweight_cal
                     modweight_tuple= tuple(modweight_cal)
                     dis_topo.pop(dis_topo.index(cal))
                     dis_topo.append(modweight_tuple)
     #   for res in result:
    #        if res.find 
     #         pop_cost_result
        # map rule
        #print result[0][0], result[0][1]
        #print node_dpid[result[0][0]]
        # to do
        #print "map rule"
        # mp rule
        #print result[0][1], result[1][0]
        #if result[0][1] == result[1][0]:
            #print result[0][1], "no change"
            #print node_dpid[result[0][1]]
            # to do
        #else:
            #print result[0][1], "change to ", result[1][0]
            #if result[0][1] == '10.10.1.45' or result[0][1] == '10.10.1.55':
                #print "port 2"
                # to do
            #elif result[0][1] == '10.10.3.45' or result[0][1] == '10.10.3.55':
                #print "port 3"
                # to do
        total_topo.append(Throughdis_topo)
        
    return total_topo
    print("######################################################################")
    #for topo in dis_topo:
      #print topo

