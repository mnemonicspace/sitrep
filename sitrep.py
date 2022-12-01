import devices
import netmiko


def main():
    vpn_dc1 = devices.create(
        "10.1.14.131", "paloalto_panos", "~/.ssh/test", "admin")

    get_info(vpn_dc1)
    return


def get_info(device):

    working_dev = device.build()

    print(working_dev)


if __name__ == "__main__":
    main()
