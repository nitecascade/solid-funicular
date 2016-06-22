Conda commands to create the Python3.5 environment
--------------------------------------------------

::

    $ conda create --name capstone35 python=3.5 anaconda
    $ source activate capstone35
    $ pip install click
    $ conda install jinja2


Conda commands to create the Python2.7 environment
--------------------------------------------------

::

    $ conda create --name capstone27 python=2.7 anaconda
    $ source activate capstone27
    $ pip install click
    $ conda install jinja2


Two ways to run programs and scripts using a Conda environment
--------------------------------------------------------------

1. Using *conda activate* with the current shell; Note: this permanently
   alters the interactive shell's environment::

    $ source activate capstone27
    (capstone27)$ my_program arg arg arg
    (capstone27)$

   To restore the previous environment it is necessary to *deactivate*
   the Conda environment::

    (capstone27)$ source deactivate
    $ 

2. Using *cenv*, which starts a subshell; Note: the interactive shell's
   environment is not altered using this method::

    $ bin/cenv capstone27 my_program arg arg arg
    $

   There is no need to deactivate anything using this method.

Which method is better? The end result should be identical with either
method. Using *cenv* allows running a pipeline where the components can
be in different Conda envs::

    $ bin/cenv capstone27 my_py27_prog.py | bin/cenv capstone35 my_py35_prog.py


(Optional) Add a blank line before each shell prompt
----------------------------------------------------

::

    $ eval "$( adjust_blanks_before_prompt.sh add )"
