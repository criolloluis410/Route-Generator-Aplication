# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FrmNodosyPesos.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FrmNodosyPesos(object):
    def setupUi(self, FrmNodosyPesos):
        FrmNodosyPesos.setObjectName("FrmNodosyPesos")
        FrmNodosyPesos.resize(388, 428)
        self.btnCerrar = QtWidgets.QPushButton(FrmNodosyPesos)
        self.btnCerrar.setGeometry(QtCore.QRect(150, 380, 75, 23))
        self.btnCerrar.setObjectName("btnCerrar")
        self.tbl_tableWidgetNodosyPesos = QtWidgets.QTableWidget(FrmNodosyPesos)
        self.tbl_tableWidgetNodosyPesos.setGeometry(QtCore.QRect(30, 50, 331, 311))
        self.tbl_tableWidgetNodosyPesos.setObjectName("tbl_tableWidgetNodosyPesos")
        self.tbl_tableWidgetNodosyPesos.setColumnCount(3)
        self.tbl_tableWidgetNodosyPesos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_tableWidgetNodosyPesos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_tableWidgetNodosyPesos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_tableWidgetNodosyPesos.setHorizontalHeaderItem(2, item)
        self.label = QtWidgets.QLabel(FrmNodosyPesos)
        self.label.setGeometry(QtCore.QRect(90, 10, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(FrmNodosyPesos)
        QtCore.QMetaObject.connectSlotsByName(FrmNodosyPesos)

    def retranslateUi(self, FrmNodosyPesos):
        _translate = QtCore.QCoreApplication.translate
        FrmNodosyPesos.setWindowTitle(_translate("FrmNodosyPesos", "Nodos y Pesos"))
        self.btnCerrar.setText(_translate("FrmNodosyPesos", "Close"))
        item = self.tbl_tableWidgetNodosyPesos.horizontalHeaderItem(0)
        item.setText(_translate("FrmNodosyPesos", "SRC_ADDR"))
        item = self.tbl_tableWidgetNodosyPesos.horizontalHeaderItem(1)
        item.setText(_translate("FrmNodosyPesos", "WEIGHT"))
        item = self.tbl_tableWidgetNodosyPesos.horizontalHeaderItem(2)
        item.setText(_translate("FrmNodosyPesos", "DSR_ADDR"))
        self.label.setText(_translate("FrmNodosyPesos", "Complete Nodes and Weights"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmNodosyPesos = QtWidgets.QDialog()
    ui = Ui_FrmNodosyPesos()
    ui.setupUi(FrmNodosyPesos)
    FrmNodosyPesos.show()
    sys.exit(app.exec_())
