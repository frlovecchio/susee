# -*- coding: utf-8 -*-
##############################
##### Functions  #############
##############################
# Studio Tecnico Pugliautomazione - Monopoli (BA)
# Copyright (c)
# v2.0 2020-07-22
# v2.1 2020-12-29   swap_convert()
# v2.2 2020-12-29   fixed offset
# v2.3 2021-04-23
# v2.4 2021-05-15
# v2.5 2022-03-03
# v2.6 2022-06-02  fixed len register control
# v2.7 2022-06-23   len registers
# v2.8 2022-07-01   date Pasquetta
# v2.9 2022-07-10   t_to_DateTime()
# v3.0 2022-10-09   t_to_DateTime()
# v3.1 2022-11-10
# v3.2 2022-11-16
# v3.3 2023-06-27   fixed F2

import pandas as pd
import struct
import os
import sys
import time
import pytz
from datetime import datetime
import importlib

from socket import *
from susee.see_dict import err_code

# ----------------------------------------------
#       Format Conversions Functions
# ----------------------------------------------
def ulongswap_convert(hexa, hexb):
    hh = hexa * 16 ** 4 + hexb
    # print('hexa,hexb, hh, int(hh): {} {} {} {} '.format(hexa,hexb, hh, int(hh) ))
    return int(hh)


def longswap_convert(hexa, hexb):
    hh = hexa * 16 ** 4 + hexb
    if hh > 0x7fffffff:
        hh = hh - 16 ** 8 + 1
    return int(hh)


def swap_convert(hexa):
    hh = hexa
    if hh > 0x7fff:
        hh = hh - 16 ** 4 + 1
    return int(hh)


def float_convert(hex_a, hex_b):
    # Converts two words in swapfloat
    hh = hex_a * 16 ** 4 + hex_b
    return float('{0:.2f}'.format(struct.unpack('!f', struct.pack('>I', hh))[0]))


def double_convert(hex_a, hex_b, hex_c, hex_d):
    # Converts four words in  float
    hex_double = hex_a * 16 ** 12 + hex_b * 16 ** 8 + hex_c * 16 ** 4 + hex_d
    return float('{0:.2f}'.format(struct.unpack('!d', struct.pack('>Q', hex_double))[0]))


def int_double_convert(hex_a, hex_b, hex_c, hex_d):
    # Converts four words in  double u-integer
    hex_double = hex_a * 16 ** 12 + hex_b * 16 ** 8 + hex_c * 16 ** 4 + hex_d
    return int(hex_double)


def isNaN(num):
    # Check: numero is NaN
    return num != num


