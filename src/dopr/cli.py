import argparse, sys

class CreateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        inumber, itype, isize = values
        namespace.instance_number = inumber
        namespace.instance_type = itype
        namespace.instance_size = isize

class RemoveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        namespace.resource_type = values[0]


def create_parser():
    parser = argparse.ArgumentParser(
        description="""
            CLI Tool for my Digital Ocean Workspace
        """
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", '--create', help='Create a Droplet',
        nargs=3,
        metavar=("INSTANCE_NUMBER", "INSTANCE_TYPE", "INSTANCE_SIZE"),
        action=CreateAction)

    parser.add_argument("-p", "--packages", help="Packages to install", nargs='+')
    parser.add_argument("-w", "--with-inventory", help="Create an Ansible Inventory file", nargs='+')
    group.add_argument("-a", "--add-domains", nargs='+' , help='Create domain & subdomains' )
    group.add_argument("--clean", help="Remove all resources", action="store_true")
    group.add_argument("-d", "--destroy", nargs=1, metavar=("RESOURCE_TYPE"), action=RemoveAction, help="Remove Specific Resource")
    group.add_argument("-l", "--list", help="List all resources", action="store_true")
    group.add_argument("-s", "--status", help="Check status", action="store_true")

    return parser

def main():
    from dopr import actions
    parser = create_parser()
    args = vars(parser.parse_args())
    #print(args)
    #sys.exit(0)
    if "instance_number" in args:
        actions.create(args['instance_type'], args['instance_number'], args['instance_size'], args['packages'], args["with_inventory"])
    elif "resource_type" in args:
        actions.remove_resource(args["resource_type"])
    elif args["list"]:
        actions.list()
    elif args["clean"]:
        actions.clean()
    elif args["status"]:
        actions.status()
    elif ( args["add_domains"] and len(args["add_domains"]) > 0 ):
        actions.create_domains(args["add_domains"])
    else:
        parser.print_help()

