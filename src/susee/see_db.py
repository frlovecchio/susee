# -*- coding: utf-8 -*-
##############################
##### DATABASE Functions  ####
##############################
# Studio Tecnico Pugliautomazione - Monopoli (BA)
# Copyright (c)
# v2.0 2020-07-03
# v2.1 2020-07-22
# v2.2 2020-09-19
# v2.3 2020-12-27
# v2.4 2020-12-27 fixed exec_sql1
# v2.5 2021-02-15
# v2.6 2021-02-22
# v2.6 2021-02-23 fixed seeAdmin
# v2.7 2021-02-28
# v2.8 2021-05-04
# v3.0 2021-05-12  Table_read
# v3.1 2021-05-15
# v3.2 2021-05-17
# v3.3 2021-06-08
# v3.4 2021-07-05
# v3.5 2022-02-01
# v3.6 2022-02-14
# v3.7 2022-06-04  dataDB_seeLast_Read()
# v3.8 2022-01-07
# v3.9 2022-07-06   drop duplicated
# v3.91 2022-07-10   drop duplicated
# v3.92 2022-08-17
# v3.93 2022-08-18
# v3.94 2022-08-29
# v3.95 2022-10-12
# v4.0  2022-10-12
# v4.1  2022-11-15
# v4.2  2022-11-16
# v4.3  2022-11-17
# v4.4  2022-11-23
# v4.5  2022-11-25
# v4.5  2022-11-26  class db_table, db tableSys
# v4.6  2022-11-30  db_table -> create new year tables
# v5.0  2023-01-02  corretta creazione nuove tabelle
# v5.1  2023-01-03
# v5.2  2023-05-06
# v5.3  2024-01-05

from datetime import datetime, timedelta
import mysql.connector
import os
import pandas as pd

from susee.see_comm import internet_ip
from susee.see_dict import message_strings, err_code
from susee.see_functions import time_utc, push_log, utctime_to_tZone, tZone_to_utctime, time_local

