Instructions for installing Python module *louvain*
---------------------------------------------------

Note that there are (at least) two different PyPI packages for the **Louvain
community detection** software.::

    $ pip search louvain
    ...
    python-louvain (0.5)    - Louvain algorithm for community detection
    louvain (0.5.3)         - Louvain is a general algorithm for methods of community detection in large networks.

- *python-louvain* is a pure-Python implementation with a dependency on
  *networkx*, itself a pure-Python implementation of graph algorithms.

- *louvain* is a different PyPI package with a dependency on *igraph*, a C/C++
  library of graph algorithms.

These instructions are for installing the **louvain** PyPI package using Pip.
See also the PyPI page for the **louvain** package::

    https://pypi.python.org/pypi/louvain/

Steps
-----

The straightforward installation using Pip may not work on Mac OS X under
Anaconda. The install appears to be successful, but Python encounters a
linker error during import of the louvain package.

The following installation steps worked.

0. Make sure the correct **Python executable** runs for the remaining steps.
   The executable should be located in a **Conda** env::

    $ type python
    python is /Users/fmachi/anaconda2/envs/capstone35/bin/python
    $ 

   Make sure that the **louvain** PyPI package is not installed::

    $ pip uninstall louvain
    $ 

   Do the same for **python-igraph**::

    $ pip uninstall python-igraph
    $ 

1. Make sure the **C library for igraph** is installed. I use MacPorts::

     $ sudo port install igraph
     $ ls -l /opt/local/include/igraph
     ls -l /opt/local/include/igraph
     total 1048
     -rw-r--r--  1 root  admin   2800 Nov 28  2014 igraph.h
     -rw-r--r--  1 root  admin   8441 Nov 28  2014 igraph_adjlist.h
     ...
     $ ls -l /opt/local/lib/libigraph.dylib
     lrwxr-xr-x  1 root  admin  17 Nov 28  2014 /opt/local/lib/libigraph.dylib -> libigraph.0.dylib
     $ 

3. Check that **pkg-config** shows the correct paths for **igraph**::

    $ pkg-config --cflags --libs igraph
    -I/opt/local/include/igraph -L/opt/local/lib -ligraph
    $ 

   If this is not the case, it may be necessary to add or alter the
   **igraph.pc** config file in the *pkgconfig* directory under the
   active *Anaconda env*. This is the one I created::

    $ pwd
    ~/anaconda2/envs/capstone35/lib/pkgconfig

    $ cat ./igraph.pc
    prefix=/Users/fmachi/anaconda2/envs/capstone35
    exec_prefix=${prefix}
    libdir=${exec_prefix}/lib
    includedir=${prefix}/include
    modules=1

    Name: igraph
    Version: 1.0.0
    Description: igraph
    Requires:
    Libs: -L${libdir} -ligraph
    Libs.private:   -lz   -liconv -lm
    Cflags: -I${includedir}/igraph
    $ 

4. Use Pip to download **python-igraph**, build a *wheel* for it, then install
   that wheel::

    $  pip download python-igraph
    $  pip wheel python-igraph-0.7.1.post6.tar.gz 
    $  pip install python_igraph-0.7.1.post6-cp35-cp35m-macosx_10_5_x86_64.whl 

5. Now use Pip to install the **louvain** package. The simple Pip command
   should work::

    $ pip install louvain

   but if that proves troublesome, do the same steps as for *python-igraph*::

    $  pip download louvain
    $  pip wheel louvain-0.5.3.tar.gz 
    $  pip install louvain-0.5.3-cp35-cp35m-macosx_10_5_x86_64.whl 

6. Try it out::

    $ python
    >>> import louvain
    >>> louvain.__file__
    '/Users/fmachi/anaconda2/envs/capstone35/lib/python3.5/site-packages/louvain/__init__.py'
