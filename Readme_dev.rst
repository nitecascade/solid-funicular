To create the Conda environment capstone35
------------------------------------------

See Readme_conda.

Setup the shell environment using *conda activate*
--------------------------------------------------

Activate the conda environment capstone35::

    $ source activate capstone35

Do some additional initialization to the shell environment::

    $ source ./env.sh

Verify that PATH has been updated correctly::

    $ type python
    python is .../anaconda2/envs/capstone35/bin/python

    $ type meetup-groups.py
    meetup-groups.py is .../bin/meetup-groups.py


Setup the shell environment using *cenv*
----------------------------------------

Start a subshell initialized to the conda environment capstone35::

    $ bin/cenv -e env.sh capstone35 bash
    (capstone35)$ 

Verify that PATH has been updated correctly::

    (capstone35)$ type python
    python is .../anaconda2/envs/capstone35/bin/python

    (capstone35)$ type meetup-groups.py
    meetup-groups.py is .../bin/meetup-groups.py


Workflow
--------

Download the list of Meetup groups near SF::

    $ meetup-groups.py >groups.json
    $ wc -l groups.json
        8288 groups.json

Extract just group_ids and group names for Meetup groups near SF::

    $ group_summary.py groups.json | sort -n >groups.txt
    $ head groups.txt
    26434 The San Francisco Bay Area British and Irish Social Club
    33172 中文俱樂部 Chinese Language Group in The San Francisco Bay Area
    41930 The San Francisco Peninsula Dads Meetup Group
    54356 The San Francisco English Bulldog Meetup Group
    54659 Entrepreneurs & VCs
    62769 The San Francisco Formula 1 Meetup Group
    63891 LES AMI(E)S FRANCOPHONES DE SAN FRANCISCO
    63937 Alameda / Contra Costa Co. Rendez-vous français
    65802 San Franciso Game Development Meetup Group
    67805 SF German Stammtisch

Download the Meetup group membership data for groups near SF::

    $ get-meetup-members-in-all-groups.sh groups.txt

Check the contents of the members_in_group stash::

    $ get-meetup-members-in-all-groups.sh /dev/null
    stash big_data/members_in_group_:
    members_in_group_/2/6/26434.json
    members_in_group_/3/3/33172.json
    members_in_group_/4/1/41930.json
    members_in_group_/5/4/54356.json
    members_in_group_/5/4/54659.json
    members_in_group_/6/2/62769.json
    members_in_group_/6/3/63891.json
    members_in_group_/6/3/63937.json
    members_in_group_/6/5/65802.json
    members_in_group_/6/7/67805.json
    ...
