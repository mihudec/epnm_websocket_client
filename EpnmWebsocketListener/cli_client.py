import argparse
import getpass
from EpnmWebsocketListener import EpnmWebsocketListener

class PasswordPromptAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None
        ):
        super(PasswordPromptAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help
        )

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)

def parse_args():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--host", dest="host", type=str, required=True, help="IP or FQDN of EPNM Server")
    arg_parser.add_argument("--user", dest="username", type=str, required=True, help="Username")
    arg_parser.add_argument("--ask-password", dest="password", action=PasswordPromptAction, type=str, required=True, help="Password")
    arg_parser.add_argument("--topic", dest="topic", type=str, required=True, help="Topic", choices=['inventory', 'service-activation', 'template-execution', 'alarm', 'all'])
    arg_parser.add_argument("-v", "--verbosity", dest="verbosity", type=int, choices=[1, 2, 3, 4, 5], default=4, help="Verbosity level")

    args = arg_parser.parse_args()
    # args["password"] = getpass.getpass()
    return args

def main():
    args = parse_args()
    client = EpnmWebsocketListener(host=args.host, username=args.username, password=args.password, verbosity=args.verbosity)
    client.run(topic=args.topic)

if __name__ == '__main__':
    main()