def build_param(pDict, idDev, list_name, codeError, TimeStamp, Delay, ):
    '''
    Builds the device's value

    v.2.9 - 2018-11-05
    v.3.0 - 2020-06-30
    v.3.1 - 2020-10-29
    v.3.2 - 2020-12-03
    v.3.3 - 2021-01-21
    v.3.4 - 2021-04-23
    v.3.5 - 2022-02-02

    Parameters:
    -idDev,         self.idDevPack['idDev'],
    -list_name,     rr[self.pDict[x]['idAddrList'] - 1
    -codeError,     self.codeError_rr[self.pDict[x]['idAddrList'] - 1],
    -TimeStamp,     self.TimeStamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
    -Delay,         self.Delay

    -pDict[x] example
            {
            'idAddrList':   1,
            'addr':         10,
            'idParam':      104,
            'k':            1,
            'offset':       0,
            'words':        2,
            'type':         0,
            }

    for x in range(len(self.pDict)):
        self.param_list[x] = build_param(self.pDict[x],
                                         self.idDevPack['idDev'],
                                         self.rr[self.pDict[x]['idAddrList'] - 1],
                                         self.codeError_rr[self.pDict[x]['idAddrList'] - 1],
                                         self.TimeStamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
                                         self.rr_delay[self.pDict[x]['idAddrList'] - 1] * 10 ** -6)

    # Tipi di conversione
    # numwords ==1
    #    type =0 no conversion
    #    type =1 swap byte
    #
    # numwords == 2
    #     type =0 float_converter   {-1, 0}
    #     type =1 ulongswap_convert {0 , 1}
    #     type =2 longswap_convert  {0 , 1}
    #     type =3 long_convert      {1, 0}
    #     type =4 ulong_convert     {1, 0}
    #     type =5 float_converter   {1, 0}
    #
    # numwords == 4
    #      type =0 double_convert      { -1, 0 , +1 , +2 }
    #      type =1 double_convert      {  0, +1 , +2, +3 }
    #      type =2 int_double_convert  { -1, 0 , +1 , +2 }
    #
    # return    : dizionario come da Dict_Generate
    '''

    num_type = pDict['type']
    addr = pDict['addr']
    words = pDict['words']
    k = pDict['k']
    offset = pDict['offset']
    idParam = pDict['idParam']
    numwords = pDict['words']

    value_ = 0

    try:
        len_list = len(list_name.registers)
        aaa = list_name.registers[addr]
    except:
        len_list = 0
        codeError += err_code['lenreg_zero']

    if len_list >= numwords:  # >= addr + words-1:  2022-06-15
        if numwords == 1:
            if num_type == 0:
                value_ = list_name.registers[addr] * k + offset

            if num_type == 1:
                value_ = swap_convert(list_name.registers[addr]) * k + offset

        elif numwords == 2:
            if num_type == 0:
                value_ = float_convert(list_name.registers[addr - 1],
                                       list_name.registers[addr]) * k + offset
            elif num_type == 1:
                value_ = ulongswap_convert(list_name.registers[addr],
                                           list_name.registers[addr + 1]) * k + offset
            elif num_type == 2:
                value_ = longswap_convert(list_name.registers[addr],
                                          list_name.registers[addr + 1]) * k + offset
            elif num_type == 3:
                value_ = longswap_convert(list_name.registers[addr + 1],
                                          list_name.registers[addr]) * k + offset
            elif num_type == 4:
                value_ = ulongswap_convert(list_name.registers[addr + 1],
                                           list_name.registers[addr]) * k + offset
            elif num_type == 5:
                value_ = float_convert(list_name.registers[addr + 1],
                                       list_name.registers[addr]) * k + offset
            elif num_type == 6:
                value_ = float_convert(list_name.registers[addr],
                                       list_name.registers[addr + 1]) * k + offset

        elif numwords == 4:
            if num_type == 0:
                value_ = double_convert(list_name.registers[addr - 1],
                                        list_name.registers[addr],
                                        list_name.registers[addr + 1],
                                        list_name.registers[addr + 2]) * k + offset
            elif num_type == 1:
                value_ = double_convert(list_name.registers[addr],
                                        list_name.registers[addr + 1],
                                        list_name.registers[addr + 2],
                                        list_name.registers[addr + 3]) * k + offset
            elif num_type == 2:
                value_ = int_double_convert(list_name.registers[addr - 1],
                                            list_name.registers[addr],
                                            list_name.registers[addr + 1],
                                            list_name.registers[addr + 2]) * k + offset
            elif num_type == 3:
                value_ = int_double_convert(list_name.registers[addr],
                                            list_name.registers[addr + 1],
                                            list_name.registers[addr + 2],
                                            list_name.registers[addr + 3]) * k + offset
    else:
        value_ = 0
    if isNaN(value_):
        value_ = 0
        codeError += err_code['value_NaN']

    return Dict_Generate(idDevice=str(idDev),
                         idParam=str(idParam),
                         Date=TimeStamp,
                         Value=float(value_),
                         Delay=Delay,
                         Code=codeError
                         )


def Dict_Generate(idDevice, idParam, Date, Value, Delay, Code):
    # Genera un dizionario dati
    return dict(idDevice=str(idDevice),
                idParam=str(idParam),
                Date=Date,
                Value=float(Value),
                Delay=Delay,
                Code=Code
                )
    #


#
# Log
#
def push_log(stringa):
    # salva su file - config_log{}
    # con datetime
    # v2.0 2022-06-15

    # print('------- AAA ---------- def push_log(stringa): ', stringa)
    filedatetime = '{:%Y%m%d}'.format(time_utc())
    filename = filedatetime + 'log_file.log'
    stringa = '{:%Y-%m-%d %H:%M:%S}'.format(time_utc()) + ' - ' + stringa + '\n'
    topstring = '---------------  susee Log file ------------------ ' + '\n'
    f = []
    file_ok = True
    if os.path.isfile(filename):
        try:
            f = open(filename, 'a')
        except os.error:  # as err:
            file_ok = False
        else:
            f.write(stringa)
            f.close()
    else:
        try:
            f = open(filename, 'w')
        except os.error:  # as err:
            file_ok = False
            print(' [msg] - see_functions.push_log() - Impossibile creare il file:', filename)
        else:
            f.write(topstring)
            f.write(stringa)
            f.close()
            file_ok = True
    return file_ok

