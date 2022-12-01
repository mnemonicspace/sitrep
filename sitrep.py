import devices
import netmiko


def main():

    # create devices
    dev_list = {
        "vpn_dc1": devices.create("10.1.14.131", "paloalto_panos", "admin"),
        "dc1_6807": devices.create("10.1.14.52", "cisco_ios", "admin")
    }
    # run test function on device
    [get_info(dev) for dev in dev_list.values()]


# Function to Get System Info
def get_info(device):
    # create netmiko object with device attrib
    working_dev = device.build()
    # Just print the object for now, no calls yet
    print(working_dev)


if __name__ == "__main__":
    main()
