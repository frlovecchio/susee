# -*- coding: utf-8 -*-
# Studio Tecnico Pugliautomazione - ing. F.S. Lovecchio - Bari, Italy

'''
BSD 3-Clause License
Copyright (c) 2018, Studio Tecnico Pugliautomazione - ing. F.S. Lovecchio - Bari Italy
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


ver = '1.6 - 2022-02-07'
ver = '1.7 - 2022-06-02'
ver = '1.8 - 2022-06-23'
ver = '2.0 - 2022-07-10'
ver = '2.1 - 2022-07-24'
ver = '2.2 - 2022-07-31'
ver = '2.31 - 2022-08-23'
ver = '2.32 - 2022-09-10'
ver = '2.33 - 2022-09-30'
ver = '2.34 - 2022-10-03'
ver = '3.0  - 2022-11-12' #added class events
ver = '3.1  - 2022-11-16' #added class events



sample_params = {
    'sampleTime': 10,   # [s]
    'sampleShift': 0,   # [s]
    'sampleType': 0,    #0: endless
    'waitTime' : 0.0,  #s   wait time after close connection with devices (default=0)
    'utc_time': True,
    'open_close_conn': False, #True: open and close connection at any cycle
    'num_try' : 3 #Numbr of attempts to read registers
}


# Opzioni
options_ = {
    'LogFile': True,
    'Messages': True,
    'datafileBk': False,  # backup file - config_data_bk{}
    'tempfileBk': False,  # temp-backup file waiting at database connection - config_mysql_bk{}
    'tempArrayBk': False,
    'threads': True,
    'dataDdBk': True,
    'lastData': True,
}


# Opzioni
options_ = {
    'LogFile': True,
    'Messages': True,
    'datafileBk': False,    # backup file - config_data_bk{}
    'tempfileBk': True,     # temp-backup file waiting at database connection - config_mysql_bk{}
    'tempArrayBk': False,
    'threads': False,       #True: reads devices; False: read servers
    'dataDdBk': True,
    'lastData': True,
    'custom': True,
    'fastSample': True,     #fast sample for CABIN's devices and SCADA report
    'UpgradeWeb': False,     #Ugrade sysTable of web interface
}

from decouple import config

user_db = config('user_db', default='username')
pswd_db = config('pswd_db', default='password')
host_db = config('host_db', default='127.0.0.1')
port_db = config('port_db', default='3306')
job_id = config('job_id', default='000')

res_data = {
    'user': user_db,
    'passwd': pswd_db,
    'host': host_db,  # '10.8.0.1',
    'port': port_db,
}

config_mysql = {
    **res_data,

    'database': 'seedb' + job_id,
    'tableRaw': 'see' + job_id + 'Raw',
    'tableDeps': 'see' + job_id + 'Deps',
    'tableEvents': 'see' + job_id + 'Events',
    'tableEventsSys': 'see' + job_id + 'EventsSys',
    'tableJoin': 'see' + job_id + 'Join',
    'tableLast': 'see' + job_id + 'Last',
    'tableLastFast': 'see' + job_id + 'LastFast',
    'tableMac': 'see' + job_id + 'Mac',
    'tableParams': 'see' + job_id + 'Params',
    'tableProd': 'see' + job_id + 'Prod',
    'tableSysRaw': 'see' + job_id + 'SysSetRaw',
    'tableSys': 'see' + job_id + 'Sys',
    'language': 'ENG',
    'tZone': 'Europe/Rome',
    'maxConnectTime': 30,  # [s]

    'config_mysql_bk': {
        'path': '',
        'filename': '__mysql_' + job_id + 'bk.csv',
        'topstring': '',
        'max_rows_reload': 25,
        'enable': options_['tempfileBk']
    },
    'config_data_bk': {
        'path': '',
        'filename': job_id + 'bk.csv',
        'topstring': ';'.join(('Data', 'Device', 'idPar', 'Value', 'Code')),
        'max_rows_reload': sample_params['sampleTime'] * 20
    }
}


# List of devices
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

idDevices_pack[1] = {
    'typeDev': 'P32',
    'idDev': 'd01',
    'method': 'tcp',
    'ipAddr_COM': '192.168.1.101',
    'idAddr': 1,
    'Port': '502',
    'timeout': 1,
    'enable': 1,
}
