To set up a fresh EC2 instance
------------------------------

Install some essentials::

    $ sudo yum install tmux
    $ sudo yum install git
    $ wget http://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh
    $ bash Anaconda2-4.0.0-Linux-x86_64.sh

Create conda envs

    See Readme_conda

Clone the capstone repo::

    $ mkdir -p ~/git/galvanize
    $ cd ~/git/galvanize
    $ git clone https://github.com/nitecascade/solid-funicular.git

Install the AWS keys. You will have to get these from Amazon.com
or copy them from another host where you saved it::

    $ ls -l ~/.aws/
    total 20
    -rwxr-xr-x 1 ec2-user ec2-user 1552 Jun 22 23:29 env_to_json.sh
    -rw-r--r-- 1 ec2-user ec2-user   55 Jun 22 23:29 makefile
    -rw-r--r-- 1 ec2-user ec2-user  248 Jun 22 23:29 Readme
    -rw-r--r-- 1 ec2-user ec2-user  120 Jun 22 23:29 rootkey.env
    -rw-r--r-- 1 ec2-user ec2-user  178 Jun 22 23:29 rootkey.json

Install the MeetUp.com API key. You will have to get this from Meetup.com
or copy it from another host where you saved it::

    $ ls -l ~/.meetup/
    total 8
    -rw-r--r--  1 fmachi  502  31 Jun 20 12:12 apikey

(Optional) Install bash startup files::

    $ cd
    $ wget -O bash_setup.zip http://bit.ly/28Ojy6b
    $ unzip bash_setup.zip
    $ bash_setup/install.sh

Check that all the files were symlinked correctly. The install script will not
overwrite existing files. Move those files out of the way and try installing
again.
