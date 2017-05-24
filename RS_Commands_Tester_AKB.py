# -*- coding: utf-8 -*-

import serial
import Tester_AKB

class RS_Commands_Tester_AKB(object):

    def __init__(self, in_app : Tester_AKB):
        self.app = in_app

    #*********************************************************************
    # определение свободных COM портов
    #*********************************************************************
    def scan_COM_ports(self):
        """scan for available ports. return a list of tuples (num, name)"""
        #перечень доступных портов
        available = []
        for i in range(self.app.NUMBER_SCAN_PORTS):
            try:
                s = serial.Serial(i)
                available.append((s.portstr))
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available


    def Init_RS_Var(self, baudrate):
        '''
        Первичная инициализация переменных для RS
        :param baudrate:
        :return None:
        '''
        if baudrate == 115200:
            self.time_to_rx = 20#
        elif baudrate == 57600:
            self.time_to_rx = 40#
        elif baudrate == 38400:
            self.time_to_rx = 60#
        elif baudrate == 19200:
            self.time_to_rx = 100#
        elif baudrate == 9600:
            self.time_to_rx = 150#
        elif baudrate == 1200:
            self.time_to_rx = 1200#
        #начальные данные для передатчика
        self.rs_start = bytearray([0x55])   #стартовая последовательность для RS
        self.pack_size_TX = 0    #размер передаваемого пакета в байтах
        self.pack_seq_TX = 0     #номер пакета в последовательности
        self.cmd_tx = 0           #ID1 передаваемой команды
        self.num_chnl_tx = 0           #ID2 передаваемой команды
        self.DATA_TX = bytearray([0x00]) #данные для передачи
        #начальные данные для приемника
        self.pack_size_RX = 0    #размер принятого пакета в байтах
        self.pack_seq_RX = 0     #номер принятого пакета в последовательности
        self.ID_RX = 0           #ID принятой команды


    def Serial_Config(self, baudrate, nom_com):
        '''#*********************************************************************
        # настройка порта nom_com на скорость baudrate
        # {int} [baudrate] - скорость работы порта
        # {str} [nom_com] - номер ком порта
        #*********************************************************************'''
        self.ser = serial.Serial(nom_com,#'COM25',
                    baudrate=baudrate,#9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=0,
                    bytesize=serial.EIGHTBITS,
                    xonxoff=0)


    def Serial_Close(self):
        '''
        #*********************************************************************
        # закрыть порт
        #*********************************************************************
        :return:
        '''
        if self.ser.isOpen():
            self.ser.close()


    def Transmit_RS_Data (self):
        '''
        #*********************************************************************
        # передача пакета в RS
        #*********************************************************************
        :return:
        '''
        if self.ser.isOpen():
            #полезные данные для передачи
            useful_data =   self.cmd_tx.to_bytes(1,'little') + \
                            self.num_chnl_tx.to_bytes(1,'little') + \
                            self.num_relay_tx.to_bytes(1,'little') + \
                            self.num_chnl_1_tx.to_bytes(1,'little') + \
                            self.num_chnl_2_tx.to_bytes(1,'little') + \
                            self.mode_tx.to_bytes(1,'little') + \
                            self.time_tx.to_bytes(1,'little')
            # все данные для передачи
            self.rs_send_pack = self.rs_start + \
                                useful_data
            self.ser.write(self.rs_send_pack)
            if self.app.MODE == 'TEST':
                self.app.event.Show_TX_DATA(self.rs_send_pack)
            return 'Ok'


    def Recieve_RS_Data(self):
        '''
        #*********************************************************************
        #проверка наличия данных в буфере RS
        #*********************************************************************
        :return:
        '''
        RX_Data = ''  #данных нет
        while self.ser.inWaiting() > 0:
            RX_Data = self.ser.read(self.app.MAX_WAIT_BYTES)
        return RX_Data


    def Send_Command_AKB(self, cmd_tx, num_chnl_tx = 0, num_relay_tx = 0, num_chnl_1_tx = 0, num_chnl_2_tx = 0, mode_tx = 2, time_tx = 1):
        '''
        #*********************************************************************
        # отправить запрос "обнуление каналов"
        #*********************************************************************
        :param cmd_tx:
        :param num_chnl_tx:
        :param num_relay_tx:
        :param num_chnl_1_tx:
        :param num_chnl_2_tx:
        :param mode_tx:
        :param time_tx:
        :return:
        '''
        self.app.Set_Status_AKB(cmd_tx)
        self.cmd_tx = cmd_tx
        self.num_chnl_tx = num_chnl_tx
        self.num_relay_tx = num_relay_tx
        self.num_chnl_1_tx = num_chnl_1_tx
        self.num_chnl_2_tx = num_chnl_2_tx
        self.mode_tx = mode_tx
        self.time_tx = time_tx
        self.Transmit_RS_Data() #передаем данные в порт
        return
