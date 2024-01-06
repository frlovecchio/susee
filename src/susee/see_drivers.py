# -*- coding: utf-8 -*-
#################################################
########   Device DRIVERS #######################
#################################################
# Studio Tecnico Pugliautomazione - Bari
# eng. Francesco Saverio Lovecchio
# www.pugliautomazione.it

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
# v2.8 2022-01-25 P32M5, duR, duT
# v2.9 2022-05-24 ab1
# v3.0 2022-12-21 THD: duT, duR, P32M5, ab1
# v3.1 2023-04-04 THD: duT, duR, P32M5, ab1, ab4
# v3.2 2023-10-05 drivers zlog, lv2

from susee.see_comm import c_comm_devices

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class c_driver_P32M5(c_comm_devices):
    '''
    Device: SIEMENS SENTRON PAC3200
    idParam  descrITA                    descrENG        um    Acronimo
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2	            Voltage UL1_L2	V	UL1_L2
    107	  Corrente L1	                Current L1	A	IL1
    141   Max Tensione UL1-UL2
    176   Min Tensione UL1-UL2
    #no132	  Potenza apparente totale	    Apparent Power  - Total	VA	S_TOT
    133	  Potenza attiva totale     	Active Power  - Total	W	P_TOT
    134	  Potenza reattiva totale	    Reactive Power  - Total	VAr	Q_TOT
    135	  Fattore di potenza totale	    Power Factor  - Total	na	PF_TOT
    222	  Energia Attiva importata	    Active Energy Imported 	Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	Reactive Energy Imported	VArh	EnQ_Imp_Tar1
    208   Contapezzi
    '''

    # v. 1.0     2022 - 02 - 14
    # v. 2.0     2022 - 04 - 25
    # v. 2.1     2022-11-11 added 176 and 141

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        # Set Address list
        self.addrList = {}
        self.addrList[1] = (1, 83)
        self.addrList[2] = (801, 837)
        self.addrList[3] = (213, 221)
        self.addrList[4] = (149, 155)
        self.paramDict()

    def paramDict(self):
        # Parameters format

        numPar = -1
        addrList = self.addrList

        # 104 Tensione  L1L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 7 - (addrList[1][0] - 1),
            'idParam': 104,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0,
            'words': 2,
            'type': 0,
        }


        # 141 Tensione  Massima UL1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 81 - (addrList[1][0] - 1),
            'idParam': 141,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 176 Tensione  Minima UL1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 151 - (addrList[4][0] - 1),
            'idParam': 176,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0,
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
            'max': '',
            'min': '',
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # # 132 - Potenza Apparente totale
        # numPar += 1
        # self.pDict[numPar] = {
        #     'idAddrList': 1,
        #     'addr': 63 - (addrList[1][0] - 1),
        #     'idParam': 132,
        #     'k': 1,
        #     'offset': 0,
        #     'words': 2,
        #     'type': 0,
        # }

        # 133 - Potenza attiva totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 65 - (addrList[1][0] - 1),
            'idParam': 133,
            'k': 1,
            'max': '',
            'min': '',
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
            'max': '',
            'min': '',
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
            'max': '',
            'min': '',
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

        # 208 - Contapezzi
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 215 - (addrList[3][0] - 1),
            'idParam': 208,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 1,
        }
class c_driver_P32M5_THD(c_comm_devices):
    '''
    Device: SIEMENS SENTRON PAC3200 + Armoniche
    idParam  descrITA                    descrENG        um    Acronimo
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2	            Voltage UL1_L2	V	UL1_L2
    107	  Corrente L1	                Current L1	A	IL1
    141   Max Tensione UL1-UL2
    176   Min Tensione UL1-UL2
    #no132	  Potenza apparente totale	    Apparent Power  - Total	VA	S_TOT
    133	  Potenza attiva totale     	Active Power  - Total	W	P_TOT
    134	  Potenza reattiva totale	    Reactive Power  - Total	VAr	Q_TOT
    135	  Fattore di potenza totale	    Power Factor  - Total	na	PF_TOT
    222	  Energia Attiva importata	    Active Energy Imported 	Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	Reactive Energy Imported	VArh	EnQ_Imp_Tar1
    208   Contapezzi
    -------------------------------------------------------------------
    122	THD_R di tensione L1	THD_R  Voltage L1	%	VTHD_L1  43   max(117)
    123	THD_R di tensione L2	THD_R  Voltage L2	%	VTHD_L2  45
    124	THD_R di tensione L3	THD_R  Voltage L3	%	VTHD_L3  47
    125	THD_R di corrente L1	THD_R  Current L1	%	ITHD_L1  49
    126	THD_R di corrente L2	THD_R  Current L2	%	ITHD_L2  51
    127	THD_R di corrente L3	THD_R  Current L3	%	ITHD_L3  53
    '''

    # v. 1.0     2022 - 02 - 14
    # v. 2.0     2022 - 04 - 25
    # v. 2.1     2022-11-11 added 176 and 141
    # v. 3.0     2022-12-21 added THDV THDI
    # v. 3.1     2023-01-05 fixed THD addresses

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        # Set Address list
        self.addrList = {}
        self.addrList[1] = (1, 83)
        self.addrList[2] = (801, 837)
        self.addrList[3] = (213, 221)
        self.addrList[4] = (117, 155)
        self.paramDict()

    def paramDict(self):
        # Parameters format

        numPar = -1
        addrList = self.addrList

        # 104 Tensione  L1L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 7 - (addrList[1][0] - 1),
            'idParam': 104,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0,
            'words': 2,
            'type': 0,
        }


        # 141 Tensione  Massima UL1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 81 - (addrList[1][0] - 1),
            'idParam': 141,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 176 Tensione  Minima UL1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 151 - (addrList[4][0] - 1),
            'idParam': 176,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0,
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
            'max': '',
            'min': '',
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # # 132 - Potenza Apparente totale
        # numPar += 1
        # self.pDict[numPar] = {
        #     'idAddrList': 1,
        #     'addr': 63 - (addrList[1][0] - 1),
        #     'idParam': 132,
        #     'k': 1,
        #     'offset': 0,
        #     'words': 2,
        #     'type': 0,
        # }

        # 133 - Potenza attiva totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 65 - (addrList[1][0] - 1),
            'idParam': 133,
            'k': 1,
            'max': '',
            'min': '',
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
            'max': '',
            'min': '',
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
            'max': '',
            'min': '',
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

        # 208 - Contapezzi
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 215 - (addrList[3][0] - 1),
            'idParam': 208,
            'k': 1,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        #------------------------------------

        # 122	THD_R di tensione L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 43 - (addrList[1][0] - 1),
            'idParam': 122,
            'k': 1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 123	THD_R di tensione L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 45 - (addrList[1][0] - 1),
            'idParam': 123,
            'k': 1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 124	THD_R di tensione L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 47 - (addrList[1][0] - 1),
            'idParam': 124,
            'k': 1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 125	THD_R di corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 49 - (addrList[1][0] - 1),
            'idParam': 125,
            'k': 1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 126	THD_R di corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 51 - (addrList[1][0] - 1),
            'idParam': 126,
            'k': 1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 0,
        }

        # 127	THD_R di corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 53 - (addrList[1][0] - 1),
            'idParam': 127,
            'k': 1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 0,
        }
