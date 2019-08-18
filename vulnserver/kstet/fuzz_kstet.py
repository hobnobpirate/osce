#!/usr/bin/python3
"""A boofuzz fuzzing template for vulnserver KSTET"""

import boofuzz as bf


def get_banner(target: bf.Target, my_logger: bf.FuzzLoggerCsv, session: bf.Session, *args, **kwargs) -> None:
    """Get vulnserver banner for boofuzz callback"""
    banner_template = b"Welcome to Vulnerable Server! Enter HELP for help."
    try:
        banner = target.recv(1024)
    except:
        print("Unable to connect. Target is down. Exiting.")
        exit()

    my_logger.log_check("Receiving banner..")
    if banner_template in banner:
        my_logger.log_pass("banner received")
    else:
        my_logger.log_fail("No banner received")
        print("No banner received, exiting..")
        exit()


def main() -> None:
    """Run the fuzzer"""
    port = 9999
    host = "192.168.99.100"
    protocol = "tcp"

    csv_log = open("fuzz_results_KSTET.csv", "w")
    my_logger = [bf.FuzzLoggerCsv(file_handle=csv_log)]
    target = bf.Target(connection=bf.SocketConnection(host, port, proto=protocol))
    session = bf.Session(target=target)

    # FUZZING PARAMETERS
    bf.s_initialize("KSTET")
    bf.s_string("KSTET", fuzzable=False)
    bf.s_delim(" ", fuzzable=False)
    bf.s_string("FUZZ") #Fuzzable parameter
    bf.s_static("\r\n")
    
    #session.sleep_time = 1.0
    session.connect(bf.s_get("KSTET"), callback=get_banner)
    session.fuzz()


if __name__ == "__main__":
    main()
