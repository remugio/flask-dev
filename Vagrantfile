# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
 config.vm.box = "hashicorp/precise64"
 
 dirname = File.basename(Dir.getwd)
 config.vm.hostname = dirname

 config.vm.network "forwarded_port", guest: 5000, host: 5000
 config.vm.network "forwarded_port", guest: 8080, host: 8089
 config.vm.network "forwarded_port", guest: 80, host: 8091

$script = <<SCRIPT
echo "Provisioning Flask, Tornado, Zeroconf"
sudo apt-get update
sudo apt-get -y install python avahi-daemon python-pip git curl upstart libmysqlclient-dev python-dev apache2
sudo pip install -r /vagrant/requirements.txt

# Set MySQL root password
debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password root'
debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password root'
echo "phpmyadmin phpmyadmin/dbconfig-install boolean true" | debconf-set-selections
echo "phpmyadmin phpmyadmin/app-password-confirm password root" | debconf-set-selections
echo "phpmyadmin phpmyadmin/mysql/admin-pass password root" | debconf-set-selections
echo "phpmyadmin phpmyadmin/mysql/app-pass password root" | debconf-set-selections
echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2" | debconf-set-selections

# Install MySQL packages
apt-get -y install mysql-server phpmyadmin

# Setup database
echo "DROP DATABASE IF EXISTS flaskr" | mysql -uroot -proot
echo "CREATE USER 'admin'@'localhost' IDENTIFIED BY 'default'" | mysql -uroot -proot
echo "CREATE DATABASE flaskr" | mysql -uroot -proot
echo "GRANT ALL ON flaskr.* TO 'admin'@'localhost'" | mysql -uroot -proot
echo "FLUSH PRIVILEGES" | mysql -uroot -proot
mysql -uroot -proot flaskr < /vagrant/schema.sql

cp -v /vagrant/tornado.conf /etc/init/tornado.conf
sudo initctl emit vagrant-ready
SCRIPT

config.vm.provision "shell", inline: $script

end