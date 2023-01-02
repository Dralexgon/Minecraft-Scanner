class Ipv4:
    def __init__(self, ip = (0, 0, 0, 0)):
        if type(ip) == str:
            self.ip = self.from_string(ip).ip
        elif type(ip) == tuple:
            self.ip = ip
        else:
            raise TypeError("Type not supported")
    
    def from_string(self, ip):
        split_ip = ip.split(".")
        for i in range(len(split_ip)):
            split_ip[i] = int(split_ip[i])
        return Ipv4(tuple(split_ip))
    
    def from_tuple(self, ip):
        return Ipv4(ip)
    
    def __str__(self):
        return str(self.ip[0]) + "." + str(self.ip[1]) + "." + str(self.ip[2]) + "." + str(self.ip[3])
    
    def __add__(self, other):
        if type(other) == Ipv4:
            return self.add_ipv4(other)
        elif type(other) == int:
            return self.add_int(other)
        elif type(other) == str:
            return self.from_string(other)
        elif type(other) == tuple:
            return self.from_tuple(other)
        else:
            raise TypeError("Type not supported")
    
    def add_ipv4(self, other):
        new_ip = []
        for i in range(4):
            total = self.ip[3 - i] + other.ip[3 - i]
            if total > 255:
                total -= 256
                if i == 3:
                    raise ValueError("IP too big")
                else:
                    self.ip[3 - i - 1] += 1
            new_ip.append(total)
        return Ipv4(tuple(new_ip))
    
    def add_int(self, other):
        new_ip = []
        for i in range(4):
            total = self.ip[3 - i] + other
            if total > 255:
                total -= 256
                if i == 3:
                    raise ValueError("IP too big")
                else:
                    self.ip[3 - i - 1] += 1
            new_ip.append(total)
        return Ipv4(tuple(new_ip))
    
    def __sub__(self, other):
        if type(other) == Ipv4:
            return self.sub_ipv4(other)
        elif type(other) == int:
            return self.sub_int(other)
        elif type(other) == str:
            return self.from_string(other).ip
        elif type(other) == tuple:
            return self.from_tuple(other).ip
        else:
            raise TypeError("Type not supported")
    
    def sub_ipv4(self, other):
        new_ip = []
        for i in range(4):
            total = self.ip[3 - i] - other.ip[3 - i]
            if total < 0:
                total += 256
                if i == 3:
                    raise ValueError("IP too small")
                else:
                    self.ip[3 - i - 1] -= 1
            new_ip.append(total)
        return Ipv4(tuple(new_ip))
    
    def sub_int(self, other):
        new_ip = []
        for i in range(4):
            total = self.ip[3 - i] - other
            if total < 0:
                total += 256
                if i == 3:
                    raise ValueError("IP too small")
                else:
                    self.ip[3 - i - 1] -= 1
            new_ip.append(total)
        return Ipv4(tuple(new_ip))
    
    def __eq__(self, other):
        if type(other) == Ipv4:
            return self.ip == other.ip
        elif type(other) == str:
            return self.ip == self.from_string(other).ip
        elif type(other) == tuple:
            return self.ip == self.from_tuple(other).ip
        else:
            raise TypeError("Type not supported")