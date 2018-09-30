import argparse

class CreateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        inumber, itype, isize = values 
        namespace.instance_number = inumber
        namespace.instance_type = itype
        namespace.instance_size = isize

def create_parser():
    parser = argparse.ArgumentParser(
        description="""
            CLI Tool for my Digital Ocean Workspace
        """
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", '--create', help='Create Instance  <INSTANCE_NUMBER> <INSTANCE_TYPE> <INSTANCE_SIZE>',
        nargs=3,
        metavar=("INSTANCE_NUMBER", "INSTANCE_TYPE", "INSTANCE_SIZE"),
        action=CreateAction)
    parser.add_argument("-p", "--packages", help="Packages to install", 
        nargs='+')
    
    parser.add_argument("-w ", "--with-inventory", help="Create an Ansible Inventory file", nargs='+')

    group.add_argument("--clean", help="Remove all resources", action="store_true")
    group.add_argument("--list", help="List all resources", action="store_true")
    group.add_argument("--status", help="Check status", action="store_true")

    return parser

def main():
    from dopr import actions 
    parser = create_parser()
    args = vars(parser.parse_args())
    # print(args)     
    if "instance_number" in args:
        actions.create(args['instance_type'], args['instance_number'], args['instance_size'], args['packages'], args["with_inventory"])
    elif args["list"]:
        actions.list()
    elif args["clean"]:
        actions.clean()
    elif args["status"]:
        actions.status()
    else:
        parser.print_help()

