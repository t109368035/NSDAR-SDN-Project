import math

class network_slice :
    def __init__(self,user_data):
        self.user_data = user_data


    def slice_alg(self,user_data):

        wmap_slice={'wmap15':["slice_1","slice_2"],
                    'wmap25':["slice_3","slice_4"]}

        slice_to_vlan = {'slice_1' : ['vlan_1', 'vlan_2'],
                         'slice_2' : ['vlan_3', 'vlan_4'],
                         'slice_3' : ['vlan_5', 'vlan_6'],
                         'slice_4' : ['vlan_7', 'vlan_8']}
        
        slice_set1 = []
        slice_set2 = []            

        t1=0
        t2=0
        t3=0
        c=0
        result=user_data

        for n in range(len(user_data)):
            if user_data[n][2] == 1 :
                t1+=1
            elif user_data[n][2] == 2 :
                t2+=1
            elif user_data[n][2] == 3 :
                t3+=1
        tt = t1+t2+t3
        #print ("t1 : " , t1 , " t2 : " , t2 , " t3 : " , t3 , "tt :" , tt)
        
        #choose slice
        for i in range(len(user_data)):    
            if t1 == 0 :
                if t2 == 0 :
                    if t3 == 0 :
                        continue
                    else:
                        result=user_data
                        result[i].append(wmap_slice[user_data[i][0]][0])

                else :
                    if user_data[i][2] == 2 and c < round(t2/2.0) :
                        result[i].append(wmap_slice[user_data[i][0]][0])
                        c+=1
                    elif user_data[i][2] == 2 :
                        result[i].append(wmap_slice[user_data[i][0]][1])
                    elif user_data[i][2] == 3 and t2%2 == 0 :
                        result[i].append(wmap_slice[user_data[i][0]][0])
                    elif user_data[i][2] == 3 :
                        result[i].append(wmap_slice[user_data[i][0]][1])

            else :
                if t2 > 4 :
                    if user_data[i][2] == 1 :
                        result[i].append(wmap_slice[user_data[i][0]][0])
                    elif user_data[i][2] == 2 and c < (tt-2):
                        result[i].append(wmap_slice[user_data[i][0]][1])
                        c+=1
                    elif user_data[i][2] == 2 :
                        result[i].append(wmap_slice[user_data[i][0]][0])        
                    elif user_data[i][2] == 3 and t2 > tt/2.0 :
                        result[i].append(wmap_slice[user_data[i][0]][0])
                    elif user_data[i][2] == 3 :
                        result[i].append(wmap_slice[user_data[i][0]][1])

                else :
                    if user_data[i][2] == 1 :
                        result[i].append(wmap_slice[user_data[i][0]][0])
                    elif user_data[i][2] == 2 :
                        result[i].append(wmap_slice[user_data[i][0]][1])      
                    elif user_data[i][2] == 3 and t2 > tt/2.0 :
                        result[i].append(wmap_slice[user_data[i][0]][0])
                    elif user_data[i][2] == 3 :
                        result[i].append(wmap_slice[user_data[i][0]][1])    

        #set queue
        for j in range(len(user_data)):
            if user_data[j][2] == 1 :
                result[j][2]="q1"

            elif user_data[j][2] == 2 :
                result[j][2]="q2"

            elif user_data[j][2] == 3 :
                result[j][2]="q3"

        #return result

        for k in range(len(result)) :
            if result[k][3] == wmap_slice[result[k][0]][0] :
                slice_set1.append(result[k])
            elif  result[k][3] == wmap_slice[result[k][0]][1] :
                slice_set2.append(result[k])

        vlan_set1 = slice_set1
        vlan_set2 = slice_set2

        for m in range(len(slice_set1)) :
            Q1=slice_set1[0][2]
            if slice_set1[m][2] == Q1 :
                vlan_set1[m][3] = slice_to_vlan[slice_set1[m][3]][0]
            else :
                vlan_set1[m][3] = slice_to_vlan[slice_set1[m][3]][1] 

        for l in range(len(slice_set2)) :
            Q2=slice_set2[0][2]
            if slice_set2[l][2] == Q2 :
                vlan_set2[l][3] = slice_to_vlan[slice_set2[l][3]][0]
            else :
                vlan_set2[l][3] = slice_to_vlan[slice_set2[l][3]][1]            

        vlan_result = vlan_set1 + vlan_set2
        return vlan_result



   

    '''
    def vlan_choose(self,slice_result) :

        wmap_slice={"10.10.1.15":["slice_1","slice_2"],
                    "10.10.1.25":["slice_3","slice_4"]}
        
        slice_to_vlan = {'slice_1' : ['vlan_1', 'vlan_2'],
                         'slice_2' : ['vlan_3', 'vlan_4'],
                         'slice_3' : ['vlan_5', 'vlan_6'],
                         'slice_4' : ['vlan_7', 'vlan_8']}
        
        slice_set1 = []
        slice_set2 = []
        '''

             





        