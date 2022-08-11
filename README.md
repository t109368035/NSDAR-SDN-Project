### 實驗網路架構
<img src="./image/experiment_mesh_structure.jpg">

**網路架構說明**

- SDN控制器 : RYU Controller  
- 節點組成 : 兩個樹梅派連接--結合OLSR以及OVS  
- 使用Wi-Fi頻段 : 2.4GHz以及5GHz  

### 實驗控制器架構
<img src="./image/network_manager_structure.jpg">

**控制器架構說明**

- Slice Manager： [[path_calculate](path_calculate)]   
  - 創建、管理網路切片，分配網路資源。  
- Node Status Collection： [[node_info](node_info)]  
  - 收集、紀錄網路節點上各種資訊。  
- Client Manager： [[get_user](get_user)]
  - 管理網路中的客戶端，為客戶端使用的不同網路流分配網路切片。  

### NSDAR-SDN演算法說明
<img src="./image/network_slice_simulate.jpg" width="500">

**網路切片路由方法介紹**  

- 網路切片創建  
  - 保證不同網路服務之QoS  
- 網路切片路由路徑選擇依據  
  - ETT總和最小之路徑優先  
  - 鏈路頻寬符合網路應用優先  
- 以網路流應用為導向分配網路切片  
  - 相同應用有相同路由路徑  
  - 避免重複制定一樣的路由規則  

### 網路切片設計
<img src="./image/network_slice_design.jpg">

**網路切片設計說明**
- Mission-critical IoT  
  - 在網路環境裡享有20Mbps的頻寬。  
- Mobile Broadband  
  - 在網路環境裡享有10Mbps的頻寬。  
- Massive IoT  
  - 在網路環境裡享有4Mbps的頻寬。  
- Default Path  
  - 在客戶端進入網路環境時，給予客戶連線上網的預設路由路徑，並且在控制器辨認其網路流應用後，將不同應用的網路流分配到不同的網路切片。  
