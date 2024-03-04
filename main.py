from PyQt5 import QtCore, QtGui, QtWidgets
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.logTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logTextBrowser.setObjectName("logTextBrowser")
        self.verticalLayout.addWidget(self.logTextBrowser)
        self.createProcessButton = QtWidgets.QPushButton(self.centralwidget)
        self.createProcessButton.setObjectName("createProcessButton")
        self.verticalLayout.addWidget(self.createProcessButton)
        self.allocateResourcesButton = QtWidgets.QPushButton(self.centralwidget)
        self.allocateResourcesButton.setObjectName("allocateResourcesButton")
        self.verticalLayout.addWidget(self.allocateResourcesButton)
        self.takeResourcesButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeResourcesButton.setObjectName("takeResourcesButton")
        self.verticalLayout.addWidget(self.takeResourcesButton)
        self.interruptButton = QtWidgets.QPushButton(self.centralwidget)
        self.interruptButton.setObjectName("interruptButton")
        self.verticalLayout.addWidget(self.interruptButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.createProcessButton.clicked.connect(self.create_processes)
        self.allocateResourcesButton.clicked.connect(self.allocate_resources)
        self.takeResourcesButton.clicked.connect(self.take_resources)
        self.interruptButton.clicked.connect(self.interrupt_process)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.createProcessButton.setText(_translate("MainWindow", "Создать процессы"))
        self.allocateResourcesButton.setText(_translate("MainWindow", "Выделить ресурсы"))
        self.takeResourcesButton.setText(_translate("MainWindow", "Забрать ресурсы"))
        self.interruptButton.setText(_translate("MainWindow", "Прерывание"))

    def create_processes(self):
        self.scene.clear()
        self.logTextBrowser.clear()

        states = ["Порождение", "Ожидание", "Окончание"]
        process_logs = [QtGui.QColor(QtCore.Qt.gray), QtGui.QColor(QtCore.Qt.blue), QtGui.QColor(QtCore.Qt.red)]

        process_positions = [(50, 50), (50, 150), (50, 250), (50, 350), (50, 450)]

        for i, pos in enumerate(process_positions):
            process_item = QtWidgets.QGraphicsRectItem(0, 0, 100, 50)
            process_item.setBrush(process_logs[0])
            process_item.setPos(pos[0], pos[1])
            self.scene.addItem(process_item)

            process_label = QtWidgets.QGraphicsTextItem(str(i + 1))
            process_label.setPos(pos[0] + 40, pos[1] + 20)
            self.scene.addItem(process_label)

            self.logTextBrowser.append(f"Процесс {i + 1}: {states[0]}")

    def allocate_resources(self):
        process_items = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem)]
        process_to_allocate = random.choice(process_items)
        if process_to_allocate.brush().color() != QtGui.QColor(QtCore.Qt.red):
            process_to_allocate.setBrush(QtGui.QColor(QtCore.Qt.yellow))
            process_index = process_items.index(process_to_allocate) + 1
            self.logTextBrowser.append(f"Выделены ресурсы процессу {process_index}")

            process_item = next(item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem) and item == process_to_allocate)
            process_item_index = process_items.index(process_to_allocate)

            if process_item_index < len(process_items) - 1:
                next_process_item = process_items[process_item_index + 1]
                next_process_item.setBrush(QtGui.QColor(QtCore.Qt.blue))
                self.logTextBrowser.append(f"Процесс {process_index}: Активность")

    def take_resources(self):
        process_items = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem)]
        process_to_take = random.choice(process_items)
        if process_to_take.brush().color() == QtGui.QColor(QtCore.Qt.yellow):
            process_to_take.setBrush(QtGui.QColor(QtCore.Qt.red))
            process_index = process_items.index(process_to_take) + 1
            self.logTextBrowser.append(f"Ресурсы забраны у процесса {process_index}")

    def interrupt_process(self):
        process_items = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem)]
        process_to_interrupt = random.choice(process_items)
        process_to_interrupt.setBrush(QtGui.QColor(QtCore.Qt.gray))
        process_index = process_items.index(process_to_interrupt) + 1
        self.logTextBrowser.append(f"Процесс {process_index} прерван")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())