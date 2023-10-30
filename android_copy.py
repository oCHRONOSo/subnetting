import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QRadioButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction

class SubnetCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        theme_menu = menubar.addMenu("themes")
        themes = self.get_qss_files_in_folder()
        self.theme_actions = []

        for theme_name, theme_path in themes:
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, path=theme_path: self.load_theme(path))
            theme_menu.addAction(action)
            self.theme_actions.append(action)
        
        self.setWindowTitle("Subnet Calculator")
        self.setGeometry(100, 100, 400, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        self.ip_label = QLabel("Enter IP Address:")
        self.ip_entry = QLineEdit()
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_entry)
        self.mask_label = QLabel("Enter Subnet Mask:")
        self.mask_entry = QLineEdit()
        layout.addWidget(self.mask_label)
        layout.addWidget(self.mask_entry)
        self.calculation_method_label = QLabel("Select Calculation Method:")
        layout.addWidget(self.calculation_method_label)
        self.subnets_radio = QRadioButton("Subnets")
        self.subnets_radio.setChecked(True)
        layout.addWidget(self.subnets_radio)
        self.hosts_radio = QRadioButton("Hosts")
        layout.addWidget(self.hosts_radio)
        self.num_label = QLabel("Number of Subnets:")
        self.num_entry = QLineEdit()
        layout.addWidget(self.num_label)
        layout.addWidget(self.num_entry)
        self.host_label = QLabel("Number of Hosts per Subnet:")
        self.host_entry = QLineEdit()
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_entry)
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_subnets)
        layout.addWidget(self.calculate_button)
        self.result_text = QTextEdit()
        layout.addWidget(self.result_text)
        central_widget.setLayout(layout)

    def load_theme(self, theme_path):
        with open(theme_path, 'r') as file:
            theme_code = file.read()
            self.setStyleSheet(theme_code)
    
    def get_qss_files_in_folder(self):
        qss_files_info = []  # List to store (name, path) pairs of QSS files

        for file in os.listdir("./qss"):  # Adjust the folder path here
            if file.endswith('.qss'):
                qss_file_path = os.path.join("./qss", file)  # Adjust the folder path here
                qss_files_info.append((file, qss_file_path))

        return qss_files_info
    
    def calculate_subnets(self):
        ip = self.ip_entry.text()
        mask = self.mask_entry.text()

        if not valid_ip(ip):
            self.result_text.setPlainText("Invalid IP. Please enter a valid IP address.")
            return

        if not valid_mask(mask):
            self.result_text.setPlainText("Invalid Subnet Mask. Please enter a valid subnet mask.")
            return

        mask = int(mask) if '.' not in mask else iptobin(mask).count("1")
        max_subnet = 2 ** (32 - mask - 2)
        calculation_method = "subnets" if self.subnets_radio.isChecked() else "hosts"

        if calculation_method == "subnets":
            subnet_num = int(self.num_entry.text())
            rango = subnet_num

            if subnet_num > max_subnet:
                self.result_text.setPlainText(f"The maximum number of subnets is {max_subnet}.")
                return

            n = 0
            while subnet_num > 2 ** n:
                n = n + 1

        elif calculation_method == "hosts":
            max_host = 2 ** (32 - mask - 1)
            host = int(self.host_entry.text())

            if host > max_host:
                self.result_text.setPlainText(f"The maximum number of hosts per subnet is {max_host}.")
                return

            n_host = 0
            while 2 ** n_host < host + 2:
                n_host += 1

            n = 32 - mask - n_host
            rango = 2 ** n

        net_bin = ''.join('1' if a == '1' and b == '1' else '0' for a, b in zip(iptobin(ip), masktoaddress(mask, False)))
        net = [int(part, 2) for part in addchar(net_bin).split(".")]

        newmask = mask + n
        subnet_size = 2 ** (32 - newmask)
        host_num = subnet_size - 2

        self.result_text.setPlainText("Subnets:\n")
        c = int(net_bin[mask:], 2)

        for k in range(rango):
            subnet_bin = net_bin[:mask] + bin(c)[2:].zfill(32 - mask)
            ip_parts = [int(part, 2) for part in addchar(subnet_bin).split(".")]
            subnet_ip = ""
            k = 1
            for i in ip_parts:
                if k < len(ip_parts):
                    subnet_ip += str(i) + "."
                    k += 1
                else:
                    subnet_ip += str(i)

            first_host_ip, last_host_ip, broadcast_ip = subnet_range(subnet_bin, newmask)

            self.result_text.append(f"IP subred: {subnet_ip}/{newmask}")
            self.result_text.append(f"Primer Host: {'.'.join(map(str, first_host_ip))}")
            self.result_text.append(f"Ultimo Host: {'.'.join(map(str, last_host_ip))}")
            self.result_text.append(f"IP broadcast: {'.'.join(map(str, broadcast_ip))}\n")

            c += int(net_bin[mask:], 2) + subnet_size

def valid_ip(ip_str):
    ip_components = ip_str.split(".")
    if len(ip_components) != 4:
        return False
    for component in ip_components:
        if not component.isdigit():
            return False
        value = int(component)
        if value < 0 or value > 255:
            return False
    return True

def valid_mask(mask_str):
    try:
        if int(mask_str) > 0 and int(mask_str) < 32:
            return True
    except:
        parts = mask_str.split('.')
        if len(parts) != 4:
            return False
        binary_mask = ''
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
                binary_num = bin(num)[2:].zfill(8)
                binary_mask += binary_num
            except ValueError:
                return False

        if '0' in binary_mask:
            index_of_first_zero = binary_mask.index('0')
            if '1' in binary_mask[index_of_first_zero:]:
                return False

        return True
    else:
        return False
    
            
def addchar(todot, pos=8, char="."):
    tostring = char.join([todot[i:i + pos] for i in range(0, len(todot), pos)])
    return tostring

def iptobin(ip, asarray=False):
    ip_parts = [bin(int(part))[2:].zfill(8) for part in ip.split(".")]
    ip_bin = ""
    for i in range(len(ip_parts)):
        ip_bin += ip_parts[i]
    if asarray == False:
        return ip_bin
    else:
        return ip_parts

def masktoaddress(mask, inumbers=True):
    maskaddr = ''
    for i in range(mask):
        maskaddr += "1"
    for i in range(32 - mask):
        maskaddr += "0"
    masknum = [int(part, 2) for part in addchar(maskaddr).split(".")]
    if inumbers == True:
        return masknum
    else:
        return maskaddr

def subnet_range(subnet_ip, newmask):
    subnet_size = 2 ** (32 - newmask)
    first_host = subnet_ip[:newmask] + bin(int(subnet_ip[newmask:], 2) + 1)[2:].zfill(32 - newmask)
    first_host_ip = [int(part, 2) for part in addchar(first_host).split(".")]
    last_host = subnet_ip[:newmask] + bin(int(subnet_ip[newmask:], 2) + subnet_size - 2)[2:].zfill(32 - newmask)
    last_host_ip = [int(part, 2) for part in addchar(last_host).split(".")]
    broadcast_ip = subnet_ip[:newmask] + bin(int(subnet_ip[newmask:], 2) + subnet_size - 1)[2:].zfill(32 - newmask)
    broadcast_ip = [int(part, 2) for part in addchar(broadcast_ip).split(".")]
    return first_host_ip, last_host_ip, broadcast_ip

def load_style_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def main():
    app = QApplication(sys.argv)
    # style_code = load_style_from_file('qss/Hookmark.qss')
    # app.setStyleSheet(style_code)
    calculator = SubnetCalculator()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