class seedatadb:
    #
    # Connection to Database management
    #

    def __init__(self, configMysql, *args, **kwargs):
        self.configMysql = configMysql

        # Write array
        self.array_sql = []

        # self.tempdf = pd.DataFrame()  #used to temp store df for .csv file
        # self.dfDevPar = pd.DataFrame()  # used to temp store df for SysRawData

        # check socket if available. 1=ok, -1=none
        self.db_connect = internet_ip()

    # Tools
    def exec_sql1(self, sql: str, _bresult: bool):
        # _bresult : flag used to specify if the functions output data from db
        #  2019-10-31  - version with always two outputs used only in svuota_file_array()
        #              - exec_sql() deleted
        # v2.0 2020-08-04 - fixed bugs
        # v2.1 2020-12-02 - declared out_sql
        # v2.2 2020-12-03 - flag output
        # v2.3 2021-02-02 - timeout
        # v2.4 2022-02-01 - minors
        # v2.5 2022-08-19
        # v2.6 2022-10-09

        config_mysql = self.configMysql

        flag_db = False
        out_sql = []

        # Timeout [s] - Connetion to the DB
        try:
            msT_ = config_mysql['maxConnectTime']
        except:
            msT_ = 1000

        #print(f' > AAA [msg] - Database connection timeout: {msT_} [s]')

        # SQL timeout
        # sql = "SET STATEMENT max_statement_time=" + str(msT_) + ' for ' + sql

        try:
            cnx = mysql.connector.connect(user=config_mysql['user'],
                                          passwd=config_mysql['passwd'],
                                          host=config_mysql['host'],
                                          port=config_mysql['port'],
                                          database=config_mysql['database'],
                                          connect_timeout=msT_,
                                          auth_plugin='mysql_native_password',
                                          )
            cursor = cnx.cursor()
            cursor.execute(sql)
            flag_db = True

        except mysql.connector.Error as err:
            push_log('exec_sql1() - ' + message_strings[9] + '\n err: ' + str(
                err) + '\n sql: ' + sql)  # 'msg_09 - Database MYSQL non accessibile.'
            print('> exeq_sql1() -  DataBase Error: ', err)
            # print('> exeq_sql1() -  sql: ', sql)
            return flag_db, str(err)

        if _bresult == False:
            cnx.commit()
            cnx.close()
            cursor.close()
            return flag_db, '0'
        else:
            out_sql = cursor.fetchall()
            cnx.close()
            cursor.close()
            return out_sql, '0'

    #
    # TABLE seeLast MANAGEMENT
    #
    def dataDB_seeLast_Clear(self, tableName):
        # Delete the last sampled data in the table see000Last
        # v2.0
        # 2020-03-21
        # rename the default tableName
        # v2.1 2020-07-02
        # v2.2 2022-02-01
        # v2.3 2022-07-10           tableName

        sql = 'DELETE  FROM %s where idNum>0' % (tableName)

        if self.db_connect:
            flag_db, _ = self.exec_sql1(sql, False)
            return flag_db
        else:
            str_ = 'dataDelete_Last() - no web connection'
            push_log(str_)
            return 0

    def dataDB_seeLast_write(self, dataPack, tableName , flag_tZone=False or None, ):
        # Store data in the seeLast Table
        # v1.1 2020-04-02 - do not activate flag_tzone!
        # v1.2 2020-07-02
        # v1.3 2021-01-06
        # v1.4 2022-07-10  tableName


        dataPack_ = dataPack
        # Clear Table
        self.dataDB_seeLast_Clear(tableName)

        # Local config table
        # TimeZone
        if flag_tZone:
            tZone = self.configMysql['tZone']  # timezone utctime_to_tZone(date_[0], self.configMysql['tZone'] )
            if tZone != '':
                for xx in range(len(dataPack_)):
                    for ii in range(len(dataPack_[xx])):
                        date_ = [y for x, y in dataPack_[xx][ii].items() if x == 'Date']
                        dataPack_[xx][ii]['Date'] = utctime_to_tZone(date_[0], tZone)

        return self.data_store_pack(dataPack_, tableName) #self.configMysql['tableLast'])

    def dataDB_seeLast_read(self, idDevice, idParam, tableName):
        # Reads actual data from
        # v2.0 2020-07-07
        # v2.1 2022-02-01
        # v2.2 2022-02-14
        # v2.3 2022-06-04
        # v2.4 2022-08-29

        load_data={}
        load_data['idDev'] = idDevice
        load_data['idPars'] = idParam

        list_idDevs = tuple(load_data['idDev']) if isinstance(load_data['idDev'], list) else "('" + load_data[
            'idDev'] + "')"
        list_idParams = tuple(load_data['idPars']) if isinstance(load_data['idPars'], list) else "('" + load_data[
            'idPars'] + "')"


        sql_ = "select date, idDevice, idParam, value,  Code, Delay  " \
               "from {0}.{1}  where idDevice in {2} and idParam in {3}; ".format(
            self.configMysql['database'],
            tableName,
            list_idDevs,
            list_idParams)

        db_1 = pd.DataFrame([0])

        if idDevice == 'All':
            sql_ = "select date, idDevice, idParam, value,  Code, Delay  from {0}.{1}  where idParam in {2};".format(
                self.configMysql['database'],
                tableName,
                list_idParams)

        if idParam == 'All':
            sql_ = "select date, idDevice, idParam, value,  Code, Delay  from {0}.{1} where idDevice in {2};".format(
                self.configMysql['database'],
                tableName,
                list_idDevs,
            )

        if idParam == 'All' and idDevice == 'All':
            sql_ = "select date, idDevice, idParam, value,  Code, Delay  from {0}.{1} ; ".format(
                self.configMysql['database'],
                tableName,
            )

        if self.db_connect:
            out_, _ = self.exec_sql1(sql_, True)  # format [(par1, par2,...)]
            db_1 = pd.DataFrame(data=out_,
                                columns=['DateTime', 'idDevice', 'idParam', 'Value', 'Code', 'Delay'],
                                )
        else:
            str_ = '[msg] dataDB_seeLast_read() - no web connection'
            push_log(str_)

        return db_1

    #
    # Generic Table read/write
    #
    def dataDB_Table_read(self, tableName):
        # Reads  all data from a generic table  and creates a Dataframe
        # v1.1 2021-05-12
        # v1.2 2022-02-01
        # v1.3 2022-08-18
        # v1.4 2022-11-19

        err = ''
        df = pd.DataFrame()

        # Reads Data from the table
        sql_ = 'select * from {0}.{1}'.format(self.configMysql['database'], tableName)
        sql_ = sql_.replace("'", '')
        try:
            data_, err = self.exec_sql1(sql_, True)
        except:
            return [], err

        # Reads Column names from the table
        sql_ = 'show columns from {0}.{1}'.format(self.configMysql['database'], tableName)
        sql_ = sql_.replace("'", '')
        try:
            temp_, err = self.exec_sql1(sql_, True)
            cols_ = [x[0] for x in temp_]
        except:
            return [], err

        # Creates Dataframe
        df = pd.DataFrame(data=data_, columns=cols_)

        # Drop idNum
        try:
            df.drop(columns='idNum', inplace=True)
        except:
            pass

        return df, err

    def dataDB_Table_write(self, df, tableName):
        # Writes a Dataframe  to a generic table
        # df is a dataFrame with the appropriate columns
        # v1.1 2020-10-20

        # Drop idNum
        try:
            df.drop(columns='idNum', inplace=True)
        except:
            pass

        sql1 = 'INSERT INTO {0}.{1} {2} '.format(self.configMysql['database'], tableName, tuple(df.columns))
        sql1 = sql1.replace("'", '')

        sql2 = 'VALUES {};'.format(tuple(map(tuple, df.to_numpy())))
        sql2 = sql2.replace('((', '(')
        sql2 = sql2.replace('))', ')')
        sql2 = sql2.replace('),);', ');')
        sql1 += sql2

        #print('AAA  sql:', sql1)
        flagdb, err = self.exec_sql1(sql1, False)

        return flagdb, err

    #
    # Table seeRAW read/write
    #

    def dataDB_seeRaw_read(self, load_data):

        #
        # Reads Data from see000Raw Table according to load_data infos
        # Input
        '''
            load_data ={}
            #Selected Variables
            load_data['idDev']      =
            load_data['idPars']     =
            load_data['startDate']  =
            load_data['endDate']    =
            load_data['timeStep']   =
            load_data['database'] =
            load_data['tZone'] =
            load_data['parUM'] =
            load_data['parDescr'] =
            load_data['enable'] =

        '''
        #       idDev:  str or list of str
        #       idPars: str or list of str
        # returns dataFrame
        # v1.9 2018-08-21
        # v2.0 2021-05-15
        # v2.1 2022-02-01

        # Check if multiple devices/parameters
        if isinstance(load_data['idDev'], list):
            if len(load_data['idDev']) == 1:
                load_data['idDev'] = load_data['idDev'][0]

        if isinstance(load_data['idPars'], list):
            if len(load_data['idPars']) == 1:
                load_data['idPars'] = load_data['idPars'][0]

        list_idDevs = tuple(load_data['idDev']) if isinstance(load_data['idDev'], list) else "('" + load_data[
            'idDev'] + "')"
        list_idParams = tuple(load_data['idPars']) if isinstance(load_data['idPars'], list) else "('" + load_data[
            'idPars'] + "')"

        # Translate local dates to utc
        if load_data['tZone']:
            startDate = tZone_to_utctime(load_data['startDate'], load_data['tZone'])
            endDate = tZone_to_utctime(load_data['endDate'], load_data['tZone'])
        else:
            startDate = load_data['startDate']
            endDate = load_data['endDate']

        # SQL
        sql_ = ' Select Date, idDevice, idParam, Value, Code, Delay  '
        sql_ += 'from {}.{} '.format(load_data['database'], load_data['table'])
        sql_ += 'where idDevice in {} and idParam in {} '.format(list_idDevs, list_idParams)
        sql_ += "and Date between '{}' AND '{}' ".format(startDate, endDate)

        try:
            df, err = self.exec_sql1(sql_, True)
            df = pd.DataFrame(data=df,
                              columns=['DateTime', 'idDevice', 'idParam', 'Value', 'Code', 'Delay'],
                              )
            df.set_index('DateTime', inplace=True)
            df.index.name = 'DateTime'
            err += ' ' + sql_

        except:
            df = pd.DataFrame()
            err = '[msg] dataDB_seeRaw_read() - no connection with DB. sql_:' + sql_

        return df, err

    def pivotRead_RawData(self, load_data):
        # Creates Pivot table "DateTime/Parameter/Value" from seeRaw data
        # v1.0 2020-11-06
        # v1.1 2020-11-23
        # v2.0 2021-05-15  tz_localize, dataDB_seeRaw_read
        # v2.1 2022-02-01
        # v2.2 2022-08-17
        # v2.2 2022-08-29   no df1 = df1[~df1.index.duplicated(keep='first')]
        # v2.2 2022-09-02
        # v2.3 2022-10-12
        # v2.4 2022-11-17
        # v2.5 2022-11-25

        # Read RAW Data

        df, err = self.dataDB_seeRaw_read(load_data)

        if len(df) == 0:
            print(err)
            return pd.DataFrame(), pd.DataFrame(), err

        # Creates Field idDev_idParam
        df['idxPar'] = df['idDevice'] + '_' + df['idParam']

        # Adapt DateTime to timezone
        if load_data['tZone']:
            # deltaTime = ((utctime_to_tZone(datetime.now(),load_data['tZone']) - datetime.now()).seconds + 1) // 3600  # deltatime in hours
            # df.index = df.index.to_series().apply(lambda x: x + timedelta(hours=deltaTime))  # update datetime
            # df['DateTime'] = df['DateTime'].apply(lambda x: utctime_to_tZone(x, tZone))  # Pivot Columns names: device_param
            df.index = df.index.tz_localize('utc').tz_convert(load_data['tZone'])
            df.reset_index(inplace=True)
            df['DateTime'] = df['DateTime'].apply(lambda x: x.replace(tzinfo=None))
            df = df.set_index('DateTime')

        # Code for not sampled data
        # df.update(df[df['idDevice'].isna()].loc[:, 'idDevice'].fillna(value=load_data['idDev']))
        # df.update(df[df['idParam'].isna()].loc[:, 'idParam'].fillna(value=load_data['idPars']))
        # df.update(df[df['Code'].isna()].loc[:, 'Code'].fillna(value=error_code))

        # Pivot Table - filter data with specified error code or 0
        df1 = df
        if load_data['code'] != '':
            df1 = df1[df1['Code'] == load_data['code']]
        #else:
        #    df1 = df1[df1['Code'] == 0]

        if len(df1) == 0:
            print(err)
            return pd.DataFrame(), pd.DataFrame(), err

        # Shift time
        # if load_data['shiftStep'] != 0:
        #    df1.index = df1.index.to_period(load_data['timeStep']) + load_data['shiftStep']
        #    df1.index = df1.index.to_timestamp(load_data['timeStep'])  # riconversione index in timestamp per plot

        # Drops duplicated  - filter for DST time shifts
        if len(df1['idxPar'].unique())==1:
            df1 = df1[~df1.index.duplicated(keep='first')]

        #df1 = df1.drop_duplicates(keep='first')

        # Creates pivot table
        pivot_ = df1.reset_index().pivot(
            index='DateTime',
            columns='idxPar',
            values='Value')

        # Filters only time stepped records
        if load_data['timeStep'] != '0t':
            pivot_ = pivot_.resample(load_data['timeStep']).max()

        # Drops duplicated  - filter for DST time shifts
        # pivot_ = pivot_[~pivot_.index.duplicated(keep='first')]
        # pivot_.dropna(inplace=True)

        # df index DateTime
        pivot_.index.name = 'DateTime'
        pivot_.columns.name = ''

        return pivot_, df1, err

    def dataDB_seeRaw_write(self, df, date_format='%d/%m/%Y %H:%M' or None, time_to_utc=False):
        # Writes a Dataframe  to the Raw Data  seetable
        # Table fields = ('Date', 'idDevice', 'idParam', 'Code','Delay', 'Value')
        # v1.0 2020-07-12
        # v1.1 2021-05-12

        database_ = self.configMysql['database']
        table_ = self.configMysql['tableRaw']
        # Drop idNum
        df.drop(columns='idNum', inplace=True)

        # Date format is 26/03/2020 23:03
        # Convert Datetime from local time string fromat   to utc Datetime format

        if time_to_utc:
            df['Date'] = df['Date'].apply(lambda x: tZone_to_utctime(
                datetime.strptime(x, date_format),
                self.configMysql['tZone']
            ))
        else:
            df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, date_format))

        flagdb, _ = self.dataDB_Table_write(df, table_)

        return flagdb

    #
    # Table see000Params read
    #
    def dataDB_seeParams_read(self, idParam):
        # Reads Parameters Table data
        # 'idParam', 'paramDescr', 'um', 'Acronimo'
        # v1.0 2020-07-07
        # v1.1 2022-02-01
        # v1.2 2022-02-14

        db_1 = pd.DataFrame([0])

        sql_ = '''
                select idParam, {3}, um, Acronimo from {0}.{1}  
                where idParam='{2}';
               '''.format(
            self.configMysql['database'],
            self.configMysql['tableParams'],
            idParam,
            'descr' + self.configMysql['language'],
        )

        if idParam == 'All':
            sql_ = sql_.replace('idParam=', 'idParam!=')

        if self.db_connect:
            out_, _ = self.exec_sql1(sql_, True)  # format [(par1, par2,...)]
            db_1 = pd.DataFrame(data=out_,
                                columns=['idParam', 'paramDescr', 'um', 'Acronimo'],
                                )
        else:
            str_ = '[msg] dataDB_seeParams_read() - no web connection'
            push_log(str_)

        return db_1

    #
    # Table see000Mac read
    #
    def dataDB_seeMac_read(self, idMac):
        # Reads MAchine  Table data
        #   v1.0    2020-07-07
        #   v1.1    2022-02-14

        db_1 = pd.DataFrame([0])
        sql_ = "select  idMac, descrLANG  from {0}.{1}  " \
               "where idMac= '{2}'; ".format(
                                        self.configMysql['database'],
                                        self.configMysql['tableMac'],
                            idMac)

        sql_ = sql_.replace('descrLANG', 'descr' + self.configMysql['language'])

        if idMac == 'All':
            sql_ = sql_.replace('idMac=', 'idMac!=')

        if self.db_connect:
            out_, _ = self.exec_sql1(sql_, True)  # format [(par1, par2,...)]
            db_1 = pd.DataFrame(data=out_,
                                columns=['idMac', 'machDescr'],
                                )
        else:
            str_ = '[msg] dataDB_seeParams_read() - no web connection'
            push_log(str_)

        return db_1
    #
    # Table see000 Devices read
    #
    def dataDB_seeDevice_read(self, idDev):
        # Reads Devices Table data
        # fields: 'idDevice', 'idDep', idMac', 'machDescr'
        #   v1.0    2022-08-23


        df_idDev = pd.DataFrame([0])
        sql_ = "select  idDevice, idMac, idDep  from {0}.{1}  " \
               "where idDevice= '{2}'; ".format(
                                        self.configMysql['database'],
                                        self.configMysql['tableJoin'],
                                        idDev)

        if 'All' in idDev:
            sql_ = sql_.replace('idDevice=', 'idDevice!=')

        if self.db_connect:
            out_, _ = self.exec_sql1(sql_, True)  # format [(par1, par2,...)]
            df_idDev = pd.DataFrame(data=out_,
                                columns=['idDevice', 'idMac', 'idDep'],
                                )
        else:
            str_ = '[msg] dataDB_seeParams_read() - no web connection'
            push_log(str_)

        df_idMac = self.dataDB_seeMac_read('All')  # fields: 'idMac', 'machDescr'
        df_idDev = pd.merge(df_idDev, df_idMac, how='left', on= 'idMac')
        # fields: 'idDevice', 'idDep', idMac', 'machDescr'

        return df_idDev

    #
    # Table see000Deps read
    #
    def dataDB_seeDep_read(self, idDep):
        # Reads Departments  Table data
        # v1.0  2020-07-07
        # v1.1  2022-02-14

        db_1 = pd.DataFrame([0])
        sql_ = "select  idDep, descrLANG  from {0}.{1}  " \
               "where idDep='{2}'; ".format(
            self.configMysql['database'],
            self.configMysql['tableDeps'],
            idDep)

        sql_ = sql_.replace('descrLANG', 'descr' + self.configMysql['language'])

        if idDep == 'All':
            sql_ = sql_.replace('idDep=', 'idDep!=')

        if self.db_connect:
            out_, _ = self.exec_sql1(sql_, True)  # format [(par1, par2,...)]
            db_1 = pd.DataFrame(data=out_,
                                columns=['idDep', 'depDescr'],
                                )
        else:
            str_ = '[msg] dataDB_seeDep_read() - no web connection'
            push_log(str_)

        return db_1

    #
    # Table see000SysSetRaw read
    #
    def dataDB_seeSysRaw_read(self, type):
        # Reads table System Raw Data
        # v1.0 2020-10-25
        # v2.0 2021-05-12
        # v2.1 2022-02-01
        # v2.2 2022-02-14

        db_1 = pd.DataFrame([0])

        if type == 'Raw':
            table_ = self.configMysql['tableSysRaw']

        elif type == 'Prod':
            table_ = self.configMysql['tableSysProdw']

        if self.db_connect:
            db_1, _ = self.dataDB_Table_read(self.configMysql['tableSysRaw'])
        else:

            str_ = '[msg1] - dataDB_seeSysRaw_read() - no database connection'
            push_log(str_)

        return db_1

    #
    # Table see000Prod write
    #
    def dataDB_seeProd_write(self, df, date_format='%d/%m/%Y %H:%M' or None, UTC_flag=False):
        # Writes a Dataframe  to the Production  seetable
        # Options: time utc conversion, date format adjiustment
        # Table fields = ('Date', 'Value', 'idProd', 'idMac', 'idParam', 'Code')
        # v1.0 2020-07-12
        # v1.1 2021-04-23
        # 2021-05-12 - upgrade

        database_ = self.configMysql['database']
        table_ = self.configMysql['tableProd']

        # Drop idNum
        try:
            df.drop(columns='idNum', inplace=True)
        except:
            pass

        if UTC_flag:
            # Date format is 26/03/2020 23:03
            # Convert Datetime from local time string format   to utc Datetime format
            df['Date'] = df['Date'].apply(
                lambda x: tZone_to_utctime(datetime.strptime(x, date_format), self.configMysql['tZone'])
            )
        flag_, err = self.dataDB_Table_write(df, table_)
        return flag_, err

    # Production Data
    def dataDB_Prod_Article(self):
        # Collects data about production of articles
        # v1.0 2021-05-12
        # v1.1 2021-05-13

        # 1. Extract production resources
        # 2. Filter on article
        config_mysql = self.configMysql
        # Join Table Names
        t_jArtJob = config_mysql['tablejArtJob']
        t_jJobDep = config_mysql['tablejJobDep']
        t_jDepMac = config_mysql['tablejDepMac']
        t_jMacDev = config_mysql['tablejMacDev']
        # t_Articoli = config_mysql['tableArt']   # idArt, idParams, Description

        # METHOD Merge tables 1 - merge tables
        test_ = False
        if test_:
            # Read table contents
            ArtJob,_ = self.dataDB_Table_read(t_jArtJob)
            JobDep,_ = self.dataDB_Table_read(t_jArtJob)
            DepMac,_ = self.dataDB_Table_read(t_jDepMac)
            MacDev,_  = self.dataDB_Table_read(t_jMacDev)

            # tableArt
            df0 = pd.merge(ArtJob, JobDep, how='left', on='idJob')
            df0 = pd.merge(df0, DepMac, how='left', on='idDep')
            df0 = pd.merge(df0, MacDev, how='left', on='idMac')

        # METHOD Merge tables 2 - sql
        cols_ = 'idArt,{0}.idJob,{1}.idDep,DateStart,DateEnd,{2}.idMac,sign,idDevice'.format(t_jJobDep,
                                                                                             t_jDepMac,
                                                                                             t_jMacDev,
                                                                                             t_jArtJob)

        from_ = ' FROM {3} LEFT JOIN ({0}, {1},{2})'.format(t_jJobDep,
                                                            t_jDepMac,
                                                            t_jMacDev,
                                                            t_jArtJob)

        on_ = ' ON ({0}.idJob={3}.idJob AND {1}.idDep={0}.idDep AND {2}.idMac={1}.idMac)'.format(t_jJobDep,
                                                                                                 t_jDepMac,
                                                                                                 t_jMacDev,
                                                                                                 t_jArtJob)
        # where_ = ' where idArt = {}'.format(article)

        sql_ = 'SELECT ' + cols_ + from_ + on_  # + where_
        columns_ = ['idArt', 'idJob', 'idDep', 'DateStart', 'DateEnd', 'idMac', 'sign', 'idDevice']
        dbjArt, _ = self.exec_sql1(sql_, True)
        artTable = pd.DataFrame(data=dbjArt, columns=columns_)

        '''
            artTable 	
               idArt  idJob  idDep  DateStart    DateEnd              idMac sign idDevice
            0   Art1   Job1  dep01 2021-04-25 2021-04-30       Forno_Cucina    +      d01
            1   Art1   Job1  dep01 2021-04-25 2021-04-30         Forno_Tunn    +      d09
            2   Art1   Job1  dep01 2021-04-25 2021-04-30          Gen_Forno    -      d07
            3   Art1   Job2  dep02 2021-02-01 2021-02-28  Celle_Evaporatori    +      d03
            ...
        '''
        return artTable

    #
    # DATA Backup Management
    #
    def reload_filebackup(self, **kwargs):
        # Check and reload data in temp file/array __mysql
        # 2019-07-20  fixed stop connect to DB if first attempt fails
        # 2019-07-20  execute_sql() in place of push_db()
        # 2019-08-27  fixed filename - like push_file()
        # v2.0 2020-07-03
        # v2.1 2020-07-19 fixed configMySql
        # v3.0 2020-09-19 if h>0

        config_mysql_bk = self.configMysql['config_mysql_bk']

        filename = config_mysql_bk['filename']

        try:
            oldText = kwargs['oldText']
            newText = kwargs['newText']
        except:
            oldText = ''
            newText = ''
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
        except:
            # print('[msg] reload_filebackup() - file {} not available'.format(filename))
            # push_log('[msg] reload_filebackup() - file {} not available'.format(filename))
            pass
        else:
            h = min(config_mysql_bk['max_rows_reload'], len(lines))

            # Svuota file
            msg_file = 'reload_filebackup()'
            idLine = 0

            if h > 0:
                for x in range(h):
                    sql_ = lines[idLine]
                    sql_ = sql_.replace(oldText, newText)

                    # print('oldText: ', oldText)
                    # print('newText: ', newText)
                    # print('> sql_: ', sql_[:200])
                    flag_db, err = self.exec_sql1(sql_, False)
                    str_ = str(err + '\n sql: ' + sql_)
                    if flag_db == True:
                        msg_ = "[msg_1] - {3}. Line {0}/{1} stored. {2} remaining".format(
                            str(x), str(h), str(len(lines)), msg_file)
                        print(msg_)
                        push_log(msg_)
                    else:
                        f1 = open(filename + '_error.csv', 'a+')
                        f1.writelines(sql_)
                        f1.close()
                        if 'Duplicate' in err:
                            msg_ = "[msg_3] - {3}. Line {0}/{1} DELETED as it is a DUPLICATE. {2} remaining".format(
                                str(x), str(h), str(len(lines)), msg_file)
                            print(msg_)
                            push_log(msg_)

                        elif sql_ == '\n' or sql_ == '':
                            msg_ = "[msg_3.1] - {3}. Line {0}/{1} DELETEDas it is None. {2} remaining".format(
                                str(x), str(h), str(len(lines)), msg_file)
                            print(msg_)
                            push_log(msg_)
                        else:
                            if lines[idLine] != '\n':
                                msg_ = "[msg_4] - {3}. Line {0}/{1} not stored. {2} remaining. MySQL Error: {4}" \
                                    .format(str(x), str(h), str(len(lines)), msg_file, err)
                                print(msg_)
                                push_log(msg_)
                    del lines[idLine]

                # Rewrite remaining lines in file
                f = open(filename, 'w')
                f.writelines(lines)
                f.close()

                msg_ = '[msg_5] - Stored {} lines to file: {}'.format(len(lines), filename)
                print(msg_)
                push_log(msg_)

    def reload_arrayBackup(self):
        # 2019-11-11  svuota array
        # v2.0 2020-07-04
        # v2.11 2020-07-19
        # v2.12 2020-07-26
        # v3.0  2020-09-19  if h>0

        msg_file = 'reload_arrayBackup()'
        config_mysql_bk = self.configMysql['config_mysql_bk']
        filename = config_mysql_bk['filename']
        lines = self.array_sql
        h = min(config_mysql_bk['max_rows_reload'], len(lines))
        idLine = 0

        if h > 0:
            for x in range(h):
                sql_ = lines[idLine]
                flag_db, err = self.exec_sql1(sql_, False)
                str_ = str(err + '\n sql: ' + sql_)

                if flag_db == True:
                    msg_ = "[msg_1] reload_arrayBackup() - {3}. Line {0}/{1} stored. {2} remaining".format(
                        str(x), str(h), str(len(lines)), msg_file)
                    print(msg_)
                    push_log(msg_)

                else:

                    f1 = open(filename + '_error.csv', 'a+')
                    f1.writelines(sql_)
                    f1.close()

                    if 'Duplicate' in err:
                        msg_ = "[msg_3] reload_arrayBackup - {3}. Line {0}/{1} DELETED as it is a DUPLICATE. {2} remaining".format(
                            str(x), str(h), str(len(lines)), msg_file)
                        print(msg_)
                        push_log(msg_)
                    elif sql_ == '\n' or sql_ == '':
                        msg_ = "[msg_3.1] reload_arrayBackup - {3}. Line {0}/{1} DELETEDas it is None. {2} remaining".format(
                            str(x), str(h), str(len(lines)), msg_file)
                        print(msg_)
                        push_log(msg_)

                    else:
                        if lines[idLine] != '\n':
                            msg_ = "[msg_4] reload_arrayBackup - {3}. Line {0}/{1} not stored. {2} remaining. MySQL Error: {4}" \
                                .format(str(x), str(h), str(len(lines)), msg_file, err)
                            print(msg_)
                            push_log(msg_)

                del lines[idLine]

            msg_ = '[msg_5] reload_arrayBackup - Stored {} remaining lines in array_sql'.format(len(lines))
            print(msg_)
            push_log(msg_)

    def data_store_pack(self, dataPack, table_, *args, **kwargs):
        # Memorizza i dati di piu' strumenti
        # v1.0 2020-07-03
        # v2.0 2021-01-06
        # v2.1 2022-07-10

        len_pack = len(dataPack)
        store_flag = []

        for i in range(len_pack):
            store_flag.append(self.data_store(dataPack[i], table_))
        return store_flag

    def data_store_db(self, param_list, table_, **kwargs):
        # Memorizza i dati solo su db
        # v1.0 2020-07-03
        # v2.0 2020-12-27
        # v3.0 2021-01-06

        item = param_list[0]
        keys = [x for x in item.keys()]
        sql1 = 'INSERT INTO %s (%s) ' % (table_, keys)
        sql2 = 'VALUES '

        for xx in range(len(param_list)):
            item = param_list[xx]
            vals = [x for x in item.values()]
            sql2 += '( %s ),' % vals

        sql2 = sql2[:-1]
        sql1 = sql1.replace('[', '')
        sql1 = sql1.replace(']', '')
        sql1 = sql1.replace("'", '')
        sql2 = sql2.replace('[', '')
        sql2 = sql2.replace(']', '')
        sql2 += r';'
        sql = sql1 + sql2

        flagDB, err = self.exec_sql1(sql, False)
        return flagDB, err, sql

    def data_store(self, param_list, table_):
        # Memorizza i dati di param_list in
        # 1. mysql DB
        # 2. backup file
        # 3. temp-array

        # v2.7 2019-07-20   pack data
        # v3.0 2020-07-04
        # v3.1 2020-12-03   integrated data_store_db()
        # v3.2 2021-01-06   table

        config_mysql_bk = self.configMysql['config_mysql_bk']
        flag_db = 0
        flag_file = 0
        filename = ''
        store_flag = 0
        err_ ='none'
        db_connect = internet_ip()
        sql_ = '[msg] see_db.data_store() - error: no internet connection'

        # storage flag
        #     0=none
        #     1=Mysql
        #     2=file
        #     3=array

        # print('dbconnect', db_connect)

        if db_connect:
            flag_db, err_, sql_ = self.data_store_db(param_list, table_)
            # flag_db, _ = self.exec_sql1( sql, 0)

        if flag_db:
            # print('...sql ---->>> db_mysql... ip', config_mysql['host'])
            store_flag = '1'
        else:
            if config_mysql_bk['enable']:
                filename = config_mysql_bk['filename']
                flag_file = self.write_to_file(filename, sql_)
            if flag_file:
                store_flag = '2'
                push_log(message_strings[10] % (filename))  #  data_store() - DB nok,  backup su file %s ',
            else:
                self.write_array(sql_)
                # print('> sql: ', sql[:200])
                push_log(message_strings[13])
                store_flag = '3'
                print('> data_store() - store_flag3: stored sql array to array_sql. Size: ', str(len(self.array_sql)))

        return store_flag  #, err_, sql_

    def write_array(self, sql):
        #
        # Adds a row to global array_sql with stringa
        #
        # v2.0 2020-07-04
        # v2.1 2022-012-01 - minors

        self.array_sql.append(sql)
        items = len(self.array_sql)
        return items

    def write_to_file(self, file_name, stringa):
        #
        # Adds a row to file_name with stringa
        #
        # v2.0 2020-07-04
        # v2.1 2020-09-19 no "\n"

        stringa += "\n"

        # store in mysql backup file
        if 'INSERT ' in stringa:
            filedatetime = ''  # -> to mysql_bk
        else:
            # store in Backup file
            filedatetime = '{:%Y_%B}'.format(time_utc())

        filename = filedatetime + file_name

        file_ok = True
        if os.path.isfile(filename):
            try:
                f = open(filename, 'a')
            except os.error:  # as err
                file_ok = False
            else:
                f.write(stringa)
                f.close()
        else:
            try:
                f = open(filename, 'w')
            except os.error:  # as err:
                file_ok = False
                print(message_strings[3], filename)
            else:
                f.write(stringa)
                f.close()
        return file_ok

    def dataDB_newTab_y(self, tableName, year_):
        # Creates a new seeTable every year
        # v1.0 2020-04-20
        # v1.1 2020-07-02

        seeDB_ = self.configMysql['database']
        seeTab_ = tableName  # self.configMysql['tableRaw']
        seeTabNew_ = seeTab_ + '_' + str(year_)

        sql_1 = 'ALTER TABLE {0}.{1} RENAME TO {0}.{2} ;'.format(
            seeDB_,
            seeTab_,
            seeTabNew_,
        )

        sql_2 = 'CREATE TABLE {0}.{1} LIKE {0}.{2};'.format(
            seeDB_,
            seeTab_,
            seeTabNew_,
        )

        err1 = '0'
        err2 = '0'
        _, err1 = self.exec_sql1(sql_1, False)
        _, err2 = self.exec_sql1(sql_2, False)

        if err1 != '0':
            txt_ = '[msg] - dataDB_seeTab_y: 1. error in renaming  table {0}'.format(seeTab_, )
            print(txt_)
            push_log(txt_)
        else:
            txt_ = '[msg] - dataDB_newseeTab_y: 1. table  {0} renamed to  {1}'.format(seeTab_, seeTabNew_)
            print(txt_)
            push_log(txt_)

        if err2 != '0':
            txt_ = '[msg] - dataDB_newseeTab_y: 2. error in creating the new table err1:{0}.'.format(seeTab_)
            print(txt_)
            push_log(txt_)
        else:
            txt_ = '[msg] - dataDB_seeTab_y: 2. new table {0} created.'.format(seeTab_)
            print(txt_)
            push_log(txt_)

    def parDesc(self, parId):
        #Returns the parameter description
        # v1.0 2022-11-25
        #

        # Table
        #   DateTime    idDev   Par     Value   u.m
        df_Param = self.dataDB_seeParams_read('All')
        '''
                    idParam                    paramDescr      um      Acronimo
            0       101                        Voltage UL1_N       V         UL1_N
            1       102                        Voltage UL2_N       V         UL2_N
            2       103                        Voltage UL3_N       V         UL3_N
        '''
        try:
                descr = df_Param[df_Param['idParam'] == parId]['paramDescr'].to_list()[0]
        except:
                descr = ''

        return descr

