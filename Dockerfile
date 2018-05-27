FROM debian:8.10
RUN apt-get update
RUN apt-get install -y python-pip python-dev lib32ncurses5-dev net-tools
RUN apt-get install -y openvswitch-common openvswitch-switch python-openvswitch
RUN pip install ishell
RUN pip install netifaces
ADD command.py /
ADD console.py /
ADD log.py /
ADD util.py /
ADD utils.py /
ADD vswitch.py /
ADD common.py /
ADD shell.py /
CMD ["python","./shell.py"]
