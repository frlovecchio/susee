# -*- coding: utf-8 -*-

############################################
########### SEE WEB Based Functions   ######
############################################
# v2.0 2020-07-04
# v3.0 2020-10-23
# v3.1 2021-02-07
# v3.2 2021-02-21 see_ADMIN
# v3.3 2021-02-22 see_ADMIN
# v3.4 2021-02-27 interpolate
# v3.5 2021-02-28 interpolate
# v3.6 2021-03-09 shift -1
# v3.7 2021-04-12
# v4.0 2021-05-15
# v4.1 2021-05-20  plot_mscatter()
# v4.2 2021-06-03  upto 100 colors
# v4.3 2022-06-03
# v4.4 2022-06-29
# v4.4 2022-07-07
# v4.5 2022-07-12
# v4.6 2022-08-18
# v4.7 2022-08-19
# v4.8 2022-08-20
# v4.9 2022-08-21
# v5.0 2022-08-22
# v5.1 2022-09-02
# v5.2 2022-09-05
# v5.3 2022-11-10   moved events functions to see_668
# v5.3 2022-11-20
# v5.4 2022-11-20
# v5.5 2022-11-21

import pandas as pd
import numpy as np
import time
from numpy import NaN
import socket
import importlib
from susee.see_dict import err_code, params_id, message_strings
from susee.see_functions import push_log, datetime_to_F123, Dict_Generate, utctime_to_tZone, to_file
from susee.see_comm import internet_ip
from susee.see_db import seedatadb

from django.shortcuts import render
from datetime import datetime, timedelta

from bokeh.plotting import figure, show

from bokeh.embed import components
from bokeh.models import ColumnDataSource, ranges, Label, LabelSet, FactorRange, DatetimeTickFormatter, \
    NumeralTickFormatter

from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap, cumsum
from bokeh.palettes import Category20c

class seeweb(seedatadb):
    # v2.0 2020-10-23

    def __init__(self, configMysql, *args, **kwargs):
        super().__init__(configMysql)

    @classmethod
    def username(cls, request):
        # v1.0 2020-10-23

        from django.contrib.auth.models import Group
        # filter the Group model for current logged in user instance
        query_set = Group.objects.filter(user=request.user)
        groups_ = []
        for g in query_set:
            groups_.append(g.name)
        return request.user.username, groups_[0]

    def load_df(self, dbparams, UpdateFlag=None):
        # v2.0 2020-07-4
        # v2.1 2020-07-13

        df = pd.DataFrame([0])
        if UpdateFlag is True:
            df = self.fill_dataparam(self.configMysql, dbparams)
        else:
            df = pd.DataFrame.from_records(dbparams.objects.all().values())
        return df

    def fill_sysSet(self, mode,  **kwargs):
        # Regererate the tabSysData table (filter-- form data)
        # v1.9.1 - 2018-08-28
        # v1.10 - 2020-06-29 daysBack, no Param Description
        # v1.11 - 2020-07-03  in class
        # v2.00 - 2020-07-03
        # v2.01 - 2020-11-08
        # v2.02 - 2020-11-13
        # v2.1  - 2022-08-18
        # v2.2  - 2022-08-19
        # v2.3  - 2022-08-22
        # v2.4  - 2022-08-23

        # Variables
        config_mysql = self.configMysql
        tabParam = config_mysql['tableParams']
        language = config_mysql['language']
        seeDB = config_mysql['database']
        tableRaw = config_mysql['tableRaw']


        #tableRaw = config_mysql['tableLast']

        tableSysRaw = config_mysql['tableSysRaw']

        maxConnectTime_default = config_mysql['maxConnectTime']
        config_mysql['maxConnectTime'] = 60*60*8
        print(f" {'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())} - config_mysql['maxConnectTime']: {config_mysql['maxConnectTime']} [s]")

        if mode == 'Raw':

            #tabSysData = config_mysql['tableSysRaw']
            tabData = config_mysql['tableRaw']

            sql_concat = 'SELECT date_format(Date,"%Y-%m-%d") as Date1, idDevice, idParam ' \
                         + 'FROM seedb.seedata group by idDevice, idParam, Date1;'

            '''
            esempio
            SELECT date_format(Date, "%Y-%m-%d") as Date1, idDevice, idParam
            FROM DeroWeb.see608
            group  by idDevice, idParam, Date1;
            '''
            sql_concat = sql_concat.replace('seedb', seeDB)
            sql_concat = sql_concat.replace('descrLAN', 'descr' + language)
            sql_concat = sql_concat.replace('seedata', tableRaw)
            sql_concat = sql_concat.replace('seeParam', tabParam)

            print(' -> Running query on DB ... sql: ', sql_concat)
            dbData_, _ = seedatadb.exec_sql1(self, sql_concat, True)
            df_Data = pd.DataFrame(dbData_, columns=['Date', 'idDevice', 'idParam']) #, 'parDescr', 'parUm'])
            print(' -> Collected dbData: ', df_Data)

            config_mysql['maxConnectTime'] = maxConnectTime_default
            print(f"  - config_mysql['maxConnectTime']: {config_mysql['maxConnectTime']} [s]")


            #Load Table Parameters
            t_Params = config_mysql['tableParams']
            dbParams = self.dataDB_Table_read(t_Params)
            df_Params = pd.DataFrame(dbParams, columns=['idParam', 'descrITA', 'descrENG', 'um'])  # , 'parDescr', 'parUm'])
            print(' -> Collected df_Params: ', df_Params)
            #Merge tables
            df_Data = pd.merge(df_Data, df_Params, how='left', on='idParam')

            nok_data = ['inf', '-inf', 'nan', 'NaN', 'None', None, np.inf, np.nan]
            df_Data = df_Data.replace(nok_data, '--')
            df_Data = df_Data.fillna('--')

            if 'ITA' in self.configMysql['language']:
                df_Data= df_Data.drop('descrITA', axis=1)
                df_Data = df_Data.rename(columns={'descrENG': 'parDescr',
                                                  'um': 'parUm'})
            if 'ENG' in self.configMysql['language']:
                df_Data= df_Data.drop('descrENG', axis=1)
                df_Data = df_Data.rename(columns={'descrITA': 'parDescr',
                                                  'um': 'parUm'})
            else:
                df_Data= df_Data.drop('descrENG', axis=1)
                df_Data = df_Data.rename(columns={'descrITA': 'parDescr',
                                                  'um': 'parUm'})
            print(' -> df_Data dataFrame: ', df_Data)

        # Reformata DATE
        # df['Date']= df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d') )

        # Delete existing table
        sql_ = f"DELETE FROM {seeDB}.{tableSysRaw} where idNum>0;"
        flag_db, err_ = self.exec_sql1(sql_, 0)

        self.save_sql(err_, flag_db, sql_, 'Table setRaw deleted')

        #Filling SetRaw Table
        print(f" {'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())} -> Table SetRaw filling ...")

        # flag_db, err_ = self.dataDB_Table_write(df_Data, tabSysData)
        # Save to SysSetRaw

        df = df_Data

        # Drop idNum
        try:
            df.drop(columns='idNum', inplace=True)
        except:
            pass

        sql1 = 'INSERT INTO {0}.{1} {2} '.format(seeDB, tableSysRaw, tuple(df.columns))
        sql1 = sql1.replace("'", '')
        sql2 = 'VALUES {};'.format(tuple(map(tuple, df.to_numpy())))
        sql2 = sql2.replace('((', '(')
        sql2 = sql2.replace('))', ')')
        sql2 = sql2.replace('),);', ');')
        sql1 += sql2

        to_file(sql1,'sql____SetRawTable.txt')

        flagdb, err = self.exec_sql1(sql1, 0)
        self.save_sql(err_, flag_db, sql_, 'Table setRaw filled')

        print(f"{'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())} -> Table setRaw filled ...  err: {err_} ")
        return df, flagdb

    def save_sql(self, err_, flag_db, sql_, msg_1):
        if flag_db:
            msg_ = f' -> [msg] fill_sysSet() - {msg_1}'
            push_log(msg_)
            print(msg_)

        else:
            msg_ = f' -> [msg] fill_sysSet() - {msg_1} - {message_strings[20]} - err: {err_}'
            push_log(msg_)
            print(msg_)

            config_mysql_bk = self.configMysql['config_mysql_bk']
            if config_mysql_bk['enable']:
                filename = config_mysql_bk['filename']
                flag_file = self.write_to_file(filename, sql_)
                msg_ = f'[msg] fill_sysSet() - {msg_1} - {message_strings[10]} in {filename}'
                print(msg_)
                push_log(msg_)