class c_driver_sh2(c_comm_devices):
    '''
    Device: Schneider PM3250
    idParam  descrITA
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2
    105	  Tensione UL2_L3
    106	  Tensione UL3_L1
    107	  Corrente L1
    108	  Corrente L2
    109	  Corrente L3
    119   Fattore di potenza L1
    120   Fattore di potenza L2
    121   Fattore di potenza L3
    133	  Potenza attiva totale     	 	W	P_TOT
    134	  Potenza reattiva totale	     	VAr	Q_TOT
    135	  Fattore di potenza totale	        na	PF_TOT
    222	  Energia Attiva importata	        Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	    VArh	EnQ_Imp_Tar1
    '''

    # v2.0 2020-09-30
    # v3.1 2021-01-26
    # v3.2 2022-04-25

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {}
        self.addrList[1] = (3000 - 1, 3036 - 1)
        self.addrList[2] = (3060 - 1, 3096 - 1)
        self.addrList[3] = (3204 - 1, 3224 - 1)
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        pDict = {}
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3020 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3022 - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3024 - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3000 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 5 - 108 Corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3002 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 6 - 109 Corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3004 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 3078 - (addrList[2][0] + shift_),
            'idParam': 119,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 3080 - (addrList[2][0] + shift_),
            'idParam': 120,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        #  10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 3082 - (addrList[2][0] + shift_),
            'idParam': 121,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        #  11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 3060 - (addrList[2][0] + shift_),
            'idParam': 133,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 3068 - (addrList[2][0] + shift_),
            'idParam': 134,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 3084 - (addrList[2][0] + shift_),
            'idParam': 135,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 6,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 3204 - (addrList[3][0] + shift_),
            'idParam': 222,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 4,
            'type': 3,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 3220 - (addrList[3][0] + shift_),
            'idParam': 226,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 4,
            'type': 3,
        }
class c_driver_duR(c_comm_devices):
    '''
    Device: DUCATI  DUCA-LCD-RTU
    idParam  descrITA
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2
    105	  Tensione UL2_L3
    106	  Tensione UL3_L1
    107	  Corrente L1
    108	  Corrente L2
    109	  Corrente L3
    119   Fattore di potenza L1
    120   Fattore di potenza L2
    121   Fattore di potenza L3
    133	  Potenza attiva totale     	 	W	P_TOT
    134	  Potenza reattiva totale	     	VAr	Q_TOT
    135	  Fattore di potenza totale	        na	PF_TOT
    222	  Energia Attiva importata	        Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	    VArh	EnQ_Imp_Tar1
    '''

    # Ducati
    # v1.0 2021-01-10
    # v2.0 2022-04-25

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}
        # Set Address list
        self.addrList = {}
        self.addrList[1] = (1, 41)
        self.addrList[2] = (79, 121)
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        pDict = {}
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 6 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 8 - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 10 - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 20 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 5  - 108 Corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 22 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 6  - 109 Corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 24 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 26 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 28 - (addrList[1][0] + shift_),
            'idParam': 119,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 30 - (addrList[1][0] + shift_),
            'idParam': 120,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 32 - (addrList[1][0] + shift_),
            'idParam': 121,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 34 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 82 - (addrList[2][0] + shift_),
            'idParam': 134,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 106 - (addrList[2][0] + shift_),
            'idParam': 222,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 114 - (addrList[2][0] + shift_),
            'idParam': 226,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }
class c_driver_duR_THD(c_comm_devices):
    '''

    Device: DUCATI DUCA-LCD-RTU  THD
    idParam descrITA

    -------------------------------------------------------------------------

    104	Tensione UL1_L2
    105 Tensione UL2_L3
    106	Tensione UL3_L1
    107	Corrente L1
    108	Corrente L2
    109	Corrente L3
    119 Fattore di potenza L1
    120 Fattore di potenza L2
    121 Fattore di potenza L3
    133	Potenza attiva totale     	 	W	P_TOT
    134	Potenza reattiva totale	     	VAr	Q_TOT
    135	Fattore di potenza totale	        na	PF_TOT
    222	Energia Attiva importata	        Wh	EnP_Imp_Tar1
    226	Energia Reattiva importata	    VArh	EnQ_Imp_Tar1

    --------------------------------------------------------------------------

    122	THD_R di tensione L1	THD_R  Voltage L1	%	VTHD_L1  218  (%/10)
    123	THD_R di tensione L2	THD_R  Voltage L2	%	VTHD_L2  220  (%/10)
    124	THD_R di tensione L3	THD_R  Voltage L3	%	VTHD_L3  222  (%/10)
    125	THD_R di corrente L1	THD_R  Current L1	%	ITHD_L1  212  (%/10)
    126	THD_R di corrente L2	THD_R  Current L2	%	ITHD_L2  214  (%/10)
    127	THD_R di corrente L3	THD_R  Current L3	%	ITHD_L3  216  (%/10)

    '''

    # Ducati
    # v1.0 2021-01-10
    # v2.0 2022-04-25
    # v3.0 2022-12-21   THD

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}
        # Set Address list
        self.addrList = {}
        self.addrList[1] = (1, 41)
        self.addrList[2] = (79, 121)
        self.addrList[3] = (211, 233)
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        pDict = {}
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 6 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 8 - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 10 - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 20 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 5  - 108 Corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 22 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 6  - 109 Corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 24 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 26 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 28 - (addrList[1][0] + shift_),
            'idParam': 119,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 30 - (addrList[1][0] + shift_),
            'idParam': 120,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 32 - (addrList[1][0] + shift_),
            'idParam': 121,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 34 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 82 - (addrList[2][0] + shift_),
            'idParam': 134,
            'k': 1.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 106 - (addrList[2][0] + shift_),
            'idParam': 222,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 114 - (addrList[2][0] + shift_),
            'idParam': 226,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # ------------------------------------

        # 122	THD_R di tensione L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 218 - (addrList[3][0] + shift_),
            'idParam': 122,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 123	THD_R di tensione L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 220 - (addrList[3][0] + shift_),
            'idParam': 123,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 124	THD_R di tensione L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 222 - (addrList[3][0] + shift_),
            'idParam': 124,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 125	THD_R di corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 212 - (addrList[3][0] + shift_),
            'idParam': 125,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 126	THD_R di corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 214 - (addrList[3][0] + shift_),
            'idParam': 126,
            'max': 1000,
            'min': 0,
            'k': .1,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 127	THD_R di corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 216 - (addrList[3][0] + shift_),
            'idParam': 127,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }
