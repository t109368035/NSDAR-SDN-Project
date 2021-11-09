def all_dpid_to_bridge():
    dpid_to_bridge = {
        ### channel:8 and channel:13
        '27310741590990' : 'map15_ovsbr1',
        '145234203695054' : 'map15_ovsbr2',
        '145234203657311' : 'mp55_ovsbr1',
        '27310741570752' : 'mp55_ovsbr2',
        '145234203673937' : 'mpp99_ovsbr1',
        '145234203662402' : 'mpp99_ovsbr2',
        
        ### channel:3 and channel:13
        '145234203392259' : 'map25_ovsbr1',
        '145234203662428' : 'map25_ovsbr2',
        '27310741594218' : 'mp45_ovsbr1',
        '145234203391803' : 'mp45_ovsbr2',
        '27310741608024' : 'mpp98_ovsbr1',
        '145234203695083' : 'mpp98_ovsbr2'
    }

    return dpid_to_bridge