class Events(seedatadb):
    # Event Instance Management
    # v1.0 2022-11-11
    # v1.1 2022-11-12
    # v1.3 2022-11-13
    # v1.4 2022-11-25

    def __init__(self, configMysql, dataEvents):
        super().__init__(configMysql)
        self.configMysql = configMysql
        self.dataEvents = dataEvents
        self.TableEvents = configMysql['tableEvents']

        self.stateAlarm = False
        self.stateAlarm_old = False

        self.startMinute = 0
        self.stateChange = 'STABLE'
        self.actValue = 0
        self.startEn = 0
        self.actEn = 0
        self.code= -1

        #Init Data
        self.init_data()
        self.TimeStamp = time_local(tZone = self.configMysql['tZone'])
        self.TimeStamp = datetime.strftime(self.TimeStamp, '%Y-%m-%d %H:%M:%S')


    def init_data(self):
        #v1.0 2022-11-13

        self.idEvent = self.dataEvents['00'][0].lower()
        self.eventType = self.dataEvents['01'][0].lower()

        self.energyType = False
        if 'energy' in self.eventType:
            self.energyType = True

        self.evDescr = self.dataEvents['01'][0]
        self.idDev = self.dataEvents['02'][0]
        self.idParam = self.dataEvents['03'][0]
        self.setLimit = float(self.dataEvents['04'][0])
        self.k_ = float(self.dataEvents['05'][0])
        self.eventFunction = self.dataEvents['06'][0]
        self.um = self.dataEvents['07'][0]
        self.hyst_pu = float(self.dataEvents['08'][0]) *0.01
        self.enable = self.dataEvents['0a'][0]
        self.msgUP = self.dataEvents['0b'][0]
        self.msgDOWN = self.dataEvents['0c'][0]

        '''
        dataEvents={
        '00': ['enMax', 'Overall Energy control'],
        '0a': [True, 'Alarm enable'],
        '0b': ['Avviso: Attivo SUPERAMENTO LIMITE ENERGIA', 'email ON text'],
        '0c': ['Avviso: Rientrato SUPERAMENTO LIMITE ENERGIA', 'email OFF text'],
        '01': ['Over Energy timebased on qH', 'Alarm description'],
        '02': ['d00', 'event idDev'],
        '03': ['222', 'event idParam [kWh]'],
        '04': ['1.0', 'Energy Limit [kWh]'],
        '05': ['1000', 'k limit multiplication factor'],
        '06': ['>=', 'Alarm function <actValue> vs. <setValue> '],
        '07': ['kWh', ' limit measure unit'],
        '08': ['0', 'Hysteresis %'],
        '''

    def qt_energy(self, idDev, idPar):
        #Calculates Energy in the last quarter of hour
        #v1.0 2022-11-11
        #v1.1 2022-11-15

        # Read data from Last Table
        df_Last = self.dataDB_seeLast_read(idDev, idPar, self.configMysql['tableLast'])
        self.code = float(df_Last['Code'])

        '''
            DateTime               idDevice idParam        Value  Code    Delay
            0 2022-11-11 14:46:00      d00     222  246880800.0     0  2332.11
        '''

        #Exctract Energy value
        #try:
        self.actEn = float(df_Last['Value'])
        self.TimeStamp_minute = df_Last['DateTime'][0].minute

        #except:
        #    return -1

        #Update startEn
        if self.TimeStamp_minute in [0,15,30,45]:
            self.startMinute = self.TimeStamp_minute
            self.startEn = self.actEn

        #Calculates diffEn
        self.diffEn = self.actEn - self.startEn


        #Calculates Power Tendency [W]
        try:
            self.actPower = self.diffEn/(self.TimeStamp_minute-self.startMinute) * 60.0 
        except:
            self.actPower = 0
            self.code = err_code['value_NaN']

        self.actPower= self.actPower * self.k_
        self.actValue = self.diffEn * self.k_

    def set_Event(self):
        # set Event status
        #v1.0 2022-11-11
        #v1.1 2022-11-16

        self.actValue = 0
        self.code = -1
        self.TimeStamp = time_local(tZone = self.configMysql['tZone'])
        self.TimeStamp = datetime.strftime(self.TimeStamp, '%Y-%m-%d %H:%M:%S')

        #try:
        if self.energyType:
            self.qt_energy(self.idDev, self.idParam)

        else:
            df_Last = self.dataDB_seeLast_read(self.idDev, self.idParam, self.configMysql['tableLast'])
            try:
                self.code = float(df_Last['Code'])
            except:
                self.code = df_Last['Code']

            self.actValue = float(df_Last['Value']) * self.k_
        #except:
        #    pass

        if int(self.code) == 0:

            if '>' in self.eventFunction:
                # State alarm ON    ActValue>= setValue + Hist
                # State alarm OFF    ActValue < setValue - Hist
                if self.actValue >= self.setLimit*(1 + self.hyst_pu*0):
                    self.stateAlarm = True
                if self.actValue < self.setLimit*(1 - self.hyst_pu):
                    self.stateAlarm = False

            if '<' in self.eventFunction:
                # State alarm ON    ActValue <= setValue - Hist
                # State alarm OFF   ActValue>= setValue + Hist
                if  self.actValue <= self.setLimit*(1 - self.hyst_pu*0):
                    self.stateAlarm = True
                if  self.actValue > self.setLimit*(1 + self.hyst_pu):
                    self.stateAlarm = False

            if self.eventFunction =='=':
                # State alarm ON    ActValue == setValue - Hist
                # State alarm OFF   ActValue != setValue + Hist
                if  self.actValue == self.setLimit*(1 - self.hyst_pu):
                    self.stateAlarm = True
                if  self.actValue != self.setLimit*(1 + self.hyst_pu):
                    self.stateAlarm = False

            # Event change of state
            if self.stateAlarm_old != self.stateAlarm:
                if self.stateAlarm:
                    self.stateChange = 'UP'
                else:
                    self.stateChange = 'DOWN'

            if self.stateAlarm_old == self.stateAlarm:
                self.stateChange = 'STABLE'

            self.stateAlarm_old = self.stateAlarm
        else:
            self.stateChange = f'ERROR id:' + str(self.code)
            self.stateAlarm_old = False


    def reset_Alarm(self):
        #v1.0 2022-11-11

        self.stateAlarm = False

    def write_TableEvent(self, tableName):
        #v1.1 2022-11-17
        #v1.2 2022-12-21

        # df = pd.DataFrame(data={
        #         'Date':[self.TimeStamp],
        #         'idEvent':[self.idEvent],
        #         'setLimit':[self.setLimit],
        #         'function': [self.idDev + '-' + self.idParam + '[' + self.um +'] ' + self.eventFunction],
        #         'actValue':[self.actValue],
        #         'hyst':[self.hyst_pu*100],
        #         'Status':[self.stateAlarm],
        #         'upDown':[self.stateChange],
        #         })

        df = pd.DataFrame(data={
                'Date':[self.TimeStamp],
                'idEvent':[self.idEvent],
                'setLimit': [self.setLimit],
                'actValue': [self.actValue],
                'Note': [self.stateChange],
                })


        w_tab = self.dataDB_Table_write(df, tableName)
        return w_tab

    def write_TableEventLast(self, tableName):
        #v1.1 2022-11-17
        #v1.2 2022-12-21

        df = pd.DataFrame(data={
                'Date':[self.TimeStamp],
                'idEvent':[self.idEvent],
                'setLimit':[self.setLimit],
                'function': [self.idDev + '-' + self.idParam + '[' + self.um +'] ' + self.eventFunction],
                'actValue':[self.actValue],
                'hyst':[self.hyst_pu*100],
                'Status':[self.stateAlarm],
                'upDown':[self.stateChange],
                })

        w_tab = self.dataDB_Table_write(df, tableName)
        return w_tab