class c_driver_duT(c_comm_devices):
    '''
    Device: DUCATI  DUCA-LCD-TCP
    idParam  descrITA
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2
    105	  Tensione UL2_L3
    106	  Tensione UL3_L1
    107	  Corrente L1
    108	  Corrente L2
    109	  Corrente L3
    119   Fattore di potenza L1
    120   Fattore di potenza L2
    121   Fattore di potenza L3
    133	  Potenza attiva totale     	 	W	P_TOT
    134	  Potenza reattiva totale	     	VAr	Q_TOT
    135	  Fattore di potenza totale	        na	PF_TOT
    222	  Energia Attiva importata	        Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	    VArh	EnQ_Imp_Tar1
    128   Frequenza di rete   Hz
    '''

    # Ducati
    # v1.0 2021-01-10
    # v2.0 2022-04-25

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {1: (0x1008, 0x1042),
                         2: (0x1046, 0x1048)
                         }

        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 0
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1008 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x100A - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x100C - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1010 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 5  - 108 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1012 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 6  - 109 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1014 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1016 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1018 - (addrList[1][0] + shift_),
            'idParam': 119,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x101A - (addrList[1][0] + shift_),
            'idParam': 120,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x101C - (addrList[1][0] + shift_),
            'idParam': 121,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x102E - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1036 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x103E - (addrList[1][0] + shift_),
            'idParam': 222,
            'k': 100,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1040 - (addrList[1][0] + shift_),
            'idParam': 226,
            'k': 100,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 15  - 128 frequenza
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 0x1046 - (addrList[2][0] + shift_),
            'idParam': 128,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

class c_driver_duT_THD(c_comm_devices):

    '''
    Device: DUCATI  DUCA-LCD-TCP
    idParam  descrITA
    -------------------------------------------------------------------------
    104	 Tensione UL1_L2
    105	 Tensione UL2_L3
    106	 Tensione UL3_L1
    107	 Corrente L1
    108	 Corrente L2
    109	 Corrente L3
    119  Fattore di potenza L1
    120  Fattore di potenza L2
    121  Fattore di potenza L3
    133	 Potenza attiva totale     	 	W	P_TOT
    134	 Potenza reattiva totale	    VAr	Q_TOT
    135	 Fattore di potenza totale	    na	PF_TOT
    222	 Energia Attiva importata	    Wh	EnP_Imp_Tar1
    226	 Energia Reattiva importata	    VAr EnQ_Imp_Tar1
    128  Frequenza di rete Hz

    -------------------------------------------------------------------------

    122	THD_R di tensione L1	THD_R  Voltage L1	%	VTHD_L1  1306H  (%/10)
    123	THD_R di tensione L2	THD_R  Voltage L2	%	VTHD_L2  1308H  (%/10)
    124	THD_R di tensione L3	THD_R  Voltage L3	%	VTHD_L3  130AH  (%/10)
    125	THD_R di corrente L1	THD_R  Current L1	%	ITHD_L1  1300H  (%/10)
    126	THD_R di corrente L2	THD_R  Current L2	%	ITHD_L2  1302H  (%/10)
    127	THD_R di corrente L3	THD_R  Current L3	%	ITHD_L3  1304H  (%/10)

    '''
    # Ducati
    # v1.0 2021-01-10
    # v2.0 2022-04-25
    # v3.0 2022-12-21  THD

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}

        # Set Address list
        self.addrList = {
                         1: (0x1008, 0x1042),
                         2: (0x1046, 0x1048),
                         3: (0x1300, 0x130A)
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 0
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1008 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x100A - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x100C - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1010 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 5  - 108 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1012 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 6  - 109 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1014 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1016 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1018 - (addrList[1][0] + shift_),
            'idParam': 119,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x101A - (addrList[1][0] + shift_),
            'idParam': 120,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x101C - (addrList[1][0] + shift_),
            'idParam': 121,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x102E - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1036 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x103E - (addrList[1][0] + shift_),
            'idParam': 222,
            'k': 100,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 0x1040 - (addrList[1][0] + shift_),
            'idParam': 226,
            'k': 100,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 15  - 128 frequenza
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 0x1046 - (addrList[2][0] + shift_),
            'idParam': 128,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        #---------------------------------


        # 122	THD_R di tensione L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 0x1306 - (addrList[3][0] + shift_),
            'idParam': 122,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 123	THD_R di tensione L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 0x1308 - (addrList[3][0] + shift_),
            'idParam': 123,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 124	THD_R di tensione L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 0x130A - (addrList[3][0] + shift_),
            'idParam': 124,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 125	THD_R di corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 0x1300 - (addrList[3][0] + shift_),
            'idParam': 125,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 126	THD_R di corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 0x1302 - (addrList[3][0] + shift_),
            'idParam': 126,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }

        # 127	THD_R di corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 0x1304 - (addrList[3][0] + shift_),
            'idParam': 127,
            'k': .1,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 2,
            'type': 1,
        }




class c_driver_ab1(c_comm_devices):
    '''
    Device: ABB M4M 20
    idParam  descrITA
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2
    105	  Tensione UL2_L3
    106	  Tensione UL3_L1
    107	  Corrente L1
    108	  Corrente L2
    109	  Corrente L3
    119   Fattore di potenza L1
    120   Fattore di potenza L2
    121   Fattore di potenza L3
    133	  Potenza attiva totale     	 	W	P_TOT
    134	  Potenza reattiva totale	     	VAr	Q_TOT
    135	  Fattore di potenza totale	        na	PF_TOT
    222	  Energia Attiva importata	        Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	    VArh	EnQ_Imp_Tar1
    '''

    # v1.0 2022-05-23

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {1: (23298, 23364),
                         2: (20480, 20498),
                         3: (23808, 23810),
                         # 4: (23808, 23808),
                         # 5: (23936, 23936),
                         # 6: (24064, 24064),
                         4: (24576, 24578),
                         5: (24704, 24706),
                         6: (24832, 24834),
                         # 2: (23516, 23587),
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 0
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23304 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23306 - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23308 - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23312 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 5  - 108 Corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23314 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 6  - 109 Corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23316 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23360 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23361 - (addrList[1][0] + shift_),
            'idParam': 119,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23362 - (addrList[1][0] + shift_),
            'idParam': 120,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23363 - (addrList[1][0] + shift_),
            'idParam': 121,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23322 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23330 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 20480 - (addrList[2][0] + shift_),
            'idParam': 222,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 4,
            'type': 3,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 20492 - (addrList[2][0] + shift_),
            'idParam': 226,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 4,
            'type': 3,
        }


