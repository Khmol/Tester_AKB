# -*- encoding: utf-8 -*-

import unittest, sys
import Tester_AKB
from PyQt5 import QtWidgets

RS_LOOP = False

class TestUM(unittest.TestCase):
    def setUp(self):
        self.widg = QtWidgets.QApplication(sys.argv)
        self.app = Tester_AKB.Tester_AKB()
        self.b_list = bytearray ((0x55, 0xaa, 0x17, 0x00, 0xe, 0x8, 0x1d))
        self.rs_receive_pack = bytearray(self.b_list)


    def test_Widgets(self):
        res = self.app.event.Init_Widgets()
        self.assertEqual(res, None)
        res = self.app.event.Enable_Widgets()
        self.assertEqual(res, None)
        res = self.app.event.Disable_Widgets()
        self.assertEqual(res, None)
        res = self.app.event.pb_Open_COM_Header()
        self.assertEqual(res, None)
        res = self.app.event.pb_Close_COM_Header()
        self.assertEqual(res, None)

    def test_Parsing_Rx_Pack(self):
        res = self.app.app.Parsing_Rx_Pack(self.rs_receive_pack)
        self.assertEqual(res, (0xaa, 0x17, 0x00, 0xe, 0x8, 0x1d, False))

    def test_pb_Clear_Channels_Header(self):
        # конфигурируем RS
        self.app.rs.Serial_Config(115200, 'COM5')
        self.app.rs.Init_RS_Var(115200)
        res = self.app.event.pb_Clear_Channels_Header()
        self.assertEqual(res, 'Ok')
        if RS_LOOP == True:
            rs_receive_pack = self.app.rs.Recieve_RS_Data()    #получаем аднные
            self.assertEqual(rs_receive_pack, self.b_list[1:])

    # def test_Show_Warning_TX_OK(self):
    #     start_index = 7
    #     length = 13
    #     res = self.mainapp.event.Show_Warning_TX_OK(self.rs_receive_pack, start_index, length)
    #     self.assertTrue(res)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
