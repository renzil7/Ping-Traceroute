"""
Author: Renzil Dourado (rd9012)

CN Project 3
rd9012_traceroute.py

Implementation of Traceroute part of Project 3
"""
import socket as sc
import struct as st
import time
import sys
from random import *


def main():
    """
    This method takes input from the user and sets appropriate
    flags and parameters and then calls the ping method
    :return: None
    """

    # setting default parameters
    data_size = 56
    count = 3
    summary = False
    onlyIP = False

    argLen = len(sys.argv)
    if argLen == 2:
        PING_HOST = sys.argv[1]
        try:
            sc.gethostbyname(PING_HOST)
        except:
            print("Unable to resolve target system name " + sys.argv[1] + ". Please check the name and try again.")
            sys.exit(0)
        ping(PING_HOST, data_size, count, summary, onlyIP)

    elif argLen > 2:
        PING_HOST = sys.argv[argLen - 1]
        try:
            sc.gethostbyname(PING_HOST)
        except:
            print("Unable to resolve target system name " + sys.argv[2] + ". Please check the name and try again.")
            sys.exit(0)

        arguments = sys.argv[1:]
        del arguments[-1]
        i = 0
        try:
            while i < len(arguments):
                command = arguments[i]
                if command == "-n":
                    onlyIP = True
                    i += 1
                elif command == "-S":
                    summary = True
                    i += 1
                elif command == "-q":
                    count = arguments[i + 1]
                    i += 2
                else:
                    printMenu()
                    sys.exit(0)

            ping(PING_HOST, data_size, count, summary, onlyIP)
        except ValueError:
            printMenu()
            sys.exit(0)
    else:
        printMenu()
        sys.exit(0)


def printMenu():
    """
    This method just prints the Traceroute Menu
    :return:
    """
    print()
    print("Usage       :rd9012_traceroute.py -n/-q/-S hostname")
    print()
    print("MENU")
    print("----------------------------------------------------------------------------------------------")
    print("-n          :Print hop addresses numerically rather than symbolically and numerically.")
    print("-q nqueries :Set the number of probes per ``ttl'' to nqueries. ")
    print("-S          :Print a summary of how many probes were not answered for each hop")
    print()


def ping(PING_HOST, data_size, count, summary, onlyIP):
    """
    This method sends count number of packets to intermediate routers
    on the path to the destination, each time increasing the TTL by 1
    untill the destination is reached
    :param PING_HOST: Host whose path is to be traced
    :param data_size: size of data packet to be sent
    :param count: number of packets to be sent per TTL
    :param summary: boolean value which specifies summary to be dispalyed or not
    :param onlyIP: boolean value which specifies if only IP is to be displayed
    :return: None
    """
    count = int(count)
    data_size = int(data_size)
    print()
    print("Tracing route to " + PING_HOST + " [" + sc.gethostbyname(PING_HOST) + "]")
    print("over a maximum of 30 hops:")
    print()
    TTL = 1
    sr_no = 1
    # Maximum of 30 hops
    try:
        while TTL <= 30:
            counter = 0
            packets_sent = 0
            packets_received = 0
            sequence_no = 0
            response_times = []

            # Sending packets per TTL
            while counter < count:
                pingSocket = sc.socket(sc.AF_INET, sc.SOCK_RAW, sc.IPPROTO_ICMP)
                pingSocket.settimeout(3)
                startTime = time.time()
                try:
                    sequence_no += 1
                    pingSocket.setsockopt(sc.SOL_IP, sc.IP_TTL, TTL)
                    pingSocket.sendto(ping_packet(data_size, sequence_no), (PING_HOST, 0))
                    packets_sent += 1
                    reply, address = pingSocket.recvfrom(1024)
                except:
                    response_times.append("*")
                    pingSocket.close()
                    counter += 1
                    continue
                endTime = time.time()
                packets_received += 1
                response_time = int((endTime - startTime) * 1000)
                response_times.append(response_time)
                replying_address = address[0]
                counter += 1

            if onlyIP:
                domain_name = ""

            else:
                try:
                    domain_name = sc.gethostbyaddr(replying_address)[0]
                except:
                    domain_name = ""

            print(str(sr_no) + "\t", end='')
            count_TO = 0
            for item in response_times:
                if item == "*":
                    print(str(item) + "  \t", end='')
                    count_TO += 1
                else:
                    print(str(item) + "ms\t", end='')
            if count_TO != len(response_times):
                print(replying_address + "\t" + str(domain_name))
            else:
                print("Request timed out")

            if summary:
                packets_lost = packets_sent - packets_received
                loss = (packets_lost / packets_sent) * 100
                print("Traceroute statistics for " + str(replying_address) + ":")
                print("Probes: Sent =" + str(packets_sent) + ", Received = " + str(packets_received) + ", Lost =" + str(
                    packets_lost) + " (" + str(loss) + "% loss),")
            print()

            TTL += 1
            sr_no += 1
            if sc.gethostbyname(PING_HOST) == replying_address:
                break
        print("Trace complete.")
        print()
    except KeyboardInterrupt:
        pass


def ping_packet(data_size, sequence_no):
    """
    This method creates an ICMP packet to be sent
    :param data_size: size of the data to be sent
    :param sequence_no: incremented sequence number for each packet
    :return: the iCMP packet
    """

    type = 8
    code = 0
    id = randint(1, 9999)
    check = 0
    header = st.pack("!BBHHH", type, code, check, id, sequence_no)
    data = "A" * data_size
    data = bytes(data, encoding='utf8')
    checksum = calculate_checksum(header + data)
    icmp_packet = st.pack("!BBHHH", type, code, checksum, id, sequence_no) + data
    return icmp_packet


def calculate_checksum(packet):
    """
    This method calculates the checksum to be added
    to the ICMP packet.
    It performs one complement addition and finally
    takes a complement of the result and returns the result
    :param packet: data+header
    :return: checksum
    """

    count = 0
    sum = 0
    isLengthOdd = len(packet) % 2
    if isLengthOdd:
        length = len(packet) - 1
    else:
        length = len(packet)

    while (count < length):
        sum += (packet[count] << 8) + packet[count + 1]
        carry = sum >> 16
        sum = sum & 0xFFFF
        sum += carry
        count += 2

    if isLengthOdd:
        sum += (packet[length] << 8)
        carry = sum >> 16
        sum = sum & 0xFFFF
        sum += carry
    sum = ~sum & 0xFFFF
    return sum


if __name__ == '__main__':
    main()