class c_driver_ab1_THD(c_comm_devices):
    '''
    Device: ABB M4M 20
    idParam  descrITA
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2
    105	  Tensione UL2_L3
    106	  Tensione UL3_L1
    107	  Corrente L1
    108	  Corrente L2
    109	  Corrente L3
    119   Fattore di potenza L1
    120   Fattore di potenza L2
    121   Fattore di potenza L3
    133	  Potenza attiva totale     	 	W	P_TOT
    134	  Potenza reattiva totale	     	VAr	Q_TOT
    135	  Fattore di potenza totale	        na	PF_TOT
    222	  Energia Attiva importata	        Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	    VArh	EnQ_Imp_Tar1
    122	THD_R di tensione L1 %
    123	THD_R di tensione L2 %
    124	THD_R di tensione L3 %
    125	THD_R di corrente L1 %
    126	THD_R di corrente L2 %
    127	THD_R di corrente L3 %

    '''

    # v1.0 2022-05-23
    # v1.1 2023-01-04

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {1: (23298, 23364),
                         2: (20480, 20498),
                         3: (23808, 23810),
                         7: (23936, 23938),
                         8: (24064, 24066),
                         4: (24576, 24578),
                         5: (24704, 24706),
                         6: (24832, 24834),
                         # 2: (23516, 23587),
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList

        # Calcolo parametri
        # 1  - 104 Tensione  L1L2
        numPar += 1
        shift_ = 0
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23304 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 2  - 105 Tensione  L2L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23306 - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 3  - 106 Tensione  L3L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23308 - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 4  - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23312 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 5  - 108 Corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23314 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 6  - 109 Corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23316 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        # 7  - 135 fdp tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23360 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 8  - 119 fdp L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23361 - (addrList[1][0] + shift_),
            'idParam': 119,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 9  - 120 fdp L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23362 - (addrList[1][0] + shift_),
            'idParam': 120,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 10  - 121 fdp L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23363 - (addrList[1][0] + shift_),
            'idParam': 121,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 11  - 133 P Attiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23322 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 2,
        }

        # 12  - 134 P Reattiva Tot
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23330 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 0.01,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 20,
        }

        # 13  - 222 Energia Attiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 20480 - (addrList[2][0] + shift_),
            'idParam': 222,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 4,
            'type': 3,
        }

        # 14  - 226 Energia Reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 20492 - (addrList[2][0] + shift_),
            'idParam': 226,
            'k': 10.0,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 4,
            'type': 3,
        }

    #---------------- THD ---------------------------
        # 15  - 122 VTHD% L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 23808 - (addrList[3][0] + shift_),
            'idParam': 122,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 15  - 123 VTHD% L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 7,
            'addr': 23936 - (addrList[7][0] + shift_),
            'idParam': 123,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 15  - 124 VTHD% L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 8,
            'addr': 24064 - (addrList[8][0] + shift_),
            'idParam': 124,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 16  - 125 ITHD% I1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 24576 - (addrList[4][0] + shift_),
            'idParam': 125,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 17  - 126 ITHD% I2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 24704 - (addrList[5][0] + shift_),
            'idParam': 126,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 18  - 127 ITHD% I3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 6,
            'addr': 24832 - (addrList[6][0] + shift_),
            'idParam': 127,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }


class c_driver_ab2(c_comm_devices):
    '''
    Device: ABB ABB REF615 - relè di protezione
    idParam  descrITA
    -------------------------------------------------------------------------
        IDPAR	Description	u.m.	DeviceType	Addr	Word	Type	Fcode	RW	 k
        107	Corrente L1	A		138	1	Unsigned	FC04	R	 0,001
        108	Corrente L2	A		139	1	Unsigned	FC04	R	 0,001
        109	Corrente L3	A		140	1	Unsigned	FC04	R	 0,001
        263	Corrente Neutro	A		141	1	Unsigned	FC04	R	 0,001
        104	Tensione UL1_L2	V		155	1	Unsigned	FC04	R	 0,001*Un
        105	Tensione UL2_L3	V		156	1	Unsigned	FC04	R	 0,001*Un
        106	Tensione UL3_L1	V		157	1	Unsigned	FC04	R	 0,001*Un
        132	Potenza apparente totale	VA		161	2	SignedLong	FC04	R	 1.000,000
        133	Potenza attiva totale	W		163	2	SignedLong	FC04	R	 1.000,000
        134	Potenza reattiva totale	VAr		165	2	SignedLong	FC04	R	 1.000,000
        135	Fattore di potenza totale	na		167	1	Signed	FC04	R	 0,001
        128	Frequency	Hz		168	1	Unsigned	FC04	R	 0,010
        222	Energia Attiva importata	Wh		2041	2	Unsigned	FC04	R	 1.000,000
        226	Energia Reattiva importata	VArh		2043	2	Unsigned	FC04	R	 1.000,000

    '''
    # v1.0 2022-06-12
    # v1.1 2022-06-24

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}
        # Set Address list
        self.addrList = {1: (130, 170),
                         2: (2040, 2050)
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList
        shift_ = 1
        k_v = 0.001*20000
        k_a = 0.078836
        type_= 2
        # Calcolo parametri
        # 1  - 107 Tensione  L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 155 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': k_v,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }

        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 156 - (addrList[1][0] + shift_),
            'idParam': 105,
            'k': k_v,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 157 - (addrList[1][0] + shift_),
            'idParam': 106,
            'k': k_v,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }

        # 4  -  107	Corrente L1	pu
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 138 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': k_a,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }

        # 3  -  107	Corrente L1	pu
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 139 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': k_a,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }
        # 3  -  107	Corrente L1	pu
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 140 - (addrList[1][0] + shift_),
            'idParam': 109,
            'k': k_a,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }

        # 3  -  263 Corrente neutro [A]
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 141 - (addrList[1][0] + shift_),
            'idParam': 263,
            'k': k_a,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }

        # 3  -  128	Frequenza
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 168 - (addrList[1][0] + shift_),
            'idParam': 128,
            'k': 0.01*100,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }


        # 3  -  132	Pot. App Totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 165 - (addrList[1][0] + shift_),
            'idParam': 132,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 3  -  133	Pot. attiva Totale [W]
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 161 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 3  -  134	Pot. reattiva Totale [VAr]
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 163 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 3 - 135 Fattore di potenza Totale []
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 167 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 1,
        }
class c_driver_ab3(c_comm_devices):
    '''
    Device: ABB PR120/D-M communication module
    Function read_inputs (04)
    idParam  descrITA
    -------------------------------------------------------------------------
       IDPAR	Description	u.m.	DeviceType	Addr
        1000	State 1	na		100
        1001	State 2	na		101
        1002	State 3	na		102
        1003	State 4	na		103
        1004	State 5	na		104
        1005	State 6	na		105
        1006	State 7	na		106
        1007	State 8	na		107
        1008	State 9	na		108


    '''
    # v1.0 2022-06-15

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}
        # Set Address list
        self.addrList = {1: (100, 108)}
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList
        shift_ = 0
        # Calcolo parametri
        # 1 - 1000	State 1	na
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 100 - (addrList[1][0] + shift_),
            'idParam': 1000,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 2 - 1001	State 1	na
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 101 - (addrList[1][0] + shift_),
            'idParam': 1001,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        # 3 - 1002 State 1	na
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 102 - (addrList[1][0] + shift_),
            'idParam': 1002,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,

        }

        # 4 - 1001	State 1	na
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 103 - (addrList[1][0] + shift_),
            'idParam': 1004,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
