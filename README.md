# Ping-Traceroute
This project is a replica of the real world Ping and Traceroute applications. 

The submission consists of 2 python files<br>
1. rd9012_ping.py
2. rd9012_traceroute.py

NOTE: This code requires root access.<br>
	    May need to run the python terminal/command prompt as admin with the firewall turned off<br>
	    This is beacuse the code uses raw socket<br>
	
For rd9012_ping.py<br>

MENU:<br>
-c count     	:Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified ping will operate until interrupted.<br>
-i wait      	:Wait wait seconds between sending each packet. The default is to wait for one second between each packet.<br>
-s packetsize	:Specify the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes when combined with the 8 bytes of ICMP header data.<br>
-t timeout   	:Specify a timeout, in seconds, before ping exits regardless of how many packets have been received.<br>

STEPS TO RUN THE CODE:<br>

1. Open the python terminal/ command prompt as admin i.e. run as admin
2. Type python(or python3) rd9012_ping.py -c/-i/-s/-t hostname
   For example,
   a. python rd9012_ping.py google.com 		This is the ping with default number of packets, to stop, use ctrl+c 
   b. python rd9012_ping.py -c 2 google.com This will terminate after c packets have been sent
   c. python rd9012_ping.py -i 3 google.com This is the ping with default number of packets, to stop, use ctrl+c
   d. python rd9012_ping.py -s 3 google.com This is the ping with default number of packets, to stop, use ctrl+c
   e. python rd9012_ping.py -t 3 google.com This will terminate after timeout, to stop before that, use ctrl+c
   

For rd9012_tarceroute.py<br>

MENU:<br>
-n          :Print hop addresses numerically rather than symbolically and numerically.<br>
-q nqueries :Set the number of probes per ttl to nqueries.<br>
-S          :Print a summary of how many probes were not answered for each hop<br>


STEPS TO RUN THE CODE:<br>

1. Open the python terminal/ command prompt as admin i.e. run as admin
2. Type python(or python3) rd9012_traceroute.py -n/-q/-S hostname
   For example,
   a. python rd9012_traceroute.py google.com      This will terminate after path is printed (max of 30 hops)
   b. python rd9012_traceroute.py -n google.com   This will terminate after path is printed (max of 30 hops)
   c. python rd9012_traceroute.py -q 5 google.com This will terminate after path is printed (max of 30 hops)
   d. python rd9012_traceroute.py -S google.com	  This will terminate after path is printed (max of 30 hops)
