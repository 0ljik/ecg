import sys
#import appserial
from time import sleep
from PyQt5.QtWidgets import (QLineEdit, QSlider, QPushButton, QGridLayout, QApplication, QWidget, QLabel, QSpinBox, QComboBox, QFileDialog, QDialog)
from PyQt5.QtCore import (Qt, QThread, QTimer)

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.g_lay = QGridLayout()
        self.top_label = QLabel('ECG Monitoring')
        #self.m_label= QLineEdit('Loading...')
        self.i_button = QPushButton('Выбрать')
        self.i_label= QLabel('Выберите файл форматом jpg, png или ..')

        self.dat_button = QPushButton('Выбрать')
        self.dat_label= QLabel('Выберите файл dat')
        self.hea_button = QPushButton('Выбрать')
        self.hea_label= QLabel('Выберите файл hea')

        self.type_label= QLabel('Выберите тип данных')
        self.type_cbox = QComboBox()
        self.calc_button = QPushButton('Расчитать')
        self.res_label= QLabel('Result\nR found on: \nGraph:\n')

        self.type_cbox.addItem("scan")
        self.type_cbox.addItem("aami")

        self.dat_button.hide()
        self.dat_label.hide()
        self.hea_button.hide()
        self.hea_label.hide()

        self.i_button.setCheckable(True)
        self.dat_button.setCheckable(True)
        self.hea_button.setCheckable(True)
        #self.r_button.setCheckable(True)

        #g_lay.addWidget(self.m_label,0,0)
        self.g_lay.addWidget(self.top_label,0,0)
        self.g_lay.addWidget(self.type_label,1,0)
        self.g_lay.addWidget(self.type_cbox,1,1)
        self.g_lay.addWidget(self.i_button,2,1)
        self.g_lay.addWidget(self.i_label,2,0)
        self.g_lay.addWidget(self.dat_button,3,1)
        self.g_lay.addWidget(self.dat_label,3,0)
        self.g_lay.addWidget(self.hea_button,4,1)
        self.g_lay.addWidget(self.hea_label,4,0)
        self.g_lay.addWidget(self.calc_button,5,0)
        self.g_lay.addWidget(self.res_label,6,0)

        self.setLayout(self.g_lay)
        self.setWindowTitle('ECG Monitoring')

        self.i_button.clicked.connect(lambda: self.file_btn_clk(self.i_button, 'i'))
        self.dat_button.clicked.connect(lambda: self.file_btn_clk(self.g_button, 'g'))
        self.hea_button.clicked.connect(lambda: self.file_btn_clk(self.p_button, 'p'))
        #self.r_button.clicked.connect(lambda: self.btn_clk(self.r_button, 'Rework','r'))

        self.type_cbox.currentTextChanged.connect(self.on_combobox_changed)

        self.show()

        self.thread = ThreadClass()
        self.thread.start()

        '''self.i_timer = QTimer()
        self.i_timer.setInterval(500)
        self.i_timer.setSingleShot(True)
        self.i_timer.timeout.connect(lambda: self.update_data(set_sel[0],self.i_spin))
        self.g_timer = QTimer()
        self.g_timer.setInterval(500)
        self.g_timer.setSingleShot(True)
        self.g_timer.timeout.connect(lambda: self.update_data(set_sel[1],self.g_spin))
        self.p_timer = QTimer()
        self.p_timer.setInterval(500)
        self.p_timer.setSingleShot(True)
        self.p_timer.timeout.connect(lambda: self.update_data(set_sel[2],self.p_spin))'''

    def s_load(self, s, set_pp, sel):
        s.setRange(set_pp[2],set_pp[3])
        s.setValue(set_pp[0])
        #s.setTickInterval(interval)
        s.valueChanged.connect(lambda: self.v_change(s , sel))
        #s.setTickPosition(QSlider.TicksBelow)

    def on_combobox_changed(self, value):
        print("combobox changed", value)
        if (value=='aami'):
            self.dat_button.show()
            self.dat_label.show()
            self.hea_button.show()
            self.hea_label.show()
            self.i_button.hide()
            self.i_label.hide()
        else:
            self.i_button.show()
            self.i_label.show()
            self.dat_button.hide()
            self.dat_label.hide()
            self.hea_button.hide()
            self.hea_label.hide()
    def file_btn_clk(self, b, sel):
        dialog = QFileDialog(self, 'Audio Files', directory, filter)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setSidebarUrls([QtCore.QUrl.fromLocalFile(place)])
        if dialog.exec_() == QDialog.Accepted:
            self._data_file = dialog.selectedFiles()[0]
            print(type(self._data_file))

    def v_change(self, s, sel):
        val = s.value()
        if type(s) == QSlider:
            getattr(self, "%s_spin" % sel).setValue(val)
        if type(s) == QSpinBox:
            getattr(self, "%s_slider" % sel).setValue(val)
            if sel!='pp' and getattr(self, "%s_button" % sel).isChecked()==True:
                getattr(self, "%s_timer" % sel).stop()
                getattr(self, "%s_timer" % sel).start()
                #getattr(self, "%s_timer" % sel).timeout.connect(lambda: self.update_data(sel,val))


            #self.emit(pyqtSignal('UpdateVal'),val)
            #self.thread.write(sel+' '+str(val))
            #appserial.send(sel+' '+str(value))

    def btn_clk(self, b, string, sel):
        if b.isChecked() == True:
            b.setText(string+' on')
            if sel!='r':
                #print(sel+' '+str(getattr(self, "%s_spin" % sel).value()))
                getattr(self, "%s_timer" % sel).stop()
                getattr(self, "%s_timer" % sel).start()
                #print(serread())
            else:
                print('to do')
        else:
            if sel!='r':
                b.setText(string+' off')
                #-appserial.send('@'+str(send_sel[sel])+':'+'0'+';n')
                #print(str(send_sel[sel])+':'+'0'+';')
    def update_data(self, sel, val):
        #-appserial.send('@'+str(send_sel[sel])+':'+str(val.value())+';n')
        print('sent')
        #print('@'+str(send_sel[sel])+':'+str(val.value())+';')
        #print('local'+str(send_sel[sel])+':'+str(val.value()))
        #print(val.value())t

class ThreadClass(QThread):
    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)
    def run(self):
        while 1:
            val = 'a'
            sleep(.05)




            #a_wind#w.m_label.setText(val.decode('utf-8'))

        #self.connect(self.Window, pyqtSignal('UpdateVal'), self.write)
"""class sThreadClass(QThread):
    def __init__(self,sel,val,parent=None):
        super(QThread, self).__init__(parent)
        self.sel=sel
        self.val=val

    def run(self):
        val = self.val
        appserial.send(self.sel+str(val))
        print(val)
        sleep(1)"""
app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
