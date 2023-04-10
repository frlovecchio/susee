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
#668 
'''
ver = '1.0 - 2022-06-03'  # class custom functions 668
ver = '1.1 - 2022-06-15'
ver = '2.0 - 2022-07-10'  # added readFast
ver = '2.1 - 2022-07-31'  # added readFast
ver = '2.2 - 2022-08-11'  # added clients management
ver = '2.3 - 2022-08-12'  # added clients management
ver = '2.4 - 2022-08-13'  # added clients management
ver = '2.5 - 2022-08-16'  # added clients management
ver = '2.5 - 2022-08-20'  # added clients management
ver = '2.6 - 2022-09-10'  # added clients management
ver = '2.7 - 2022-09-14'  # fixed bug in Tabella_GG
ver = '2.8 - 2022-09-21'  # fixed bug in Tabella_GG
ver = '2.9 - 2022-09-22'  #
ver = '3.0 - 2022-10-03'  # introduced open/close comm.
ver = '3.1 - 2022-10-09'  #
ver = '3.1 - 2022-11-01'  #
ver = '3.1 - 2022-11-09'  #  close connections in FastSample
ver = '3.2 - 2022-11-10'  #  added events service
ver = '3.3 - 2022-11-13'
ver = '3.4 - 2022-11-14'
ver = '3.5 - 2022-11-15'
ver = '3.6 - 2022-11-16'
ver = '3.7 - 2022-11-17'
ver = '3.8 - 2022-11-26'
ver = '3.91 - 2022-11-30'
ver = '4.30 - 2022-12-21'
ver = '4.31 - 2023-01-03' #668 tables new year fixed


import time
import sys
from datetime import datetime, timedelta
import copy

from susee.see_functions import time_utc, utctime_to_tZone, push_log, check_OpenPorts
from susee.see_functions import load_driver_method, filter_devices, load_dataFile, sample_data, \
    list_remoteClients, sampleFlag_, time_report, sync_report

# todo: fix custom class
# from susee668.see_668 import see668_custom
from susee.see_db import seedatadb, Events, EventsDB, db_table
from susee.see_comm import  c_comm_devices
from susee.see_web import seeweb


import logging
#import etl_data668 as cLib

global logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


#   - Messages
print('')
print('')
print('-' * 80)
print('--- SUSEE - Energy Management System Platform     --- ')
print('------------------------------------------------------ ')
print('')
print('--- Studio Tecnico Pugliautomazione - Bari, Italy --- ')
print('--- eng. Francesco Saverio Lovecchio, ph.D.       --- ')
print('--- ETL Tool %s ' % ver)
print('--- UTC Date: %s ' % (time_utc()))
print('-' * 80)
print('')
print('')
time.sleep(3)

def main():

    #  - Load custom data from custom Module cLib
    cLib = load_dataFile()
    idDevices_pack = cLib.idDevices_pack
    options_ = cLib.options_
    config_mysql = cLib.config_mysql
    sample_params = cLib.sample_params
    ###################################################

    global c000, c001
    c000 = seedatadb(config_mysql)  # - Class Storage Management
    #todo: fix custom class
    #c001 = see668_custom(config_mysql)  # Class 668 custom functions
    c002 = db_table(config_mysql)

    #   - Filter devices dataframe
    idDevices_pack = filter_devices(idDevices_pack)

    #   - List of unique Clients - ordered
    uClients = list_remoteClients(idDevices_pack, reverse=False)
    num_devices = len(idDevices_pack)
    num_clients = len(uClients)
    Time_pause = cLib.sample_params['waitTime']  # s

    if num_devices == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO DEVICES TO READ ! - - - - - - - - ')
        print('-' * 60)
        exit()

    if num_clients == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO CLIENTS TO READ ! - - - - - - - - ')
        print('-' * 60)
        exit()

    # - List of clients Drivers (no threads)
    uthreads = []
    for i in range(num_clients):
        t = c_comm_devices(uClients[i])
        uthreads.append(t)

    #   - List of  devices Drivers
    threads = []
    for i in range(num_devices):
        drivers_lib_name = 'susee.see_drivers'
        driver_class_name = 'c_driver_' + idDevices_pack[i]['typeDev']
        driver_ = load_driver_method(drivers_lib_name, driver_class_name)
        t = driver_(idDevices_pack[i])
        t.setup_regs()
        threads.append(t)

    # List of  FAST devices (Second read loop)
    # Fast Sample
    listFastDevices = cLib.custom_table['List_fastDevices']
    threadsFast = []
    for t in threads:
        if t.idDevPack['idDev'] in listFastDevices:
            threadsFast.append(t)

    #
    # Setup EVENTS
    # Reads all events data and generates list of dictionaries
    #
    ev000 = EventsDB(config_mysql)
    ev_dictList = ev000.read_eventTableSys()
    n_events = len(ev_dictList)


    #Create events instances
    list_events = []
    for i in ev_dictList:
        list_events.append(Events(config_mysql,i))
    id_events =[]
    for e in list_events:
        id_events.append(e.idEvent)

    logger.info(f'[msg] - n. {n_events} - Events id list: {id_events}')

    #Info
    for x in ev_dictList:
        # evid + evDescr
        ev_info = f"EventId: {x['00'][0]} - {x['01'][0]}"


    #Messages
    if n_events == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO EVENTS FOUND - - - - - - - - ')
        print('-' * 60)
        exit()
    else:
        print('-' * 100)
        print(f' -  - - -  - - - N. {str(n_events)} EVENTS  - - - - - - - - ')
        print('-' * 100)
        for i in list_events:
            print('idEvent: ',i.idEvent)
            [print(x) for x in sorted(i.dataEvents.items())]

    print('')
    print('')

    # EVENTS - ENERGY TYPE Setup initial value
    for x in list_events:
        if x.energyType:
            x.qt_energy(x.idDev, x.idParam)
            x.startEn = x.actEn
            print(f' --- Event id {x.idDev} - set initial energy to {x.startEn} at time {datetime.now()}')

    print('')


    time.sleep(5)

    if options_['UpgradeWeb']:
        r_= input(' Upgrade WebServer? [y/N] ')
        if r_ == 'y':
            df, e_ = seeweb(config_mysql).fill_sysSet('Raw')
        else:
            print('>> Web Upgrade skipped   ')
            time.sleep(3)

    if options_['Messages']:
        print('')
        print('')
        print('>> - - - - -  - Devices List  - - - - - - -  - -  ', num_devices)
        for ii in idDevices_pack.keys():
            print('Device n. %s ' % (ii + 1))
            [print(' {}:  {}'.format(i, idDevices_pack[ii][i])) for i in idDevices_pack[ii].keys()]
        print('>> SampleParams: ')
        [print('>> {}: '.format(ii)) for ii in sample_params.items()]
        print('>> Database: ', config_mysql['host'])
        print('-' * 40)
        print('')
        print('')

    if num_devices == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO DEVICES TO READ ! - - - - - - - - ')
        print('-' * 60)
        exit()
    else:
        print('-' * 60)
        print(' -  - - -  - - - N. %s DEVICES TO READ  - - - - - - - - ' % (str(num_devices)))
        print(' -  - - -  - - - N. %s CLIENTS TO READ  - - - - - - - - ' % (str(num_clients)))
        print(' -  - - -  - - - N. %s EVENTS           - - - - - - - - ' % (str(n_events)))
        print(f' -  - - -  - - - PAUSE TIME  {Time_pause} [s]  - - - - - - - - ')
        print('-' * 60)
    ####################################################

    time.sleep(3)
    # print('')
    # print('')
    # #Check and close open ports
    # if options_['threads']:
    #     print('')
    #     print(' - - - Close devices ports   - - - ')
    #     check_OpenPorts(idDevices_pack)
    # else:
    #     print('')
    #     print(' - - - Close clients ports   - - - ')
    #     check_OpenPorts(uClients)

    print('')
    print('')
    nDev_ = len(threads)
    print('>> Number of instances: ', nDev_)
    if nDev_ == 0:
        print('-' * 60)
        print(' -  - - -  - - - WARNING: NO DEVICES TO READ ! - - - - - - - - ')
        print('-' * 60)
        exit()

    print('')
    print('')
    if options_['threads']:
        print(f'- - - - -  Open threads connections n. {num_devices} - - - - -')
        for i, t in enumerate(threads):
            t.open_conn()
            t.start()  # Setup
            t.setDaemon = 0

        if not sample_params['open_close_conn']:
            print(f'- - - - -  Close threads  connections n. {num_devices} - - - - -')
            for i, t in enumerate(threads):
                t.close_conn()
    else:
        print(f'- - - - -  Open clients  connections n. {num_clients} - - - - -')
        for i, t in enumerate(uthreads):
            # /!\ no threads 2022-08-11
            t.open_conn()
        print('')

        if not sample_params['open_close_conn']:
            print(f'- - - - -  Close clients  connections n. {num_clients} - - - - -')
            for i, t in enumerate(uthreads):
                t.close_conn()

    time.sleep(3)
    print('')
    print('')
    print(' - - - - - Check Status of ports   - - - ')
    print('')
    print('')


    if options_['threads']:
        for i, t in enumerate(threads):
            print([i, t.idDevPack['method'], t.idDevPack['ipAddr_COM'], t.client.connect()])
            time.sleep(Time_pause)
    else:
        for i, t in enumerate(uthreads):
            print([i, t.idDevPack['method'], t.idDevPack['ipAddr_COM'], t.client.connect()])
            time.sleep(Time_pause)

    time.sleep(3)
    print('')
    print(' - - - - - Sample Types - - - - -')
    print('0. Mode - Endless loop of samples')
    print('1. Mode - Finite number of  samples -  sync cycle')
    print('')

    flag_fastStorage = False
    maxSample = 10


    #
    # 0. Mode - Endless loop of samples
    #
    if sample_params['sampleType'] == 0:
        print('')
        print('-' * 10 + '  0. Mode - Endless Number of Samples Mode  ' + '-' * 20)

        # Infinite loop time ...
        maxSample = 10 ** 10  # 10.000.000.000  -> circa 10.000 anni a 30s di campionamento
        flag_fastStorage = True

    #
    # 1. Mode - Finite number of  samples -  sync cycle
    #
    elif sample_params['sampleType'] == 1:
        print('/' * 100)
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
        # sync_cycle = input('Syncronization of cycles samples (wait till all are closed) ? [Yes/no]:')
        # if 'y' in sync_cycle.lower():
        #     sync_cycle = True
        #     logger.info(f"{t.idDevPack['idDev']} ****** SYNC CYCLES  ****  ")
        # elif 'n' in sync_cycle.lower():
        #     sync_cycle = False
        # else:
        #     sync_cycle = True

    nn = 0
    nn1 = 0
    flag_old = 0
    flag_tempfileBk = True
    flag_tempArrayBk = True
    #flag_Fast = True
    flag_Events = True
    to_sampleTime_old=0
    dataToStore_ = {}
    tZone = config_mysql['tZone']


    # Loop for both options 0, 1
    while nn < maxSample:
        # Check sample trigger
        flag_sample, TimeNow, flag_old, TimeNow_ns, to_sampleTime = sampleFlag_(sample_params, flag_old)

        # OFF -  No SAMPLE Time
        # Activites:
        #   1. Load and store tempArrayBk
        #   2. Load and store tempfileBk
        #   3. Read FastDevices
        #   4. Check connection

        #
        # if not flag_sample:
        #   1. file tempBackup DB   - ONE SHOT
        #   2. tempArrayBk -  tempArray to DB  - ONE SHOT
        #   3. Check Events
        #   4. fast device sample   - CONTINUOUSLY
            #   4.1. Check connection
            #   4.1  Store Last Fast data

        if not flag_sample and to_sampleTime != to_sampleTime_old:

            lasting_time = sample_params['sampleTime'] - sample_params['sampleShift'] - to_sampleTime
            logger.info(f' > seconds to sample: {lasting_time} [s] ------ ') #to_sampleTime: {to_sampleTime} to_sampleTime_old: {to_sampleTime_old}')
            to_sampleTime_old = to_sampleTime

            # 1. file tempBackup DB
            if options_['tempfileBk'] and flag_tempfileBk and lasting_time > 10:
                print('  ----------------- 1. reload_filebackup  ----------------')
                c000.reload_filebackup()
                flag_tempfileBk = False

            # 2. tempArrayBk -  tempArray to DB
            if options_['tempArrayBk'] and flag_tempArrayBk and lasting_time > 10:
                print(' -----------------  2. reload_arrayBackup ----------------')
                c000.reload_arrayBackup()
                flag_tempArrayBk = False

            # 3. Events management
            '''
            todo: fix custom functions
            if options_['custom'] and  lasting_time > 10:
                print('  -----------------  3. events_do ----------------')

                #Reads events setup data from DB
                ev_dictList = ev000.read_eventTableSys()
                logger.info('[msg] - Events Data Updated from EventsSys Table')
                for x, i in enumerate(ev_dictList):
                    #Update event's parameters
                    e= list_events[x]
                    e.dataEvents = i
                    e.init_data()

                    if e.enable:
                        # Reads events
                        e.set_Event()
                        estr_=  f' [msg] - event ID: {e.idEvent} - Event State:{e.stateAlarm} - Change:{e.stateChange} - actValue:{e.actValue} - Limit:{e.setLimit} - Hyst:{e.hyst_pu*100}%'
                        print(estr_)

                        # Write DB Table Events
                        if e.stateChange in ['UP', 'DOWN']:

                            #Write Table Events
                            e.write_TableEvent(config_mysql['tableEvents'])
                            print(' *********************** AAA write to table change: ', e.stateChange)
                            logger.info(estr_)

                            #Messaggio EMAIL
                            sbj_='subject not defined'
                            if e.stateChange =='UP':
                                sbj_= e.msgUP
                                msg_=f"See_668_Event {TimeNow}- VALORE SUPERATO - EVENTO {e.idEvent}-{e.evDescr} idDevice:{e.idDev}-idPAram: {e.idParam} - ActualValue: {e.actValue} {e.eventFunction} {e.setLimit}{e.um} - Isteresi_pu: {e.hyst_pu}"
                            elif e.stateChange =='DOWN':
                                sbj_= e.msgDOWN
                                msg_ = f"See_668_Event {TimeNow}- VALORE RIENTRATO - EVENTO {e.idEvent}-{e.evDescr} idDevice:{e.idDev}-idPAram: {e.idParam} ActualValue: {e.actValue} - Limite: {e.setLimit}{e.um} - Isteresi_pu: {e.hyst_pu}"

                            # SEND EMAIL
                            conf_email = {
                                **cLib.config_events['email_server'],
                                'to_email': cLib.config_events['ref_person']['email'],
                                'subject': sbj_,
                                'msg': msg_,
                            }
                            try:
                                df_sys = c001.dataDB_Table_read(c001.configMysql['tableSys'])[0]
                                conf_email['to_email'] = str(
                                    df_sys[df_sys['idParam'] == 'emailEvents'].Value.to_list()[0])

                            except:
                                pass

                            print('AAA conf_email: ', conf_email)
                            ev000.send_email(conf_email)

                            print('AAA ---------------------')
                            print('AAA sbj:',sbj_)
                            print('AAA msg_:',msg_)
                            print('AAA ---------------------')

                            #SEND EMAIL
                            conf_email = {
                                **cLib.config_events['email_server'],
                                'to_email': cLib.config_events['ref_person']['email'],
                                'subject': sbj_,
                                'msg': msg_,
                                    }

                            #Reads email from DB Table Sys
                            try:
                                df_sys = c001.dataDB_Table_read(c001.configMysql['tableSys'])[0]
                                conf_email['to_email'] = str(df_sys[df_sys['idParam'] == 'emailEvents'].Value.to_list()[0])
                                print('AAA1 conf_email: ', conf_email['to_email'])
                            except:
                                pass

                            print('AAA conf_email: ', conf_email)
                            ev000.send_email(conf_email)

                        # Write DB Table EventsLast
                        sql_= f"DELETE  FROM {config_mysql['tableEvents']+'Last'} where idEvent='{e.idEvent}';"
                        e.exec_sql1(sql_,0)
                        e.write_TableEventLast(config_mysql['tableEvents']+'Last')

                        # Add Power to energyType events
                        if e.energyType:
                            e.actValue = e.actPower
                            e.idParam =e.idParam+'/h'
                            e.um = e.um[:-1]
                            e.setLimit = e.setLimit * 4
                            e.write_TableEventLast(config_mysql['tableEvents'] + 'Last')

                        #Reset min max SIEMENS PAC3200
                        check_ = ('max' in e.eventType.lower()) or ('min' in e.eventType.lower())
                        if check_:
                            _, TimeNow, _, TimeNow_ns, _ = sampleFlag_(sample_params, 0)
                            for i, t in enumerate(uthreads):
                                t.TimeStamp = TimeNow
                                t.TimeStamp_ns = TimeNow_ns
                                # Open connection
                                if sample_params['open_close_conn']:
                                    t.open_conn()
                                # Call devices
                                for ii, tt in enumerate(threads):
                                    if tt.uCode == t.uCode:
                                        if tt.idDevPack['idDev'] == e.idDev and ('P32' in tt.idDevPack['typeDev']):
                                            # Setup device
                                            tt.TimeStamp = t.TimeStamp
                                            tt.TimeStamp_ns = t.TimeStamp_ns
                                            # Setup registers data
                                            t.idDevPack = tt.idDevPack
                                            t.addrList = tt.addrList
                                            # Execute write
                                            t.setup_regs()
                                            t.write_regs(60002, 0)
                                            t.write_regs(60003,0)
                                            # Read data from client to device
                                            tt.codeError_rr = t.codeError_rr
                                            tt.rr_dtime = t.rr_dtime
                                            tt.rr_delay = t.rr_delay

                                            msg_ = f" > Written data to: R {t.uCode}-idDev: {tt.idDevPack['idDev']}-{tt.idDevPack['typeDev']} err: {str(t.codeError_rr)} " \
                                                   f"- delay:{['{:.2f}'.format(x / 10 ** 9) for x in tt.rr_dtime]} [s]"
                                            logger.info(msg_)
                                            push_log(msg_)
                        print(' - - ' * 20)

                # 3.3 Yearly create new  Tables before to store data
                date_0 = TimeNow
                if tZone != '':
                    date_0 = utctime_to_tZone(TimeNow, tZone)
                startYear = datetime(
                    year=date_0.year,
                    month=1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                )

                diffTime = date_0 - startYear
                flag_newYear1 = False
                flag_newYear2 = False
                flag_newYear3 = False

                if diffTime < timedelta(seconds=60):
                    flag_newYear1 = c002.create_newYear(config_mysql['tableRaw'], True)

                    #668 tables
                    try:
                        flag_newYear2 = c001.create_newYear668('Tab_Misure', True)
                        flag_newYear3 = c001.create_newYear668('Tab_Prod', True)
                    except:
                        pass

                if flag_newYear1:
                    msg_ = f"flag_newYear1 - [msg] Successully created new year tables: RawTable"
                    logger.info(msg_)
                    push_log(msg_)

                if flag_newYear2:
                    msg_ = f"flag_newYear2 - [msg] Successully created new year tables: Tab_misure"
                    logger.info(msg_)
                    push_log(msg_)

                if flag_newYear3:
                    msg_ = f"flag_newYear3 - [msg] Successully created new year tables: Tab_Prod"
                    logger.info(msg_)
                    push_log(msg_)
            '''

            # 4. fast device sample
            # v1.0 2022-07-10  - Continuosly sampling of some devices
            if options_['fastSample'] and lasting_time > 10:
                nn1+=1
                _, TimeNow, _, TimeNow_ns, _ = sampleFlag_(sample_params, 0)

                for i, t in enumerate(uthreads):
                    t.TimeStamp = TimeNow
                    t.TimeStamp_ns = TimeNow_ns


                    #Open connection
                    if sample_params['open_close_conn']:
                        t.open_conn()

                    #Call devices
                    for ii, tt in enumerate(threadsFast):
                        if tt.uCode == t.uCode:
                            # Setup device
                            tt.TimeStamp = t.TimeStamp
                            tt.TimeStamp_ns = t.TimeStamp_ns
                            #Setup registers data
                            t.idDevPack = tt.idDevPack
                            t.addrList = tt.addrList
                            # Read data from client to device
                            num_try= t.read_regs_loop(sample_params['num_try'])
                            # Setup client
                            tt.rr = t.rr
                            tt.codeError_rr = t.codeError_rr
                            tt.rr_dtime = t.rr_dtime
                            tt.rr_delay = t.rr_delay

                            msg_ = f" > R {tt.uCode}-idDev: {tt.idDevPack['idDev']}-{tt.idDevPack['typeDev']} err: {str(tt.codeError_rr)} " \
                                   f"- delay:{['{:.2f}'.format(x / 10 ** 9) for x in tt.rr_dtime]} [s] - try:{num_try}"
                            logger.info(msg_)
                            push_log(msg_)

                    #Close connection
                    if  sample_params['open_close_conn']:
                        t.close_conn()

                    # WaitTime
                    time.sleep(Time_pause)

                data_pack = {}
                for i, t in enumerate(threadsFast):
                    t.build_values()
                    data_pack[i] = t.param_list
                    #logger.info(f" ****** BUILD_VALUES  ***** n. {i} - Delay: {(time.time_ns() - t.TimeStamp_ns) / 10 ** 9} s")

                # 4.1 Store Last Fast data
                if options_['lastData']:
                    # Write sample data to last table
                    if c000.configMysql['config_mysql_bk']['enable']:
                        c000.configMysql['config_mysql_bk']['enable'] = False
                        store_flag = c000.dataDB_seeLast_write(data_pack,  c000.configMysql['tableLastFast'], None)
                        c000.configMysql['config_mysql_bk']['enable'] = True
                    else:
                        store_flag =c000.dataDB_seeLast_write(data_pack, c000.configMysql['tableLastFast'], None)
                    logger.info('')
                    logger.info(f" ==============  LAST FAST DATA WRITTEN ***** Delay: {'{:2f}'.format((time.time_ns() - t.TimeStamp_ns) / 10 ** 9)} [s] ================== ")

                    # 4.2. Check connection
                # Try to reconnect to clients
                # if options_['threads']:
                #     for ii, tt in enumerate(threads):
                #         if not tt.client.connect():
                #             logger.info(f' - see_etl [msg] Check Connection uCode: {tt.uCode} - try to reconnect...')
                #             tt.open_conn()
                #         else:
                #             pass
                #             #logger.info(f' - see_etl [msg] Check Connection uCode: {tt.uCode} connected ')
                #
                # else:
                #     for ii, tt in enumerate(uthreads):
                #         if not tt.client.connect():
                #             logger.info(f' - see_etl [msg] Check Connection uCode: {tt.uCode} - try to reconnect...')
                #             tt.open_conn()
                #         else:
                #             pass
                #             #logger.info(f' - see_etl [msg] Check Connection uCode: {tt.uCode} connected ')

                #5. Events

        # ON - Sampling time
        # Activities
        # 1. Extracts Data from devices
        # 2. Store data to database

        if flag_sample:
            nn1 = 0  # reset FAST samples
            nn += 1  # increase sample counter

            # Enable off sample activities
            flag_tempfileBk = True
            flag_tempArrayBk = True
            flag_Events = True
            tStart = time.time_ns()

            logger.info(f" ****** START sample cycle n. {nn} ***** time: {TimeNow}")

            if options_['threads']:
                # Setup SAMPLE TimeStamp
                for i, t in enumerate(threads):
                    logger.info(f"idDev: {t.idDevPack['idDev']} ****** RUN THREAD SAMPLE ***** thread number: {i}")
                    t.TimeStamp = TimeNow
                    t.TimeStamp_ns = TimeNow_ns
                    t.setup_regs()

                    if sample_params['open_close_conn']:
                        t.open_conn()
                    t.run()
                    if sample_params['open_close_conn']:
                        t.close_conn()
                    time.sleep(Time_pause)

                # Wait end of run() function
                for i, t in enumerate(threads):
                    t.join()
            else:
                logger.info(f"****** NO THREADS: STARTING SEQUENTIAL SAMPLES  ****  ")

                # Call clients
                for i, t in enumerate(uthreads):

                    t.TimeStamp = TimeNow
                    t.TimeStamp_ns = TimeNow_ns

                    #Open connection
                    if sample_params['open_close_conn']:
                        t.open_conn()

                    #Call devices
                    for ii, tt in enumerate(threads):
                        if tt.uCode == t.uCode:
                            # Setup device
                            tt.TimeStamp = TimeNow
                            tt.TimeStamp_ns = TimeNow_ns

                            #Setup registers data
                            t.idDevPack = tt.idDevPack
                            t.addrList = tt.addrList
                            num_try = t.read_regs_loop(sample_params['num_try'])

                            #Read data from client to device
                            tt.rr = t.rr
                            tt.codeError_rr = t.codeError_rr
                            tt.rr_dtime = t.rr_dtime
                            tt.rr_delay = t.rr_delay

                            msg_= f" > R {tt.uCode}-idDev: {tt.idDevPack['idDev']}-{tt.idDevPack['typeDev']} err: {str(tt.codeError_rr)} " \
                                  f"- delay:{['{:.2f}'.format(x/10**9) for x in tt.rr_dtime]} [s] - try:{num_try}"
                            logger.info(msg_)
                            push_log(msg_)

                    #Close connection
                    if sample_params['open_close_conn']:
                        t.close_conn()
                    time.sleep(Time_pause)

                msg_= f" ****** END NO-threading sample cycle ***** time: {time.time_ns() / 10 ** 9} [s] - delay: {'{:.2f}'.format((time.time_ns() - tStart) / 10 ** 9)} [s]"
                logger.info(msg_)
                push_log('')
                push_log(msg_)

            # Print Message
            # for i, t in enumerate(threads):
            #     device_id = t.idDevPack['idDev']
            #     device_type = t.idDevPack['typeDev']
            #     device_method = t.idDevPack['method']
            #     err = t.codeError_rr
            #     rr_dTime = str(t.rr_dtime[0] / 10**6)
            #     seq_ = (
            #         '---> sample n. ', str(nn), device_id, device_type, device_method, str(err), str(TimeNow),
            #         'rrTime:', rr_dTime)
            #     msg_ = ' '.join(seq_)
            #     logger.info(msg_)  # comment if verbose

            # 2. Storage
            #    store to  DB
            #

            # logger.info(f" ****** END BUILD VALUES ***** time: {time.time_ns() / 10 ** 9}")
            data_pack = {}
            for i, t in enumerate(threads):
                t.build_values()
                data_pack[i] = t.param_list
                #logger.info(f" ****** BUILD_VALUES  ***** n. {i} - Delay: {(time.time_ns() - tStart) / 10 ** 9} s")

            #Extract list of idDevices
            list_devices = [x[1]['idDevice'] for x in data_pack[0].items()]

            #
            # 4. #668 Custom Routines
            #    4.1 Calculate GDM:
            #           - Active Power [W]
            #           - Reactive Power
            #
            '''
            if options_['custom']:

                # Calculate GDM (d00) Active and Reactive Power
                GDM_dev =cLib.custom_table['GDM_device']
                GDM_actPower, codeP_ = c001.see668_d00_actPower(data_pack, TimeNow, GDM_dev, '222', '133')
                GDM_reactPower, codeQ_ = c001.see668_d00_actPower(data_pack, TimeNow, GDM_dev, '226', '134')
                msg_ = f' ------------ Active power: {GDM_actPower} [W] - code: {codeP_} '
                logger.info(msg_)
                push_log(msg_)
                msg_ = f' ------------ Reactive Power: {GDM_reactPower} [VAr] - code: {codeQ_}'
                logger.info(msg_)
                push_log(msg_)

                #
                # 4. #668 Custom Routines
                #

                # 4.2 Upgrade Measure Table
                flag_custom_4 = c001.see668_TableMisure_write(data_pack,
                                                              c000.configMysql['Tabella_Misure_668'],
                                                              tZone),

                # 4.3 Upgrade Measure TableGG

                #Update Time HH:MM
                upHour = config_mysql['config_Table_GG']['upHour']
                upMinute = config_mysql['config_Table_GG']['upMinute']

                if tZone != '':
                    date_0 = utctime_to_tZone(TimeNow, tZone)

                if (date_0.hour == upHour and date_0.minute == upMinute):

                    #Array of dates. Insert as many dates as you need
                    aDate=[
                            datetime(TimeNow.year, TimeNow.month,TimeNow.day),
                            #datetime(2022,9,21),
                            #datetime(2022,9,19),
                            ]

                    flag_custom_5 = c001.see668_TableMisureGG_write(aDate)
            '''

            # 3.1 Store Last data
            if options_['lastData']:
                # Write sample data to last table
                if c000.configMysql['config_mysql_bk']['enable']:
                    c000.configMysql['config_mysql_bk']['enable'] = False
                    c000.dataDB_seeLast_write(data_pack, c000.configMysql['tableLast'], None)
                    c000.configMysql['config_mysql_bk']['enable'] = True
                else:
                    c000.dataDB_seeLast_write(data_pack, c000.configMysql['tableLast'], None)
                logger.info(f" ****** LAST DATA WRITTEN ***** Delay: {'{:.2f}'.format((time.time_ns() - tStart) / 10 ** 9)} s")

            # 3. Store data to Database
            if flag_fastStorage and options_['dataDdBk']:
                c000.data_store_pack(data_pack, config_mysql['tableRaw'])
                logger.info(f" ****** STORED DATA ***** Delay: {'{:.2f}'.format((time.time_ns() - tStart) / 10 ** 9)} [ms]")

            if not flag_fastStorage:
                # Backup DATA to Temp Memory
                dict_ = sample_data(TimeNow_ns, threads)
                dataToStore_[nn - 1] = copy.deepcopy(dict_)
            #t_to_DateTime(time.time_ns())
            logger.info(
                f" ****** END STORE VALUES ***** -  Delay: {'{:.2f}'.format((time.time_ns() - tStart) / 10 ** 9)} s")



    logger.info(f'////////  -------------- Sampling completed: n. {nn} samples ------------  //////////')

    #
    # Sampling  completed
    # Further activities
    #

    for t in threads:
        t.close_conn()
        logger.info(f"{t.idDevPack['idDev']} ****** DISABLED threads sample  **************  ")

    if not flag_fastStorage and sample_params['sampleType'] == 1:
        # Backup DATA to Database

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

#################################################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt or KeyError:
        print(' - Python script keyboard interrupted ')
        try:
            sys.exit(0)
            sys.exit()
        except Exception as exc:
            raise RuntimeError(f"[msg] - Script stopped") from exc
