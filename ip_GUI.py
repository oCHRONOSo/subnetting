import tkinter as tk
from tkinter import messagebox, font


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

def subnet_range(subnet_ip, newmask):
    subnet_size = 2 ** (32 - newmask)
    # Calculate the first host
    first_host = subnet_ip[:newmask] + bin(int(subnet_ip[newmask:], 2) + 1)[2:].zfill(32 - newmask)
    first_host_ip = [int(part, 2) for part in addchar(first_host).split(".")]
    
    # Calculate the last host
    last_host = subnet_ip[:newmask] + bin(int(subnet_ip[newmask:], 2) + subnet_size - 2)[2:].zfill(32 - newmask)
    last_host_ip = [int(part, 2) for part in addchar(last_host).split(".")]
    
    # Calculate the broadcast IP
    broadcast_ip = subnet_ip[:newmask] + bin(int(subnet_ip[newmask:], 2) + subnet_size - 1)[2:].zfill(32 - newmask)
    broadcast_ip = [int(part, 2) for part in addchar(broadcast_ip).split(".")]
    
    return first_host_ip, last_host_ip, broadcast_ip

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
        
        first_host_ip, last_host_ip, broadcast_ip = subnet_range(subnet_bin, newmask) 
       
        result_text.insert(tk.END,f"IP subred: {subnet_ip}/{newmask}\n")
        result_text.insert(tk.END,f"Primer Host: {'.'.join(map(str, first_host_ip))}\n")
        result_text.insert(tk.END,f"Ultimo Host: {'.'.join(map(str, last_host_ip))}\n")
        result_text.insert(tk.END,f"IP broadcast: {'.'.join(map(str, broadcast_ip))}\n\n")
        
        c += int(net_bin[mask:], 2) + subnet_size


bg_color = "#a8dadc"
bg_label = "#a8dadc"
fg_label = "#1d3557"
bg_entry = "#f1faee"
fg_entry = "#1d3557"

app = tk.Tk()
app.option_add("*Font", "Helvetica 11")
app.configure(bg=bg_color)
app.resizable(False, False)

app.title("Subnet Calculator")

# IP Address Entry
ip_label = tk.Label(app, text="Enter IP Address:", bg=bg_label, fg=fg_label)
ip_label.pack()
ip_entry = tk.Entry(app,bg=bg_entry,fg=fg_entry)
ip_entry.pack()

# Subnet Mask Entry
mask_label = tk.Label(app, text="Enter Subnet Mask:", bg=bg_label, fg=fg_label)
mask_label.pack()
mask_entry = tk.Entry(app,bg=bg_entry,fg=fg_entry)
mask_entry.pack()

# Radio Buttons for Calculation Method
calculation_method_var = tk.StringVar()
calculation_method_var.set("subnets")  # Default to subnets

subnet_radio = tk.Radiobutton(app, text="Subnets", variable=calculation_method_var, value="subnets", bg=bg_label, fg=fg_label)
subnet_radio.pack()

host_radio = tk.Radiobutton(app, text="Hosts", variable=calculation_method_var, value="hosts", bg=bg_label, fg=fg_label)
host_radio.pack()

# Number of Subnets or Hosts Entry
subnet_host_label = tk.Label(app, text="Number of Subnets:", bg=bg_label, fg=fg_label)
subnet_host_label.pack()
subnet_entry = tk.Entry(app,bg=bg_entry,fg=fg_entry)
subnet_entry.pack()

# Number of Hosts per Subnet Entry
host_label = tk.Label(app, text="Number of Hosts per Subnet:", bg=bg_label, fg=fg_label)
host_label.pack()
host_entry = tk.Entry(app,bg=bg_entry,fg=fg_entry)
host_entry.pack()

# Calculate Button
calculate_button = tk.Button(app, text="Calculate", command=calculate_subnets,bg="#e63946")
calculate_button.pack(pady=5)

# Result Display
result_text = tk.Text(app, height=20, width=40,bg=bg_entry,fg=fg_entry)
result_text.pack()

app.mainloop()
