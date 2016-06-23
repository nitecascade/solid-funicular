Girvan-Newman
-------------

The Girvan-Newman algorithm is in the dev version of NetworkX. Clone the
repo with::

    $ cd ~/git/galvanize
    $ git clone https://github.com/networkx/networkx.git

Then change PYTHONPATH to use that repo during import::

    $ export PYTHONPATH=~/git/galvanize/networkx
    $ cenv -e env.sh capstone35 python
    >>> import networkx as nx
    >>> nx.__file__
    '/Users/fmachi/git/galvanize/networkx/networkx/__init__.py'

The examples from the documentation work as advertised::

    >>> import networkx as nx
    >>> from nx.algorithms.community import girvan_newman

    >>> G = nx.path_graph(10)
    >>> comp = girvan_newman(G)
    >>> tuple(sorted(c) for c in next(comp))
    ([0, 1, 2, 3, 4], [5, 6, 7, 8, 9])

    >>> import itertools
    >>> G = nx.path_graph(8)
    >>> k = 2
    >>> comp = girvan_newman(G)
    >>> for communities in itertools.islice(comp, k):
    ...  print(tuple(sorted(c) for c in communities))
    ...
    ([0, 1, 2, 3], [4, 5, 6, 7])
    ([0, 1], [2, 3], [4, 5, 6, 7])
    >>> 