class c_driver_ab4(c_comm_devices):
    '''
    Device: ABB ABB Ekip COM - Interruttori di potenza
    IDPAR	Description	u.m.	DeviceType	Addr	Word	Type
    107	Corrente L1	A	F04	100	2	Ulong			 0,10000
    108	Corrente L2	A	F04	102	2	Ulong			 0,10000
    109	Corrente L3	A	F04	104	2	Ulong			 0,10000
    263	Corrente Neutro	A	F04	106	2	Ulong			 0,10000
    101	Tensione UL1_N	V	F04	150	1	Ulong			 0,10000
    102	Tensione UL2_N	V	F04	151	1	Ulong			 0,10000
    103	Tensione UL3_N	V	F04	152	1	Ulong			 0,10000
    104	Tensione UL1_L2	V	F04	154	1	Ulong			 0,10000
    105	Tensione UL2_L3	V	F04	155	1	Ulong			 0,10000
    106	Tensione UL3_L1	V	F04	156	1	Ulong			 0,10000
    113	Potenza attiva L1	W	F04	200	1	Ulong			 0,10000
    114	Potenza attiva L2	W	F04	202	1	Ulong			 0,10000
    115	Potenza attiva L3	W	F04	204	1	Ulong			 0,10000
    133	Potenza attiva totale	W	F04	206	1	Ulong			 0,10000
    116	Potenza reattiva L1	VAr	F04	208	1	Ulong			 0,10000
    117	Potenza reattiva L2	VAr	F04	210	1	Ulong			 0,10000
    118	Potenza reattiva L3	VAr	F04	212	1	Ulong			 0,10000
    134	Potenza reattiva totale	VAr	F04	214	1	Ulong			 0,10000
    110	Potenza apparente L1	VA	F04	216	1	Ulong			 0,10000
    111	Potenza apparente L2	VA	F04	218	1	Ulong			 0,10000
    112	Potenza apparente L3	VA	F04	220	1	Ulong			 0,10000
    132	Potenza apparente totale	VA	F04	222	1	Ulong			 0,10000
    119	Fattore di potenza L1	na	F04	250	1	Ulong			 0,00100
    120	Fattore di potenza L2	na	F04	251	1	Ulong			 0,00100
    121	Fattore di potenza L3	na	F04	252	1	Ulong			 0,00100
    135	Fattore di potenza totale	na	F04	253	1	Ulong			 0,00100
    128	Frequency	Hz	F04	254	1	Ulong			 0,01000
    222	Energia Attiva importata	Wh	F04	300	2	Ulong			 1.000
    226	Energia Reattiva importata	VArh	F04	306	2	Ulong			 1.000
    '''
    # v1.0 2022-06-12
    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}
        # Set Address list
        self.addrList = {1: (200  , 224 ),
                         2: (100 ,  106 ),
                         3: (250 ,  254 ),
                         4: (150 ,  158 ),
                         5: (300 ,  306 )
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList
        k_ = 100
        type_= 3
        type_1w_=1

        # Calcolo parametri


        # 107	Corrente L1 A
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 100 - (addrList[2][0]),
            'idParam': 107,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 3,
        }

        # 108	Corrente L2 A
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 102 - (addrList[2][0] ),
            'idParam': 108,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 3,
        }

        # 109	Corrente L3 A
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 104 - (addrList[2][0] ),
            'idParam': 109,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 3,
        }


        # 104	Tensione L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 154 - (addrList[4][0]),
            'idParam': 104,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 105	Tensione L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 155 - (addrList[4][0] ),
            'idParam': 105,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 106	Tensione L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 156 - (addrList[4][0] ),
            'idParam': 106,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }


        # 113	Potenza attiva L1	W	F04	200	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 200 - (addrList[1][0] ),
            'idParam': 113,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }
        # 114	Potenza attiva L2	W	F05	202	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 202 - (addrList[1][0] ),
            'idParam': 114,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 115	Potenza attiva L3	W	F05	204	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 204 - (addrList[1][0] ),
            'idParam': 115,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 133	Potenza attiva totale	W	F07	206	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 206 - (addrList[1][0] ),
            'idParam': 133,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 116	Potenza Reattiva L1 Var	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 208 - (addrList[1][0]),
            'idParam': 116,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 117	Potenza Reattiva L2 Var
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 210 - (addrList[1][0]),
            'idParam': 117,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }


        # 118	Potenza Reattiva L3 Var
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 212 - (addrList[1][0]),
            'idParam': 118,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 134	Potenza Reattiva Totale Var
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 214 - (addrList[1][0] ),
            'idParam': 134,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 119	Fattore di potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 250 - (addrList[3][0] ),
            'idParam': 119,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }

        # 120	Fattore di potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 251 - (addrList[3][0] ),
            'idParam': 120,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }

        # 121	Fattore di potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 252 - (addrList[3][0] ),
            'idParam': 121,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }


        # 135	Fattore di potenza totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 253 - (addrList[3][0] ),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }

        # 222 Energia Attiva Wh
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 300  - (addrList[5][0]),
            'idParam': 222,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 226 Energia reattiva Varh
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 306  - (addrList[5][0]),
            'idParam': 226,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }


