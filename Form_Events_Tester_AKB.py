import Tester_AKB
from PyQt5 import QtWidgets

class Form_Events_Tester_AKB(object):

    def __init__(self, main_app: Tester_AKB):
        self.app = main_app


    def Init_Widgets(self):
        '''
        #настройка действий по кнопкам
        :return:
        '''
        #настройка списка для выбора порта
        self.app.ui.comboBox_COM.addItems(self.app.rs.scan_COM_ports())
        self.app.ui.comboBox_COM.setCurrentIndex(0)
        #добавляем нужные скорости в comboBox_Baudrate
        self.app.ui.comboBox_Baudrate.addItems(self.app.BAUDRATES)
        self.app.ui.comboBox_Baudrate.setCurrentIndex(1)        #добавляем нужные скорости в comboBox_Baudrate
        #добавляем номера каналов в comboBox_Clear_Channels
        ch_list = [str(list_item) for list_item in range(1,21)]
        ch_list += ['Все']
        self.app.ui.comboBox_Clear_Channels.addItems(ch_list)
        self.app.ui.comboBox_Clear_Channels.setCurrentIndex(20)
        #добавляем номера реле в comboBox_Rele_Number
        ch_list = ['Выкл', '1', '2']
        self.app.ui.comboBox_Rele_Number.addItems(ch_list)
        self.app.ui.comboBox_Rele_Number.setCurrentIndex(1)

        #добавляем номера реле в comboBox_Rele_Contr_1
        self.Set_Value_comboBox(self.app.ui.comboBox_Rele_Contr_1, add_item = '1-10', exclude = '2')
        self.app.ui.comboBox_Rele_Contr_1.setCurrentIndex(0)
        #добавляем номера реле в comboBox_Rele_Contr_2
        self.Set_Value_comboBox(self.app.ui.comboBox_Rele_Contr_2, exclude = self.app.ui.comboBox_Rele_Contr_1.currentText())
        self.app.ui.comboBox_Rele_Contr_1.setCurrentIndex(0)

        #добавляем номера реле в comboBox_Time_Charge
        ch_list = [str(list_item) for list_item in range(1,101)]
        self.app.ui.comboBox_Time_Charge.addItems(ch_list)
        self.app.ui.comboBox_Time_Charge.setCurrentIndex(0)

        # обработчики для кнопок
        self.app.ui.pushButton_open_COM.clicked.connect(self.pb_Open_COM_Header)
        self.app.ui.pushButton_close_COM.clicked.connect(self.pb_Close_COM_Header)
        self.app.ui.pushButton_Clear_Channels.clicked.connect(self.pb_Clear_Channels_Header)
        self.app.ui.pushButton_Start_Polling.clicked.connect(self.pb_Start_Polling_Header)
        self.app.ui.pushButton_Stop_Polling.clicked.connect(self.pb_Stop_Polling_Header)
        self.app.ui.pushButton_Set_Params.clicked.connect(self.pb_Set_Params_Header)
        self.app.ui.comboBox_Rele_Contr_1.currentIndexChanged.connect(self.Rele_Contr_1_Header)
        self.app.ui.comboBox_Rele_Number.currentIndexChanged.connect(self.Rele_Number_Header)


    def Set_Value_comboBox(self, cb_Name, add_item = None, exclude = None):
        #добавляем номера реле в comboBox_Rele_Contr_x
        cb_Name.clear()
        ch_list = [str(list_item) for list_item in range(1,21)]
        if add_item:
            ch_list += [add_item]
        if exclude in ch_list:
            ch_list.remove(exclude)
        cb_Name.addItems(ch_list)


    def Enable_Widgets(self):
        '''
        #*********************************************************************
        # активация кнопок после выбора порта и скорости
        #*********************************************************************
        :return:
        '''
        self.app.ui.pushButton_Clear_Channels.setEnabled(1)
        self.app.ui.pushButton_open_COM.setDisabled(1)
        self.app.ui.pushButton_close_COM.setEnabled(1)
        self.app.ui.comboBox_Clear_Channels.setEnabled(1)
        self.app.ui.pushButton_Start_Polling.setEnabled(1)
        self.Enable_Set_Params()


    def Enable_Set_Params(self):
        self.app.ui.comboBox_Rele_Number.setEnabled(1)
        self.app.ui.comboBox_Time_Charge.setEnabled(1)
        self.app.ui.comboBox_Rele_Contr_1.setEnabled(1)
        self.app.ui.comboBox_Rele_Contr_2.setEnabled(1)
        self.app.ui.radioButton_First_Rele.setEnabled(1)
        self.app.ui.radioButton_All_Rele.setEnabled(1)
        self.app.ui.radioButton_All_Rele.setChecked(1)
        self.app.ui.pushButton_Set_Params.setEnabled(1)


    def Disable_Widgets(self):
        '''
        #*********************************************************************
        # активация кнопок после выбора порта и скорости
        #*********************************************************************
        :return:
        '''
        self.app.ui.pushButton_Clear_Channels.setDisabled(1)
        self.app.ui.pushButton_open_COM.setEnabled(1)
        self.app.ui.pushButton_close_COM.setDisabled(1)
        self.app.ui.comboBox_Clear_Channels.setDisabled(1)
        self.app.ui.pushButton_Start_Polling.setDisabled(1)
        self.app.ui.pushButton_Stop_Polling.setDisabled(1)
        self.Disable_Set_Params()


    def Disable_Set_Params(self):
        self.app.ui.comboBox_Rele_Number.setDisabled(1)
        self.app.ui.comboBox_Time_Charge.setDisabled(1)
        self.app.ui.comboBox_Rele_Contr_1.setDisabled(1)
        self.app.ui.comboBox_Rele_Contr_2.setDisabled(1)
        self.app.ui.radioButton_First_Rele.setDisabled(1)
        self.app.ui.radioButton_All_Rele.setDisabled(1)
        self.app.ui.pushButton_Set_Params.setDisabled(1)


    def pb_Open_COM_Header(self):
        '''
        :return:
        '''
        self.app.ui.comboBox_COM.setDisabled(1)
        self.app.ui.comboBox_Baudrate.setDisabled(1)
        baudrate = int(self.app.ui.comboBox_Baudrate.currentText())
        nom_com_port = self.app.ui.comboBox_COM.currentText()
        # конфигурируем RS
        self.app.rs.Serial_Config(baudrate, nom_com_port)
        self.app.rs.Init_RS_Var(baudrate)
        # изменяем видимость кнопок
        self.Enable_Widgets()


    def pb_Close_COM_Header(self):
        '''
        #*********************************************************************
        # активация кнопок после выбора порта и скорости
        #*********************************************************************
        :return:
        '''
        # self.pb_Stop_Polling_Header()
        self.app.rs.Recieve_RS_Data()
        # закрываем порт
        self.app.rs.Serial_Close()
        self.app.ui.comboBox_COM.setDisabled(1)
        self.app.ui.comboBox_Baudrate.setDisabled(1)
        self.app.ui.comboBox_COM.setEnabled(1)
        self.app.ui.comboBox_Baudrate.setEnabled(1)
        # изменяем видимость кнопок
        self.Disable_Widgets()


    def pb_Clear_Channels_Header(self):
        '''
        #*********************************************************************
        # обраотка кнопки обнулить счетчики - pushButton_Clear_Channels
        #*********************************************************************
        :return:
        '''
        num_chnl = self.app.ui.comboBox_Clear_Channels.currentText()
        if num_chnl != 'Все':
            num_chnl = int(num_chnl)
        else:
            num_chnl = 0
        # отправить "Обнуление каналов"
        self.app.rs.Send_Command_AKB(self.app.cur_cmd['CLEAR'], num_chnl)
        #запускаем таймер до отправки
        self.app.timer_RX_RS.start(self.app.rs.time_to_rx, self.app) #отправляем запрос защитного кода через self.time_to_rx мс
        return 'Ok'


    def pb_Start_Polling_Header(self):
        '''
        #*********************************************************************
        # обраотка кнопки запуск опроса каналов - pushButton_Start_Polling
        #*********************************************************************
        :return:
        '''
        # начинаем опрос с первого канала
        num_chnl = 1
        self.app.Set_Status_AKB(self.app.cur_cmd['CHECK'])
        # отправить "Обнуление каналов"
        self.app.rs.Send_Command_AKB(self.app.cur_cmd['CHECK'], num_chnl)
        #запускаем таймер ожидания ответа
        self.app.timer_RX_RS.start(self.app.rs.time_to_rx, self.app)
        self.app.ui.pushButton_Start_Polling.setDisabled(1)
        self.app.ui.pushButton_close_COM.setDisabled(1)
        self.app.ui.pushButton_Clear_Channels.setDisabled(1)
        self.app.ui.pushButton_Stop_Polling.setEnabled(1)
        # выключаем все
        self.Disable_Set_Params()
        return 'Ok'


    def pb_Stop_Polling_Header(self):
        '''
        #*********************************************************************
        # обраотка кнопки остановка опроса каналов - pushButton_Stop_Polling
        #*********************************************************************
        :return:
        '''
        self.Enable_Set_Params()
        self.Rele_Number_Header()
        self.app.ui.pushButton_Start_Polling.setEnabled(1)
        self.app.ui.pushButton_Clear_Channels.setEnabled(1)
        self.app.ui.pushButton_Stop_Polling.setDisabled(1)
        self.app.ui.pushButton_close_COM.setEnabled(1)
        self.app.Set_Status_AKB(self.app.cur_cmd['IDLE'])


    def pb_Set_Params_Header(self):
        '''
        обработчик нажатия кнопки "установить параметры"
        :return:
        '''
        self.app.Set_Status_AKB(self.app.cur_cmd['RELE'])
        t_num_rele = 0 if self.app.ui.comboBox_Rele_Number.currentIndex() == 0 else self.app.ui.comboBox_Rele_Number.currentIndex()
        t_ch_1 = int(self.app.ui.comboBox_Rele_Contr_1.currentText())\
            if (self.app.ui.comboBox_Rele_Contr_1.currentIndex()+1) < self.app.ui.comboBox_Rele_Contr_1.count()\
            else 0
        t_ch_2 = int(self.app.ui.comboBox_Rele_Contr_2.currentText()) if t_ch_1 != 0 else 0
        t_mod = 1 if self.app.ui.radioButton_First_Rele.isChecked() == True else 2
        # отправить "Обнуление каналов"
        self.app.rs.Send_Command_AKB(self.app.cur_cmd['RELE'],
                                     num_relay_tx = t_num_rele,
                                     num_chnl_1_tx = t_ch_1,
                                     num_chnl_2_tx = t_ch_2,
                                     mode_tx = t_mod,
                                     time_tx = (self.app.ui.comboBox_Time_Charge.currentIndex() + 1))
        #запускаем таймер ожидания ответа
        self.app.timer_RX_RS.start(self.app.rs.time_to_rx, self.app)


    def Rele_Contr_1_Header(self):
        '''
        обработчик изменения номера в comboBox_Rele_Contr_1
        :return:
        '''
        if self.app.ui.comboBox_Rele_Contr_1.currentIndex() == (self.app.ui.comboBox_Rele_Contr_1.count()-1):
            # выбрали каналы  1 - 10 или  11 - 20
            self.app.ui.comboBox_Rele_Contr_2.setDisabled(1)
        else:
            self.app.ui.comboBox_Rele_Contr_2.setEnabled(1)
            self.Set_Value_comboBox(self.app.ui.comboBox_Rele_Contr_2, exclude = self.app.ui.comboBox_Rele_Contr_1.currentText())


    def Rele_Number_Header(self):
        '''
        обработчик изменения номера в comboBox_Rele_Number
        :return:
        '''
        if self.app.ui.comboBox_Rele_Number.currentIndex() == 1:
            self.app.ui.comboBox_Rele_Contr_1.setEnabled(1)
            self.app.ui.comboBox_Rele_Contr_2.setEnabled(1)
            self.Set_Value_comboBox(self.app.ui.comboBox_Rele_Contr_1, add_item = '1-10', exclude = self.app.ui.comboBox_Rele_Contr_2.currentText())
        elif self.app.ui.comboBox_Rele_Number.currentIndex() == 2:
            self.app.ui.comboBox_Rele_Contr_1.setEnabled(1)
            self.app.ui.comboBox_Rele_Contr_2.setEnabled(1)
            self.Set_Value_comboBox(self.app.ui.comboBox_Rele_Contr_1, add_item = '11-20', exclude = self.app.ui.comboBox_Rele_Contr_2.currentText())
        else:
            self.app.ui.comboBox_Rele_Contr_1.setDisabled(1)
            self.app.ui.comboBox_Rele_Contr_2.setDisabled(1)

    #*********************************************************************
    #вывод сообщения - "Ошибка приема"
    #*********************************************************************
    def Show_Warning_RX_Error(self):
        QtWidgets.QMessageBox.warning(self.app, 'Ошибка',"Ошибка приема", QtWidgets.QMessageBox.Ok)
        self.app.STATUS_OLD = self.app.STATUS_NEW
        self.app.STATUS_NEW = self.app.cur_cmd["IDLE"]


    def Show_RX_DATA(self):
        '''
        #*********************************************************************
        # вывести полученный пакет из rs_receive_pack
        #*********************************************************************
        :return:
        '''
        print("получен пакет")
        for i in range(0,len(self.app.rs_receive_pack)):
            print(i,': ', hex(self.app.rs_receive_pack[i]),' ;',chr(self.app.rs_receive_pack[i]))


    def Show_TX_DATA(self, data):
        '''
        #*********************************************************************
        # вывести отправленный пакет в RS
        #*********************************************************************
        :return:
        '''
        print("передан пакет")
        for i in range(0,len(data)):
            print(i,': ', hex(data[i]),' ;',chr(data[i]))

