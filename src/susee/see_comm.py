# -*- coding: utf-8 -*-
###############################################
###########  COMMUNICATION FUNCTIONS  #########
###############################################
# 2020-09-23
# 2021-01-31  v3.0
# 2021-02-03  v3.1
# 2021-02-15  v3.2
# 2021-03-11  v3.3  rs485 try connection
# 2021-03-18  v3.4  stop thread option
# 2022-02-02  v3.5
# 2022-02-14  v3.6
# 2022-04-19  v3.7
# 2022-06-12  v3.8
# 2022-07-10  v3.9  run -> rMode
# 2022-07-31  v4.0
# 2022-08-02  v4.1
# 2022-08-11  v4.2
# 2022-08-12  v4.3
# 2022-08-16  v4.4
# 2022-08-19  v4.5
# 2022-08-20  v4.6
# 2022-11-11  v4.7
# 2022-11-17  v4.8
# 2022-12-21  v4.9  build_param check range
# 2023-08-12  v5.0  # try... pymodbus.client

try:
    # python >3.8
    from pymodbus.client import ModbusSerialClient as ModbusRTU
    from pymodbus.client import ModbusTcpClient as ModbusTCP
except:
    # python <=3.8
    from pymodbus.client.sync import ModbusSerialClient as ModbusRTU
    from pymodbus.client.sync import ModbusTcpClient as ModbusTCP

import threading
import time

from susee.see_functions import build_param, t_to_DateTime
from susee.see_dict import err_code


import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


#
# Communication Class - reads devices with Modbus Protocol
#
# v3.0 2021-01-31   - threads
# v3.1 2021-01-26
# v3.2 2021-01-31
# v3.3 2022-02-02   - minors
# v3.5 2022-06-12
# v4.0 2022-07-31

