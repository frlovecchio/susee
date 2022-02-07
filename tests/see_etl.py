# -*- coding: utf-8 -*-
# Studio Tecnico Pugliautomazione - ing. F.S. Lovecchio - Bari, Italy

"""
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
"""

'''
Test file 
'''
ver = '1.6 - 2022-02-07'
ver = '1.7 - 2022-02-07'

import time
import sys
import importlib
from datetime import datetime
from socket import *
import copy
import pandas as pd

from susee.see_functions import time_utc
from susee.see_db import seedatadb

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# class cLib:
#    pass

def main():
    #  - Load custom data from custom Module cLib
    cLib = load_dataFile()
    idDevices_pack = cLib.idDevices_pack
    options_ = cLib.options_
    config_mysql = cLib.config_mysql
    sample_params = cLib.sample_params
    ###################################################

    #   - Filter devices dataframe
    idDevices_pack = filter_devices(idDevices_pack)
    num_devices = len(idDevices_pack)
    if num_devices == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO DEVICES TO READ ! - - - - - - - - ')
        print('-' * 60)
        exit()
    else:
        print('-' * 60)
        print(' -  - - -  - - - N. %s DEVICES TO READ  - - - - - - - - ' % (str(num_devices)))
        print('-' * 60)
    ####################################################

    #   - Messages
    print('-' * 80)
    print('--- SUSEE - Energy Management System Platform     --- ')
    print('------------------------------------------------------ ')
    print('')
    print('--- Studio Tecnico Pugliautomazione - Bari, Italy --- ')
    print('--- eng. Francesco Saverio Lovecchio, ph.D.       --- ')
    print('--- ETL Tool %s ' % ver)
    print('--- UTC Data: %s ' % (time_utc()))
    print('-' * 80)
    print('')
    print('')

    if options_['Messages']:
        print('>> Devices: ', num_devices)
        for ii in idDevices_pack.keys():
            print('Device n. %s ' % (ii + 1))
            [print(' {}:  {}'.format(i, idDevices_pack[ii][i])) for i in idDevices_pack[ii].keys()]
        print('>> SampleParams: ')
        [print('>> {}: '.format(ii)) for ii in sample_params.items()]
        print('>> Database: ', config_mysql['host'])
        print('-' * 40)

    print('')
    print('')

    # check and close open ports
    print(' - - - Check open ports   - - - ')
    check_OpenPorts(idDevices_pack)

    # CHECK
    # Instruments threads
    #



    #   - Load devices Drivers
    threads = []
    for i in range(num_devices):
        driver_ = load_driver_method('susee.see_drivers', idDevices_pack[i]['typeDev'])
        t = driver_(idDevices_pack[i])
        threads.append(t)

    print('')
    print('')
    nDev_ = len(threads)
    print('>> Number of instances: ', nDev_)
    if nDev_ == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO DEVICES TO READ ! - - - - - - - - ')
        print('-' * 60)
        exit()

    # - Setup connection
    for t in threads:
        t.open_conn()
    print('')
    print('')
    print(' - - - - - Status open ports   - - - ')
    for i, t in enumerate(threads):
        print([i, t.idDevPack['idDev'], t.client.connect()])
    if options_['threads']:
        for t in threads:
            t.start()

    ####################################################################################

    print('')
    print('')



    #
    # 0. Mode - Endless loop of samples
    #
    if sample_params['sampleType'] == 0:
        print('-' * 80)
        print('-' * 10 + '  0. Mode - Endless Number of Samples Mode  ' + '-' * 20)

        # Infinite loop time
        maxSample = 10 ** 10

        flag_fastStorage = True
        sync_cycle = True

    #
    # 1. Mode - Finite number of  samples -  sync cycle
    #
    elif sample_params['sampleType'] == 1:
        print('-' * 40)
        print('-' * 10 + '  1. Mode -  Fixed Number of Samples Mode  ' + '-' * 10)
        # Input Loop control: number of cycles
        maxSample = int(input('Input number of cycles: '))

        # Input Storage mode
        flag_fastStorage = input('Instant storage ? [yes/No]:')
        if 'n' in flag_fastStorage.lower():
            flag_fastStorage = False
        elif 'y' in flag_fastStorage.lower():
            flag_fastStorage = True
        else:
            flag_fastStorage = False

        # Sync Cycle Storage mode
        sync_cycle = input('Syncronization of cycles samples (wait all ended) ? [Yes/no]:')
        if 'y' in sync_cycle.lower():
            sync_cycle = True
            logger.info(f"{t.idDevPack['idDev']} ****** SYNC CYCLES  ****  ")
        elif 'n' in sync_cycle.lower():
            sync_cycle = False
        else:
            sync_cycle = True
        for t in threads:
            t.sync_ = sync_cycle

    n = 0
    flag_old = 0
    flag_tempfileBk = False
    flag_tempArrayBk = False
    to_sampleTime_old = 0
    dataToStore_ = {}

    c000 = seedatadb(config_mysql)  # - Class Storage Management

    # Loop for both options 0, 1
    while n < maxSample:
        # Check sample trigger
        flag_sample, TimeNow, flag_old, TimeNow_ns, to_sampleTime = sampleFlag_(sample_params, flag_old)

        # OFF-SAMPLE Time
        # Activites:
        #   1.     tempArrayBk
        #   2.     tempfileBk
        #
        if to_sampleTime != to_sampleTime_old:
            logger.info(' > {} - seconds to sample: {}'.format(TimeNow, sample_params['sampleTime'] - to_sampleTime))
            to_sampleTime_old = to_sampleTime

            # tempArrayBk -  tempArray to DB
            if options_['tempArrayBk'] and flag_tempArrayBk:
                c000.reload_arrayBackup()
                flag_tempArrayBk = False

            # file tempBackup DB
            if options_['tempfileBk'] and flag_tempfileBk:
                c000.reload_filebackup()
                flag_tempfileBk = False

        # Sampling time
        if flag_sample:
            n += 1
            # Enable off sample activities
            flag_tempfileBk = True
            flag_tempArrayBk = True

            if options_['threads']:
                for t in threads:
                    logger.info(f"{t.idDevPack['idDev']} ****** SET TimeStamp *****  ")
                    t.TimeStamp = TimeNow
                    t.TimeStamp_ns = TimeNow_ns

                for t in threads:
                    logger.info(f"{t.idDevPack['idDev']} ****** ENABLE SAMPLE  ****  ")
                    t.read_en = True

                if sync_cycle:
                    tStart = time.time_ns()
                    logger.info(f" ****** START sample cycle  ***** time: {tStart / 10 ** 9}")
                    if sample_params['sampleTime'] > 0:
                        waitTime = sample_params['sampleTime'] * 0.8 * 10 ** 9  # [ns]
                    else:
                        waitTime = len(threads) * 5 * 10 ** 9  # [ns]

                    end_ = True
                    while end_:
                        for t in threads:
                            end_ = t.read_en
                        if (time.time_ns() - tStart) > waitTime:
                            end_ = False
                            logger.info(
                                f" ****** Exdeeded Waiting sample cycle time {waitTime} s ***** actual time: {time.time_ns() / 10 ** 9} - delay: {(time.time_ns() - tStart) / 10 ** 9}")
                    logger.info(
                        f" ****** END threading sample cycle ***** time: {time.time_ns() / 10 ** 9} - delay: {(time.time_ns() - tStart) / 10 ** 9}")
                else:
                    logger.info(
                        f" ****** NO Syncronization of Threading CYCLE SAMPLES ! ***** time: {time.time_ns() / 10 ** 9} - delay: {(time.time_ns() - tStart) / 10 ** 9}")

            else:
                logger.info(f"{t.idDevPack['idDev']} ****** NO THREADS: STARTING SEQUENTIAL SAMPLES  ****  ")
                tStart = TimeNow_ns  # time.time_ns()
                for t in threads:
                    t.TimeStamp = TimeNow
                    t.TimeStamp_ns = TimeNow_ns
                    t.read_en = True

                    # Run sample
                    t.run_once()

                logger.info(
                    f" ****** END NO-threading sample cycle ***** time: {time.time_ns() / 10 ** 9} - delay: {(time.time_ns() - tStart) / 10 ** 9}")

            # Print Messsage
            for t in threads:
                device_id = t.idDevPack['idDev']
                device_type = t.idDevPack['typeDev']
                device_method = t.idDevPack['method']
                err = t.codeError_rr
                delay_ = int(((t.time_[3] - TimeNow_ns) * 10 ** -6) * 1000) / 1000  # [ms]
                rr_dTime = str(t.rr_dtime[0] / 1000000)
                seq_ = (
                    '---> sample n. ', str(n), device_id, device_type, device_method, str(err), str(TimeNow),
                    'devReadTime[ms]:',
                    str(delay_) + ' ms', 'rrTime:', rr_dTime)
                logger.info(' '.join(seq_))

            # 3. Storage
            # store to  DB
            if flag_fastStorage and options_['dataDdBk']:
                data_pack = {}
                # logger.info(f" ****** END BUILD VALUES ***** time: {time.time_ns() / 10 ** 9}")
                for i, t in enumerate(threads):
                    t.build_values()
                    data_pack[i] = t.param_list
                    logger.info(f" ****** BUILD_VALUES  ***** n. {i} - Delay: {(time.time_ns() - tStart) / 10 ** 9} s")
                c000.data_store_pack(data_pack, config_mysql['tableRaw'])
                logger.info(f" ****** STORED DATA ***** Delay: {(time.time_ns() - tStart) / 10 ** 9} s")

                if options_['lastData']:
                    if c000.configMysql['config_mysql_bk']['enable']:
                        c000.configMysql['config_mysql_bk']['enable'] = False
                        c000.dataDB_seeLast_write(data_pack, None)
                        c000.configMysql['config_mysql_bk']['enable'] = True
                    else:
                        c000.dataDB_seeLast_write(data_pack, None)
                logger.info(f" ****** LAST DATA ***** Delay: {(time.time_ns() - tStart) / 10 ** 9} s")

            if not flag_fastStorage:
                # Backup DATA to Temp Memory
                dict_ = sample_data(TimeNow_ns, threads)
                dataToStore_[n - 1] = copy.deepcopy(dict_)

            logger.info(
                f" ****** END STORE VALUES ***** time: {time.time_ns() / 10 ** 9} -  Delay: {(time.time_ns() - tStart) / 10 ** 9} s")

    logger.info(' /////////  -------------- Sampling completed ------------  //////////')
    for t in threads:
        logger.info(f"{t.idDevPack['idDev']} ****** DISABLE SAMPLE  ****  ")
        t.read_en = False
        t.close_conn()

    if not flag_fastStorage:
        # 3. Calculate Values
        for i in range(maxSample):
            for ii, t in enumerate(threads):
                # build values
                t.rr = dataToStore_[i][ii]['rr']
                t.time_ = dataToStore_[i][ii]['time_array']
                t.rr_dtime = dataToStore_[i][ii]['rr_dtime']
                t.TimeStamp = dataToStore_[i][ii]['TimeStamp']
                t.codeError_rr = dataToStore_[i][ii]['rr_error']
                t.build_values()
                dataToStore_[i][ii]['paramList'] = t.param_list

        # 5. Backup data to db
        if options_['dataDdBk']:
            # store to db - or tempFile (if tempfileBk) or tempArray.)
            data_pack = {}
            for i in range(maxSample):
                for ii, t in enumerate(threads):
                    data_pack[ii] = dataToStore_[i][ii]['paramList']
                flag_datastore = c000.data_store_pack(data_pack, config_mysql['tableRaw'])
                print('> database storage code: %s - sample n. %s - device n. %s' % (flag_datastore, i + 1, ii + 1))

        else:
            flag_datastore = ['noflag_db_store']
        # 6. Time report
        dfTime_ = time_report(dataToStore_)
        dfSync_ = sync_report(dataToStore_)
        print('-' * 10 + '   Time Report  ' + '-' * 10)
        print(dfTime_)
        print('-' * 10 + '   Sync Report  ' + '-' * 10)
        print(dfSync_)
        print('-' * 10 + '   Statistics  ' + '-' * 10)
        samples_ = len(dfTime_)
        print(' - Total Samples:', samples_)

        minTime = datetime.strptime(dfTime_["DateTime"].min(), '%Y-%m-%d %H:%M:%S.%f')
        maxTime = datetime.strptime(dfTime_["DateTime"].max(), '%Y-%m-%d %H:%M:%S.%f')

        dd = (maxTime - minTime)
        deltaTime = (dd.seconds + dd.microseconds * 10 ** -6)

        print(' TimeSTart:', dfTime_["DateTime"].min())
        print(' TimeEnd:', dfTime_["DateTime"].max())

        print(' deltaTime {} [s]'.format(deltaTime))
        print(' frequency [Hz]: {}'.format(samples_ / deltaTime))

        print('-' * 10 + '   Saving to files dfTime_report.csv / dfSync_report.csv ' + '-' * 10)

        dfTime_.to_csv('dfTime_report.csv')
        dfSync_.to_csv('dfSync_report.csv')

        print('-' * 10 + '   Done    ' + '-' * 10)