class seeReport(seedatadb):
    def __init__(self, configMysql, *args, **kwargs):
        super().__init__(configMysql)

        self.configMysql = configMysql
        # Event Table setup
        self.ev_ = {}

        self.ev_
        self.ev_['ev01_actValue'] = 10 ** 20  # float(self.dataDB_seeLast_read('d00', '222')[0][0])
        self.ev_['ev01_minute'] = 0

        self.ev_['ev01_up'] = False
        self.ev_['ev02_up'] = False
        self.ev_['ev03_up'] = False

        self.ev_['ev01_write'] = False
        self.ev_['ev02_write'] = False
        self.ev_['ev03_write'] = False

        self.ev_['ev01_emailAbil'] = False
        self.ev_['ev02_emailAbil'] = False
        self.ev_['ev03_emailAbil'] = False
        self.tZone = configMysql['tZone']

    #
    # Interpolate data
    #
    def f_interpolate(self, load_data):
        # FIlls empty data
        # df is a dataframe:
        #           timestep: minute
        #           Datetime  '2021-02-18 11:01:00'
        #           energy parameters (222,226)

        #   Services:
        #       a. Extract all data '0t'
        #       b. Filter max energy over 1 minute
        #       c. Interpolate
        #
        # v.1.0 2021-02-27
        # v.1.1 2021-02-28
        # v.1.2 2021-05-17
        # v.1.3 2022-09-02
        # v.1.4 2022-09-05


        # a. Extract all data and merge with dfDateTime
        #load_data['timeStep'] = '0t'    #set timestep to samplingStep
        df0, _ ,_= self.pivotRead_RawData(load_data)
        dfDateTime = self.f_create_dfDatetime(load_data) # timeStep = '30s'
        df0 = pd.merge(dfDateTime, df0, how='left', left_index=True, right_index=True)

        if len(df0) > 1:
            # b. Filters the max energy value within a minute
            #df0 = df0.resample('1t').max()
            pass
        else:
            return df0

        # --------old
        # df0['Date'] = [datetime(x.year, x.month, x.day, x.hour, x.minute) for x in df0.index]
        # df0 = df0.drop_duplicates(subset =['Date'], keep='first')
        # df0 = df0.groupby('Date').max()
        # df0.index.names = ['DateTime']
        # 3. Create dfDateTime over '1t'
        # load_data['timeStep'] = '1t'
        # dfDateTime = self.f_create_dfDatetime(load_data)
        # 4. Merge dataframe with dfDateTime
        # df0 = pd.merge(dfDateTime, df0, how='left', left_index=True, right_index=True)

        # c. Interpolate data
        df0.interpolate(limit=load_data['interpolate']['limit'],
                        limit_direction=load_data['interpolate']['direction'],
                        method='linear',
                        inplace=True,
                        )

        return df0 #.resample(timestep_).max()

    #
    # Reference DataFrame DateTime Index - dfDateTime
    #
    def f_create_dfDatetime(self, load_data):
        # Reference DataFrane DateTime Index
        # Timestep: load_data['timeStep']
        #   v1.0 2020-11-23
        #   v1.1 2020-11-25
        #   v1.2 2021-02-24
        #   v1.3 2022-07-12
        #   v1.4 2022-09-02
        #   v1.5 2022-09-05

        if load_data['timeStep'] == '0t':
            load_data['timeStep'] == load_data['samplingStep']

        dfDateTime = pd.DataFrame(data=pd.date_range(load_data['startDate'],
                                                     load_data['endDate'],
                                                     freq=load_data['timeStep']), columns=['DateTime'])
        dfDateTime = dfDateTime.set_index('DateTime')

        # if self.tZone != '':
        #    deltaTime = ((utctime_to_tZone(datetime.now(), self.tZone) - datetime.now()).seconds + 1) // 3600
        #    dfDateTime.index = dfDateTime.index.to_series().apply(lambda x: x + timedelta(hours=deltaTime))

        # Diff time in seconds
        dfDateTime['dTime_s'] = dfDateTime.index.to_series().diff().apply(lambda x: x.seconds)

        self.dfDateTime = dfDateTime

        return dfDateTime

    #
    # Add Time Measures
    #
    def f_reportAdd_TimeMeasures(self, df):
        # Adds Time Measures to the RAw Data Table
        # Measures, EnPeriod, Time [HH:xx], wP, Month, qH, Date '%Y-%m-%d %a'
        # v1.0 2021-02-24
        # v1.1 2022-07-07
        # v1.2 2022-09-02

        wD = {
            1: 'lun',
            2: 'mar',
            3: 'mer',
            4: 'gio',
            5: 'ven',
            6: 'sab',
            7: 'dom',
        }

        df['EnPeriod'] = [datetime_to_F123(x)[0] for x in df.index]
        df['Time'] = [datetime_to_F123(x)[2] for x in df.index]
        df['Time'] = df['Time'].apply(lambda x: datetime.strptime(x, "%H:%M"))
        #df['Time'] = df['Time'].apply(lambda x: '{:%H:%M}'.format(x))
        df['wP'] = [datetime_to_F123(x)[3] for x in df.index]
        df['Month'] = [str(x.year) + '/' + str(x.month) for x in df.index]
        df['hour'] = [x.hour for x in df.index]

        df['qH'] = [datetime_to_F123(x)[1] for x in df.index]
        df['qH'] = df['qH'].apply(lambda x: '{:02d}'.format(int(x)))

        df['Date'] = [datetime(x.year, x.month, x.day, 0, 0) for x in df.index]
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d') + ' ' + str(wD[x.isoweekday()]))
        #df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d %a'))

        return df


    def energy_dataframe(self, df0, load_data):
        # GENERATES formatted TableData for Machine Energy Report
        # ---  Machine Energy Report  -----------------
        # used in:  /views/see000/viewReportMachine.py
        #                       reportEnergyData()
        #  - df0  pivotTable  with 1 minute sample time
        #

        # v1.0 2022-11-18

        idDevice = load_data['idDev']

        f_sum = [
            idDevice + '_222',
            idDevice + '_226',
        ]
        f_sumd = [x + 'd' for x in f_sum]

        #Resample
        dfT1 = df0.resample('15t').max()

        # Add time related columns
        dfT1 = self.f_reportAdd_TimeMeasures(dfT1)
        # Format Time
        dfT1['Time'] = dfT1['Time'].apply(lambda x: '{:%H:%M}'.format(x))

        # W -> kW
        for x in load_data['idPars']:
            nf_ = idDevice + '_' + x
            dfT1[nf_] = dfT1[nf_].apply(lambda x: x * 0.001)

        # Energy tag
        dfT1['tag'] = dfT1['qH'] != dfT1['qH'].shift(-1)

        # Energy differences
        for x in range(len(f_sumd)):
            dfT1[f_sumd[x]] = dfT1[dfT1['tag']][f_sum[x]].diff().shift(0)

        # calcola fdp
        fdp_ = idDevice + '_135'
        fdp_act = idDevice + '_222d'
        fdp_react = idDevice + '_226d'
        #dfT1[fdp_] = dfT1[[fdp_act, fdp_react]].apply(lambda x: f_PF(x[0], x[1]))
        dfT1[fdp_] = dfT1[fdp_act] / (dfT1[fdp_act] ** 2 + dfT1[fdp_react] ** 2) ** 0.5

        return dfT1


    #
    # - - -  OLD  - - -
    #
    #
    # REPORT TABLE GENERATION
    #
    def f_reportAddMeasures_old(self, dfT1, data):
        # Adds Measures to the RAw Data Table
        # dfT1 index DateTime step 1t
        # Columns:
        #   222, 226
        # Calculates dft15 -
        # Both for Device and Machine Reports
        # v1.0 2020-07-07
        # v1.1 2021-02-24
        # OLD 2021-05-13

        f_sum = []

        # Measures, EnPeriod, Time [HH:xx], wP, Month, qH, Date '%Y-%m-%d %a'
        dfT1['EnPeriod'] = [datetime_to_F123(x)[0] for x in dfT1.index]
        dfT1['Time'] = [datetime_to_F123(x)[2] for x in dfT1.index]
        dfT1['wP'] = [datetime_to_F123(x)[3] for x in dfT1.index]
        dfT1['Month'] = [str(x.year) + '/' + str(x.month) for x in dfT1.index]
        dfT1['hour'] = [x.hour for x in dfT1.index]

        dfT1['qH'] = [datetime_to_F123(x)[1] for x in dfT1.index]
        dfT1['qH'] = dfT1['qH'].apply(lambda x: '{:02d}'.format(int(x)))

        # Date
        dfT1['Date'] = [datetime(x.year, x.month, x.day, 0, 0) for x in dfT1.index]
        dfT1['Date'] = dfT1['Date'].apply(lambda x: x.strftime('%Y-%m-%d %a'))

        # Measures @15t
        f_1 = ['Date', 'qH', 'Time']

        # Add Measures
        # @15t DataFrame
        f_m = ['EnPeriod', 'wP', 'Month', 'DateTime']

        if data['table'] == 'Prod':
            if 'idProd' in dfT1.columns:
                f_m += ['idProd']

        dfT15 = pd.DataFrame()
        dfT15[f_m] = dfT1.reset_index()[f_1 + f_m].groupby(f_1).first()

        idDev = data['idDev']

        #
        # Diff Values for Energy Devices
        #
        if data['table'] == 'Raw':
            # Sum
            if idDev + '_222' in dfT1.columns:
                f_sum = [
                    idDev + '_222',
                ]
            if idDev + '_226' in dfT1.columns:
                f_sum = [
                    idDev + '_226',
                ]
            if idDev + '_208' in dfT1.columns:
                f_sum += [idDev + '_208']

            dfT1['tags'] = dfT1['qH'] != dfT1['qH'].shift(1)
            dfT1.reset_index(inplace=True)
            dfT1.set_index(f_1, inplace=True)
            dfT15[f_sum] = dfT1[dfT1['tags']][f_sum].diff().shift(-1)
            for x in f_sum:
                dfT15.rename(columns={x: x + 'd15'}, inplace=True)

            # Power Demand
            par1 = idDev + '_133'
            par2 = idDev + '_134'

            if data['flag_GDM']:
                dfT15[par1] = dfT15[idDev + '_222d15'] * 4
                dfT15[par2] = dfT15[idDev + '_226d15'] * 4
            else:
                dfT15[par1] = dfT1.reset_index()[f_1 + [par1]].groupby(f_1).max()
                dfT15[par2] = dfT1.reset_index()[f_1 + [par2]].groupby(f_1).max()

        #
        # Diff Values for MAchine
        #
        if data['table'] == 'Prod':
            f_sum = []
            if idDev + '_202' in dfT1.columns:
                f_sum += [idDev + '_202']
            if idDev + '_203' in dfT1.columns:
                f_sum += [idDev + '_203']
            if idDev + '_204' in dfT1.columns:
                f_sum += [idDev + '_204']

            dfT1['tags'] = dfT1['qH'] != dfT1['qH'].shift(-1)
            dfT1.set_index(f_1, inplace=True)
            dfT15[f_sum] = dfT1[dfT1['tags']][f_sum].diff()
            for x in f_sum:
                dfT15.rename(columns={x: x + 'd15'}, inplace=True)

        return dfT1, dfT15

    def f_reportTable_old(self, dfT1, dfT15, data):
        #####
        #####  Calcolates the REPORT Table
        #####
        '''

        :param dfT1:
        :param dfT15:
        :param data:
            data['t_period']
            data['idDev']
            data['flag_GDM']
        :return:
        '''
        # Both Device and Machine Reports
        # v1.0 2020-07-13
        # OLD 2021-05-13

        table_ = pd.DataFrame()
        dfRep = pd.DataFrame()

        # Data
        t_period = data['t_period']
        idDev = data['idDev']
        flag_GDM = data['flag_GDM']

        # SETUP INDEX
        f_1 = []  # index parameters
        maxTformat = '{:%Y-%m-%d %H:%M}'

        if 'wP' in t_period:  # Working Period
            f_1 = ['Date', 'wP']
        if '15t' in t_period:
            f_1 = ['Date', 'qH', 'Time']
            maxTformat = '{:%H:%M}'
        if '1h' in t_period:
            # dfT15.reset_index(inplace=True)
            # dfT15['Time'] = dfT15['Time'].apply(lambda x: '{:02d}'.format(int(x[:-3])) + ':00')
            f_1 = ['Date', 'Time']
            maxTformat = '{:%H:%M}'
        if '1d' in t_period:
            f_1 = ['Date']
            maxTformat = '{:%H:%M}'
        if '1M' in t_period:
            f_1 = ['Month']
        if flag_GDM:
            f_1 += ['EnPeriod']

        #
        # DEVICE REPORT
        #
        if data['table'] == 'Raw':
            f_sum = [
                idDev + '_222d15',
                idDev + '_226d15',
            ]
            check_208 = False
            if idDev + '_208d15' in dfT15.columns:
                f_sum += [idDev + '_208d15']
                check_208 = True
            else:
                pass

            # Out at @1t
            if '1t' == t_period:
                f_sum = [
                    idDev + '_222',
                    idDev + '_226',
                ]
                # Max Values
                f_max = [idDev + '_133',
                         idDev + '_134']
                dfRep = dfT1
                dfRep[f_sum] = dfT1[f_sum].diff()
                dfRep[f_max] = dfT1[f_max]
                table_ = dfRep

                return table_, dfRep

            # Diff Values
            dfRep[f_sum] = dfT15.reset_index()[f_1 + f_sum].groupby(f_1).sum()

            # Add DateTime
            dfRep.reset_index(inplace=True)
            dfRep['DateTime'] = dfT15.reset_index()['DateTime']
            dfRep.set_index(f_1, inplace=True)

            # Add Energy Limit count
            if flag_GDM:
                f_sum += [idDev + '_222e15']
                try:
                    limit_1 = self.events_setParams(
                        {'command': 'read',
                         'idGroup': 'ev01',
                         'idParam': '04',
                         })
                    dfT15[idDev + '_222e15'] = dfT15[idDev + '_222d15'] >= float(limit_1[0][0]) * 1000
                except:
                    dfT15[idDev + '_222e15'] = NaN
                finally:
                    dfRep[idDev + '_222e15'] = dfT15.reset_index()[f_1 + [idDev + '_222e15']].groupby(f_1).sum()

            for x in f_sum:
                dfRep.rename(columns={x: x[:-2]}, inplace=True)

            # Max Values
            f_max = [idDev + '_133',
                     idDev + '_134']

            dfRep[f_max] = dfT15.reset_index()[f_1 + f_max].groupby(f_1).max()

            # Max Power value's Time
            for i in range(len(f_max)):
                # dfT2 = dfT1.reset_index().groupby(f_1)[f_max].idxmax()
                dfRep[f_max[i] + 'T'] = dfT1.reset_index()[f_1 + f_max]. \
                    groupby(f_1).apply(
                    lambda x: maxTformat.format(dfT1['DateTime'].iloc[x[f_max[i]].idxmax()])
                )

            # fdp
            fdp_ = idDev + '_135'
            fdp_act = idDev + '_222d'
            fdp_react = idDev + '_226d'
            dfRep[fdp_] = dfRep[fdp_act] / (dfRep[fdp_act] ** 2 + dfRep[fdp_react] ** 2) ** 0.5
            dfRep[fdp_] = dfRep[fdp_].apply(lambda x: '{:.2f}'.format(x))

            # Reformat data
            to_k = [idDev + '_222d',
                    idDev + '_226d',
                    idDev + '_133',
                    idDev + '_134',
                    ]

            for x in range(len(to_k)):
                dfRep[to_k[x]] = dfRep[to_k[x]].apply(lambda x: '{:.2f}'.format(x * 0.001))

            nok_data = ['inf', '-inf', 'nan', 'NaN', 'None', np.inf]
            dfRep = dfRep.replace(nok_data, NaN)

            # TAble COlumns
            set_cols = [
                idDev + '_222d',
                idDev + '_226d',
                idDev + '_133',
                idDev + '_134',
                idDev + '_135',
                idDev + '_133T',

            ]

            table_ = dfRep[set_cols].rename(columns=
            {
                idDev + '_133': 'Pmax[kW]',
                idDev + '_134': 'QMax[kVAr]',
                idDev + '_135': 'f.d.p.',
                idDev + '_222d': 'EnA[kWh]',
                idDev + '_226d': 'EnR[kVAr]',
                idDev + '_133T': 'PmaxTime',
            }
            )

            if flag_GDM:
                table_ = self.f_GDM_table(dfRep, f_1, idDev)

        #
        # MACHINE REPORT
        #
        if data['table'] == 'Prod':

            if data['table'] == 'Prod':
                if 'idProd' in dfT15.reset_index().columns:
                    f_1 += ['idProd']

            f_sum = []
            colRename = {}
            if idDev + '_202' in dfT1.columns:
                f_sum += [idDev + '_202d15']
                colRename[idDev + '_202d'] = 'ProdAct'
            if idDev + '_203' in dfT1.columns:
                f_sum += [idDev + '_203d15']
                colRename[idDev + '_203d'] = 'ProdMax'
            if idDev + '_204' in dfT1.columns:
                f_sum += [idDev + '_204d15']
                colRename[idDev + '_204d'] = 'ProdMin'

            # Diff Values
            dfRep[f_sum] = dfT15.reset_index()[f_1 + f_sum].groupby(f_1).sum()
            # Add DateTime
            dfRep.reset_index(inplace=True)
            dfRep['DateTime'] = dfT15.reset_index()['DateTime']
            dfRep.set_index(f_1, inplace=True)

            for x in f_sum:
                dfRep.rename(columns={x: x[:-2]}, inplace=True)

            # Reset at @1t
            if '1t' == t_period:
                f_sumd = [x + 'd' for x in f_sum]
                dfRep = dfT1
                dfRep[f_sumd] = dfT1[f_sum].diff()

            nok_data = ['inf', '-inf', 'nan', 'NaN', 'None', np.inf]
            dfRep = dfRep.replace(nok_data, NaN)

            table_ = dfRep
            if len(colRename) > 0:
                table_ = dfRep.rename(columns=colRename)

        return table_, dfRep

    def f_GDM_table_old(self, dfRep, f_1, idDev):
        # Generates pivot Table for GDM
        # v1.0 2020-07-11
        # OLD 2021-05-13

        fields_ = {
            idDev + '_222d': ['sum', 'EnA[kWh]'],
            idDev + '_133': ['max', 'Pmax[kW]'],
            idDev + '_135': ['sum', 'f.d.p.'],
            idDev + '_133T': ['max', 'PmaxTime'],
        }

        # fields - pivot function, fieldName

        '''
        #Count extra Limits
        limit_1 =[]
        try:
             limit_1 = c003.events_setParams(
                {'command': 'read',
                 'idGroup': 'ev01',
                 'idParam': '04',
                 })
        except:
            pass
        if  limit_1 ==[]:
            fields_[idDev + '_222e'] = ['sum', 'En>' + '--'+ '[kWh]']
        else:
            fields_[idDev + '_222e'] = ['sum', 'En>' + limit_1[0] + '[kWh]']
        '''

        agg_func_ = {x[0]: x[1][0] for x in fields_.items()}
        colName_ = {x[0]: x[1][1] for x in fields_.items()}

        df1 = pd.pivot_table(dfRep,
                             index=f_1[:-1],
                             columns='EnPeriod',
                             values=list(fields_.keys()),
                             aggfunc=agg_func_)  ###

        df1.drop(columns=[idDev + '_133T'], level=0, inplace=True)
        df1[idDev + '_133T'] = dfRep.reset_index().groupby(f_1[:-1])[idDev + '_133T'].max()

        # Reorder COlumns
        df1 = df1[[idDev + '_222d',
                   idDev + '_133',
                   idDev + '_135',
                   idDev + '_133T']]

        df1 = df1.rename(columns=colName_)
        df1 = df1.replace(['nan', 'Nan', np.nan, 'False'], NaN)

        # df1 = df1.replace(['nan', 'Nan', np.nan, 'False'], 0)
        # df1.reset_index(inplace=True)

        return df1

    def GDM_actPower_old(self, dataPack, TimeStamp, idDev, En_param, Pw_param):
        # Calculates GDM active power starting from 222 energy in seeLast Table
        # Adds the ActPower Value to the dataPack
        # v1.0 2020-04-02
        # v1.1 2020-05-28
        # v1.2 2002-07-02

        # idDev = 'd00'
        # En_param  = '222' #226
        # Pw_param  = '133'
        data_pack_ = [x for x in dataPack]
        actPower_ = -1

        for x in range(len(data_pack_)):
            if data_pack_[x][0]['idDevice'] == idDev:
                _En = [data_pack_[x][i]['Value'] for i in range(len(data_pack_[x]))
                       if data_pack_[x][i]['idParam'] == En_param
                       ]

                _Code = [data_pack_[x][i]['Code'] for i in range(len(data_pack_[x]))
                         if data_pack_[x][i]['idParam'] == En_param
                         ]

                # read seeLast Value and DateTime [utc]
                out_ = [[0, 0, 0]]
                code_ = err_code['calculation error']
                dEn_ = 0
                dTime_ = 0

                try:
                    out_ = self.dataDB_seeLast_read(idDev, En_param)
                    dTime_ = (TimeStamp - out_[0][1]).seconds / 3600  # [h]
                    if out_[0][2] == 0 and _Code[0] == 0:
                        dEn_ = (_En[0] - out_[0][0])  # [Wh]
                        actPower_ = dEn_ / dTime_
                        code_ = 0
                except:
                    pass

                for i in range(len(data_pack_[x])):
                    if data_pack_[x][i]['idParam'] == Pw_param:
                        data_pack_[x][i]['Value'] = actPower_
                        data_pack_[x][i]['Code'] = code_
                        push_log('[msg] d00_actPower - calculated the actual d00 Power [W]: ' + str(
                            actPower_) + ' code: ' + code_)

        return actPower_

