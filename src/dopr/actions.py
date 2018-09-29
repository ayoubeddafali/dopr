import digitalocean
import os
import os, sys, subprocess, random

TOKEN = os.getenv("DO_TOKEN")
manager = digitalocean.Manager(token=TOKEN)


def clean():
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.destroy()

    print("=> Destroying All Droplets")

    my_domains = manager.get_all_domains()
    for domain in my_domains:
        domain.destroy()

    print("=> Deleting All Domains")

def list():
    print("=> Listing resources :")
    my_droplets = manager.get_all_droplets()
    print("\t {} found resources".format(len(my_droplets)))
    for droplet in my_droplets:
        print("{} : {}".format(droplet.name, droplet.ip_address))
    

def create(itype="centos", inumber=1, isize="s-1vcpu-1gb"):
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
    print("=> {} machine(s) has been created : ".format(len(my_droplets)))
    seen = []
    while len(seen) != len(my_droplets) :

        for droplet in my_droplets:
            if droplet.name in seen:
                continue
            else :
                if droplet.status == "active":
                    seen.append(droplet.name)
                    print(" - {} : {}".format(droplet.name, droplet.ip_address))
        my_droplets = manager.get_all_droplets()


