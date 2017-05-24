#coding: utf8

LENGTH = 9           # нормальная длина принимаемого пакета
CMD_POS = 1          # номер байта CMD в пакете
NUM_CHNL_POS = 2     # номер байта num_chnl в пакете
PARAM_POS = 3        # номер байта param в пакете
HOURS_POS = 4        # номер байта hours в пакете
MINUTES_POS = 5      # номер байта minutes в пакете
SECONDS_POS = 6      # номер байта seconds в пакете
STATUS_RELE_1 = 7    # номер байта stat_r1 в пакете
STATUS_RELE_2 = 8    # номер байта stat_r2 в пакете

class Application(object):

    def __init__(self, in_app):
        self.app = in_app


    def Parsing_Rx_Pack(self, data_in):
        """
        парсинг полученного пакета
        param: data_in: {bytes}
        return: [cmd_rx, num_chnl, param, hours, minutes, seconds, stat_r1, stat_r2, err]:
        """
        cmd_rx = num_chnl = param = hours = minutes = seconds = stat_r1 = stat_r2 = 0
        if len(data_in) != LENGTH:
            err = True
        else:
            err = False
            # выделяем данные из пакета
            cmd_rx = int.from_bytes(data_in[CMD_POS: CMD_POS+1], byteorder='little') #преобразуем в int
            num_chnl = int.from_bytes(data_in[NUM_CHNL_POS:NUM_CHNL_POS+1], byteorder='little') #преобразуем в int
            param = int.from_bytes(data_in[PARAM_POS:PARAM_POS+1], byteorder='little') #преобразуем в int
            hours = int.from_bytes(data_in[HOURS_POS:HOURS_POS+1], byteorder='little') #преобразуем в int
            minutes = int.from_bytes(data_in[MINUTES_POS:MINUTES_POS+1], byteorder='little') #преобразуем в int
            seconds = int.from_bytes(data_in[SECONDS_POS:SECONDS_POS+1], byteorder='little') #преобразуем в int
            stat_r1 = int.from_bytes(data_in[STATUS_RELE_1:STATUS_RELE_1+1], byteorder='little') #преобразуем в int
            stat_r2 = int.from_bytes(data_in[STATUS_RELE_2:STATUS_RELE_2+1], byteorder='little') #преобразуем в int
        return (cmd_rx, num_chnl, param, hours, minutes, seconds, stat_r1, stat_r2, err)


    def Set_Frame_Color(self, color, num_chnl):
        '''
        прорисовка frame на форме красным цветом с номером num_chnl,
        если num_chnl = 0 - все
        param color - цвет 'green': зеленый, остальные - красный
        param num_chnl - номер канала для обнуления:
        return:
        '''
        if color == 'green':
            text_to_command = 'self.app.ui.frame_%d.setStyleSheet("background-color: rgb(0, 150, 53);")'
        elif color == 'red':
            text_to_command = 'self.app.ui.frame_%d.setStyleSheet("background-color: rgb(255, 117, 53);")'
        else:
            text_to_command = 'self.app.ui.frame_%d.setStyleSheet("background-color: rgb(150, 150, 150);")'
        if num_chnl != 0:
            eval(text_to_command % num_chnl)
        else:
            for i in range(1,21):
                eval(text_to_command % i)


    def Set_Label_Text( self, text, num_chnl ):
        '''
        изменение надписи поля с описанием состояния канала с номером num_chnl,
        если num_chnl = 0 - изменить надпись на всех каналах
        param: text - текст который нужно вывести
        param: num_chnl - номер канала для обнуления:
        return:
        '''
        if num_chnl != 0:
            eval('self.app.ui.label_t%d.setText("%s")'%(num_chnl, text))
        else:
            for i in range(1,21):
                eval('self.app.ui.label_t%d.setText("%s")'%(i, text))