class seeweb_plot(seedatadb):
    def __init__(self, configMysql, *args, **kwargs):
        super().__init__(configMysql, *args, **kwargs)

    def plot_vbar_stack(self, df0, pData):
        # Plots Vbar_stack data y, y1-y
        # v1.1 2020-06-24
        # v1.2 2020-07-03

        # df0.reset_index(pData['zParam'], inplace=True)
        dfP = df0[[pData['xParam'], pData['yParam'], pData['x1Param'], pData['y1Param']]]
        nok_data = ['inf', '-inf', 'nan', 'NaN', 'None', np.inf]
        dfP = dfP.replace(nok_data, np.nan)
        dfP = dfP.dropna()

        xParam = pData['xParam']
        x1Param = pData['x1Param']
        yParam = pData['yParam']
        y1Param = pData['y1Param']

        f_1 = [xParam, x1Param]
        f_sum = [yParam, y1Param]
        dfP_ = dfP[f_1 + f_sum].groupby(f_1).sum()

        x_range = list(dfP_.index)
        source = ColumnDataSource(data=dict(
            x_range=x_range,
            y_1=dfP_[f_sum[0]].values,
            y_2=dfP_[f_sum[1]].values - dfP_[f_sum[0]].values)  # max-actual
        )

        y_range = ['y_1', 'y_2']

        p = figure(x_range=FactorRange(*x_range),
                   toolbar_location=None,
                   tools=pData['toolsList'],
                   plot_width=pData['plot_width'],
                   plot_height=pData['plot_height'],
                   title=pData['plotTitle'],
                   x_axis_label=pData['x_axis_label'],
                   x_axis_type=pData['x_axis_type'],
                   y_axis_label=pData['y_axis_label'],
                   )

        p.xaxis.major_label_orientation = 0  # 3.14/4
        p.xaxis.visible = True
        p.xgrid.visible = False
        p.xaxis.major_label_text_font_size = "8pt"
        p.xaxis.major_label_text_font_style = "bold"
        p.xaxis.axis_label_text_font_style = "bold"
        p.xaxis.axis_label_standoff = 30
        p.xaxis.major_tick_out = 20
        p.xaxis.major_tick_line_color = 'white'
        p.toolbar.logo = None
        p.toolbar_location = None
        # X Axis
        x_axis_orientation = 0  # 3.14 / 4
        p.xaxis.major_label_orientation = x_axis_orientation

        p.vbar_stack(y_range, x='x_range', width=0.7, alpha=0.5, color=pData['y_axis_color'], source=source,
                     legend=f_sum)

        for x in [0]:
            labels = LabelSet(
                x='x_range',
                y=y_range[x],
                text=y_range[x],
                level='glyph',
                x_offset=pData['y_label_xoffset'],
                y_offset=pData['y_label_yoffset'],
                source=source, render_mode='canvas',
                text_font_size=pData['y_label_size'],
                text_font_style=pData['y_label_style'],
            )

        p.add_layout(labels)

        return p, dfP_

    def plot_vbar(self, dfP, pData):
        # vbar plot - vbar - y
        # x 2 levels indexed DataFrame
        # xparam != DateTime
        # v1.2 2020-06-26
        # v1.3 2020-07-02
        # v2.0 2020-07-07
        # v2.1 2021-01-26

        xParam = pData['xParam']
        yParam = pData['yParam']

        try:
            x1Param = pData['x1Param']
            f_1 = [xParam, x1Param]
        except:
            f_1 = [xParam]

        # group parameters
        f_sum = yParam

        # x groups
        # x_range = list(dfP.index)
        x_range = list(dfP[xParam])

        try:
            coulor = pData['x_group_coulor']
        except:
            coulor = ['blue', 'darkred', 'green', 'gold', 'black', 'brown', 'lightseagreen', 'olive', 'pink', 'gray']

        p = figure(x_range=FactorRange(*x_range),
                   toolbar_location=None,
                   tools=pData['toolsList'],
                   plot_width=pData['plot_width'],
                   plot_height=pData['plot_height'],
                   title=pData['plotTitle'],
                   x_axis_label=pData['x_axis_label'],
                   x_axis_type=pData['x_axis_type'],
                   y_axis_label=pData['y_axis_label'],
                   )

        p.xaxis.major_label_orientation = 3.14 / 4
        p.xaxis.visible = True
        p.xgrid.visible = False
        p.xaxis.major_label_text_font_size = "8pt"
        p.xaxis.major_label_text_font_style = "bold"
        p.xaxis.axis_label_text_font_style = "bold"
        p.xaxis.axis_label_standoff = 30
        p.xaxis.major_tick_out = 20
        p.xaxis.major_tick_line_color = 'white'
        # p.toolbar.logo = None
        # p.toolbar_location = None
        # X Axis
        x_axis_orientation = 0  # 3.14 / 4
        p.xaxis.major_label_orientation = x_axis_orientation

        y_label = yParam
        index_cmap = factor_cmap('_'.join(f_1),
                                 palette=coulor,
                                 factors=sorted(dfP.reset_index()[xParam].unique()), end=1)

        p.vbar(x='_'.join(f_1), top=yParam, width=0.9, alpha=0.5,
               source=dfP,
               # legend=y_label,
               fill_color=index_cmap,
               )

        source = ColumnDataSource(
            data=dict(
                x_range=x_range,
                y_1=dfP[f_sum].values,
            )
        )

        labels = LabelSet(
            x='x_range',
            y='y_1',
            text='y_1',
            level='glyph',
            x_offset=pData['y_label_xoffset'],
            y_offset=pData['y_label_yoffset'],
            source=source,
            render_mode='canvas',
            text_font_size=pData['y_label_size'],
            text_font_style=pData['y_label_style'],
        )

        p.add_layout(labels)
        script, div = components(p)
        return script, div, pData

    def plot_vbar_xy1(self, dfP_, pData):

        # vbar plot - vbar - y (ActPower)
        # 2020-06-26 v1.2
        # 2022-06-29 v1.3

        from bokeh.transform import factor_cmap
        from bokeh.models.tools import HoverTool

        # df0.reset_index(pData['zParam'], inplace=True)
        #dfP = df0  # [ [pData['xParam'], pData['yParam'], pData['x1Param'], pData['y1Param']] ]
        #nok_data = ['inf', '-inf', 'nan', 'NaN', 'None', np.inf]
        #dfP = dfP.replace(nok_data, np.nan)
        #dfP_ = dfP.dropna()

        xParam = pData['xParam']
        x1Param = pData['x1Param']
        yParam = pData['yParam']
        y1Param = pData['y1Param']

        f_1 = [xParam, x1Param]
        f_sum = yParam

        x_range = list(dfP_.index)
        # coulor = pData['y_axis_color']
        coulor = pData['group_colors']  # [:len(dfP_.reset_index()[xParam].unique())-1]
        p = figure(x_range=FactorRange(*x_range),
                   toolbar_location=None,
                   tools=pData['toolsList'],
                   plot_width=pData['plot_width'],
                   plot_height=pData['plot_height'],
                   title=pData['plotTitle'],
                   x_axis_label=pData['x_axis_label'],
                   x_axis_type=pData['x_axis_type'],
                   y_axis_label=pData['y_axis_label'],
                   )
        hover = p.select(dict(type=HoverTool))
        p.toolbar.logo = None
        # hover.formatters = {pData['xParam']: 'auto'}
        # xxF = '@' + pData['xParam'] + '{0,0.00}'
        yyF = '@' + pData['yParam'] + '{0,0.00}'
        y1F = '@' + pData['y1Param']
        hover.tooltips = [
            (pData['yParam'], yyF),
            (pData['y1Param'], y1F),
            # (pData['xParam'], xxF),
        ]
        hover.mode = 'mouse'

        p.xaxis.major_label_orientation = 0  # 3.14/4
        p.xaxis.visible = True
        p.xgrid.visible = False
        p.xaxis.major_label_text_font_size = "8pt"
        p.xaxis.major_label_text_font_style = "bold"
        p.xaxis.axis_label_text_font_style = "bold"
        p.xaxis.axis_label_standoff = 30
        p.xaxis.major_tick_out = 20
        p.xaxis.major_tick_line_color = 'white'
        p.toolbar.logo = None
        p.toolbar_location = None
        # X Axis
        x_axis_orientation = 0  # 3.14 / 4
        p.xaxis.major_label_orientation = x_axis_orientation

        y_label = ''
        index_cmap = factor_cmap('_'.join(f_1),
                                 palette=coulor,
                                 factors=sorted(dfP_.reset_index()[xParam].unique()), end=1)

        p.vbar(x='_'.join(f_1), top=yParam, width=0.9, alpha=0.9,
               source=dfP_,
               legend=y_label,
               fill_color=index_cmap,
               )  # , legend_labels=vBars_)

        source = ColumnDataSource(
            data=dict(
                x_range=x_range,
                y_1=dfP_[f_sum].values, )
        )

        labels = LabelSet(
            x='x_range',
            y='y_1',
            text='y_1',
            level='glyph',
            x_offset=pData['y_label_xoffset'],
            y_offset=pData['y_label_yoffset'],
            source=source,
            render_mode='canvas',
            text_font_size=pData['y_label_size'],
            text_font_style=pData['y_label_style'],
        )

        p.add_layout(labels)
        script, div = components(p)

        return script, div, pData


    def plot_scatter(self, df, pData):
        # scatter plot - xy
        # v1.3 2020-07-02
        # v1.4 2020-07-05
        # v1.5 2021-02-24
        # v1.6 2021-04-12

        p = figure(
            tools=pData['toolsList'],
            plot_width=pData['plot_width'],
            plot_height=pData['plot_height'],
            title=pData['plotTitle'],
            x_axis_label=pData['x_axis_label'],
            x_axis_type=pData['x_axis_type'],
            y_axis_label=pData['y_axis_label'],
        )

        hover = p.select(dict(type=HoverTool))
        p.toolbar.logo = None

        #
        # X Axis
        #
        x_axis_orientation = 3.14 / 4
        p.xaxis.major_label_orientation = x_axis_orientation

        if 'Date' in pData['xParam']:
            p.xaxis.formatter = DatetimeTickFormatter(
                hours=["%d %B %Y - %H:%M"],
                days=["%d %B %Y - %H:%M"],
                months=["%d %B %Y"],
                years=["%d %B %Y"],
            )
            hover.formatters = {'@' + pData['xParam']: 'datetime'}  # default: 'numeral',
            xxF = '@' + pData['xParam'] + '{%F %T}'

        else:
            hover.formatters = {'@' + pData['xParam']: 'numeral'}  # opzioni: 'numeral', 'datetime', 'printf'
            xxF = '@' + pData['xParam'] + '{0,0.00}'
            try:
                df[pData['xParam']] = df[pData['xParam']].apply(lambda x: float(x))
            except:
                pass

        # Y RANGE
        p.left[0].formatter.use_scientific = False

        # HOVER
        yyF = '@' + pData['yParam'] + '{0,0.00}'
        hover.tooltips = [
            (pData['yParam'], yyF),
            (pData['xParam'], xxF),
        ]
        hover.mode = 'mouse'

        # Option Report "Energy Hourly". Add Date to Hover
        color_ = 'blue'
        if 'Hourly' in pData['plotTitle']:
            _data = '@' + 'Date'
            hover.tooltips.append(('Date', _data))

            from bokeh.palettes import Magma, Inferno, Plasma, Viridis
            n_ = int(256 / len(df['Date'].unique().tolist()))
            list_colors = {y: Viridis[256][x * n_] for x, y in enumerate(df['Date'].unique().tolist())}
            df['DateColors'] = df['Date'].apply(lambda x: list_colors[x])
            color_ = 'DateColors'

        # Plot
        if pData['type'] == 'vbar':
            p.vbar(x=pData['xParam'], top=pData['yParam'], width=2, alpha=1,
                   source=df,
                   )

        elif pData['type'] == 'points':
            p.scatter(pData['xParam'],
                      pData['yParam'],
                      size=4, alpha=1,
                      source=df,
                      color=color_,
                      )

        elif pData['type'] == 'line':
            p.line(pData['xParam'], pData['yParam'], color='blue', source=df)
            p.circle(pData['xParam'], pData['yParam'], size=pData['y_circle_size'], color='blue', source=df)

        if pData['regLine_abil']:
            try:
                dfregLine, strReg = self.plot_regLine_data(df, pData['xParam'], pData['yParam'])
                p.line(pData['xParam'], 'regLine', color='red', source=dfregLine)
                p.circle(pData['xParam'], 'regLine', size=3, color='red', source=dfregLine)
                rLabel_ = Label(x=min(dfregLine[pData['xParam']]),
                                y=0.9 * max(dfregLine[pData['yParam']]),
                                text=strReg)
                p.add_layout(rLabel_)
                pData['strReg'] = strReg
            except:
                pData['strReg'] = 'Wrong data to build regression line'

        script, div = components(p)
        pData['p'] = p

        return script, div, pData

    def plot_regLine_data(self, df, xParam, yParam):
        # Generates the regression line
        # v1.1 2020-07-03

        import statsmodels.formula.api as smf
        results = smf.ols(formula=yParam + ' ~ ' + xParam, data=df).fit()
        regParms = results.params
        rSqr = results.rsquared
        strReg = ' y=m*x+n  ->  m=' + '{:.3e}'.format(regParms[1]) + ' ;  n= ' + '{:.3e}'.format(
            regParms[0]) + ' ;    ro= ' + '{:.3f}'.format(rSqr)
        # df5 = df5.dropna(subset=[xParam])
        df['regLine'] = results.predict(df[xParam])

        return df, strReg

    def plotHist_seeLast_Param(self, idParam):
        # Generates histogram of the selected Parameter from Last Table
        # v1.0 2020-07-02

        # Reads idPAram Values
        sql_ = "Select Date, idDevice, idParam, Value from " \
               "{0}.{1}  where Code =0' and idParam = '{2}'; ". \
            format(
            self.configMysql['database'],
            self.configMysql['table'] + 'Last',
            idParam
        )

        db_, _ = seedatadb.exec_sql1(self, sql_, True)
        df_ = pd.DataFrame(data=db_,
                           columns=['DateTime', 'idDevice', 'idParam', 'Value'],
                           )

        # Parameter Description
        idDevDescr = idParam
        idParDescr = ''
        idParUm = ''
        try:
            sql_ = "Select descrENG, um from {0}.{1}  where Code =0 and idParam = '{2}'; ". \
                format(self.configMysql['database'], self.configMysql['table'] + 'Params', idParam)
            if self.configMysql['language'] == 'ITA':
                sql_.replace('descrENG', 'descrITA')

            db_, _ = seedatadb.exec_sql1(self, sql_, True)
            idParDescr = db_[0][0]
            idParUm = db_[0][1]
            idDevDescr = idParam + '_' + idParDescr
        except:
            pass
        df_['idParDescr'] = idParDescr

        # Adapt DateTime to timezone
        if self.configMysql['tZone'] != '':
            df_['DateTime'] = df_['DateTime'].apply(lambda x: utctime_to_tZone(x, self.configMysql['tZone']))
        date_ = df_['DateTime'][1]

        # Data from see000Join Table Device -> rep -> machine
        sql_ = "Select idDevice, idMac, idDep, idMacDescr from {0}.{1}  where Code =0 and idParam = '{2}'; ". \
            format(
            self.configMysql['database'],
            self.configMysql['table'] + 'Join',
            idParam)

        db1_, _ = seedatadb.exec_sql1(self, sql_, True)
        db1_ = pd.DataFrame(data=db1_,
                            columns=[
                                'idDevice',
                                'idMac',
                                'idDep',
                                'idMacDescr']
                            )
        # Merge
        dfP = pd.merge(df_, db1_, how='left', on='idDevice')

        # Group idDep and idDev
        f_1 = ['idDep', 'idDevice']
        f_sum = ['Value']
        dfP = dfP[f_1 + f_sum].groupby(f_1).sum()

        if idParam in ['133', '134']:
            dfP[f_sum] = ['{:.2f}'.format(x * 0.001) for x in dfP[f_sum]]
            idParUm = 'k' + idParUm

        #
        #  ------------- PLOT -----------------------------
        #

        xParam = 'idDep'
        x1Param = 'idDevice'
        yParam = 'Value'

        # Plot Setup
        plotTitle = 'PLOT Actual Parameter: ' + idDevDescr + '  - DateTime: ' + '{:%d/%m/%Y %a  %H:%M}'.format(date_)

        pData = {
            # Setup Plot
            'toolsList': '',  # 'pan,box_zoom,wheel_zoom,hover,reset,save,  # box_select,lasso_select
            'plot_width': 1100,
            'plot_height': 800,
            'plotTitle': plotTitle,

            # xaxis
            'xParam': xParam,
            'x1Param': x1Param,
            'x_axis_label': '',
            'x_axis_type': 'auto',

            # yaxis
            'yParam': yParam,
            'y1Param': '',
            'y_axis_label': yParam + ' ' + idParUm,
            'y_label_size': '0.8em',
            'y_label_style': 'normal',
            'y_label_xoffset': -10,
            'y_label_yoffset': 5,
            'y_axis_color': 'blue',

            # Group
            # https://docs.bokeh.org/en/latest/docs/reference/colors.html
            'group_colors': ['blue', 'darkred', 'green', 'gold', 'black', 'brown', 'lightseagreen', 'olive', 'pink',
                             'gray']
        }

        p, _ = self.plot_vbar(dfP, pData)
        script, div = components(p)

        return script, div, dfP

    def plot_pie(self, dfP, pData):
        # pie chart
        # v1.0 2020-07-15
        # https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=p%20wedge#bokeh.plotting.figure.Figure.wedge
        # https://stackoverflow.com/questions/53892890/adding-labels-in-pie-chart-wedge-in-bokeh
        #

        from math import pi, cos, sin

        # toolstips_ = "@idMac: @pu"
        toolstips_ = '@' + pData['xDevParam'] + ': @' + pData['xParam']

        p = figure(plot_height=pData['plot_height'],
                   title=pData['plotTitle'],
                   toolbar_location=None,
                   tools=pData['toolsList'],
                   tooltips=toolstips_)

        # Bokeh pie parameters
        param_Angle = 'pu'
        radius = 0.5
        dfP['angle'] = dfP[param_Angle] / dfP[param_Angle].sum() * (2 * pi)

        xyRadius = 200

        dfP['angleCum'] = dfP['angle'].cumsum()
        dfP['anglexy'] = dfP['angleCum']

        for x in range(len(dfP) - 1):
            dfP['anglexy'].iloc[x] = dfP['angleCum'].iloc[x] - (
                    dfP['angleCum'].iloc[x + 1] - dfP['angleCum'].iloc[x]) / 2.0

        dfP['xPos'] = dfP['anglexy'].apply(lambda x: cos(x) * xyRadius)
        dfP['yPos'] = dfP['anglexy'].apply(lambda x: sin(x) * xyRadius)

        dfP['color'] = Category20c[len(dfP)]
        dfP['x_'] = 0
        dfP['y_'] = 1
        dfP['radius'] = radius
        dfP['vLabels'] = dfP['pu'].apply(lambda x: '{:2.2%}'.format(x))
        dfP['vLabels'] = dfP['idMac'] + '-' + dfP['vLabels']
        ##dfP["vLabels"] = dfP["vLabels"].str.ljust(2)

        p.wedge(x='x_', y='y_', radius='radius',
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white",
                fill_color='color',
                legend='vLabels',
                source=dfP)

        # wWedge Labels
        source = ColumnDataSource(dfP)
        labels = LabelSet(x='x_', y='y_',
                          text='vLabels',
                          # level='glyph',
                          # angle='angleCum',
                          source=source,
                          render_mode='canvas',
                          x_offset='xPos',
                          y_offset='yPos',
                          text_font_size='0.7em',  # pData['y_label_size'],
                          text_font_style=pData['y_label_style'],
                          )

        # p.add_layout(labels)
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        script, div = components(p)
        return script, div

    def plot_heat(self, df0, pData):
        ########   PLOT HEAT MAP  #################
        # v1.0 2021-04-12
        # v1.1 2022-11-20

        from bokeh.io import output_file, show
        from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                                  LinearColorMapper, PrintfTickFormatter, FixedTicker)
        from bokeh.plotting import figure
        from bokeh.sampledata.unemployment1948 import data
        from bokeh.transform import transform
        from bokeh.palettes import Magma, Inferno, Plasma, Viridis, Category20b

        yParam = pData['yParam']
        df0_p = df0.reset_index()[['hour', 'Date', yParam]]
        #df0_p[yParam] = df0_p[yParam].apply(lambda x:x*0.001)
        data.columns.name = 'Day'

        source = ColumnDataSource(df0_p)

        colors = Plasma[
            10]  # ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
        mapper = LinearColorMapper(palette=colors, low=df0_p[yParam].min(), high=df0_p[yParam].max())

        x_list = list(sorted(df0_p['hour'].unique()))
        x_ = list(map(str, x_list))
        y_ = list(reversed(df0_p['Date'].unique()))

        p = figure(
            tools=pData['toolsList'],
            plot_width=pData['plot_width'],
            plot_height=pData['plot_height'],
            title=pData['plotTitle'],
            x_axis_label=pData['x_axis_label'],
            x_axis_type=pData['x_axis_type'],
            x_axis_location="above",
            y_axis_label=pData['y_axis_label'],
            x_range=x_,
            y_range=y_,
        )

        p.rect(x="hour", y="Date", width=1, height=1, source=source,
               line_color=None, fill_color=transform(yParam, mapper))

        color_bar = ColorBar(color_mapper=mapper,
                             ticker=BasicTicker(desired_num_ticks=len(colors)),
                             formatter=PrintfTickFormatter(format="               %f.0 "))

        p.add_layout(color_bar, 'right')

        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "8px"
        p.axis.major_label_standoff = 0

        p.xaxis.ticker = FixedTicker(ticks=x_list)

        script, div = components(p)
        pData['p'] = p

        return script, div, pData

    def plot_mscatter(self, df, pData):
        # Multi scatter plot - xy - max=10
        # v1.0 2021-05-20

        p = figure(
            tools=pData['toolsList'],
            plot_width=pData['plot_width'],
            plot_height=pData['plot_height'],
            title=pData['plotTitle'],
            x_axis_label=pData['x_axis_label'],
            x_axis_type=pData['x_axis_type'],
            y_axis_label=pData['y_axis_label'],
        )

        hover = p.select(dict(type=HoverTool))
        p.toolbar.logo = None
        colors_ = ['black', 'red', 'blue', 'green', 'pink',
                   'brown', 'yellow', 'grey', 'navy', 'olive',
                   'navy', 'chocolate', 'greenyellow', 'darkmagenta', 'darkgrey',
                   'darkgreen', 'darkkahaki', 'darkmagenta', 'darkolivegreen', 'darkorange'] * 5

        #
        # X Axis
        #
        x_axis_orientation = 3.14 / 4
        p.xaxis.major_label_orientation = x_axis_orientation

        if 'Date' in pData['xParam']:
            p.xaxis.formatter = DatetimeTickFormatter(
                hours=["%d %B %Y - %H:%M"],
                days=["%d %B %Y - %H:%M"],
                months=["%d %B %Y"],
                years=["%d %B %Y"],
            )
            hover.formatters = {'@' + pData['xParam']: 'datetime'}  # default: 'numeral',
            xxF = '@' + pData['xParam'] + '{%F %T}'

        else:
            hover.formatters = {'@' + pData['xParam']: 'numeral'}  # opzioni: 'numeral', 'datetime', 'printf'
            xxF = '@' + pData['xParam'] + '{0,0.00}'
            try:
                df[pData['xParam']] = df[pData['xParam']].apply(lambda x: float(x))
            except:
                pass

        # Y RANGE
        p.left[0].formatter.use_scientific = False

        # HOVER
        yyF = []
        htool = []

        for i, x in enumerate(pData['yParam']):
            yyF.append('@' + x + '{0,0.00}')
            htool.append((x, yyF[i]))

        htool.append((pData['xParam'], xxF))
        hover.tooltips = htool
        hover.mode = 'mouse'

        # Option Report "Energy Hourly". Add Date to Hover

        # Plot
        if pData['type'] == 'vbar':
            for i in pData['yParam']:
                p.vbar(x=pData['xParam'], top=pData['yParam'][i], width=2, alpha=1,
                       source=df, color=colors_[i],
                       )

        elif pData['type'] == 'points':
            for i in pData['yParam']:
                p.scatter(pData['xParam'],
                          pData['yParam'][i],
                          size=4, alpha=1,
                          source=df,
                          color=colors_[i],
                          )

        elif pData['type'] == 'line':

            for i, x in enumerate(pData['yParam']):
                p.line(pData['xParam'], x, color=colors_[i], source=df, legend=x + ' ')
                p.circle(pData['xParam'], x, size=pData['y_circle_size'], color=colors_[i], source=df, legend=x + ' ')
                # p.line(df.reset_index()[pData['xParam']], df[x], color=colors_[i],  legend = x)
                # p.circle(df.reset_index()[pData['xParam']], df[x], size=pData['y_circle_size'], color=colors_[i],legend = x)

        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
        script, div = components(p)
        pData['p'] = p

        return script, div, pData

