from hailo_platform import Device

device = Device()
print(device.device_id)
print(device.control.get_extended_device_information())