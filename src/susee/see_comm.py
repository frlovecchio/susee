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


from pymodbus.client.sync import ModbusSerialClient as ModbusRTU
from pymodbus.client.sync import ModbusTcpClient as ModbusTCP
import threading
import time

from susee.see_functions import  build_param
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
#
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
                    'Port': '502',
                    'timeout': 1,
                    'enable': 1,
                }
        '''
        self.idDevPack = idDevPack
        self.time_ = [0] * 6
        logger.info(f"__init__ {self.idDevPack['Port']}")

        self.client = None
        self.addrList = {}
        self.num = 0
        self.read_en = False
        self.sync_ = True
        self.stop = False
        self.TimeStamp_ns = time.time_ns()  # time reference of sample: "sampling time".
        self.pDict = {}

    def setup_regs(self):
        self.n_rr = len(self.addrList)
        self.codeError_rr = [0] * self.n_rr
        self.rr = [{} for x in range(self.n_rr)]
        self.rr_dtime = [0] * self.n_rr
        self.rr_delay = [0] * self.n_rr

    def open_conn(self):
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
            logger.info(f"{self.idDevPack['idDev']} --- OPEN connnection result: {self.client.connect()}")
        except:
            logger.info(f"{self.idDevPack['idDev']} --- OPEN connnection WRONG self.client {self.client}!")

        self.time_[1] = time.time_ns()  # time after connection

        # Setup regs
        self.setup_regs()

    def close_conn(self):
        try:
            self.client.close()
            logger.info(f"{self.idDevPack['idDev']} --- CLOSE connnection result: {self.client.connect()}")
        except:
            pass
            logger.info(f"{self.idDevPack['idDev']} --- CLOSE connnection NOK   !!!!!!!!!!!!!!")

    def read_regs(self, type_):
        '''
        Reads the registers from the device one by one
        number of registers = len(addrList) = n_rr

        Type:
            'rr'       read_holding_registers
            'ir'       read_input_registers

        Output:
            - time delay            rr_delay
            - partial delta time    rr_dtime
            - error code            codeError_rr
            - registers             rr
        '''

        for x in range(self.n_rr):
            self.codeError_rr[x] = 0  # code error
            self.rr_dtime[x] = 0  # diff time to read registers
            self.rr_delay[x] = 0  # delay time form sample timeStamp

        if self.client.connect():
            for x in range(self.n_rr):
                AddrStart = self.addrList[x + 1][0]  # [*self.addrList.items()][x][1][0]
                AddrNum = self.addrList[x + 1][1] - AddrStart  # [*self.addrList.items()][x][1][1] - AddrStart

                t0_ = time.time_ns()
                if type_ == 'rr':
                    try:
                        self.rr[x] = self.client.read_holding_registers(address=AddrStart,
                                                                        count=AddrNum,
                                                                        unit=self.idDevPack['idAddr'])
                    except:
                        self.codeError_rr[x] += err_code['err_connection']

                if type_ == 'ir':
                    try:
                        self.rr[x] = self.client.read_input_registers(address=AddrStart,
                                                                      count=AddrNum,
                                                                      unit=self.idDevPack['idAddr'])
                    except:
                        self.codeError_rr[x] += err_code['err_connection']

                trr_ = time.time_ns()
                self.rr_dtime[x] = trr_ - t0_  # time to read registers
                self.rr_delay[x] = trr_ - self.TimeStamp_ns
                logger.info(f"{self.idDevPack['idDev']}:{x} --- READ REGS lenght:{self.rr[x]}  --- delay {float(self.rr_dtime[x]) / 1000.0} ms")

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
            logger.info(f"[msg]: No connection available for device:{self.idDevPack['idDev']} at time:{time.time_ns()/1000000} [ms] -----")
            for x in range(self.n_rr):
                self.rr_delay[x] = time.time_ns() - self.TimeStamp_ns
                self.codeError_rr[x] += err_code['err_connection']

    def read_regs_fast(self, type_):

        if self.client.connect():
            for x in range(self.n_rr):
                self.rr[x] = self.client.read_holding_registers(address=self.addrList[x + 1][0],
                                                                count=self.addrList[x + 1][1] - self.addrList[x + 1][0],
                                                                unit=self.idDevPack['idAddr'])
        else:
            logger.info(f"[msg]: No connection available for device:{self.idDevPack['idDev']} at time:{time.time_ns()/1000000} [ms] -----")
            for x in range(self.n_rr):
                self.rr_delay[x] = time.time_ns() - self.TimeStamp_ns
                self.codeError_rr[x] += err_code['err_connection']

    def run(self, *args):
        # Reads the devices' registers continuosly
        #  Commands:
        #   - enable        self.read_en
        #   - stop          self.stop

        while True:
            if self.read_en:
                self.time_[2] = time.time_ns()  # time before read registers
                self.read_regs('rr')
                self.time_[3] = time.time_ns()  # time After read registers
                if self.sync_:
                    self.read_en = False
            if self.stop:
                break

    def run_once(self, *args):
        # Reads the devices' registers one time
        # Commands
        #
        self.time_[2] = time.time_ns()  # time before read registers
        self.read_regs('rr')
        self.time_[3] = time.time_ns()  # time After read registers
        self.read_en = False

    def build_values(self):
        # From regs data to values - out as dictionary
        # v1.0 2020-09-27
        # v2.0 2021-01-26
        # v3.0 2021-01-26
        # v3.1 2022-02-02

        self.time_[4] = time.time_ns()  # time BEFORE data format
        self.param_list = {}
        for x in range(len(self.pDict)):
            self.param_list[x] = build_param(self.pDict[x],
                                             self.idDevPack['idDev'],
                                             self.rr[self.pDict[x]['idAddrList'] - 1],
                                             self.codeError_rr[self.pDict[x]['idAddrList'] - 1],
                                             self.TimeStamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
                                             self.rr_delay[self.pDict[x]['idAddrList'] - 1] * 10 ** -6)

        self.time_[5] = time.time_ns()  # time AFTER data format

def internet2():
    # v2.0 2020-03-22
    # check if host/port is open
    # https://stackoverflow.com/questions/3764291/checking-network-connection

    import socket
    ipaddress = socket.gethostbyname(socket.gethostname())
    if ipaddress == "127.0.0.1":
       return False
    else:
        return True

