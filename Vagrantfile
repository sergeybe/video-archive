# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"

   config.vm.provider "virtualbox" do |vb|
     vb.gui = false
     vb.memory = "2048"
   end

  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/playbook.yml"
    ansible.inventory_path = "ansible/inventory"
    ansible.become = true
    ansible.verbose = "vv"
    ansible.limit = "vagrant"
#    ansible.tags = "django"
  end
end