class see_ADMIN():
    # APP ADMIN
    # Class to check servers connections
    # v1.0 2021-02-21

    def __init__(self, idServers_pack):
        self.idServers_pack = idServers_pack
        self.port = self.idServers_pack['port']
        self.timeout = self.idServers_pack['timeout']
        self.hostname = self.idServers_pack['ipAddr']
        self.idDevice = self.idServers_pack['idServer']

        self.Code = 0
        self.idParam_conn = params_id['dev_connection']
        # check valid ip code or dns address
        if not validate_ip(self.hostname):
            try:
                self.hostname = socket.gethostbyname(self.hostname)
            except:
                self.Code = err_code['err_connection']

    # ADMIN WEB SERVICES
    def read_server(self, TimeNow):
        # Routine tests if the server is alive
        # v1.3 2018-08-17
        # v2.0 2021-02-21

        Time1 = time.time_ns()
        idStatus = internet_ip(self.hostname, self.port, self.timeout)

        # timediff = '{0:.2f}'.format(float(str(Time2-Time1).split(':')[2])*1000)
        timedelay = (time.time_ns() - Time1) * 10 ** -6
        stringa = ('-> %s server %s, %s:%s [%s] dtime = %s ms' % (
            TimeNow, self.idServers_pack['idServer'], self.hostname, self.port, str(idStatus), str(timedelay)))

        # pack_data
        pack_data = Dict_Generate(
            idDevice=self.idDevice,
            idParam=self.idParam_conn,
            TimeStamp='{:%Y-%m-%d %H:%M:%S}'.format(TimeNow),
            Value=int(idStatus),
            Delay=timedelay,
            Code=self.Code,
        )
        return pack_data, stringa

    def check_server(self, config_mysql, config_check):
        # v1.0 - 2018-07-29
        # controlla da quanto tempo un server è Ok - default= 1 periodi di sample
        # v2.0 2020-07-03
        # v3.0 2021-02-23

        c000 = seedatadb(config_mysql)
        offset = str((config_check['samples'] + 1) * config_check['sampleTime']) + 's'

        try:
            dbLast = c000.dataDB_seeLast_read(self.idDevice, self.idParam_conn)
        except:
            dbLast = {}
        return dbLast

    def check_db(self, config_mysql, dbList):
        # v3.0 - 2019-01-13
        # controlla da quanto tempo è stato letto l'ultimo dato nel db
        # v3.1 2020-07-04

        c000 = seedatadb(config_mysql)

        offset = str(10 * dbList['sampleTime']) + 's'
        # timeEnd     = pd.Timestamp(datetime.utcnow())
        # timeBegin    = pd.Timestamp(timeEnd) - pd.Timedelta(offset)
        dbTable = config_mysql['database'] + '.' + config_mysql['table']
        sql = "SELECT MAX(Date) as MaxDate FROM " + dbTable  # + " where "
        # sql+= "Date between '" + str(timeBegin) + "' and '" + str(timeEnd) + "'" #and
        sql += " ;"

        qs, _ = c000.exec_sql1(sql, _bresult=True)

        if not qs:
            push_log('- msg_q1: from %s no query result' % (dbTable))
            return pd.Timedelta(offset)

        if qs[0][0] is None:
            # print('qs: ....', qs)
            push_log('- msg_q2: from %s no query result' % (dbTable))
            return pd.Timedelta(offset)

        else:
            # print('qs: ....', qs)
            df = pd.DataFrame.from_records(qs)
            return (pd.Timestamp(datetime.utcnow()) - df.iloc[0, 0])


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def send_email(config_email, sbj, msg):
    # v1.0 2018-07-29
    # Send email to address specified in config_email
    import smtplib

    # server
    if config_email['server']:
        server = smtplib.SMTP(config_email['server'])
    else:
        server = smtplib.SMTP('smtp.gmail.com:587')

    server.timeout = 1
    server.starttls()

    # Next, log in to the server
    server.login(config_email['from_username'], config_email['from_psw'])
    msg_ = 'Subject: {}\n\n{}'.format(sbj, msg)
    # print('sending email - deltatime:%s - messaggio: %s' % (deltaTime, msg_))
    server.sendmail(config_email['from_username'], config_email['to_username'], msg_)
    server.quit()