class c_driver_ab4_THD(c_comm_devices):
    '''
    Device: ABB ABB Ekip COM - Interruttori di potenza
    IDPAR	Description	u.m.	DeviceType	Addr	Word	Type
    107	Corrente L1	A	F04	100	2	Ulong			 0,10000
    108	Corrente L2	A	F04	102	2	Ulong			 0,10000
    109	Corrente L3	A	F04	104	2	Ulong			 0,10000
    263	Corrente Neutro	A	F04	106	2	Ulong			 0,10000
    101	Tensione UL1_N	V	F04	150	1	Ulong			 0,10000
    102	Tensione UL2_N	V	F04	151	1	Ulong			 0,10000
    103	Tensione UL3_N	V	F04	152	1	Ulong			 0,10000
    104	Tensione UL1_L2	V	F04	154	1	Ulong			 0,10000
    105	Tensione UL2_L3	V	F04	155	1	Ulong			 0,10000
    106	Tensione UL3_L1	V	F04	156	1	Ulong			 0,10000
    113	Potenza attiva L1	W	F04	200	1	Ulong			 0,10000
    114	Potenza attiva L2	W	F04	202	1	Ulong			 0,10000
    115	Potenza attiva L3	W	F04	204	1	Ulong			 0,10000
    133	Potenza attiva totale	W	F04	206	1	Ulong			 0,10000
    116	Potenza reattiva L1	VAr	F04	208	1	Ulong			 0,10000
    117	Potenza reattiva L2	VAr	F04	210	1	Ulong			 0,10000
    118	Potenza reattiva L3	VAr	F04	212	1	Ulong			 0,10000
    134	Potenza reattiva totale	VAr	F04	214	1	Ulong			 0,10000
    110	Potenza apparente L1	VA	F04	216	1	Ulong			 0,10000
    111	Potenza apparente L2	VA	F04	218	1	Ulong			 0,10000
    112	Potenza apparente L3	VA	F04	220	1	Ulong			 0,10000
    132	Potenza apparente totale	VA	F04	222	1	Ulong			 0,10000
    119	Fattore di potenza L1	na	F04	250	1	Ulong			 0,00100
    120	Fattore di potenza L2	na	F04	251	1	Ulong			 0,00100
    121	Fattore di potenza L3	na	F04	252	1	Ulong			 0,00100
    135	Fattore di potenza totale	na	F04	253	1	Ulong			 0,00100
    128	Frequency	Hz	F04	254	1	Ulong			 0,01000
    222	Energia Attiva importata	Wh	F04	300	2	Ulong			 1.000
    226	Energia Reattiva importata	VArh	F04	306	2	Ulong			 1.000

    125	THD_R di corrente L1            264		X				L1 THD	1
    126	THD_R di corrente L2           265		X				L2 THD	1
    127	THD_R di corrente L3           266		X				L3 THD	1
    122	THD_R di tensione L1            268		X				V12 THD	1
    123	THD_R di tensione L2           269		X				V23 THD	1
    124	THD_R di tensione L3           270		X				V31 THD	1

    '''
    # v1.0 2023-01-03

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}
        # Set Address list
        self.addrList = {1: (200  , 224 ),
                         2: (100 ,  106 ),
                         3: (250 ,  270 ),
                         4: (150 ,  158 ),
                         5: (300 ,  306 )
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList
        k_ = 100
        type_= 3
        type_1w_=1

        # Calcolo parametri


        # 107	Corrente L1 A
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 100 - (addrList[2][0]),
            'idParam': 107,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 3,
        }

        # 108	Corrente L2 A
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 102 - (addrList[2][0] ),
            'idParam': 108,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 3,
        }

        # 109	Corrente L3 A
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 104 - (addrList[2][0] ),
            'idParam': 109,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 3,
        }


        # 104	Tensione L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 154 - (addrList[4][0]),
            'idParam': 104,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 105	Tensione L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 155 - (addrList[4][0] ),
            'idParam': 105,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 106	Tensione L1-L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 156 - (addrList[4][0] ),
            'idParam': 106,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }


        # 113	Potenza attiva L1	W	F04	200	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 200 - (addrList[1][0] ),
            'idParam': 113,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }
        # 114	Potenza attiva L2	W	F05	202	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 202 - (addrList[1][0] ),
            'idParam': 114,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 115	Potenza attiva L3	W	F05	204	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 204 - (addrList[1][0] ),
            'idParam': 115,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 133	Potenza attiva totale	W	F07	206	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 206 - (addrList[1][0] ),
            'idParam': 133,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 116	Potenza Reattiva L1 Var	1	Ulong
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 208 - (addrList[1][0]),
            'idParam': 116,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 117	Potenza Reattiva L2 Var
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 210 - (addrList[1][0]),
            'idParam': 117,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }


        # 118	Potenza Reattiva L3 Var
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 212 - (addrList[1][0]),
            'idParam': 118,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 134	Potenza Reattiva Totale Var
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 214 - (addrList[1][0] ),
            'idParam': 134,
            'k': k_,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 119	Fattore di potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 250 - (addrList[3][0] ),
            'idParam': 119,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }

        # 120	Fattore di potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 251 - (addrList[3][0] ),
            'idParam': 120,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }

        # 121	Fattore di potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 252 - (addrList[3][0] ),
            'idParam': 121,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }


        # 135	Fattore di potenza totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 253 - (addrList[3][0] ),
            'idParam': 135,
            'k': 0.001,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': type_1w_,
        }

        # 222 Energia Attiva Wh
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 300  - (addrList[5][0]),
            'idParam': 222,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        # 226 Energia reattiva Varh
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 306  - (addrList[5][0]),
            'idParam': 226,
            'k': 1000,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': type_,
        }

        #------------  THD  -------------------------------


        # 122	THD_R di tensione L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 268 - (addrList[3][0]),
            'idParam': 122,
            'k': .01,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 1,
            'type': type_1w_,
        }

        # 123	THD_R di tensione L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 269 - (addrList[3][0]),
            'idParam': 123,
            'k': .01,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 1,
            'type': type_1w_,
        }

        # 124	THD_R di tensione L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 270 - (addrList[3][0]),
            'idParam': 124,
            'k': .01,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 1,
            'type': type_1w_,
        }

        # 125	THD_R di corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 264 - (addrList[3][0]),
            'idParam': 125,
            'k': .01,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 1,
            'type': type_1w_,
        }

        # 126	THD_R di corrente L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 265 - (addrList[3][0]),
            'idParam': 126,
            'k': .01,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 1,
            'type': type_1w_,
        }

        # 127	THD_R di corrente L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 266 - (addrList[3][0]),
            'idParam': 127,
            'k': .01,
            'max': 1000,
            'min': 0,
            'offset': 0,
            'words': 1,
            'type': type_1w_,
        }


class c_driver_ts1(c_comm_devices):
    '''
    Device: TESAR TSX1 centralina temperature
    Function read_register (03)
    idParam  descrITA
    -------------------------------------------------------------------------
        370	Temperatura Valore n. 1 °C
        371	Temperatura Valore n. 2	°C
        372	Temperatura Valore n. 3	°C
        373	Temperatura Valore n. 4	°C


    '''
    # v1.0 2022-06-12
    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}
        # Set Address list
        self.addrList = {1: (15, 18)}
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList
        shift_ = 0
        # Calcolo parametri
        # 1  - Temperatura Valore n. 1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 15 - (addrList[1][0] + shift_),
            'idParam': 370,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 2  - Temperatura Valore n. 2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 16 - (addrList[1][0] + shift_),
            'idParam': 371,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 3  - Temperatura Valore n. 3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 17 - (addrList[1][0] + shift_),
            'idParam': 372,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        # 4  - Temperatura Valore n. 4
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 18 - (addrList[1][0] + shift_),
            'idParam': 373,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

