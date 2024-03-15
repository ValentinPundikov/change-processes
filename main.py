from PyQt6 import QtCore, QtGui, QtWidgets
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Размещение элементов интерфейса в окне
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Журнал событий
        self.logTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logTextBrowser.setObjectName("logTextBrowser")
        self.verticalLayout.addWidget(self.logTextBrowser)

        # Кнопки управления процессами
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

        # Графическая сцена
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        # Подключение кнопок к методам
        self.createProcessButton.clicked.connect(self.create_processes)
        self.allocateResourcesButton.clicked.connect(self.allocate_resources)
        self.takeResourcesButton.clicked.connect(self.take_resources)
        self.interruptButton.clicked.connect(self.interrupt_process)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Программа управления процессами"))
        self.createProcessButton.setText(_translate("MainWindow", "Создать процессы"))
        self.allocateResourcesButton.setText(_translate("MainWindow", "Выделить ресурсы"))
        self.takeResourcesButton.setText(_translate("MainWindow", "Забрать ресурсы"))
        self.interruptButton.setText(_translate("MainWindow", "Прервать процесс"))

    def create_processes(self):
        # Метод для создания процессов
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

            process_label = QtWidgets.QGraphicsTextItem("Process")
            process_label.setPos(pos[0] + 40, pos[1] + 20)
            self.scene.addItem(process_label)

            self.logTextBrowser.append(f"Процесс: {states[0]}")

    def allocate_resources(self):
        # Метод для выделения ресурсов
        process_items = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem)]
        process_labels = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsTextItem)]

        # Выбираем случайный процесс для выделения ресурсов
        process_index = random.randint(0, len(process_items) - 1)
        process_to_allocate = process_items[process_index]

        # Если ресурсы еще не выделены, выделяем их для выбранного процесса
        if process_to_allocate.brush().color() != QtGui.QColor(QtCore.Qt.yellow):
            process_to_allocate.setBrush(QtGui.QColor(QtCore.Qt.yellow))
            self.logTextBrowser.append("Ресурсы выделены для процесса")

            # Если есть следующий процесс, помечаем его как активный
            next_process_index = process_index + 1
            if next_process_index < len(process_items):
                next_process_item = process_items[next_process_index]
                if next_process_item.brush().color() != QtGui.QColor(QtCore.Qt.yellow):
                    next_process_item.setBrush(QtGui.QColor(QtCore.Qt.blue))
                    self.logTextBrowser.append("Следующий процесс активен")

    def take_resources(self):
        # Метод для забора ресурсов
        process_items = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem)]

        # Выбираем случайный процесс для забора ресурсов
        process_index = random.randint(0, len(process_items) - 1)
        process_to_take = process_items[process_index]

        # Если у процесса выделены ресурсы, забираем их
        if process_to_take.brush().color() == QtGui.QColor(QtCore.Qt.yellow):
            process_to_take.setBrush(QtGui.QColor(QtCore.Qt.red))
            self.logTextBrowser.append("Ресурсы забраны у процесса")

    def interrupt_process(self):
        # Метод для прерывания процесса
        process_items = [item for item in self.scene.items() if isinstance(item, QtWidgets.QGraphicsRectItem)]

        # Выбираем случайный процесс для прерывания
        process_index = random.randint(0, len(process_items) - 1)
        process_to_interrupt = process_items[process_index]

        # Прерываем выбранный процесс
        process_to_interrupt.setBrush(QtGui.QColor(QtCore.Qt.gray))
        self.logTextBrowser.append("Процесс прерван")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())