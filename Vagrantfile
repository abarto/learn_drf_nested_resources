# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  config.vm.hostname = "learn-drf-nested-resources.local"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.network "forwarded_port", guest: 80, host: 8000

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

  config.vm.synced_folder ".", "/home/vagrant/learn_drf_nested_resources/"

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

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-dev postgresql postgresql-server-dev-all nginx

    sudo -u postgres psql --command="CREATE USER learn_drf_nested_resources WITH PASSWORD 'learn_drf_nested_resources';"
    sudo -u postgres psql --command="CREATE DATABASE learn_drf_nested_resources WITH OWNER learn_drf_nested_resources;"
    sudo -u postgres psql --command="GRANT ALL PRIVILEGES ON DATABASE learn_drf_nested_resources TO learn_drf_nested_resources;"

    echo '
# learn_drf_with_images.conf

upstream django {
  server 127.0.0.1:8000;
}

server {
  listen      80;
  server_name 127.0.0.1 localhost learn-drf-nested-resources learn-drf-nested-resources.local;
  charset     utf-8;

  client_max_body_size 75M;   # adjust to taste

  location /static {
      alias /home/vagrant/learn_drf_nested_resources/learn_drf_nested_resources/static;
  }

  location / {
      proxy_pass       http://django;
      proxy_redirect   off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Host $server_name:8000;
  }
}
    ' > /etc/nginx/conf.d/learn_drf_nested_resources.conf

    service nginx restart
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv-3.4 --without-pip learn_drf_nested_resources_venv
    source learn_drf_nested_resources_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install -r learn_drf_nested_resources/requirements.txt

    cd learn_drf_nested_resources/learn_drf_nested_resources/

    python manage.py migrate

    echo '
    [
    {
        "pk": 1,
        "model": "auth.user",
        "fields": {
            "last_name": "",
            "password": "pbkdf2_sha256$20000$fUZfRXo5pI0X$uq5/DUsH4ArHdhr5Dv0gfKauW6HMrX4o3ANE5d7sois=",
            "groups": [],
            "is_superuser": true,
            "date_joined": "2015-07-08T00:22:51.199Z",
            "email": "vagrant@learn-drf-nested-resources.local",
            "first_name": "",
            "is_staff": true,
            "last_login": "2015-07-10T00:07:25.995Z",
            "is_active": true,
            "username": "admin",
            "user_permissions": []
        }
    },
    {
        "pk": 2,
        "model": "auth.user",
        "fields": {
            "last_name": "Doe",
            "password": "pbkdf2_sha256$20000$FUn3mhnbQNHz$SDYMXBmFNOcT/tKK6Xq162M8PoWv+ox3YsplPD8OWeI=",
            "groups": [],
            "is_superuser": false,
            "date_joined": "2015-07-08T00:52:05Z",
            "email": "john.doe@learn-drf-nested-resources.local",
            "first_name": "John",
            "is_staff": false,
            "last_login": null,
            "is_active": true,
            "username": "user1",
            "user_permissions": []
        }
    },
    {
        "pk": 3,
        "model": "auth.user",
        "fields": {
            "last_name": "Doe",
            "password": "pbkdf2_sha256$20000$IZ3WijqqoQQA$kszc9d98228H9Gkl/Ar64Sst2UVkrweA45TxUubgdPQ=",
            "groups": [],
            "is_superuser": false,
            "date_joined": "2015-07-08T00:53:06Z",
            "email": "jane.doe@learn-drf-nested-resources.local",
            "first_name": "Jane",
            "is_staff": false,
            "last_login": null,
            "is_active": true,
            "username": "user2",
            "user_permissions": []
        }
    },
    {
        "pk": "588660f1-4848-4a32-8eb5-9688fd4409dd",
        "model": "blogposts.blogpost",
        "fields": {
            "author": [
                "user1"
            ],
            "title": "A longer blogpost",
            "created": "2015-07-10T00:15:38.135Z",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus maximus, lorem eget accumsan maximus, ante mauris lacinia massa, sit amet pellentesque nisl leo eu libero. Fusce hendrerit risus eu vehicula cursus. Duis tincidunt enim eget felis tempus, ut consequat purus elementum. Fusce placerat quis tortor ut iaculis. Duis a tincidunt tellus. Sed viverra sem eu mollis tempus. Mauris id rutrum tortor. Praesent sit amet auctor urna. Morbi placerat lorem eget dignissim sollicitudin. Integer pulvinar sit amet turpis vitae porta. Nunc enim eros, viverra in mauris quis, porta commodo velit. Mauris nec condimentum lacus, eu lobortis ligula. Aenean quis leo a neque tincidunt sollicitudin eget a arcu. Proin in rhoncus velit. Proin vel nisi vitae ante iaculis consequat.\r\n\r\nVivamus varius gravida ultrices. Sed eu sollicitudin neque. Nullam finibus consequat libero, vitae posuere magna suscipit ut. Maecenas ultrices purus vitae lorem iaculis, a volutpat lectus tempor. Proin auctor urna dolor, ut pellentesque est fringilla eu. Curabitur placerat dolor ac ornare rhoncus. In tellus nunc, vulputate eu odio ac, facilisis venenatis arcu. In ullamcorper consequat nunc, non aliquet nulla efficitur at. Phasellus non aliquet est, vel convallis sapien. In vel dui a dui rhoncus auctor eu eu mi. Duis porttitor turpis neque. Fusce.",
            "description": "Lorem ipsum dolor sit amet...",
            "modified": "2015-07-10T00:16:34.192Z",
            "allow_comments": true,
            "slug": "a-longer-blogpost"
        }
    },
    {
        "pk": "b44d4918-219e-4496-9318-b68ab13e2b25",
        "model": "blogposts.blogpost",
        "fields": {
            "author": [
                "user1"
            ],
            "title": "A short blogpost",
            "created": "2015-07-10T00:14:06.500Z",
            "content": "This is just a short blogpost.",
            "description": "The description of the blogpost is short",
            "modified": "2015-07-10T00:14:06.501Z",
            "allow_comments": true,
            "slug": "a-short-blogpost"
        }
    },
    {
        "pk": "17288f69-bbd7-4758-adfd-a96d0fa5ca01",
        "model": "blogposts.comment",
        "fields": {
            "modified": "2015-07-10T00:24:47.766Z",
            "author": [
                "user1"
            ],
            "blogpost": "588660f1-4848-4a32-8eb5-9688fd4409dd",
            "created": "2015-07-10T00:24:47.766Z",
            "content": "I hate the Internet"
        }
    },
    {
        "pk": "1d17157d-ef58-4260-bff1-32de18417e2e",
        "model": "blogposts.comment",
        "fields": {
            "modified": "2015-07-10T00:23:33.890Z",
            "author": [
                "user2"
            ],
            "blogpost": "b44d4918-219e-4496-9318-b68ab13e2b25",
            "created": "2015-07-10T00:23:33.889Z",
            "content": "I hate this"
        }
    },
    {
        "pk": "4f442d14-6728-4280-bd0e-e4f402e7c543",
        "model": "blogposts.comment",
        "fields": {
            "modified": "2015-07-10T00:23:46.778Z",
            "author": [
                "user2"
            ],
            "blogpost": "b44d4918-219e-4496-9318-b68ab13e2b25",
            "created": "2015-07-10T00:23:46.777Z",
            "content": "I love this"
        }
    },
    {
        "pk": "72bc133a-0ec2-4eb7-b4bd-bed7a4c8e262",
        "model": "blogposts.comment",
        "fields": {
            "modified": "2015-07-10T00:23:20.959Z",
            "author": [
                "admin"
            ],
            "blogpost": "b44d4918-219e-4496-9318-b68ab13e2b25",
            "created": "2015-07-10T00:23:20.958Z",
            "content": "This blogpost is short"
        }
    },
    {
        "pk": "81ee47f5-009d-431c-a9ca-081b612f9a79",
        "model": "blogposts.comment",
        "fields": {
            "modified": "2015-07-10T00:23:40.498Z",
            "author": [
                "user2"
            ],
            "blogpost": "b44d4918-219e-4496-9318-b68ab13e2b25",
            "created": "2015-07-10T00:23:40.498Z",
            "content": "I still hate this"
        }
    },
    {
        "pk": "c3c4ea88-1f11-4317-bb6e-99eb5a578561",
        "model": "blogposts.comment",
        "fields": {
            "modified": "2015-07-10T00:24:01.162Z",
            "author": [
                "user1"
            ],
            "blogpost": "b44d4918-219e-4496-9318-b68ab13e2b25",
            "created": "2015-07-10T00:24:01.162Z",
            "content": "I hate the Internet"
        }
    },
    {
        "pk": 1,
        "model": "oauth2_provider.application",
        "fields": {
            "client_secret": "MCh6Z4EuNGoejZkBoQbzxI0yMasoGENPQ70QweqJySQhNEXZBSQ6eon2c1A81idgJsX9mCvpbJaPYY9xt1UiVvMgboj4Jw2j4Nkv6iCWe3rCmqOOKw19gI4cukDpSwSd",
            "skip_authorization": true,
            "client_type": "public",
            "name": "learn_drf_nested_resources_app",
            "user": [
                "admin"
            ],
            "redirect_uris": "",
            "client_id": "7ytbv0sG9FusDdDYRcZPUIGoNrx9TBZJnye5CVvj",
            "authorization_grant_type": "password"
        }
    }
    ]
    ' > data.json

    python manage.py loaddata data.json
    python manage.py collectstatic --noinput
  SHELL

  config.vm.provision "shell", run: "always", privileged: false, inline: <<-SHELL
    source /home/vagrant/learn_drf_nested_resources_venv/bin/activate

    cd /home/vagrant/learn_drf_nested_resources/learn_drf_nested_resources

    gunicorn --bind 127.0.0.1:8000 --daemon --workers 4 learn_drf_nested_resources.wsgi
  SHELL
end