class c_driver_se1(c_comm_devices):
    '''
    Device: SENECA centralina temperature
    Function holding_register (03)
    idParam  descrITA
    -------------------------------------------------------------------------
        370	Temperatura Valore n. 1 °C  3
    '''
    # v1.0 2022-06-23
    # v1.1 2022-12-21
    # v1.2 2022-12-22


    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)
        self.pDict = {}
        # Set Address list
        self.addrList = {1: (0, 10)}
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori
        numPar = -1
        addrList = self.addrList
        shift_ = 1
        # Calcolo parametri
        # 1  - Temperatura Valore n. 1 °C
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3 - (addrList[1][0] + shift_),
            'idParam': 370,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 4 - (addrList[1][0] + shift_), #temp interno cabina
            'idParam': 371,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 5 - (addrList[1][0] + shift_), #temp cavedio cabina
            'idParam': 372,
            'k': 0.1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

class c_driver_plc608(c_comm_devices):

    '''
    #608 - PLC

    2020-01-09
    IDPAR   Description                                        u.m.    DeviceType    Addr    Word    Type
    1004    222     Energia attiva importata Tariffa 1 di periodo    Wh        CP1            1        2        Ulong
    1005    226     Energia reattiva importata Tariffa 1 di periodo    VArh    CP1            3        2        Ulong
    1002    Stato Fascia oraria 1                            --        CP1            7        2        Ulong
    1003    Stato Fascia oraria 2                            --        CP1            9        2        Ulong
    222    1004    Energia attiva  importata Totale                Wh         CP1            11        2        Ulong
    226    1005    Energia reattiva importata Totale               VArh       CP1            13        2        Ulong
    1006    Limite energetico superato                      na         CP1            15        2        Ulong
    133     Potenza attiva di periodo                       W          CP1            17        2        Ulong
    134     Potenza reattiva di periodo                     Var        CP1            19        2        Ulong

    idAddr 1 regs 1..21  data [49664, 1, 36800, 0, 0, 0, 0, 0, 0, 0, 65535, 32767, 30848, 13194, 0, 0, 2048, 7, 16128, 2] - codeError [0] - SampleTime 0:00:00.251141

    '''

    # v1.0 2022-06-02

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {1: (1, 23),
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori

        numPar = -1
        addrList = self.addrList
        shift_ = 0

        # Calcolo parametri
        # 5  -  222    Energia attiva  importata Totale  Wh

        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 11 - (addrList[1][0] + shift_),
            'idParam': 222,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 4,
        }

        # 6  -  226    Energia reattiva importata Totale VArh
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 13 - (addrList[1][0] + shift_),
            'idParam': 226,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 4,
        }

        # 8  -  133     Potenza attiva di periodo   W
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 17 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 4,
        }

        # 9 -  134     Potenza reattiva di periodo   VAr
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 19 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 1,
            'max': '',
            'min': '',
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 4,
        }

class c_driver_zlog(c_comm_devices):
    # ver 1.0 2023-10-05 / #692

    
    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {1: (22, 50),
                         2: (129, 145),
                         3: (1002, 1032),
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori

        numPar = -1
        addrList = self.addrList
        shift_ = 0

        #1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 22 - (addrList[1][0] + shift_),
            'idParam': 31,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }
        #2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 48 - (addrList[1][0] + shift_),
            'idParam': 32,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 2,
            'type': 1,
        }

        #3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 129 - (addrList[2][0] + shift_),
            'idParam': 33,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        # 4
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 143 - (addrList[2][0] + shift_),
            'idParam': 34,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 5  Z-4RTD2/Temperatura1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1002 - (addrList[3][0] + shift_),
            'idParam': 11,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 6  Z-4RTD2/Temperatura2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1003 - (addrList[3][0] + shift_),
            'idParam': 12,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }

        # 7  Z-4RTD2/Temperatura3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1004 - (addrList[3][0] + shift_),
            'idParam': 13,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }        
        
        # 8  Z-4RTD2/Temperatura3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1005 - (addrList[3][0] + shift_),
            'idParam': 14,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        
        # 9 Z-4AI/Analogico1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1006 - (addrList[3][0] + shift_),
            'idParam': 21,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        
        # 10 Z-4AI/Analogico2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1007 - (addrList[3][0] + shift_),
            'idParam': 22,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        # 11  Z-4AI/Analogico3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1008 - (addrList[3][0] + shift_),
            'idParam': 23,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }
        # 12 Z-4AI/Analogico4
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 3,
            'addr': 1009 - (addrList[3][0] + shift_),
            'idParam': 24,
            'k': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
            'words': 1,
            'type': 0,
        }


class c_driver_lv1(c_comm_devices):
    # ver 1.0 2023-10-10 / #692
    '''
     Parametri                           Addr    k       u.m.
    104    Tensione  L1L2                13     0.01    V
    113    Potenza L1                    19     0.01    W
    114    Potenza L2                    21     0.01    W
    115    Potenza L3                    23     0.01    W
    133    Potenza attiva totale         57     0.01    W
    134    Potenza reattiva totale       59     0.01    Var
    135    Fattore di potenza totale     63
    222    Energia attiva                6689    100    Wh   6687?
    226    Energia reattiva importata    6691    100    VArh
    228    Energia reattiva esportata    6693    100    VArh
    101    V1N  Tensione L1N
    102    V2N  Tensione L2N
    103    V3N  Tensione L3N
    107    I1   Corrente L1
    108    I2   Corrente L2
    109    I3   Corrente L3
    '''

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {
            1: (0x2, 0x42),
            2: (0x1A20, 0x1A32),

        }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori

        numPar = -1
        addrList = self.addrList
        shift_ = -1

        # 1 - 104 Tensione  L1L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 13 - (addrList[1][0] + shift_),
            'idParam': 104,
            'k': 0.01,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 2 - 113 Potenza L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 19 - (addrList[1][0] + shift_),
            'idParam': 113,
            'k': 0.01,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 3 - 114 Potenza L2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 21 - (addrList[1][0] + shift_),
            'idParam': 114,
            'k': 0.01,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 4 - 115 Potenza L3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 23 - (addrList[1][0] + shift_),
            'idParam': 115,
            'k': 0.01,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 5 - 133  Potenza attiva totale W
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 57 - (addrList[1][0] + shift_),
            'idParam': 133,
            'k': 0.01,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 6 - 134 Potenza reattiva totale VAr
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 59 - (addrList[1][0] + shift_),
            'idParam': 134,
            'k': 0.01,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 7 - 135  Fattore di potenza totale
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 63 - (addrList[1][0] + shift_),
            'idParam': 135,
            'k': 0.0001,
            'words': 2,
            'type': 2,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 8 - 222 Energia attiva
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 6687 - (addrList[2][0] + shift_),
            'idParam': 222,
            'k': 100.0,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 9 - 226 Energia reattiva importata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 6691 - (addrList[2][0] + shift_),
            'idParam': 226,
            'k': 100.0,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 10 - 228 Energia reattiva esportata
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 6693 - (addrList[2][0] + shift_),
            'idParam': 228,
            'k': 100.0,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 11 - 101  Tensione L1N
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 1 - (addrList[1][0] + shift_),
            'idParam': 101,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 12 - 102  Tensione L2N
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 3 - (addrList[1][0] + shift_),
            'idParam': 102,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 13 - 103 Tensione L3N
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 5 - (addrList[1][0] + shift_),
            'idParam': 103,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 14 - 107 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 7 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 15 - 108  Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 9 - (addrList[1][0] + shift_),
            'idParam': 108,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 16 - 109 Corrente L1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 1,
            'addr': 11 - (addrList[1][0] + shift_),
            'idParam': 107,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }



