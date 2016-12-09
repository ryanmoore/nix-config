.PHONY: ansible ubuntu help all

all: help;

help:
	@echo "Usage: \`make <target>' where target is:"
	@echo "    ubuntu - installs needed ubuntu packages"
	@echo "    ansible - runs ansible"
	@echo
	@echo "Expected usage is 2 commands:"
	@echo "    sudo make ubuntu  # sudo needed for packages"
	@echo "    make ansible  # will prompt for sudo" 

ubuntu:
	@echo "Installing minimum set of apps needed for ansible"
	apt install pip libssl-dev build-essential
	pip install ansible
	@echo
	@echo "IMPORTANT: Create a Gnome Terminal profile called \"Solarized\""
	@echo "\t this will be used for the solarized colorscheme in order to"
	@echo "\t preserve the \"Default\""
	@echo

ansible:
	ansible-playbook -i ./ansible/hosts -s ./ansible/setup.yml --connection=local --ask-sudo-pass
