import devices
import netmiko


def main():

    # create devices
    vpn_dc1 = devices.create(
        "10.1.14.131", "paloalto_panos", "~/.ssh/test", "admin")

    # run test function on device
    get_info(vpn_dc1)


# Function to Get System Info
def get_info(device):
    # create netmiko object with device attrib
    working_dev = device.build()
    # Just print the object for now, no calls yet
    print(working_dev)


if __name__ == "__main__":
    main()
