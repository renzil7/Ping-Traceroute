"""
Author: Renzil Dourado (rd9012)

CN Project 3
rd9012_traceroute.py

Implementation of Ping part of Project 3
"""
import socket as sc
from socket import timeout
import struct as st
import time
import sys
from random import *


def main():
    """
    This function takes the input, sets appropriate flags
    and then calls the ping method with the appropriate
    parameters.
    :return: None
    """

    # Setting the default parameters
    data_size = 56
    wait_time = 1
    count = "infinity"
    total_time_out = 100

    argLen = len(sys.argv)
    if argLen == 2:
        PING_HOST = sys.argv[1]
        try:
            sc.gethostbyname(PING_HOST)
        except:
            print("Ping request could not find host " + sys.argv[1] + ". Please check the name and try again.")
            sys.exit(0)
        ping(PING_HOST, data_size, wait_time, count, total_time_out)

    elif argLen > 2:
        PING_HOST = sys.argv[argLen - 1]
        try:
            sc.gethostbyname(PING_HOST)
        except:
            print("Ping request could not find host " + sys.argv[3] + ". Please check the name and try again.")
            sys.exit(0)

        arguments = sys.argv[1:]
        del arguments[-1]
        i = 0

        try:
            # Setting appropriate parameters for the ping method
            while i < len(arguments):
                command = arguments[i]
                value = arguments[i + 1]
                i += 2
                if command == "-c":
                    count = value
                elif command == "-i":
                    wait_time = value
                elif command == "-s":
                    data_size = value
                elif command == "-t":
                    total_time_out = value
                else:
                    printMenu()
                    sys.exit(0)

            ping(PING_HOST, data_size, wait_time, count, total_time_out)
        except:
            printMenu()
            sys.exit(0)
    else:
        printMenu()
        sys.exit(0)


def printMenu():
    """
    This method just prints the Ping Menu
    :return: None
    """
    print()
    print("Usage        :rd9012_ping.py -c/-i/-s/-t hostname")
    print()
    print("MENU")
    print("----------------------------------------------------------------------------------------------")
    print(
        "-c count     :Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified,")
    print("              ping will operate until interrupted.")
    print(
        "-i wait      :Wait wait seconds between sending each packet. The default is to wait for one second between each packet.")
    print(
        "-s packetsize:Specify the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes ")
    print("              when combined with the 8 bytes of ICMP header data.")
    print(
        "-t timeout   :Specify a timeout, in seconds, before ping exits regardless of how many packets have been received.")
    print()


def ping(PING_HOST, data_size, wait_time, count, total_time_out):
    """
    This method sends an ICMP packet using RAW socket to the given
    host and receives the reply packet and at the end displays the
    ping statistics just as seen on pinging a host in windows.
    :param PING_HOST: Name of the host to be pinged
    :param data_size: Size of the icmp payload to be sent
    :param wait_time: wait time between sending packets
    :param count: Number of packets to be sent
    :param total_time_out: Time out irrespective of packets received
    :return: None
    """
    packets_sent = 0
    packets_received = 0
    sequence_no = 0
    response_times = []
    data_size = int(data_size)
    wait_time = int(wait_time)
    total_time_out = int(total_time_out)
    print()
    print("Pinging " + PING_HOST + " [" + sc.gethostbyname(PING_HOST) + "] with " + str(data_size) + " bytes of data")
    startping = time.time()

    try:
        # If number of packets not specified
        if count == "infinity":
            while True:
                if time.time() - startping > total_time_out:
                    print("Time Out")
                    break
                pingSocket = sc.socket(sc.AF_INET, sc.SOCK_RAW, sc.IPPROTO_ICMP)
                pingSocket.settimeout(3)
                startTime = time.time()
                try:
                    sequence_no += 1
                    pingSocket.sendto(ping_packet(data_size, sequence_no), (PING_HOST, 0))
                    packets_sent += 1
                    reply, address = pingSocket.recvfrom(1024)
                except:
                    print("Request timed out.")
                    pingSocket.close()
                    time.sleep(wait_time)
                    continue
                endTime = time.time()
                packets_received += 1
                response_time = int((endTime - startTime) * 1000)
                response_times.append(response_time)
                print("Reply from " + str(address[0]) + ": bytes=" + str(len(reply) - 28) + " time=" + str(
                    response_time) + "ms" + " TTL=" + str(reply[8]))
                time.sleep(wait_time)

        else:
            # If number of packets specified
            count = int(count)
            while count > 0:
                if time.time() - startping > total_time_out:
                    print("Time Out")
                    break
                pingSocket = sc.socket(sc.AF_INET, sc.SOCK_RAW, sc.IPPROTO_ICMP)
                pingSocket.settimeout(3)
                startTime = time.time()
                try:
                    sequence_no += 1
                    pingSocket.sendto(ping_packet(data_size, sequence_no), (PING_HOST, 0))
                    packets_sent += 1
                    reply, address = pingSocket.recvfrom(1024)
                except timeout:
                    print("Request timed out.")
                    pingSocket.close()
                    time.sleep(wait_time)
                    continue
                endTime = time.time()
                packets_received += 1
                response_time = int((endTime - startTime) * 1000)
                response_times.append(response_time)
                print("Reply from " + str(address[0]) + ": bytes=" + str(data_size) + " time=" + str(
                    response_time) + "ms" + " TTL=" + str(reply[8]))
                count -= 1
                time.sleep(wait_time)
    except KeyboardInterrupt:
        pass

    packets_lost = packets_sent - packets_received
    loss = (packets_lost / packets_sent) * 100
    print("")
    print("Ping statistics for " + sc.gethostbyname(PING_HOST) + ":")
    print("Packets: Sent =" + str(packets_sent) + ", Received = " + str(packets_received) + ", Lost =" + str(
        packets_lost) + " (" + str(loss) + "% loss),")
    if len(response_times) > 0:
        maximum = max(response_times)
        minimum = min(response_times)
        average = sum(response_times) / len(response_times)
        print("Approximate round trip times in milli-seconds:")
        print("Minimum =" + str(minimum) + "ms, Maximum = " + str(maximum) + "ms, Average =" + str(average) + " ms")


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