#
#   - Functions
#
def load_driver_method(driver_pack_name, driver_name):
    # Loads device's driver
    # v1.0  2022-02-07

    '''
    Inputs:
        driver_pack_name = 'susee.see_drivers'
        driver_name = 'P32'
    '''

    try:
        driverLib_ = importlib.util.find_spec(driver_pack_name)
        driver_name = 'c_driver_' + driver_name
        spec = importlib.util.spec_from_file_location(driver_name, driverLib_.origin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        driver_ = getattr(module, driver_name)
        print(f"---- loaded driver of device id '{driver_name}' . driver name:  {driver_.__name__}   -------------")
    except Exception as exc:
        raise RuntimeError(f"[msg] - Driver of device id {driver_name} not found ") from exc
    return driver_

def filter_devices(pack):
    # Filters  enabled devices
    # v1.0 2022-01-29
    pack1 = {}
    xx = 0
    for x in pack.keys():
        if pack[x]['enable']:
            pack1[xx] = pack[x]
            xx += 1
    return pack1

def load_dataFile():
    # Import the data file
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
                print(f"[msg] - error: custom data file: '{customLib}' not found")
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

def sampleFlag_(sample_params, flag_old):
    # Sample flag
    # v.1.1 2020-09-2
    # v.1.2 2022-02-07

    TimeNow_ns = time.time_ns()
    TimeNow = datetime.fromtimestamp(TimeNow_ns * 10 ** -9)
    timeSeconds = TimeNow.minute * 60 + TimeNow.second + TimeNow.microsecond * 10 ** -6

    sampleTime = sample_params['sampleTime']  # [s]

    if sampleTime >= 1:
        TimeNow = datetime(TimeNow.year, TimeNow.month, TimeNow.day, TimeNow.hour, TimeNow.minute, TimeNow.second)

    ####  check flag_sample  ####
    flag_sample = False  # TimeNow.second

    if sampleTime > 1:
        flag_sample = (int(timeSeconds) % int(sampleTime)) == int(sample_params['sampleShift']) and \
                      flag_old != TimeNow.second
        flag_old = TimeNow.second

    if 0 < sampleTime <= 1:
        flag_sample = int(timeSeconds * 10 ** 2) % int(sampleTime * 10 ** 2) == 0 and \
                      flag_old != int(timeSeconds * 10 ** 2)
        flag_old = int(timeSeconds * 10 ** 2)

    if sampleTime == 0:
        return True, TimeNow, 0, TimeNow_ns, 0

    return flag_sample, TimeNow, flag_old, TimeNow_ns, int(timeSeconds) % int(sampleTime)

def t_to_DateTime(tt):
    # Convert time_ns() to DateTime
    # v0.0 2020-09-27

    t1 = datetime.fromtimestamp(tt * 10 ** -9)
    return t1.strftime('%Y-%m-%d %H:%M:%S.%f')

def time_report(_dataToStore):
    # v1.0  2020-09-28

    s_ = len(_dataToStore)  # samples
    d_ = len(_dataToStore[0])  # devices
    tab_ = []
    k_ = 10 ** -9
    k1_ = 10 ** -6
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
    # Syncronizatio report -
    # Sample timing
    # v1.0 2020-09-28

    s_ = len(_dataToStore)  # samples
    d_ = len(_dataToStore[0])  # devices
    tab_ = []
    k1_ = 10 ** -6
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

#
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt or KeyError:
        print(' - Python script keyboard interrupted ')
        try:
            sys.exit(0)
        except Exception as exc:
            raise RuntimeError(f"[msg] - Script stopped") from exc