#
# Export csv
#
def to_file(stringa, filename):
    # salva su file -
    #
    # v1.0 2022-08-22

    file_ok = True
    if os.path.isfile(filename):
        try:
            f = open(filename, 'a')
        except os.error:  # as err:
            file_ok = False
        else:
            f.write(stringa)
            f.close()
    else:
        try:
            f = open(filename, 'w')
        except os.error:  # as err:
            file_ok = False
            print(' [msg] - see_functions.to_file() - Impossibile creare il file:', filename)
        else:
            f.write(stringa)
            f.close()
            file_ok = True
    return file_ok


# Web socket
def MyWebServer():
    print('Starting web server ....')
    import http.server
    import socketserver
    PORT = 8001
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("m597 webserver serving at port", PORT)
        httpd.serve_forever()


def push_webfile(testo):
    # testo  multiriga
    # Moduli
    filename = 'index.htm'
    f = []
    file_ok = True
    stringa = []

    TimeNow = str(time_utc())
    stringa.append('<html>')
    stringa.append('<body>' + '<br />')
    stringa.append('Lettura strumenti sistema di monitoraggio - ' + TimeNow + ' - ' + '<br />')
    stringa.append('-' * 150 + '<br />' + '<br />')
    for i in range(len(testo)):
        stringa.append(testo[i] + '<br />')

    stringa.append('<body>')
    stringa.append('<html>')

    if os.path.isfile(filename) | 1:
        try:
            f = open(filename, 'w')
        except os.error:  # as err:
            file_ok = False
            print('Impossibile creare il file:', filename)
        else:
            for i in range(len(stringa)):
                f.write(stringa[i])
            f.close()
            file_ok = True

    return file_ok


#
# Time Tools
#
def time_utc():
    UTC = pytz.utc
    dt = datetime.now(UTC)
    return dt


def time_local(tZone):
    # Time zone accordint to the timeZone
    # v1.0 2020-07-26
    IST = pytz.timezone(tZone)
    dt = datetime.now(IST)
    return dt



def utctime_to_tZone(utc_str_date, tZone):
    # v3.0 2019-01-02 - timezone
    # v3.1 2021-05-15

    tz = pytz.timezone(tZone)

    if 'time' in str(type(utc_str_date)):
        try:
            utc_str_date = utc_str_date.replace(tzinfo=pytz.timezone('utc')).astimezone(tz=tz).strftime(
                '%Y-%m-%d %H:%M:%S')
            utc_str_date = datetime.strptime(str(utc_str_date).split('+')[0], '%Y-%m-%d %H:%M:%S')
            return utc_str_date
        except:
            print('nok_time utctime_to_tZone. utc_time:', utc_str_date)
            return utc_str_date

    if 'str' in str(type(utc_str_date)):
        try:
            utc_str_date = datetime.strptime(utc_str_date, '%Y-%m-%d %H:%M:%S')
            utc_str_date = utc_str_date.replace(tzinfo=pytz.timezone('utc')).astimezone(tz=tz).strftime(
                '%Y-%m-%d %H:%M:%S')
            return utc_str_date
        except:
            print('nok_str utctime_to_tZone. utc_time:', utc_str_date)
            return utc_str_date


def tZone_to_utctime(str_date, tZone):
    # Convert a UTC time to local time
    # v1.0 2020-04-25 - from timezone to utc
    # v2.0 2021-05-15
    # n.b.  pytz.timezone('Europe/Rome')  --> <DstTzInfo 'Europe/Rome' LMT+0:50:00 STD>
    # v2.1 2022-02-15

    local_now = datetime.now()
    diff_local_utc = utctime_to_tZone(local_now, tZone) - local_now

    if 'time' in str(type(str_date)):
        try:
            # str_date = str_date.replace(tzinfo=pytz.timezone(tZone)).astimezone(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
            # str_date = datetime.strptime(str(str_date).split('+')[0], '%Y-%m-%d %H:%M:%S')
            str_date = str_date - diff_local_utc  # v2.1 2022-02-15
            return str_date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            print('[msg] nok_time utctime_to_tZone. utc_time:', str_date)
            return str_date

    if 'str' in str(type(str_date)):
        try:
            # str_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
            # str_date = str_date.replace(tzinfo=pytz.timezone(tZone)).astimezone(tz=tz).strftime( '%Y-%m-%d %H:%M:%S')
            str_date = str_date - diff_local_utc  # v2.1 2022-02-15
            return str_date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            print('> nok_str utctime_to_tZone. utc_time:', str_date)
            return str_date