def push_csv1(df,  sep, filename):
    # Creates csv file
    # v2.2 2018-09-18
    # v3.0 2022-11-21

    from django.http import HttpResponse
    import csv

    if isinstance(df, pd.DataFrame):
        if df.size > 0:
            df=df.apply(lambda x: x.astype(str).str.replace('.', sep, regex=True))
            qset = [list(df.columns)]
            qset += [(df.iloc[x, :]) for x in range(len(df))]
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename=' + filename
            response['Content-Type'] = 'text/csv'
            writer = csv.writer(response, delimiter=';')
            for row in qset:
                writer.writerow(row)
            return response
    else:
        pass


#
# WEB REPORTS Functions
# Machine Energy
# GDM Energu
# 2022

def f_PF(a,r):
    #calculates PF
    #v1.0 2022-11-18
    fdp_=-1
    try:
        fdp_ = a/(a**2 + r**2)**0.5
    except:
        pass

    if fdp_!=fdp_:
        fdp_= 0

    return fdp_

def load_ConfigFile(request):
    # Import config file module
    # v1.0 2020-10-25
    # v1.1 2022-06-14
    # v1.2 2022-10-19 deleted
    # v1.3 2022-11-20

    username_, group_ = seeweb.username(request)
    cfig = ''
    template = 'seeSRV/error_page.html/'
    context = {
        'text1': f"[msg2] - User's app has not been defined.",
        'text2': f"{username_} - Group: {group_}"
    }

    if group_:
        try:
            module_name = 'seeSRV.py.config_' + group_
            cfig = importlib.import_module(module_name)
        except:
            pass

    return cfig, template, context


