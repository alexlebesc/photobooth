echo auto | sudo tee /sys/bus/usb/devices/2-2/power/control
echo '2-2' | sudo tee /sys/bus/usb/drivers/usb/unbind