def t_to_DateTime(tt):
    # Convert time_ns() to DateTime
    # v0.0 2020-09-27
    # v0.1 2022-07-10

    t1 = datetime.fromtimestamp(tt * 10 ** -9)
    return t1.strftime('%Y-%m-%d %H:%M:%S.%f')


#
# Datetime attributes
#
def datetime_to_F123(date_):
    # Categorize a date according to F1,F2, F3 time period
    # and quaterly of hour
    # date_ strimg format  '%Y-%m-%d %H:%M:%S' or datetime
    #   v1.0    2020-04-27
    #   v1.1    2022-02-15
    #   v1.2    2023-06-27  fixed bug


    if 'str' in str(type(date_)):
        date_ = datetime.strptime(date_, '%Y-%m-%d %H:%M:%S')

    dateYear = date_.year
    dateMonth = date_.month
    dateDay = date_.day
    # 0= sunday
    dateWeekDay = date_.isoweekday()
    dateHour = date_.hour
    date_YMD = datetime(dateYear, dateMonth, dateDay)

    # Holydays
    x = dateYear
    noWdays = [datetime(x, 1, 1)]
    noWdays += [datetime(x, 1, 6)]
    noWdays += [datetime(x, 4, 25)]
    noWdays += [datetime(x, 5, 1)]
    noWdays += [datetime(x, 6, 2)]
    noWdays += [datetime(x, 8, 15)]
    noWdays += [datetime(x, 11, 1)]
    noWdays += [datetime(x, 12, 8)]
    noWdays += [datetime(x, 12, 25)]
    noWdays += [datetime(x, 12, 26)]
    # Pasquetta  http://calendario.eugeniosongia.com/datapasqua.htm
    noWdays += [datetime(2020, 4, 22)]
    noWdays += [datetime(2021, 4, 5)]
    noWdays += [datetime(2022, 4, 18)]
    noWdays += [datetime(2023, 4, 10)]
    noWdays += [datetime(2024, 1, 4)]
    noWdays += [datetime(2025, 4, 21)]
    noWdays += [datetime(2026, 4, 6)]
    noWdays += [datetime(2027, 3, 29)]
    noWdays += [datetime(2028, 4, 17)]
    noWdays += [datetime(2029, 4, 2)]
    noWdays += [datetime(2030, 4, 22)]

    # Fasce orarie F1, F2, F3

    condF2 = (dateWeekDay == 6 and dateHour in range(7, 23)) or \
             (dateWeekDay in [1,2,3,4,5]) and (dateHour in [7, 19, 20, 21, 22])

    condF3 = (date_YMD in noWdays or dateWeekDay == 7) or \
             (dateHour in [23, 0, 1, 2, 3, 4, 5, 6])

    if condF2:
        period_F123 = 'F2'
    elif condF3:
        period_F123 = 'F3'
    else:
        period_F123 = 'F1'

    # index quaterly of hour since 1= 00.00 to 96 = 23:45
    # format
    p_ = divmod(dateHour * 60 + date_.minute, 15)  # period 0..95
    pp_ = divmod(p_[0], 4)  # periods in hours
    qHTime = str(pp_[0]) + ':' + str('{:02d}'.format(pp_[1] * 15))  # hh:mm
    qH = p_[0] + 1  # 0...14  -> 1..15

    # Turno orario lavorativo
    # wp1 da 6 a 14
    # wp2 da 14 a 22
    # wp3 da 22 a 6

    if (dateHour in range(6, 14)):
        wPeriod_ = 1
    if (dateHour in range(14, 22)):
        wPeriod_ = 2
    if (dateHour in [22, 23, 0, 1, 2, 3, 4, 5]):
        wPeriod_ = 3

    return period_F123, qH, qHTime, wPeriod_