class c_driver_lv2(c_comm_devices):
    # ver 1.0 2023-10-05 / #692
    '''
    1 Tensione UL1-L2 – valore medio V
    2 Tensione UL2-L3 – valore medio V
    3 Tensione UL3-L1 – valore medio V
    4 Corrente L1 – valore medio A
    5 Corrente L2 – valore medio A
    6 Corrente L3 – valore medio A
    7 Frequenza – valore medio Hz
    8 Corrente neutro – valore medio A
    9 Fattore di potenza L1 – valore medio .
    10 Fattore di potenza L2 – valore medio .
    11 Fattore di potenza L3 – valore medio .
    12 THD-R di corrente L1 – valore medio %
    13 THD-R di corrente L2 – valore medio %
    14 THD-R di corrente L3 – valore medio %
    15 THD-R di tensione L1-L2 – valore medio %
    16 THD-R di tensione L2-L3 – valore medio %
    17 THD-R di tensione L3-L1 – valore medio %
    18 Corrente L1 – max A
    19 Corrente L2 – max A
    20 Corrente L3 – max A
    21 Tensione UL1-N – min V
    22 Tensione UL2-N – min V
    23 Tensione UL3-N – min V
    24 Energia Attiva importata Wh
    25 Energia Reattiva importata VArh
    26 THD-R di Tensione UL1-N – valore medio V
    27 THD-R di Tensione UL2-N – valore medio V
    28 THD-R di Tensione UL3-N – valore medio V
    29 Corrente L1 - min A
    30 Corrente L2 - min A
    31 Corrente L3 - min A
    32 Tensione UL1-N – max V
    33 Tensione UL2-N – max V
    34 Tensione UL3-N – max V
    '''

    def __init__(self, idDevices_pack, *args, **kwargs):
        super().__init__(idDevices_pack)

        self.pDict = {}

        # Set Address list
        self.addrList = {
                         1: (0x39, 0x41),
                         2: (0x3FF, 0x40B),
                         3: (0x5FF, 0x60B),
                         4: (0x805, 0x831),
                         5: (0x845, 0x863),
                         6: (0x1A1F, 0x1A25)
                         }
        self.paramDict()

    def paramDict(self):
        # Elaborazione registri - valori

        numPar = -1
        addrList = self.addrList
        shift_ = 0

        # 0
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 2,
            'addr': 0 - (addrList[2][0] + shift_),
            'idParam': 138,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 1
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   2,
            'addr':         2 - (addrList[2][0] + shift_),
            'idParam':      139,
            'k':            0.01,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 2
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   2,
            'addr':         4 - (addrList[2][0] + shift_),
            'idParam':      140,
            'k':            0.01,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 3
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   2,
            'addr':         6 - (addrList[2][0] + shift_),
            'idParam':      144,
            'k':            0.0001,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 4
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   2,
            'addr':         8 - (addrList[2][0] + shift_),
            'idParam':      145,
            'k':            0.0001,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 5
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   2,
            'addr':         10 - (addrList[2][0] + shift_),
            'idParam':      146,
            'k':            0.0001,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 6
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   3,
            'addr':         6 - (addrList[3][0] + shift_),
            'idParam':      173,
            'k':            0.01,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 7
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   3,
            'addr':         2 - (addrList[3][0] + shift_),
            'idParam':      174,
            'k':            0.01,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 8
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   3,
            'addr':         4 - (addrList[3][0] + shift_),
            'idParam':      175,
            'k':            0.01,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 9
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   3,
            'addr':         6 - (addrList[3][0] + shift_),
            'idParam':      179,
            'k':            0.0001,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 10
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   3,
            'addr':         8 - (addrList[3][0] + shift_),
            'idParam':      180,
            'k':            0.0001,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 11
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList':   3,
            'addr':         10 - (addrList[3][0] + shift_),
            'idParam':      181,
            'k':            0.0001,
            'words':        2,
            'type':         1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 12
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 0 - (addrList[4][0] + shift_),
            'idParam': 280,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 12
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 0 - (addrList[4][0] + shift_),
            'idParam': 280,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 13
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 2 - (addrList[4][0] + shift_),
            'idParam': 281,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 14
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 4 - (addrList[4][0] + shift_),
            'idParam': 282,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 15
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 6 - (addrList[4][0] + shift_),
            'idParam': 330,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 16
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 8 - (addrList[4][0] + shift_),
            'idParam': 331,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        # 17
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 10 - (addrList[4][0] + shift_),
            'idParam': 332,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 18
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 42 - (addrList[4][0] + shift_),
            'idParam': 348,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        

        # 19
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 0 - (addrList[5][0] + shift_),
            'idParam': 359,
            'k': 0.001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 20
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 12 - (addrList[5][0] + shift_),
            'idParam': 360,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 21
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 14 - (addrList[5][0] + shift_),
            'idParam': 361,
            'k': 0.001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 22
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 16 - (addrList[5][0] + shift_),
            'idParam': 362,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 23
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 18 - (addrList[5][0] + shift_),
            'idParam': 363,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 24
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 20 - (addrList[5][0] + shift_),
            'idParam': 364,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 25
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 22 - (addrList[5][0] + shift_),
            'idParam': 365,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 26
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 24 - (addrList[5][0] + shift_),
            'idParam': 366,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 27
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 26- (addrList[5][0] + shift_),
            'idParam': 367,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
        
        # 28
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 5,
            'addr': 28 - (addrList[5][0] + shift_),
            'idParam': 368,
            'k': 0.01,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 29
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 6,
            'addr': 0 - (addrList[6][0] + shift_),
            'idParam': 222,
            'k': 100,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }


        # 30
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 6,
            'addr': 4 - (addrList[6][0] + shift_),
            'idParam': 226,
            'k': 100,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }


        # 31
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 30 - (addrList[4][0] + shift_),
            'idParam': 342,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 32
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 32 - (addrList[4][0] + shift_),
            'idParam': 343,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }

        # 33
        numPar += 1
        self.pDict[numPar] = {
            'idAddrList': 4,
            'addr': 34 - (addrList[4][0] + shift_),
            'idParam': 344,
            'k': 0.0001,
            'words': 2,
            'type': 1,
            'offset': 0.0,
            'max': '',
            'min': '',
        }