class EventsDB(seedatadb):
    #Reads all events data and generates list of dictionaries
    #v1.0   2022-11-12

    def __init__(self, configMysql):
        super().__init__(configMysql)
        self.configMysql = configMysql

    def read_eventTableSys(self):
        # Reads EVENTS DATA
        #v1.0 2022-11-12

        df_ev, _ = self.dataDB_Table_read(self.configMysql['tableEventsSys'])
        if len(df_ev)>0:
            ev_list = df_ev['idGroup'].unique().tolist()
            ev_list = sorted(ev_list)
            n_events = len(ev_list)  # number of events
        else:
            return []

        # Extract events' data
        ev_dict = []
        for i, x in enumerate(ev_list):
            ev_data = df_ev.loc[:, ['idParam', 'Value', 'Description']][df_ev['idGroup'] == x]

            #Set parameter '00' to event id
            ev_data.loc[:,'Value'][ev_data['idParam']=='00']=x

            ev_data = ev_data.values.tolist()
            ev_dict.append({y[0]: [y[1], y[2]] for y in ev_data})

        #List of Events' Dictionary
        self.ev_dict = ev_dict

        return ev_dict

    def read_eventTable(self, tableName):
        #v1.0 2022-11-12
        #v1.1 2022-11-12

        df, _ = self.dataDB_Table_read(tableName)
        if 'Last' in tableName:
            df = df.sort_values(by="idEvent")
        else:
            df = df.sort_values(by="Date",ascending=False)
        return df

    def clear_eventTable(self, tableName):
        #v1.0 2022-11-12
        if 'Events' in tableName:
            sql_ = f"DELETE FROM {tableName} where idNum>=0;"
            return self.exec_sql1(sql_, False)

    def upDate_to_SysTable(self, idEvent, value, idParam, tableName):
        #Update value un tableSYS
        #v1.0 2022-11-12

        sql1 = "UPDATE {0}.{1} ".format(self.configMysql['database'], tableName) #
        sql1 += "SET Value={0} ".format(value)
        sql1 += "WHERE idGroup='{0}' and idParam ='{1}' ".format(idEvent,idParam)

        return self.exec_sql1(sql1, False)

    def send_email(self, conf):
        # v1.0 2018-07-29
        # Send email to address specified in config_email
        import smtplib

        '''
            conf_email = {
                'from_email': cLib.config_events['email_server']['email'],
                'to_email': cLib.config_events['ref_person']['email'],
                'smtp': cLib.config_events['email_server']['smtp'],  # 'smtp.gmail.com: 587', #'smtps.aruba.it:465',
                'from_psw': cLib.config_events['email_server']['password'],
                'timeout':  cLib.config_events['email_server']['timeout'],
                'subject': sbj_,
                'msg': msg_,
                    }
        '''
        # server
        server = smtplib.SMTP(conf['smtp'])
        server.timeout = conf['timeout']
        server.starttls()
        server.login(conf['from_email'], conf['from_psw'])

        msg_ = 'Subject: {}\n\n{}'.format(conf['subject'], conf['msg'])

        # print('sending email - deltatime:%s - messaggio: %s' % (deltaTime, msg_))

        server.sendmail(conf['from_email'], conf['to_email'], msg_)
        server.quit()


