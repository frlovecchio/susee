# -*- coding: utf-8 -*-
#################################################
########   Device DRIVERS #######################
#################################################
#Studio Tecnico Pugliautomazione - Bari
#eng. Francesco Saverio Lovecchio
#www.pugliautomazione.it

# All rights reserved
# Copyright (c)
# v2.0 2020-07-22
# v2.1 2020-09-23
# v2.2 2020-09-30
# v2.3 2020-10-30
# v2.4 2020-11-01 sh1
# v2.5 2021-01-10 p32M6
# v2.6 2021-02-14 lv
# v2.7 2022-01-24 P32



import logging


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


from susee.see_comm import c_comm_devices


class c_driver_P32(c_comm_devices):
    '''
    Device: SIEMENS SENTRON PAC3200

    idParam  descrITA                    descrENG        um    Acronimo
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2	            Voltage UL1_L2	V	UL1_L2
    107	  Corrente L1	                Current L1	A	IL1
    132	  Potenza apparente totale	    Apparent Power  - Total	VA	S_TOT
    133	  Potenza attiva totale     	Active Power  - Total	W	P_TOT
    134	  Potenza reattiva totale	    Reactive Power  - Total	VAr	Q_TOT
    135	  Fattore di potenza totale	    Power Factor  - Total	na	PF_TOT
    222	  Energia Attiva importata	    Active Energy Imported 	Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	Reactive Energy Imported	VArh	EnQ_Imp_Tar1
    '''
    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        # Set Address list
        self.addrList = {}
        self.addrList[1] = (1, 83)
        self.addrList[2] = (801, 837)
        #pDict
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori

        numPar = -1
        addrList=  self.addrList

        # 104 Tensione  L1L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 7 - (addrList[1][0] - 1),
            'idParam': 104,
            'k': 1,
            'offset':0,
            'words': 2,
            'type': 0,
        }

        # 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 13 - (addrList[1][0] - 1),
            'idParam': 107,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 132 - Potenza Apparente totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 63 - (addrList[1][0] - 1),
            'idParam': 132,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 133 - Potenza attiva totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 65 - (addrList[1][0] - 1),
            'idParam': 133,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 0,
        }


        # 134 - Potenza reattiva totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 67 - (addrList[1][0] - 1),
            'idParam': 134,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 135  - Fattore di potenza
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 69 - (addrList[1][0] - 1),
            'idParam': 135,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 222 - Energia attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 801 - (addrList[2][0] - 1),
            'idParam': 222,
            'k': 1,
            'offset': 0,
            'words': 4,
            'type': 0,
        }


        # 226 - Energia reattiva  importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 817 - (addrList[2][0] - 1),
            'idParam': 226,
            'k': 1,
            'offset': 0,
            'words': 4,
            'type': 0,
        }