#2022-10-09
#
# see Data ETL Functions
#


def load_driver_method(driver_pack_name, driver_name):
    # Loads device's driver
    # v1.0  2022-02-07
    # v1.1  2022-04-18

    '''
    Inputs examples:
        driver_pack_name =  'susee.see_drivers'
        driver_name =       'c_driver_P32'
    '''
    driver_ = None
    try:
        driverLib_ = importlib.util.find_spec(driver_pack_name)
        spec = importlib.util.spec_from_file_location(driver_name, driverLib_.origin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        driver_ = getattr(module, driver_name)
        # print(f"---- loaded driver of device id '{driver_name}' . driver name:  {driver_.__name__}   -------------")
    except Exception as exc:
        raise RuntimeError(f"[msg] - Driver of device id {driver_name} not found ") from exc
    return driver_


def filter_devices(pack):
    # Filters and returns package of enabled devices
    # v1.0 2022-01-29

    pack1 = {}
    xx = 0
    for x in pack.keys():
        if pack[x]['enable']:
            pack1[xx] = pack[x]
            xx += 1
    return pack1


def load_dataFile():
    # Import the configuration data file
    # option '-d' name_file.dy
    # v1.0 2022-01-29

    #
    # Option: -d name_datafile.py
    #
    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            customLib = ''
            try:
                customLib = sys.argv[2]
                if customLib[-3:] == '.py':
                    customLib = customLib[:-3]
                return importlib.import_module(customLib, package=None)
            except:

                print(f"[msg] - error: custom data file: '{customLib}' not found or file error")
                exit()
        else:
            print('[msg] - error: option -d missing')
            exit()
    else:
        print('[msg] error: option -d missing')
        exit()


def sample_data(TimeNow_ns, devInstance_):
    # Store DATA
    # v1.0 2020-09-27
    #

    _dataSample = {}
    for i in range(len(devInstance_)):
        _dataSample[i] = {
            'sampleTime': TimeNow_ns,  # time_ns
            'idDevice': devInstance_[i].idDevPack['idDev'],
            # 'paramList':    devInstance_[i].param_list,
            'rr': devInstance_[i].rr,
            'rr_error': devInstance_[i].codeError_rr,
            'rr_dtime': devInstance_[i].rr_dtime,
            'time_array': devInstance_[i].time_,  # list [ns]
            'TimeStamp': devInstance_[i].TimeStamp
        }
    return _dataSample


def check_OpenPorts(idDevices_pack):
    for i in range(len(idDevices_pack)):
        # time.sleep(1)
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(1)
        if idDevices_pack[i]['method'] == 'tcp':
            result = s.connect_ex(
                (idDevices_pack[i]['ipAddr_COM'],
                 int(idDevices_pack[i]['Port']))
            )
            if result == 0:
                s.close()
                print('idDev: {} ip: {} port: {} has been closed'.format(
                    idDevices_pack[i]['idDev'],
                    idDevices_pack[i]['ipAddr_COM'],
                    idDevices_pack[i]['Port'])
                )
    print('-' * 40)

def list_remoteClients(idDevices_pack, reverse ):
    # Create idDevice list of single clients
    # v1.0 2022-08-10
    # v1.1 2022-08-12
    # v1.2 2022-10-28   sort by ip
    # v1.3 2022-11-09
    # v1.4 2022-11-10

    list_rClients = {}
    n = 0
    uCode_list = []
    def uCode(i, pack):
        return ';'.join((pack[i]['method'], pack[i]['ipAddr_COM'], pack[i]['Port']))

    #uCode_list.append(uCode(0))
    for i in range(len(idDevices_pack)):
        uCode_ = uCode(i,idDevices_pack)
        if uCode_ not in uCode_list:
            list_rClients[n] = idDevices_pack[i]
            uCode_list.append(uCode_)
            n += 1
    #
    #Generate ordered list of ipAddr
    #
    uCode_list = sorted(uCode_list, reverse= reverse)

    #
    #Sort list of clients by ip
    #
    list_rClients1 = {}
    n = 0
    for uC in uCode_list:
        for i in range(len(list_rClients)):
            if uCode(i,list_rClients) == uC:
                list_rClients1[n] = list_rClients[i]
                n += 1
    return list_rClients1

def sampleFlag_(sample_params, flag_old):
    #
    # Sample flag
    # returns time parameters and the flag_sample
    # sample_params = {
    #     'sampleTime': 60,  # [s]
    #     'sampleShift': 30,  # [s]
    #     'sampleType': 0,
    #     'utc_time': True,
    # }
    # v.1.1 2020-09-2
    # v.1.2 2022-02-07
    # v.1.3 2022-07-10

    TimeNow_ns = time.time_ns()
    if sample_params['utc_time']:
        TimeNow = time_utc()
    else:
        TimeNow = datetime.fromtimestamp(TimeNow_ns * 10 ** -9)

    timeSeconds = TimeNow.minute * 60 + TimeNow.second + TimeNow.microsecond * 10 ** -6
    sampleTime = sample_params['sampleTime']  # [s]
    sampleShift = sample_params['sampleShift']  # [s]

    if sampleTime >= 1:
        TimeNow = datetime(TimeNow.year, TimeNow.month, TimeNow.day, TimeNow.hour, TimeNow.minute, TimeNow.second)

    ####  check flag_sample  ####
    flag_sample = False  # TimeNow.second

    if sampleTime > 1:
        flag_sample = (int(timeSeconds) % int(sampleTime)) == int(sampleShift) and \
                      flag_old != TimeNow.second
        flag_old = TimeNow.second  # one flag each second

    if 0 < sampleTime <= 1:
        flag_sample = int(timeSeconds * 10 ** 2) % int(sampleTime * 10 ** 2) == 0 and \
                      flag_old != int(timeSeconds * 10 ** 2)
        flag_old = int(timeSeconds * 10 ** 2)  # one flag each centi.second

    if sampleTime == 0:
        return True, TimeNow, 0, TimeNow_ns, 0

    return flag_sample, TimeNow, flag_old, TimeNow_ns, int(timeSeconds) % (int(sampleTime) - int(sampleShift))


def time_report(_dataToStore):
    # v1.0  2020-09-28

    s_ = len(_dataToStore)  # samples
    d_ = len(_dataToStore[0])  # devices
    tab_ = []
    k1_ = 10 ** -6
    df = pd.DataFrame()

    for i in range(s_):
        for ii in range(d_):
            tab_.append(
                [
                    'sample ' + str(i + 1),
                    t_to_DateTime(_dataToStore[i][ii]['sampleTime']),
                    _dataToStore[i][ii]['idDevice'],
                    (_dataToStore[i][ii]['time_array'][1] - _dataToStore[i][ii]['time_array'][0]) * k1_,  # connTime
                    (_dataToStore[i][ii]['time_array'][3] - _dataToStore[i][ii]['time_array'][2]) * k1_,  # rrTIme
                    (_dataToStore[i][ii]['time_array'][5] - _dataToStore[i][ii]['time_array'][4]) * k1_,  # buildTime
                    [_dataToStore[i][ii]['rr_dtime'][iii] * k1_ for iii in range(len(_dataToStore[i][ii]['rr_dtime']))],
                ]
            )
        df = pd.DataFrame(tab_,
                          columns=['idSample',
                                   'DateTime',
                                   'idDev',
                                   'connTime[ms]',
                                   'rrTime[ms]',
                                   'buildTime[ms]',
                                   'rr_dtime[ms]'
                                   ])
    return df


def sync_report(_dataToStore):
    # Syncronization report -
    # Sample timing
    # v1.0 2020-09-28

    s_ = len(_dataToStore)  # samples
    d_ = len(_dataToStore[0])  # devices
    tab_ = []
    k1_ = 10 ** -6
    df = pd.DataFrame()

    for i in range(s_):
        min_ = min([_dataToStore[i][ii]['time_array'][2] for ii in range(d_)])
        max_ = max([_dataToStore[i][ii]['time_array'][3] for ii in range(d_)])

        tab_.append(
            [
                'sample ' + str(i + 1),  # sample time
                t_to_DateTime(_dataToStore[i][0]['sampleTime']),
                (max_ - min_) * k1_,  # sync time [ms]

            ]
        )
        df = pd.DataFrame(tab_,
                          columns=['idSample',
                                   'DateTime',
                                   'syncTime[ms]'])
    return df


