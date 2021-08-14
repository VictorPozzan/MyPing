
class Ping_Data:

    def __init__(self):
        self.accept = 0
        self.lost = 0
        self.sumtime = 0
        self.shorttime = 10000
        self.longtime = 0
        self.avgtime = 0
        self.count = 0

    def print_ping(self,ping_time, dest_ipv4):
        self.count += 1 
        if ping_time > 0: #há uma resposta
            return_time = int(ping_time * 1000)
            print("Reply from:", dest_ipv4, "Byte = 32 time = ", return_time, "ms")
            self.accept += 1
            self.sumtime += return_time
            if return_time > self.longtime:
                self.longtime = return_time
            if return_time < self.shorttime:
                self.shorttime = return_time
        else:
            self.lost += 1
            print("Request timed out")  
            
            
        

    def statistics_ping(self, dest_ipv4):
        self.avgtime = self.sumtime/self.accept
        lost_percentage = 0
        if self.lost > 0:
            lost_percentage = (self.lost / self.count) * 100
        print("Ping statistic for: ", dest_ipv4)
        print("Packet: Sent = ", self.count, "Receive = ", self.accept, "Lost = ", self.lost, " (", lost_percentage ,"% Lost)")
        if lost_percentage != 100:
            print("RTT (round-trip-time) in milliseconds: Shortest = ", self.shorttime, "ms, longest = ", self.longtime, "ms, average = ", self.avgtime, "ms")