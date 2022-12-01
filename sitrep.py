import devices
import netmiko


def main():

    # create devices
    dev_list = {
        "vpn_dc1": devices.create("vpn_dc1", "10.10.20.78", "linux", "ansible"),
        "dc1_6807": devices.create("dc1_6807", "10.10.10.53", "linux", "ansible")
    }
    # run test function on device
    [get_info(dev) for dev in dev_list.values()]


# Function to Get System Info
def get_info(device):
    # create netmiko object with device attrib
    working_dev = device.build()

    # Netmiko run command
    with netmiko.ConnectHandler(**working_dev) as net_connect:
        output = net_connect.send_command("uptime")

    print(f"\n{device.name}: {output}\n")


if __name__ == "__main__":
    main()
