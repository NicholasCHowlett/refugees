# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/trusty64"

  # Provisioning with shell script below. Installs Python web application development environment.
  config.vm.provision "shell", inline: <<-SHELL

  # install apache (development package needed for mod_wsgi module)
  apt-get update
  apt-get install -y apache2
  apt-get install -y apache2-dev

  # create virtual environment (venv)
  sudo apt-get install -y python3-pip
  sudo apt-get install python3.4-venv
  cd /vagrant
  python3 -m venv adani

  # install mod_wsgi & ipython packages locally (within venv)
  source adani/bin/activate
  pip3 install -U pip
  pip3 install mod_wsgi
  pip3 install ipython

  # link vagrant directory to web server's document root directory
  sudo ln -fs /vagrant /var/www

  # map base url to python application script
  sudo sed -i '$a WSGIScriptAlias / /var/www/vagrant/adani.py' /etc/apache2/apache2.conf

  # load mod_wsgi module
  sudo sed -i '$a WSGIPythonHome "/vagrant/adani"' /etc/apache2/apache2.conf
  sudo sed -i '$a LoadModule wsgi_module "/vagrant/adani/lib/python3.4/site-packages/mod_wsgi/server/mod_wsgi-py34.cpython-34m.so"' /etc/apache2/apache2.conf

  sudo service apache2 restart

  # install git globally (outside venv)
  deactivate
  sudo apt-get install -y git

  # install web scraping related packages locally 
  source adani/bin/activate
  pip3 install beautifulsoup4
  pip3 install lxml
  pip3 install requests

  SHELL

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.
end
