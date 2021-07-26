# Quickstart

## Instalation

Download ZIP file or clone the repository:

```
git clone git@github.com:mihudec/epnm_websocket_client.git
```

Note: Tested on Python 3.9, partialy on 3.8


## Usage

```
python3 cli_client.py --host 1.2.3.4 --user admin --topic all --ask-password --echo
Password: <enter secret password>
```

Incomming messages are by default stored in `epnm_output` in your Current Working Directory (CWD)

Logfile is by default in `epnm_websocket.log` in CWD


## Help

```
cd ./EpnmWebsocketClient
python3 cli_client.py --help
usage: cli_client.py [-h] --host HOST --user USERNAME --ask-password --topic {inventory,service-activation,template-execution,alarm,all} [-v {1,2,3,4,5}] [--echo]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           IP or FQDN of EPNM Server
  --user USERNAME       Username
  --ask-password        Password prompt switch - DO NOT ENTER PASSWORD, wait for prompt
  --topic {inventory,service-activation,template-execution,alarm,all}
                        Topic
  -v {1,2,3,4,5}, --verbosity {1,2,3,4,5}
                        Verbosity level
  --echo                If specified, will print incomming messages to stdout
```