class db_table(seedatadb):
    # CReates tables in DB
    # v1.0   2022-11-26
    # v1.1   2023-04-23

    def __init__(self, configMysql):
        super().__init__(configMysql)
        self.configMysql = configMysql
        self.db = configMysql['database']

    def table_check(self, tableName):
        #v1.1 2022-11-30

        sql_check= "CHECK TABLE tableName QUICK;"
        sql_check= sql_check.replace('tableName', tableName)

        sql_check= f'''
        SELECT COUNT(TABLE_NAME) FROM information_schema.TABLES
        WHERE
        TABLE_SCHEMA LIKE '{self.db}'
        AND TABLE_TYPE LIKE 'BASE TABLE'
        AND TABLE_NAME LIKE '{tableName}';
        '''

        self.sql_check=sql_check
        out1, out2 = self.exec_sql1(sql_check,True)
        flag_ = False
        try:
            flag_ = out1[0][0]>0
        except:
             pass
        return flag_

    def create_table(self, sql_, tableName):
        # Execute sql_ code
        # Check if tableName exists
        # v1.0 2022-11-30

        self.lastsql = sql_
        out1, out2 = self.exec_sql1(sql_, False)
        return self.table_check(tableName)

    def create_database(self, databaseName):
        # Execute sql_ code
        # Check if tableName exists
        # v1.0 2024-01-05

        sql_ = f'''CREATE DATABASE IF NOT EXISTS {databaseName};'''
        out1, out2 = self.exec_sql1(sql_, False)

        return out1, out2

    def table_raw(self, tableName):


        sql_=f'''
                    CREATE TABLE IF NOT EXISTS `see000Raw` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `idDevice` varchar(20) DEFAULT NULL,
                      `Date` datetime(6) DEFAULT NULL,
                      `idParam` varchar(20) DEFAULT NULL,
                      `Value` float(20,4) DEFAULT NULL,
                      `Delay` float DEFAULT NULL,
                      `Code` int DEFAULT NULL,
                      PRIMARY KEY (`idNum`),
                      UNIQUE KEY `NoDouble` (`idDevice`,`idParam`,`Date`,`Code`)
                    );  
                '''

        sql_=sql_.replace('see000Raw', tableName)

        return self.create_table(sql_, tableName)

    def table_devices(self, tableName):

        sql_ = f'''
        CREATE TABLE IF NOT EXISTS `see000Dev` (
          `idNum` int NOT NULL AUTO_INCREMENT,
          `idDevice` varchar(10) DEFAULT NULL,
          `Manufacturer` varchar(50) DEFAULT NULL,
          `Model` varchar(50) DEFAULT NULL,
          PRIMARY KEY (`idNum`),
          UNIQUE KEY `NoDouble` (`idDevice`)
        );
                '''

        sql_=sql_.replace('see000Dev', tableName)

        return self.create_table(sql_, tableName)

    def table_events(self, tableName):

        sql_ = f'''

                    CREATE TABLE IF NOT EXISTS `see000Events` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `Date` datetime(6) DEFAULT NULL,
                      `idEvent` char(10) DEFAULT NULL,
                      `setLimit` char(10) DEFAULT NULL,
                       `actValue` float null,
                      `Note` char(50) DEFAULT NULL,
                      PRIMARY KEY (`idNum`)
                    );  
                '''

        sql_=sql_.replace('see000Events', tableName)

        return self.create_table(sql_, tableName)

    def table_eventsLast(self, tableName):
        'v1.1 2024-01-05'

        sql_ = f'''

                    create table IF NOT EXISTS `see000EventsLast`
                    (
                        idNum    int auto_increment primary key,
                        Date     datetime null,
                        idEvent  char(50) null,
                        actValue float null,
                        `function` char(50) null,
                        setLimit float  null,
                        hyst     float  null,
                        Status   char(50) null,
                        upDown   char(50) null
                    );
                '''
        sql_=sql_.replace('see000EventsLast', tableName)

        return self.create_table(sql_, tableName)

    def table_rawLast(self, tableName):
        return self.table_raw(tableName)

    def table_eventsSys(self, tableName):

        sql_ = f'''
                CREATE TABLE IF NOT EXISTS `see000Sys` (
                  `idNum` int NOT NULL AUTO_INCREMENT,
                  `idGroup` char(10) DEFAULT NULL,
                  `idParam` char(10) DEFAULT NULL,
                  `Value` char(255) DEFAULT NULL,
                  `Description` char(255) DEFAULT NULL,
                  PRIMARY KEY (`idNum`)
                );
                '''
        sql_=sql_.replace('see000Sys', tableName)

        return self.create_table(sql_, tableName)

    def table_params(self, tableName):

        sql_ = f'''
                    CREATE TABLE IF NOT EXISTS `see000Params` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `idParam` varchar(10) DEFAULT NULL,
                      `descrITA` varchar(255) DEFAULT NULL,
                      `descrENG` varchar(255) DEFAULT NULL,
                      `um` varchar(10) DEFAULT NULL,
                      `Acronimo` varchar(30) DEFAULT NULL,
                      PRIMARY KEY (`idNum`),
                      UNIQUE KEY `NoDouble` (`idParam`)
                    )  ;
                '''
        sql_=sql_.replace('see000Params', tableName)

        return self.create_table(sql_, tableName)

    def table_machines(self, tableName):
        sql_ = f'''
                    CREATE TABLE IF NOT EXISTS `see000Mac` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `idMac` varchar(50) DEFAULT NULL,
                      `descrENG` varchar(255) DEFAULT NULL,
                      `descrITA` varchar(255) DEFAULT NULL,
                       PRIMARY KEY (`idNum`),
                      UNIQUE KEY `NoDouble` (`idMac`)
                    );
                '''
        sql_=sql_.replace('see000Mac', tableName)

        return self.create_table(sql_, tableName)

    def table_departments(self, tableName):
        sql_ = f'''
                    CREATE TABLE IF NOT EXISTS `see000Deps` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `idDep` varchar(10) DEFAULT NULL,
                      `descrENG` varchar(255) DEFAULT NULL,
                      `descrITA` varchar(255) DEFAULT NULL,
                       PRIMARY KEY (`idNum`),
                      UNIQUE KEY `NoDouble` (`idDep`)
                    );
                   '''

        sql_=sql_.replace('see000Deps', tableName)

        return self.create_table(sql_, tableName)

    def table_join(self, tableName):
        sql_ = f'''
                    CREATE TABLE IF NOT EXISTS `see000Join` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `idDevice` varchar(50) DEFAULT NULL,
                      `idMac` varchar(50) DEFAULT NULL,
                      `idDep` varchar(50) DEFAULT NULL,
                       PRIMARY KEY (`idNum`),
                       UNIQUE KEY `NoDouble` (`idDevice`,`idMac`,`idDep`)
                    );
                   '''
        sql_=sql_.replace('see000Join', tableName)

        return self.create_table(sql_, tableName)

    def table_SysSetRaw(self, tableName):
        sql_ = f'''
                    CREATE TABLE IF NOT EXISTS  `see000SysSetRaw` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `Date` varchar(16)DEFAULT NULL,
                      `idDevice` varchar(16) DEFAULT NULL,
                      `idParam` varchar(16) DEFAULT NULL,
                      `parDescr` varchar(120) DEFAULT NULL,
                      `parUm` varchar(16) DEFAULT NULL,
                      PRIMARY KEY (`idNum`),
                      UNIQUE KEY `NoDouble` (`Date`,`idDevice`,`idParam`,`parDescr`,`parUm`)
                    );  
                   '''
        sql_=sql_.replace('see000SysSetRaw', tableName)

        return self.create_table(sql_, tableName)

    def table_Sys(self, tableName):
        sql_ = f'''
                     CREATE TABLE IF NOT EXISTS  `see000Sys` (
                      `idNum` int NOT NULL AUTO_INCREMENT,
                      `idParam` varchar(16) DEFAULT NULL,
                      `Description` varchar(120) DEFAULT NULL,
                      `Value` varchar(120) DEFAULT NULL,
                      PRIMARY KEY (`idNum`),
                      UNIQUE KEY `NoDouble` (`idParam`)
                    );  
                   '''
        sql_=sql_.replace('see000Sys', tableName)

        return self.create_table(sql_, tableName)

    def params_Addparam(self, tableName , param):
        'ver 1.1 2023-05-06'

        sql_ = f'''
                    INSERT INTO see000Params(idParam, descrITA, descrENG, um, Acronimo)
                    VALUES  
                   '''
        sql_=sql_.replace('see000Params', tableName)

        if param =='Default':
            # clear table
            sql_clear = f'delete from {tableName} where idParam>1;'
            self.exec_sql1(sql_clear, False)
            print('> TabParams cleared ')

            #Load default parameter
            param = self.paramsAddDefault()

        sql_+= param
        return self.exec_sql1(sql_, False)

    def sysTable_Addparam(self, tableName , param):
        'ver 1.1 2023-05-06'
        sql_ = f'''
                    INSERT INTO see000Sys(idParam, Description, Value)
                    VALUES 
                   '''
        sql_=sql_.replace('see000Sys', tableName)

        if param =='Default':
            # clear table
            sql_clear = f'delete from {tableName} where idNum>0;'
            self.exec_sql1(sql_clear, False)
            print('> TabParams cleared ')

            #load default parameters
            param = self.sysTableAddDefault()

        sql_+= param
        return self.exec_sql1(sql_, False)

    def paramsAddDefault(self):
        return '''           
                ('100','Connessione del dispositivo','Device connection','na','dev_conn'),
                ('101','Tensione UL1_N','Voltage UL1_N','V','UL1_N'),
                ('102','Tensione UL2_N','Voltage UL2_N','V','UL2_N'),
                ('103','Tensione UL3_N','Voltage UL3_N','V','UL3_N'),
                ('104','Tensione UL1_L2','Voltage UL1_L2','V','UL1_L2'),
                ('105','Tensione UL2_L3','Voltage UL2_L3','V','UL2_L3'),
                ('106','Tensione UL3_L1','Voltage UL3_L1','V','UL3_L1'),
                ('107','Corrente L1','Current L1','A','IL1'),
                ('108','Corrente L2','Current L2','A','IL2'),
                ('109','Corrente L3','Current L3','A','IL3'),
                ('110','Potenza apparente L1','Apparent Power L1','VA','S_L1'),
                ('111','Potenza apparente L2','Apparent Power L2','VA','S_L2'),
                ('112','Potenza apparente L3','Apparent Power L3','VA','S_L3'),
                ('113','Potenza attiva L1','Active Power L1','W','P_L1'),
                ('114','Potenza attiva L2','Active Power L2','W','P_L2'),
                ('115','Potenza attiva L3','Active Power L3','W','P_L3'),
                ('116','Potenza reattiva L1','Reactive Power L1','VAr','Q_L1'),
                ('117','Potenza reattiva L2','Reactive Power L2','VAr','Q_L2'),
                ('118','Potenza reattiva L3','Reactive Power L3','VAr','Q_L3'),
                ('119','Fattore di potenza L1','Power Factor L1','na','PF_L1'),
                ('120','Fattore di potenza L2','Power Factor L2','na','PF_L2'),
                ('121','Fattore di potenza L3','Power Factor L3','na','PF_L3'),
                ('122','THD_R di tensione L1','THD_R  Voltage L1','%','VTHD_L1'),
                ('123','THD_R di tensione L2','THD_R  Voltage L2','%','VTHD_L2'),
                ('124','THD_R di tensione L3','THD_R  Voltage L3','%','VTHD_L3'),
                ('125','THD_R di corrente L1','THD_R  Current L1','%','ITHD_L1'),
                ('126','THD_R di corrente L2','THD_R  Current L2','%','ITHD_L2'),
                ('127','THD_R di corrente L3','THD_R  Current L3','%','ITHD_L3'),
                ('128','Frequency','Frequency','Hz','f'),
                ('129','Valore medio di tensione UL_N','Mean Value Voltage UL_N','V','Mean_UL_N'),
                ('130','Valore medio di tensione UL_L','Mean Value Voltage UL_L','V','Mean_UL_L'),
                ('131','Valore medio di corrente','Mean Value Current','A','Mean_I'),
                ('132','Potenza apparente totale','Apparent Power  - Total','VA','S_TOT'),
                ('133','Potenza attiva totale','Active Power  - Total','W','P_TOT'),
                ('134','Potenza reattiva totale','Reactive Power  - Total','VAr','Q_TOT'),
                ('135','Fattore di potenza totale','Power Factor  - Total','na','PF_TOT'),
                ('136','Asimmetria di tensione fase_fase','Asym.Factor - Voltage PH-PH','%','V_VASYM'),
                ('137','Asimmetria di ampiezza di corrente','Asym.Factor -  Current','%','IASYM'),
                ('138','Tensione UL1_N_max','Voltage UL1_N_max','V','Max_UL1_N'),
                ('139','Tensione UL2_N_max','Voltage UL2_N_max','V','Max_UL2_N'),
                ('140','Tensione UL3_N_max','Voltage UL3_N_max','V','Max_UL3_N'),
                ('141','Tensione UL1_L2_max','Voltage UL1_L2_max','V','Max_UL1_L2'),
                ('142','Tensione UL2_L3_max','Voltage UL2_L3_max','V','Max_UL2_L3'),
                ('143','Tensione UL3_L1_max','Voltage UL3_L1_max','V','Max_UL3_L1'),
                ('144','Corrente L1_max','Current L1_max','A','Max_IL1'),
                ('145','Corrente L2_max','Current L2_max','A','Max_IL2'),
                ('146','Corrente L3_max','Current L3_max','A','Max_IL3'),
                ('147','Potenza apparente L1_max','Apparent Power L1_max','VA','Max_S_L1'),
                ('148','Potenza apparente L2_max','Apparent Power L2_max','VA','Max_S_L2'),
                ('149','Potenza apparente L3_max','Apparent Power L3_max','VA','Max_S_L3'),
                ('150','Potenza attiva L1_max','Active Power L1_max','W','Max_P_L1'),
                ('151','Potenza attiva L2_max','Active Power L2_max','W','Max_P_L2'),
                ('152','Potenza attiva L3_max','Active Power L3_max','W','Max_P_L3'),
                ('153','Potenza reattiva L1_max','Reactive Power L1_max','VAr','Max_Q_L1'),
                ('154','Potenza reattiva L2_max','Reactive Power L2_max','VAr','Max_Q_L2'),
                ('155','Potenza reattiva L3_max','Reactive Power L3_max','VAr','Max_Q_L3'),
                ('156','Fattore di potenza L1_max','Power Factor L1_max','na','Max_PF_L1'),
                ('157','Fattore di potenza L2_max','Power Factor L2_max','na','Max_PF_L2'),
                ('158','Fattore di potenza L3_max','Power Factor L3_max','na','Max_PF_L3'),
                ('159','THD_R di tensione L1_max','THD_R  Voltage L1_max','%','Max_ITHD_L1'),
                ('160','THD_R di tensione L2_max','THD_R  Voltage L2_max','%','Max_ITHD_L2'),
                ('161','THD_R di tensione L3_max','THD_R  Voltage L3_max','%','Max_ITHD_L3'),
                ('162','THD_R di corrente L1_max','THD_R  Current L1_max','%','Max_VTHD_L1'),
                ('163','THD_R di corrente L2_max','THD_R  Current L2_max','%','Max_VTHD_L2'),
                ('164','THD_R di corrente L3_max','THD_R  Current L3_max','%','Max_VTHD_L3'),
                ('165','Frequency_max','Frequency_max','Hz','Max_F_Hz'),
                ('166','Valore medio di tensione UL_N_max','Mean Value Voltage UL_N_max','V','Mean_Max_UL_N'),
                ('167','Valore medio di tensione UL_L_max','Mean Value Voltage UL_L_max','V','Mean_Max_UL_L'),
                ('168','Valore medio di corrente_max','Mean Value Current_max','A','Mean_Max_I'),
                ('169','Potenza apparente totale_max','Apparent Power  - Total_max','VA','Max_S_TOT'),
                ('170','Potenza attiva totale_max','Active Power  - Total_max','W','Max_P_TOT'),
                ('171','Potenza reattiva totale_max','Reactive Power  - Total_max','VAr','Max_Q_TOT'),
                ('172','Fattore di potenza totale_max','Power Factor  - Total_max','na','Max_PF_TOT'),
                ('173','Tensione UL1_N_min','Voltage UL1_N_min','V','Min_UL1_N'),
                ('174','Tensione UL2_N_min','Voltage UL2_N_min','V','Min_UL2_N'),
                ('175','Tensione UL3_N_min','Voltage UL3_N_min','V','Min_UL3_N'),
                ('176','Tensione UL1_L2_min','Voltage UL1_L2_min','V','Min_UL1_L2'),
                ('177','Tensione UL2_L3_min','Voltage UL2_L3_min','V','Min_UL2_L3'),
                ('178','Tensione UL3_L1_min','Voltage UL3_L1_min','V','Min_UL3_L1'),
                ('179','Corrente L1_min','Current L1_min','A','Min_IL1'),
                ('180','Corrente L2_min','Current L2_min','A','Min_IL2'),
                ('181','Corrente L3_min','Current L3_min','A','Min_IL3'),
                ('182','Potenza apparente L1_min','Apparent Power L1_min','VA','Min_S_L1'),
                ('183','Potenza apparente L2_min','Apparent Power L2_min','VA','Min_S_L2'),
                ('184','Potenza apparente L3_min','Apparent Power L3_min','VA','Min_S_L3'),
                ('185','Potenza attiva L1_min','Active Power L1_min','W','Min_P_L1'),
                ('186','Potenza attiva L2_min','Active Power L2_min','W','Min_P_L2'),
                ('187','Potenza attiva L3_min','Active Power L3_min','W','Min_P_L3'),
                ('188','Potenza reattiva L1_min','Reactive Power L1_min','VAr','Min_Q_L1'),
                ('189','Potenza reattiva L2_min','Reactive Power L2_min','VAr','Min_Q_L2'),
                ('190','Potenza reattiva L3_min','Reactive Power L3_min','VAr','Min_Q_L3'),
                ('191','Fattore di potenza L1_min','Power Factor L1_min','na','Min_PF_L1'),
                ('192','Fattore di potenza L2_min','Power Factor L2_min','na','Min_PF_L2'),
                ('193','Fattore di potenza L3_min','Power Factor L3_min','na','Min_PF_L3'),
                ('194','Frequency_min','Frequency_min','Hz','Min_F_Hz'),
                ('195','Valore medio di tensione UL_N_min','Mean Value Voltage UL_N_min','V','Mean_Min_UL_N'),
                ('196','Valore medio di tensione UL_L_min','Mean Value Voltage UL_L_min','V','Mean_Min_UL_L'),
                ('197','Valore medio di corrente_min','Mean Value Current_min','A','Mean_Min_I'),
                ('198','Potenza apparente totale_min','Apparent Power  - Total_min','VA','Min_S_TOT'),
                ('199','Potenza attiva totale_min','Active Power  - Total_min','W','Min_P_TOT'),
                ('200','Potenza reattiva totale_min','Reactive Power  - Total_min','VAr','Min_Q_TOT'),
                ('201','Fattore di potenza totale_min','Power Factor  - Total_min','na','Min_PF_TOT'),
                ('202','Produzione attuale cumulata','Actual cumulated production','pieces','Prod_Act'),
                ('203','Produzione massima','Max lProduction limit','pieces','Prod_Max'),
                ('204','Produzione minima','Min Production Limit','pieces','Prod_Min'),
                ('205','Produzione scartata','Discarted Production','pieces','Prod_Disc'),
                ('206','Velocità di produzione','Production speed','pieces/min','Prod_Speed'),
                ('207','Contatore delle ore di esercizio ','Running time [h]','s','RunTime'),
                ('208','Contatore universale (programmabile)','Counter','na','Counter'),
                ('209','cosPhi L1','cosPhi L1','na','cosPhi1'),
                ('210','cosPhi L2','cosPhi L2','na','cosPhi2'),
                ('211','cosPhi L3','cosPhi L3','na','cosPhi3'),
                ('212','Potenza Attiva Importata media di periodo','Active Power - Imported Mean Value','na','Mean_P_Imp'),
                ('213','Potenza Reattiva Importata  media di periodo','Reactive Powe r- Imported Mean Value','VAr','Mean_Q_Imp'),
                ('214','Potenza Attiva Esportata media di periodo','Active Power- Exported Mean Value','W','Mean_P_Exp'),
                ('215','Potenza Reattiva Esportata media di periodo','Reactive Power - Exported Mean Value','VAr','Mean_Q_Exp'),
                ('216','Potenza Attiva Importata Massima di periodo','Active Power Imported - Max Period Value','W','Max_P_Period'),
                ('217','Potenza Attiva Importata Minima di periodo','Active Power Imported - Min Period Value','W','Min_P_Period'),
                ('218','Potenza Reattiva Importata Massima di periodo','Reactive Power Imported - Max Period Value','VAr','Max_Q_Period'),
                ('219','Potenza Reattiva Importata Minima di periodo','Reactive Power Imported - Min Period Value','VAr','Min_Q_Period'),
                ('220','Contatore universale (programmabile)','Counter','na','Univ_counter'),
                ('222','Energia Attiva importata','Active Energy Imported ','Wh','EnP_Imp_Tar1'),
                ('223','Energia Attiva importata Tariffa 2','Active Energy Imported - Tariff 2','Wh','EnP_Imp_Tar2'),
                ('224','Energia Attiva esportata','Active Energy Exported  ','Wh','EnP_Exp_Tar1'),
                ('225','Energia Attiva esportata Tariffa 2','Active Energy Exported  - Tariff 2','Wh','EnP_Exp_Tar2'),
                ('226','Energia Reattiva importata','Reactive Energy Imported','VArh','EnQ_Imp_Tar1'),
                ('227','Energia Reattiva importata Tariffa 2','Reactive Energy Imported - Tariff 2','VArh','EnQ_Imp_Tar2'),
                ('228','Energia Reattiva esportata','Reactive Energy Exported','VArh','EnQ_Exp_Tar1'),
                ('229','Energia Reattiva esportata Tariffa 2','Reactive Energy Exported - Tariff 2','VArh','EnQ_Exp_Tar2'),
                ('230','Energia apparente Tariffa 1 ','Apparent Energy','VAh','EnS'),
                ('231','Contaore di misura','Hour counter of measurement time','0,1h',''),
                ('232','Tipo di connessione','Connectionn type','na',''),
                ('233','Voltage measurement using TV?','Voltage measurement using TV?','na',''),
                ('234','Primary voltage ','Primary voltage ','V',''),
                ('235','Secondary voltage','Secondary voltage','V',''),
                ('236','Current measurement using current transducers?','Current measurement using current transducers?','na',''),
                ('237','Primary current','Primary current','A',''),
                ('238','Secondary current 1A, 5A','Secondary current 1A, 5A','A',''),
                ('239','Invert CT poloarity? ','Invert CT poloarity? ','na',''),
                ('240','Not used','Not used','na',''),
                ('241','Zero point suppression level (% rated current)','Zero point suppression level (% rated current)','na',''),
                ('242','Demand Period ','Demand Period ','na',''),
                ('243','Synchronization via bus 1: yes','Synchronization via bus 1: yes','na',''),
                ('244','Asimmetria di tensione fase_neutro','Asym.FactorVoltage fase_neutro','%','V_NASYM'),
                ('245','THD_R di tensione L1_L2','THD_R Voltage L1_L2','%','VTHD_L1_L2'),
                ('246','THD_R di tensione L2_L3','THD_R Voltage L2_L3','%','VTHD_L2_L3'),
                ('247','THD_R di tensione L3_L1','THD_R Voltage L3_L1','%','VTHD_L3_L1'),
                ('248','Reset Maximum values =0','Reset Maximum values =1','na',''),
                ('249','Reset minimum values =0','Reset minimum values =1','na',''),
                ('250','Reset energy counter (0 =all)','Reset energy counter (0 =all)','na',''),
                ('251','Synchronization of the demand period = Demand Period','Synchronization of the demand period = Demand Period','na',''),
                ('252','Switching tariff (0= On peak ; 1= Off peak)','Switching tariff (0= On peak ; 1= Off peak)','na',''),
                ('253','Acknowledge the diagnostics bit (cf. stored bits in 205)','Acknowledge the diagnostics bit (cf. stored bits in 205)','na',''),
                ('254','Switching outputs','Switching outputs','na',''),
                ('255','Switching command for vector group','Switching command for vector group','na',''),
                ('256','Activation of a changed IP configuration','Activation of a changed IP configuration','na',''),
                ('257','IP address','IP address','na',''),
                ('258','Subnet mask','Subnet mask','na',''),
                ('259','Gateway','Gateway','na',''),
                ('260','Angolo sfasamento V1_I1','Angolo sfasamento V1_I1','°','Ang_1'),
                ('261','Angolo sfasamento V2_I2','Angolo sfasamento V2_I2','°','Ang_2'),
                ('262','Angolo sfasamento V3_I3','Angolo sfasamento V3_I3','°','Ang_3'),
                ('263','Corrente Neutro','Current Neutro','A','I_N'),
                ('264','Energia Attiva Importata parziale','Energia Attiva Importata parziale','Wh',''),
                ('265','Energia Attiva Esportata parziale','Energia Attiva Esportata parziale','Wh',''),
                ('266','Energia Reattiva Importata parziale','Energia Reattiva Importata parziale','Varh',''),
                ('267','Energia Reattiva Esportata parziale','Energia Reattiva Esportata parziale','Varh',''),
                ('268','Energia Apparente parziale','Energia Apparente parziale','VAh',''),
                ('269','Reset contaore','Reset contaore','na',''),
                ('270','Segno Potenza Attiva (1=ind_2 = cap)','Segno Active Power (1=ind_2 = cap)','na',''),
                ('271','Segno Potenza Reattiva  (1=ind_2 = cap)','Segno Reactive Power  (1=ind_2 = cap)','na',''),
                ('272','Timer','Timer','s',''),
                ('273','Settore Fattore di potenza (0: PF=0,1;1:ind;2:cap)','Settore Power Factor (0: PF=0,1;1:ind;2:cap)','na',''),
                ('274','Segno Potenza Attiva L1','Segno Active Power L1','na',''),
                ('275','Segno Potenza Attiva L2','Segno Active Power L2','na',''),
                ('276','Segno Potenza Attiva L3','Segno Active Power L3','na',''),
                ('277','Segno Potenza Reattiva L1','Segno Reactive Power L1','na',''),
                ('278','Segno Potenza Reattiva L2','Segno Reactive Power L2','na',''),
                ('279','Segno Potenza Reattiva L3','Segno Reactive Power L3','na',''),
                ('280','Corrente L1_mean','Current L1_mean','A',''),
                ('281','Corrente L2_mean','Current L2_mean','A',''),
                ('282','Corrente L3_mean','Current L3_mean','A',''),
                ('283','cosPHI L1_max','cosPHI L1_max','na',''),
                ('284','cosPHI L2_max','cosPHI L2_max','na',''),
                ('285','cosPHI L3_max','cosPHI L3_max','na',''),
                ('286','Rapporto trasformazione TA','Rapporto trasformazione TA','na',''),
                ('287','Rapporto trasformazione TV','Rapporto trasformazione TV','na',''),
                ('288','Energia attiva importata fase 1','Energia attiva importata fase 2','Wh',''),
                ('289','Energia attiva esportata fase 1','Energia attiva esportata fase 2','Wh',''),
                ('290','Energia attiva importata fase 2','Energia attiva importata fase 3','Wh',''),
                ('291','Energia attiva esportata fase 2','Energia attiva esportata fase 3','Wh',''),
                ('292','Energia attiva importata fase 3','Energia attiva importata fase 4','Wh',''),
                ('293','Energia attiva esportata fase 3','Energia attiva esportata fase 4','Wh',''),
                ('294','Bilancio energie attive (imp_esp)','Bilancio energie attive (imp_esp)','',''),
                ('295','Bilancio energie reattive (imp_esp)','Bilancio energie reattive (imp_esp)','',''),
                ('296','Energia Capacitiva Importata','Energia Capacitiva Importata','Varh',''),
                ('297','Energia Capacitiva Esportata','Energia Capacitiva Esportata','Varh',''),
                ('298','Ordine delle fasi','Ordine delle fasi','na',''),
                ('299','THD_R di corrente In','THD_R di Current In','%','ITHD_In'),
                ('300','Impulsi En Attiva Esportata','Impulsi En Attiva Esportata','pulse','#505'),
                ('301','Impulsi En Attiva Importata','Impulsi En Attiva Importata','pulse','#505'),
                ('302','Impulsi En Reattiva Esportata','Impulsi En Reattiva Esportata','pulse','#505'),
                ('303','Impulsi En Reattiva Importata','Impulsi En Reattiva Importata','pulse','#505'),
                ('304','Asimmetria di tensione fase_fase_max','Asym.FactorVoltage fase_fase_max','%',''),
                ('305','Asimmetria di tensione fase_neutro_max','Asym.FactorVoltage fase_neutro_max','%',''),
                ('306','Asimmetria di ampiezza di corrente_max','Asym.Factorampiezza di Current_max','%',''),
                ('307','Corrente neutro_max','Current neutro_max','A',''),
                ('308','THD_R di tensione L1_L2_max','THD_R di Voltage L1_L2_max','%',''),
                ('309','THD_R di tensione L2_L3_max','THD_R di Voltage L2_L3_max','%',''),
                ('310','THD_R di tensione L3_L1_max','THD_R di Voltage L3_L1_max','%',''),
                ('311','cosPHI L1_min','cosPHI L1_min','na',''),
                ('312','cosPHI L2_min','cosPHI L2_min','na',''),
                ('313','cosPHI L3_min','cosPHI L3_min','na',''),
                ('314','Asimmetria di tensione fase_fase_min','Asym.FactorVoltage fase_fase_min','%',''),
                ('315','Asimmetria di tensione fase_neutro_min','Asym.FactorVoltage fase_neutro_min','%',''),
                ('316','Asimmetria di ampiezza di corrente_min','Asym.Factorampiezza di Current_min','%',''),
                ('317','Corrente neutro_min','Current neutro_min','A',''),
                ('318','THD_R di tensione L1_min','THD_R di Voltage L1_min','%',''),
                ('319','THD_R di tensione L2_min','THD_R di Voltage L2_min','%',''),
                ('320','THD_R di tensione L3_min','THD_R di Voltage L3_min','%',''),
                ('321','THD_R di corrente L1_min','THD_R di Current L1_min','%',''),
                ('322','THD_R di corrente L2_min','THD_R di Current L2_min','%',''),
                ('323','THD_R di corrente L3_min','THD_R di Current L3_min','%',''),
                ('324','THD_R di tensione L1_L2_min','THD_R di Voltage L1_L2_min','%',''),
                ('325','THD_R di tensione L2_L3_min','THD_R di Voltage L2_L3_min','%',''),
                ('326','THD_R di tensione L3_L1_min','THD_R di Voltage L3_L1_min','%',''),
                ('327','Tensione UL1_N_mean','Voltage UL1_N_mean','V',''),
                ('328','Tensione UL2_N_mean','Voltage UL2_N_mean','V',''),
                ('329','Tensione UL3_N_mean','Voltage UL3_N_mean','V',''),
                ('330','Tensione UL1_L2_mean','Voltage UL1_L2_mean','V',''),
                ('331','Tensione UL2_L3_mean','Voltage UL2_L3_mean','V',''),
                ('332','Tensione UL3_L1_mean','Voltage UL3_L1_mean','V',''),
                ('333','Potenza attiva L1_mean','Active Power L1_mean','W',''),
                ('334','Potenza attiva L2_mean','Active Power L2_mean','W',''),
                ('335','Potenza attiva L3_mean','Active Power L3_mean','W',''),
                ('336','Potenza reattiva L1_mean','Reactive Power L1_mean','VAr',''),
                ('337','Potenza reattiva L2_mean','Reactive Power L2_mean','VAr',''),
                ('338','Potenza reattiva L3_mean','Reactive Power L3_mean','VAr',''),
                ('339','Potenza apparente L1_mean','Apparent Power L1_mean','VA',''),
                ('340','Potenza apparente L2_mean','Apparent Power L2_mean','VA',''),
                ('341','Potenza apparente L3_mean','Apparent Power L3_mean','VA',''),
                ('342','Fattore di potenza L1_mean','Power Factor L1_mean','na',''),
                ('343','Fattore di potenza L2_mean','Power Factor L2_mean','na',''),
                ('344','Fattore di potenza L3_mean','Power Factor L3_mean','na',''),
                ('345','cosPHI L1_mean','cosPHI L1_mean','na',''),
                ('346','cosPHI L2_mean','cosPHI L2_mean','na',''),
                ('347','cosPHI L3_mean','cosPHI L3_mean','na',''),
                ('348','Frequency_mean','Frequency_mean','Hz',''),
                ('349','Valore medio di tensione UL_N_mean','Mean Value Voltage UL_N_mean','V',''),
                ('350','Valore medio di tensione UL_L_mean','Mean Value Voltage UL_L_mean','V',''),
                ('351','Valore medio di corrente_mean','Mean Value Current_mean','A',''),
                ('352','Potenza attiva totale_mean','Active Power  - Total_mean','W',''),
                ('353','Potenza reattiva totale_mean','Reactive Power  - Total_mean','VAr',''),
                ('354','Potenza apparente totale_mean','Apparent Power  - Total_mean','VA',''),
                ('355','Fattore di potenza totale_mean','Power Factor  - Total_mean','na',''),
                ('356','Asimmetria di tensione fase_fase_mean','Asym.FactorVoltage ph_ph_mean','%',''),
                ('357','Asimmetria di tensione fase_neutro_mean','Asym.FactorVoltage ph_neutral_mean','%',''),
                ('358','Asimmetria di ampiezza di corrente_mean','Asym.Factorampiezza di Current_mean','%',''),
                ('359','Corrente neutro_mean','Current - Neutral_mean','A',''),
                ('360','THD_R di tensione L1_mean','THD_R  Voltage L1_mean','%',''),
                ('361','THD_R di tensione L2_mean','THD_R  Voltage L2_mean','%',''),
                ('362','THD_R di tensione L3_mean','THD_R  Voltage L3_mean','%',''),
                ('363','THD_R di corrente L1_mean','THD_R  Current L1_mean','%',''),
                ('364','THD_R di corrente L2_mean','THD_R  Current L2_mean','%',''),
                ('365','THD_R di corrente L3_mean','THD_R  Current L3_mean','%',''),
                ('366','THD_R di tensione L1_L2_mean','THD_R  Voltage L1_L2_mean','%',''),
                ('367','THD_R di tensione L2_L3_mean','THD_R  Voltage L2_L3_mean','%',''),
                ('368','THD_R di tensione L3_L1_mean','THD_R  Voltage L3_L1_mean','%',''),
                ('370','Temperatura Valore n. 1 ','Temperature Value n. 1 ','°C',''),
                ('371','Temperatura Valore n. 2','Temperature Value n. 2','°C',''),
                ('372','Temperatura Valore n. 3','Temperature Value n. 3','°C',''),
                ('373','Temperatura Valore n. 4','Temperature Value n. 4','°C',''),
                ('374','Temperatura Valore n. 5','Temperature Value n. 5','°C',''),
                ('375','Temperatura Valore n. 6','Temperature Value n. 6','°C',''),
                ('376','Temperatura Valore n. 7','Temperature Value n. 7','°C',''),
                ('377','Temperatura Valore n. 8','Temperature Value n. 8','°C',''),
                ('378','Temperatura Valore n. 9','Temperature Value n. 9','°C',''),
                ('379','Temperatura Valore n. 10','Temperature Value n. 10','°C',''),
                ('380','Temperatura Valore n. 11','Temperature Value n. 11','°C',''),
                ('381','Temperatura Valore n. 12','Temperature Value n. 12','°C',''),
                ('382','Temperatura Valore n. 13','Temperature Value n. 13','°C',''),
                ('383','Temperatura Valore n. 14','Temperature Value n. 14','°C',''),
                ('384','Temperatura Valore n. 15','Temperature Value n. 15','°C',''),
                ('385','Temperatura Valore n. 16','Temperature Value n. 16','°C',''),
                ('390','Flusso gas 1','Gas Flux 1','kg/s',''),
                ('391','Flusso gas 2','Gas Flux 2','kg/s',''),
                ('392','Flusso gas 3','Gas Flux 3','kg/s',''),
                ('393','Flusso gas 4','Gas Flux 4','kg/s',''),
                ('394','Flusso gas 5','Gas Flux 5','kg/s',''),
                ('395','Flusso gas 6','Gas Flux 6','kg/s',''),
                ('396','Flusso gas 7','Gas Flux 7','kg/s',''),
                ('397','Flusso gas 8','Gas Flux 8','kg/s',''),
                ('398','Flusso gas 9','Gas Flux 9','kg/s',''),
                ('399','Flusso gas 10','Gas Flux 10','kg/s',''),
                ('400','Flusso gas 11','Gas Flux 11','kg/s',''),
                ('401','Flusso gas 12','Gas Flux 12','kg/s',''),
                ('402','Flusso gas 13','Gas Flux 13','kg/s',''),
                ('403','Flusso gas 14','Gas Flux 14','kg/s',''),
                ('404','Flusso gas 15','Gas Flux 15','kg/s',''),
                ('405','Flusso gas 16','Gas Flux 16','kg/s',''),
                ('500','H_in_tot_cum ','H_in_tot_cum ','J',''),
                ('501','H_out_tot_cum ','H_out_tot_cum ','J',''),
                ('502','H_tot_cum ','H_tot_cum ','J',''),
                ('503','Hex_in_tot_cum ','Hex_in_tot_cum ','J',''),
                ('504','Hex_out_tot_cum ','Hex_out_tot_cum ','J',''),
                ('505','Hex_tot_cum ','Hex_tot_cum ','J',''),
                ('506','Ex_in_tot_cum ','Ex_in_tot_cum ','J',''),
                ('507','Ex_out_tot_cum ','Ex_out_tot_cum ','J',''),
                ('508','Ex_tot_cum ','Ex_tot_cum ','J',''),
                ('509','S_in_tot_cum ','S_in_tot_cum ','J',''),
                ('510','S_out_tot_cum ','S_out_tot_cum ','J',''),
                ('511','S_tot_cum ','S_tot_cum ','J',''),
                ('512','el_in_tot_cum ','el_in_tot_cum ','J',''),
                ('513','el_out_tot_cum ','el_out_tot_cum ','J',''),
                ('514','el_tot_cum ','el_tot_cum ','J',''),
                ('515','En_in_tot_cum ','En_in_tot_cum ','J',''),
                ('516','En_out_tot_cum ','En_out_tot_cum ','J',''),
                ('517','En_tot_cum ','En_tot_cum ','J',''),
                ('518','Ex_out_net_cum ','Ex_out_net_cum ','J',''),
                ('519','Ex_loss_cum ','Ex_loss_cum ','J',''),
                ('520','S_el_tot_cum ','S_el_tot_cum ','J',''),
                ('521','En_eff_cum ','En_eff_cum ','na',''),
                ('522','Ex_gen_eff_cum ','Ex_gen_eff_cum ','na',''),
                ('523','Ex_net_eff_cum','Ex_net_eff_cum','na','');
                '''

    def sysTableAddDefault(self):
        txt_='''
                ('emailEvents','Events Manager email','frlovecchio@gmail.com'),
                ('yearRaw','Table Raw year' ,'2022');
                '''
        actYear = datetime.now().year
        return txt_.replace('2022', str(actYear))

    def create_newYear(self, tableName, flag_):
        # Create new year table: tablename_year
        # flag_ 1: create new table
        # v1.0 2022-11-30

        flag1 = False
        flag2 = False

        TimeNow = datetime.utcnow()
        tZone = self.configMysql['tZone']
        if tZone != '':
            date_0 = utctime_to_tZone(TimeNow, tZone)
            year_ = date_0.year
        else:
            year_ = TimeNow.year

        ck_table = self.table_check(tableName)
        ck_table_year_1 = self.table_check(tableName + '_' + str(year_-1))

        if flag_:
            if ck_table and not(ck_table_year_1):
                sql_1 = 'RENAME TABLE {0}.{1} TO {0}.{2} ;'.format(
                    self.configMysql['database'],
                    tableName,
                    tableName+'_'+str(year_-1),
                    )
                #rename table
                flag1 = self.create_table(sql_1, tableName+'_' + str(year_-1))

                #create new table
                if flag1:
                    if 'Raw'.lower() in tableName.lower():
                        flag2 = self.table_raw(tableName)

        return flag1 and flag2

    def create_all(self):
        'v1.1 2023-05-06'
        'v1.2 2024-01-05'

        try:
            self.create_database(self.configMysql['database'])
            print(f'''> Database {self.configMysql['database']} created''')
        except:
            print(f'''> Database {self.configMysql['database']} NOT created''')
            pass

        self.table_raw(self.configMysql['tableRaw'])
        print('> Table tableRaw created' )
        self.table_events(self.configMysql['tableEvents'])
        print('> Table tableEvents created')
        self.table_eventsLast(self.configMysql['tableEventsLast'])
        print('> Table tableEventsLast created')
        self.table_rawLast(self.configMysql['tableLast'])
        print('> Table tableLast created')
        self.table_Sys(self.configMysql['tableSys'])
        print('> Table tableSys created')
        self.table_SysSetRaw(self.configMysql['tableSysRaw'])
        print('> Table tableSysRaw created')
        self.table_eventsSys(self.configMysql['tableEventsSys'])
        print('> Table tableEventsSys created')
        self.table_params(self.configMysql['tableParams'])
        print('> Table tableParams created')
        self.table_machines(self.configMysql['tableMac'])
        print('> Table tableMac created')
        self.table_departments(self.configMysql['tableDeps'])
        print('> Table tableDeps created')
        self.table_join(self.configMysql['tableJoin'])
        print('> Table tableJoin created')

        try:
            self.sysTable_Addparam(self.configMysql['tableSys'],'Default')
            print('> Table see000Sys - Added default parameters')
        except:
            print('[msg] - see_db - error in creating table sysTable_Addparam()')

        try:
            self.params_Addparam(self.configMysql['tableParams'], 'Default')
            print('> Table TabParams - Added default parameters')
        except:
            print('[msg] - see_db - error in creating table params_Addparam()')