class c_comm_devices(threading.Thread):
    def __init__(self, idDevPack, *args, **kwargs):
        super(c_comm_devices, self).__init__(*args, **kwargs)
        '''
        Example idDevPack:
            idDevices_pack = {}
            idDevices_pack[0] = {
                    'typeDev': 'P32',
                    'idDev': 'd00',
                    'method': 'tcp',
                    'ipAddr_COM': '192.168.1.100',
                    'idAddr': 1,
                    'Function': 'rr'
                    'Port': '502',
                    'timeout': 1,
                    'enable': 1,
                }
        '''
        self.idDevPack = idDevPack
        self.addrList = []
        self.num = 0
        self.time_ = [0]*6
        self.read_en = False
        #self.sync_ = True
        self.stop = False
        self.TimeStamp_ns = time.time_ns()  # time reference of sample: "sampling time".
        self.TimeNow = '' #datetime.fromtimestamp(self.TimeStamp_ns * 10 ** -9)
        self.pDict = {}


        #uCode - identificativo dispositivo di rete
        self.uCode = ';'.join((idDevPack['method'], idDevPack['ipAddr_COM'], idDevPack['Port']))

    def open_conn(self):
        # v2.0  2022-08-01
        if self.idDevPack['method'] == 'rtu':
            #
            # Connessione RTU
            #
            COMport = self.idDevPack['ipAddr_COM']
            baudrate = self.idDevPack['baudrate']
            timeout = self.idDevPack['timeout']
            Parity = self.idDevPack['parity']  # 'N': none; 'E': even; 'O': odd; default: N
            Stopbits = self.idDevPack['StopBits']  # 1

            self.client = ModbusRTU(
                method='rtu',
                port=COMport,
                baudrate=baudrate,
                timeout=timeout,
                parity=Parity,
                Bytesize=8,
                Stopbitss=Stopbits,
            )

        elif self.idDevPack['method'] == 'tcp':
            #
            # Connessione TCP
            #
            ipAddr = self.idDevPack['ipAddr_COM']
            timeout = self.idDevPack['timeout']
            idPort = self.idDevPack['Port']

            self.client = ModbusTCP(ipAddr, port=idPort)
            self.client.timeout = timeout
        try:
            logger.info(f"{self.idDevPack['idDev']} - {self.idDevPack['ipAddr_COM']} - OPEN port: {self.client.connect()}")
        except:
            logger.info(f"{self.idDevPack['idDev']} --- OPEN connnection WRONG self.client {self.client}!")

        self.time_[1] = time.time_ns()  # time after connection

    def close_conn(self):
        try:
            self.client.close()
            logger.info(f"{self.idDevPack['idDev']} --- CLOSE connnection result: {self.client.connect()}")
        except:
            logger.info(f"{self.idDevPack['idDev']} --- CLOSE connnection NOK   !!!!!!!!!!!!!!")


    def read_regs_loop(self, number_loops):
        #Reads registers till no error
        #v1.0 2022-11-17

        for x in range(number_loops):
            error= self.read_regs()
            if error==0:
                return x+1

        return number_loops

    def setup_regs(self):
        self.n_rr = len(self.addrList)
        self.codeError_rr = [0] * self.n_rr
        self.rr = [{0} for x in range(self.n_rr)]
        self.rr_dtime = [0] * self.n_rr
        self.rr_delay = [0] * self.n_rr
        self.codeError_wrr = 0
        self.sum_error = 0

    def read_regs(self):
        '''
        Reads the registers from the device one by one
        number of registers = len(addrList) = n_rr

        function_:
            'rr'       read_holding_registers
            'ir'       read_input_registers

        Output:
            - time delay            rr_delay
            - error code            codeError_rr
            - registers             rr
        '''

        #Clean registers
        self.setup_regs()

        if self.client.connect():
            for x in range(self.n_rr):
                AddrStart = self.addrList[x + 1][0]  # [*self.addrList.items()][x][1][0]
                AddrNum = self.addrList[x + 1][1] - AddrStart  # [*self.addrList.items()][x][1][1] - AddrStart
                t0_ = time.time_ns()
                if self.idDevPack['Function'] == 'rr':
                    try:
                        self.rr[x] = self.client.read_holding_registers(address=AddrStart,
                                                                        count=AddrNum,
                                                                        unit=self.idDevPack['idAddr'])
                    except:
                        self.codeError_rr[x] += err_code['err_connection']

                if self.idDevPack['Function'] == 'ir':
                    try:
                        self.rr[x] = self.client.read_input_registers(address=AddrStart,
                                                                      count=AddrNum,
                                                                      unit=self.idDevPack['idAddr'])
                    except:
                        self.codeError_rr[x] += err_code['err_connection']

                trr_ = time.time_ns()
                self.rr_dtime[x] = trr_ - t0_  # time to read registers ns
                self.rr_delay[x] = trr_ - self.TimeStamp_ns

                #logger.info(f"{self.idDevPack['idDev']}:{x} --- READ REGS lenght:{self.rr[x]}  --- delay {float(self.rr_dtime[x]) / 1000.0} ms")

                try:
                    if self.rr[x].function_code > 0x80:
                        self.codeError_rr[x] += err_code['err_register']
                except:
                    pass
                try:
                    if self.rr[x].string:
                        self.codeError_rr[x] += err_code['err_register']
                except:
                    pass
        else:
            Time_Now= t_to_DateTime(time.time_ns())
            logger.info(f"[msg]: No connection  for device: {self.idDevPack['idDev']}-({self.idDevPack['ipAddr_COM']}) at time:  {Time_Now} -----")
            for x in range(self.n_rr):
                self.rr_delay[x] = time.time_ns() - self.TimeStamp_ns
                self.codeError_rr[x] += err_code['err_connection']

        for x in range(self.n_rr):
            self.sum_error += self.codeError_rr[x]

        return self.sum_error

    def read_regs_fast(self):
        if self.client.connect():
            for x in range(self.n_rr):
                self.rr[x] = self.client.read_holding_registers(address=self.addrList[x + 1][0],
                                                                count=self.addrList[x + 1][1] - self.addrList[x + 1][0],
                                                                unit=self.idDevPack['idAddr'])
        else:
            logger.info(f"[msg]: No connection  for device: {self.idDevPack['idDev']}-({self.idDevPack['ipAddr_COM']}) at time:{time.time_ns()/1000000} [ms] -----")
            for x in range(self.n_rr):
                self.rr_delay[x] = time.time_ns() - self.TimeStamp_ns
                self.codeError_rr[x] += err_code['err_connection']

            self.sum_error += self.codeError_rr[x]
        return self.sum_error

    def run(self, *args):
        # Reads the devices' registers continuosly
        #  Commands:
        #   - enable        self.read_en
        #   - stop          self.stop
        # v2.1 2022-07-31   deleted while  cycle
        #print(f" -- [msg] thread.run() - idDev: {self.idDevPack['idDev']}")
        self.time_[2] = time.time_ns()  # time before read registers
        self.read_regs()  #'rr' F04, 'ir'
        self.time_[3] = time.time_ns()  # time After read registers

    def write_regs(self, addrReg, value):
        #v1.0 2022-11-11

        '''
        Write the registers from the device one by one
        number of registers = len(addrList) = n_rr
        '''

        if self.client.connect():
                #try:
                self.wrr = self.client.write_register(addrReg, value, unit=self.idDevPack['idAddr'])
                #except:
                #    self.codeError_wrr += err_code['err_connection']

                try:
                    if self.wrr.function_code > 0x80:
                        self.codeError_wrr  += err_code['err_register']
                except:
                    pass
                try:
                    if self.wrr .string:
                        self.codeError_wrr  += err_code['err_register']
                except:
                    pass

                if self.codeError_wrr == 0:
                    logger.info(
                        f"[msg]: written to device: {self.idDevPack['idDev']}-({self.idDevPack['ipAddr_COM']}) -----")
                else:
                    logger.info(
                        f"[msg]: NOT written to device: {self.idDevPack['idDev']}-({self.idDevPack['ipAddr_COM']}) error: {self.codeError_wrr} -----")
        else:
            Time_Now= t_to_DateTime(time.time_ns())
            logger.info(f"[msg]: No connection  for WRITING to device: {self.idDevPack['idDev']}-({self.idDevPack['ipAddr_COM']}) at time:  {Time_Now} -----")


    def run_once(self):
        # Reads the devices' registers one time
        # Commands
        # v2.0 2022-07-10   rMode
        # v2.1 2022-07-31
        self.run()

    def build_values(self):
        # From regs data to values - out as dictionary
        # v1.0 2020-09-27
        # v2.0 2021-01-26
        # v3.0 2021-01-26
        # v3.1 2022-02-02
        # v3.2 2022-11-17
        # v4.0 2022-12-21 check range

        '''

        parameters Dictionary

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
        :return:
        '''

        self.time_[4] = time.time_ns()  # time BEFORE data format
        self.param_list = {}
        for x in range(len(self.pDict)):


            index_ = self.pDict[x]['idAddrList'] - 1
            self.param_list[x] = build_param(self.pDict[x],
                                             self.idDevPack['idDev'],
                                             self.rr[index_],
                                             self.codeError_rr[index_],
                                             self.TimeStamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
                                             self.rr_delay[index_] * (10 ** -6))

            #Check value range
            flag_=False
            try:
                flag_= type(self.pDict[x]['min']) != str and type(self.pDict[x]['max']) != str
            except:
                pass

            if flag_:
                value = self.param_list[x]['Value']
                if (value < self.pDict[x]['min']) or (value > self.pDict[x]['max']):
                    self.param_list[x]['Value'] = 0.0

        self.time_[5] = time.time_ns()  # time AFTER data format

def internet_ip():
    # v2.0 2020-03-22
    # check if host/port is open and returns machine ip address
    # https://stackoverflow.com/questions/3764291/checking-network-connection
    # 2022-02-14 renamed internet2()

    import socket
    ipaddress = socket.gethostbyname(socket.gethostname())
    if ipaddress == "127.0.0.1":
       return False
    else:
       return True