# Report ACTUAL


def f_dfDev_diff(df0, config_repAct):
    # Report Actual
    # Given the set of idDevices and the OverAll Device
    # Calculates difference OverAll - set
    # v1.0 2020-07-15
    # v1.1 2022-08-29

    fields_ = config_repAct['fields']
    idMainDev =config_repAct['idGDM']
    idSetDevs =config_repAct['virtual_Machine_1']

    data = {
                'idDevice': config_repAct['idDevice'],
                'idM': config_repAct['idM'],
                'MachDescr': config_repAct['MachDescr'],
                'idDep': config_repAct['idDep'],
               }

    df0 = df0[fields_]

    # Extracts the idMainDev Energy
    idMainValue = df0[df0['idDevice'] == idMainDev]['Value'].sum()

    # Calculates the totale Value of  idSetDevs
    dfCab = df0[fields_][df0['idDevice'].isin(idSetDevs)]


    # Calculates the diff
    data['Value'] = idMainValue - dfCab['Value'].sum()

    # Add the record 'diffDev'
    setDiff = [data]

    df0 = pd.concat([df0, pd.DataFrame(setDiff)]) #, axis=1, join='inner')
    # Calculates Percentages

    try:
        df0['pu'] = df0['Value'] / idMainValue
        df0['perc'] = df0['pu'].apply(lambda x: '{:.2%}'.format(x))
    except:
        df0['pu']=None
        df0['perc']= None
    return df0

