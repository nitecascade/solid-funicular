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

(Optional) Install bash startup files::

    $ cd
    $ wget -O bash_setup.zip http://bit.ly/28Ojy6b
    $ unzip bash_setup.zip
    $ bash_setup/install.sh

Check that all the files were symlinked correctly. The install script will not
overwrite existing files. Move those files out of the way and try installing
again.
