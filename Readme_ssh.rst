Setup SSH config file to streamline connecting to EC2 instances
---------------------------------------------------------------

Edit the file ~/.ssh/config (or create it if you do not have one),
and put an entry like this into it::

    Host ec2-m4 m4
        Hostname ec2-54-227-206-115.compute-1.amazonaws.com
        User ec2-user
        Protocol 2
        IdentityFile ~/.ssh/ec2-galvanize.pem

The first line lists *aliases* for the remote host. The *Hostname* line
is the DNS name or IP address of the remote. The *User* line specifies
which remote user to connect as. The *Protocol* lines indicates which
SSH connection protocol to use; you probably should leave this as *2*.
The last line indicates the *PEM* file to use.

Make sure the permissions on ~/.ssh/config are *rw-------*, or equivalently
*600*::

    $ chmod 600 ~/.ssh/config

With the SSH config file set up as shown, you will be able to run this::

    $ ssh ec2-m4

instead of this::

    $ ssh -i ~/.ssh/ec2-galvanize.pem ec2-user@ec2-54-227-206-115.compute-1.amazonaws.com

The following also works because any one of the multiple *aliases* from the
Host line can be used::

    $ ssh m4

And when copying files from the local host to the EC2 host, you can use::

    $ scp file-on-my-laptop m4:

to copy *file-on-my-laptop* to the home directory on the EC2 host, instead of::

    $ scp -i ~/.ssh/ec2-galvanize.pem file-on-my-laptop ec2-user@ec2-54-227-206-115.compute-1.amazonaws.com:
