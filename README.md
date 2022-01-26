Su.S.E.E. - SUpervisor System for Energy Efficiency

SUSEE has been developed to support Energy Managers to implement ISO 50001 Energy Management Systems, and Energy Audit.
The Python script is able to read data from any Modbus device at fixed sampling time, transform and store data in a database. 

The main characteristics are:
- OS: Linux Debian >= 9.0
- Python >= 3.5
- Compatible with any Modbus RTU/TCP devices 
- Free sampling time > 1s
- Data quality control
- Time sample delay control

Install
------------
$ pip install susee

Usage
-----------
>Default Device
- The testing script 'see_etl.py' performs energy data acquisition from the SIEMENS SENTRON PAC3200 Power Meter.

>List of parameters 
- The standard list of electrical parameters acquired at each sampling time is:
        
        n.    paramID    Description     unit
        __________________________________________
        # 1  - 104      Voltage  L1L2   [V]
        # 2  - 107      Current L1      [A]
        # 8  - 132      Total Apparent Power [VA]
        # 9 -  133      Total Active Power [W]
        # 10 - 134      Total Reactive Power  [VAr]
        # 11 - 135      PF Power Factor
        # 12 - 222      Imported Active Energy [Wh]
        # 13 - 226      Imported Reactive Energy [VArh]


>Database Tables
- The acquired data are read from the device's Modbus TCP port and stored in a MariaDB database.
  - Default jobID: 000 
  - Default Database name: seedb000
  - Tables: see000Raw, see000Last, see000Params



    n.   Table          Description
    ------------------------------------------------
    1   see000Raw      Read data 
    2   see000Last     Last sampled data
    3   see000Params   Tables of parameters    



  Tables: see000Raw, see000Last
  
    Columns:
    -idNum int(12) AI PK 
    -idDevice varchar(20) 
    -Date datetime(6) 
    -idParam varchar(20) 
    -Value float(20,4) 
    -Delay float 
    -Code int(11)
    
    The 'Code' fields is a data's quality parameter
    Code = {
          'err_connection'    :  1,
          'driver error'      :  2,    
          'server_off'        :  4,   
          'err_register'      :  8,
          'value_NaN'         :  16,
          'lenreg_zero'       :  32,
          'driver not found'  :  64,
          }

  Table: see000Params
  - --------------------------------
    Columns:
            idNum int(12) AI PK 
            idParam varchar(10) 
            descrITA varchar(255) 
            descrENG varchar(255) 
            um varchar(10) 
            Acronimo varchar(30)

    idParam  descrITA                    descrENG        um    Acronimo
    -------------------------------------------------------------------------
    104	  Tensione UL1_L2	            Voltage UL1_L2	V	UL1_L2
    107	  Corrente L1	                Current L1	A	IL1
    132	  Potenza apparente totale	    Apparent Power  - Total	VA	S_TOT
    133	  Potenza attiva totale     	Active Power  - Total	W	P_TOT
    134	  Potenza reattiva totale	    Reactive Power  - Total	VAr	Q_TOT
    135	  Fattore di potenza totale	    Power Factor  - Total	na	PF_TOT
    222	  Energia Attiva importata	    Active Energy Imported 	Wh	EnP_Imp_Tar1
    226	  Energia Reattiva importata	Reactive Energy Imported	VArh	EnQ_Imp_Tar1
                            

How to run the script
-------------------------------
- Setup the above MariaDB database structure
- Put the following reserved info in a .env file 
  - user_db = 'username' 
  - pswd_db = 'password!'
  - port_db = '3306' 
  - host_db = 'xxx.xxx.xxx.xxx'
- Connect a SIEMENS PAC3200 device in your local network
- Set the desired sampletime in etl_data.py (default smpletime: 10 s)
- Set the PAC3200 ip address in etl_data.py (default ip: 192.168.1.100)
- run: 
    $ python see_etl.py -d eft_data.py
- check if raw data have been stored in tha see000Raw database table


    idNum   idDevice    Date                         idParam     Value       Delay   Code
    -----------------------------------------------------------------------------------------
    398882	d00	        2021-02-18 10:30:00.000000	104	     395.1900	178.778	0
    398883	d00	        2021-02-18 10:30:00.000000	105	     393.3600	178.778	0
    398884	d00	        2021-02-18 10:30:00.000000	106	     397.6700	178.778	0


Contribute
--------------
Your contribution is welcome. 

License
-------------
The MIT License (MIT)
