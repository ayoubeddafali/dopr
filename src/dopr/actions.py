import digitalocean
import os, sys, subprocess, random, time

TOKEN = os.getenv("DO_TOKEN")
manager = digitalocean.Manager(token=TOKEN)

def install(packages, ips, itype):
    print("Installing {} packages : {}".format(len(packages), packages ))
    time.sleep(30)
    for droplet in ips:
        CMD = "ssh -o 'StrictHostKeyChecking no' root@{} 'sudo apt-get install -y'".format(droplet)  if itype == "ubuntu" else "ssh -o 'StrictHostKeyChecking no' root@{} 'sudo yum install -y'".format(ip)
        for p in packages:
            print("=> Installing {}".format(p))
            try:
                subprocess.call("{} {}".format(CMD, p), shell=True)
            except Exception as e :
                print("Error install package {}".format(p))
                print(e)

def list():
    print("=> Listing resources :")
    my_droplets = manager.get_all_droplets()
    print("\t {} found resources".format(len(my_droplets)))
    for droplet in my_droplets:
        print("{} : {}".format(droplet.name, droplet.ip_address))

def status():
    print("=> Checking Status")
    my_droplets = manager.get_all_droplets()
    if len(my_droplets) > 0:
        for droplet in my_droplets:
            print("{} [{}] : {}".format(droplet.name, droplet.ip_address,  droplet.status))
    else:
        print("No droplets has been found")

def create_domains(domains):
    ip = domains[0]
    domain_name = domains[1]
    sub_domains = domains[2:]

    domain = digitalocean.Domain(token=TOKEN)
    domain.name = domain_name
    domain.ip_address = ip
    try:
        d = domain.create()
    except Exception as e:
        print(e)

    print("=> {} domain has been created : ".format(domain_name))

    if (sub_domains and len(sub_domains) > 0):
        for sub in sub_domains:
            domain.create_new_domain_record(type="A", name=sub, data=ip)
            print("\t- {}.{} domain has been created. ".format(sub, domain))

def remove_resource(resource_type):
    if resource_type.lower() == "droplets" or resource_type.lower() == "droplet" :
        print("=> Destroying All Droplets")
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            droplet.destroy()
    elif resource_type.lower() == "domains" or resource_type.lower() == "domain":
        print("=> Deleting All Domains")
        my_domains = manager.get_all_domains()
        for domain in my_domains:
            domain.destroy()
    else :
        print("Invalid Resource '{}'".format(resource_type))

def clean():
    remove_resource("droplets")
    remove_resource("domains")

def create(itype="centos", inumber=1, isize="s-1vcpu-1gb", packages=[], inventory=[]):
    print("=> Provisionning ....")
    manager = digitalocean.Manager(token=TOKEN)
    keys = manager.get_all_sshkeys()
    image = 'centos-7-x64' if itype == "centos" else 'ubuntu-16-04-x64'

    droplets = []
    for i in range(int(inumber)):
        droplets.append("vm{}".format(i+1))

    for droplet in droplets :
        d = digitalocean.Droplet(token=TOKEN,
                                name="gen-temp-{}".format(droplet),
                                region='sfo2', # Amster
                                image=image, # Ubuntu 14.04 x64
                                size_slug=isize,  # 512MB
                                ssh_keys=keys, #Automatic conversion
                                backups=False)

        d.create()

    my_droplets = manager.get_all_droplets()
    print("=> {} machine(s) has been created.".format(len(my_droplets)))
    seen = []
    print("=> Waiting for Instances to be active...")
    while len(seen) != len(my_droplets) :
        for droplet in my_droplets:
            if droplet.name in [ n["name"] for n in seen]:
                continue
            elif droplet.status == "active":
                seen.append({"name": droplet.name, "ip": droplet.ip_address})
        my_droplets = manager.get_all_droplets()

    print("All this Instance are in actif state :")

    for d in seen:
        print(" - {} : {}".format(d["name"], d["ip"]))
        time.sleep(0.5)

    droplets_ips = map(lambda d: d.ip_address , my_droplets)
    if ( packages and ( len(packages) > 0 )  ):
        install(packages, droplets_ips, itype)

    if ( inventory and ( len(inventory) > 0 )  ) :
        f =  open("inventory", "w")
        for i, host in enumerate(inventory):
            f.write("\n[{}]\n{}".format(host, seen[i]["ip"]))
        f.close()

