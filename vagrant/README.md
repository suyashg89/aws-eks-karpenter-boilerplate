# Vagrant Virtual Machines

[Hashicorp Vagrant](https://www.vagrantup.com/intro) is a tool for building and managing virtual machine environments in a single workflow. It gives you a disposable environment and consistent workflow for developing and testing infrastructure management scripts. For more information about Vagrant, please check its [documentation](https://www.vagrantup.com/docs)

## Pre-Requisites

This folder contains vagrantfile to create an Ubuntu 16.04 Linux environment with python, Docker-CE, Ansible, AWS CLI, etc. installed in it. To use the vagrantfile, please complete the below pre-requisites in your local system:-

- Install VirtualBox by [downloading](https://www.virtualbox.org/wiki/Downloads) and installing it with default steps as recommended during installation.
- Install Vagrant by following the [installation insructions](https://www.vagrantup.com/docs/installation).
- Install vagrant-vbguest plugin by following the [installation instructions](https://github.com/dotless-de/vagrant-vbguest).

## Configure Your Vagrant VM

Please follow the below steps to configure your choice of vagrant VM by following below steps:-

1 From your cmd prompt, run the below commands from a folder location in your system to setup the Vagrant project:-

- `$ mkdir vagrant`
- `$ cd vagrant`

2 Place the vagrantfile in the newly created `vagrant` folder from the above step.

3 Update the required parameters in the vagrantfile as instructed in the comments.

4 Run `vagrant up` from the same location where you have placed your vagrantfile. It will start setting up the vagrant VM and generally takes 3-4 mins to complete.

5 Once the VM setup is completed, run `vagrant ssh` to ssh into your vagrant VM.

6 To run ansible playbooks using the ansible installed in Ubuntu 16.04 VM, please activate the virtualEnv by running `source /home/vagrant/venv/bin/activate` which uses Python3 as its default python environment.
