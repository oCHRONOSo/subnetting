#import ipaddress


# functions
""" def valid_ip(ip_str):
    try:
        ip = ipaddress.IPv4Address(ip_str)  # IPv6Address for IPv6 validation
        return True
    except ipaddress.AddressValueError:
        return False """


def valid_ip(ip_str):
    # Split the IP address into its components
    ip_components = ip_str.split(".")

    # Check if there are exactly 4 components
    if len(ip_components) != 4:
        return False

    # Check each component for validity
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
       
        # Check if the binary representation is a prefix of 1's followed by 0's
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




# getting the input
switch = True
while switch :
    ip = input("IP (ej:192.168.1.0) : ")
    if valid_ip(ip) == False :
        print("verifica tu ip")
        #exit()
    else:
        switch = False






switch = True
while switch :
    mask = input("mascara (ej:24 o 255.255.255.0): ")
    if valid_mask(mask) == False:
        print("verifica tu mascara")
        #exit()
    else:
        switch = False




if mask.find(".") != -1 :
    mask = int(iptobin(mask).count("1"))
else:
    mask = int(mask)


max_subnet = 2**(32 - mask - 2)


switch = True
while switch :
    sh = input("calcular las subredes usando numero de host por subred (h) o numero de subredes (s): ")


    if sh == "s":
        subnet_num = int(input("numero de subredes :"))
        rango = subnet_num
        if subnet_num > max_subnet :
            print(f"el numero maximo de subredes es {max_subnet}")
            exit()
       
        n = 0
        while subnet_num > 2**n:
            n = n + 1


        print(f"maximo numero de subredes: {2**n}")
        switch = False
    elif sh == "h":
       
        host = int(input("numero de hosts/subred : "))
        n_host = 0
       
        while 2**n_host < host + 2:
            n_host += 1


        n = 32 - mask - n_host
        rango = 2**n
        switch = False
    else:
        print("tiene que ser (s) o (h)")
        #exit()
   








# get the network IP


# net_bin = bin(int(iptobin(ip), 2) & int(masktoaddress(mask, False), 2))[2:]
net_bin = ''.join('1' if a == '1' and b == '1' else '0' for a, b in zip(iptobin(ip), masktoaddress(mask, False)))
net = [int(part, 2) for part in addchar(net_bin).split(".")]


# calculating the new subnet mask
newmask = mask + n
# print(newmask)
# calculating the new subnet size and available hosts
subnet_size = 2**(32-newmask)
# print(subnet_size)
host_num = subnet_size - 2
print("numero maximo de hosts en cada subnet: " + str(host_num))


print(f"la red inicial de la ip {net}")
print(f"la mascara de la red inicial {masktoaddress(mask)}")
# convert to binary : print(bin(6)[2:].zfill(8))






c = int(net_bin[mask:], 2)
for k in range(rango):


    subnet_bin = net_bin[:mask] + bin(c)[2:].zfill(32-mask)
    ip_parts = [int(part, 2) for part in addchar(subnet_bin).split(".")]
    # print(addchar(subnet_bin))
    subnet_ip = ""
    k=1
    for i in ip_parts:
        if k < len(ip_parts) :
            subnet_ip += str(i)+"."
            k += 1
        else:
            subnet_ip += str(i)
       
       
    print(f"{subnet_ip}/{newmask}")
    c += int(net_bin[mask:], 2) + subnet_size






# print("No es mi culpa que no te funciona este programa !")







