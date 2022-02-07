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

sample_params = {
    'sampleTime': 10,  # [s]
    'sampleDelay': 0,  # [s]
    'sampleShift': 0,  # [s]
    'sampleType': 0,
    'utc_time': True,
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
    'tableJoin': 'see' + job_id + 'Join',
    'tableLast': 'see' + job_id + 'Last',
    'tableMac': 'see' + job_id + 'Mac',
    'tableParams': 'see' + job_id + 'Params',
    'tableProd': 'see' + job_id + 'Prod',
    'tableSysRaw': 'see' + job_id + 'SysSetRaw',
    'language': 'ENG',
    'tZone': 'Europe/Rome',

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


