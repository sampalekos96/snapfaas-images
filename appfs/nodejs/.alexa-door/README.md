### Description
This function send out "open the door" request to the door device described below.

### Door Device
```bash
cd door-device
./deploy.sh
```
The commands above should deploy a door device in a docker container.

### Test
After deploying a door device, one can use `make test` to test.

`make test` returns success message when the IP is the machine's IP address (typically eth0's IP address)
and returns failure message when the IP is incorrect.

`make test` should always successfully print a json message.
