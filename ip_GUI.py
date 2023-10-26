import tkinter as tk
from tkinter import messagebox

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
        if len (parts) != 4:
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
    tostring = char.join([todot[i:i+pos] for i in range(0, len(todot), pos)])
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
    for i in range(32-mask):
        maskaddr += "0"
    # convert to numbers
    masknum = [int(part, 2) for part in addchar(maskaddr).split(".")]
    if inumbers == True:
        return masknum
    else:
        return maskaddr

def calculate_subnets():
    ip = ip_entry.get()
    mask = mask_entry.get()
    
    if not valid_ip(ip):
        messagebox.showerror("Invalid IP", "Please enter a valid IP address.")
        return

    if not valid_mask(mask):
        messagebox.showerror("Invalid Subnet Mask", "Please enter a valid subnet mask.")
        return

    mask = int(mask) if '.' not in mask else iptobin(mask).count("1")

    max_subnet = 2**(32 - mask - 2)
    calculation_method = calculation_method_var.get()

    if calculation_method == "subnets":
        subnet_num = int(subnet_entry.get())
        rango = subnet_num

        if subnet_num > max_subnet:
            messagebox.showerror("Invalid Subnet Number", f"The maximum number of subnets is {max_subnet}.")
            return

        n = 0
        while subnet_num > 2**n:
            n = n + 1

    elif calculation_method == "hosts":
        max_host = 2**(32 - mask - 1)
        host = int(host_entry.get())

        if host > max_host:
            messagebox.showerror("Invalid Host Number", f"The maximum number of hosts per subnet is {max_host}.")
            return

        n_host = 0
        while 2**n_host < host + 2:
            n_host += 1

        n = 32 - mask - n_host
        rango = 2**n

    net_bin = ''.join('1' if a == '1' and b == '1' else '0' for a, b in zip(iptobin(ip), masktoaddress(mask, False)))
    net = [int(part, 2) for part in addchar(net_bin).split(".")]

    newmask = mask + n
    subnet_size = 2**(32-newmask)
    host_num = subnet_size - 2

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Subnets:\n")
    c = int(net_bin[mask:], 2)
    
    for k in range(rango):
        subnet_bin = net_bin[:mask] + bin(c)[2:].zfill(32-mask)
        ip_parts = [int(part, 2) for part in addchar(subnet_bin).split(".")]
        subnet_ip = ""
        k = 1
        for i in ip_parts:
            if k < len(ip_parts):
                subnet_ip += str(i) + "."
                k += 1
            else:
                subnet_ip += str(i)
        result_text.insert(tk.END, f"{subnet_ip}/{newmask}\n")
        c += int(net_bin[mask:], 2) + subnet_size

app = tk.Tk()
app.title("Subnet Calculator")

# IP Address Entry
ip_label = tk.Label(app, text="Enter IP Address:")
ip_label.pack()
ip_entry = tk.Entry(app)
ip_entry.pack()

# Subnet Mask Entry
mask_label = tk.Label(app, text="Enter Subnet Mask:")
mask_label.pack()
mask_entry = tk.Entry(app)
mask_entry.pack()

# Radio Buttons for Calculation Method
calculation_method_var = tk.StringVar()
calculation_method_var.set("subnets")  # Default to subnets

subnet_radio = tk.Radiobutton(app, text="Number of Subnets", variable=calculation_method_var, value="subnets")
subnet_radio.pack()

host_radio = tk.Radiobutton(app, text="Number of Hosts per Subnet", variable=calculation_method_var, value="hosts")
host_radio.pack()

# Number of Subnets or Hosts Entry
subnet_host_label = tk.Label(app, text="Number of Subnets/Hosts:")
subnet_host_label.pack()
subnet_entry = tk.Entry(app)
subnet_entry.pack()

# Number of Hosts per Subnet Entry
host_label = tk.Label(app, text="Number of Hosts per Subnet:")
host_label.pack()
host_entry = tk.Entry(app)
host_entry.pack()

# Calculate Button
calculate_button = tk.Button(app, text="Calculate Subnets", command=calculate_subnets)
calculate_button.pack()

# Result Display
result_text = tk.Text(app, height=10, width=40)
result_text.pack()

app.mainloop()
