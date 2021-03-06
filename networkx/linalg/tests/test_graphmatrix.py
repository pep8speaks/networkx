import pytest
numpy = pytest.importorskip('numpy')
npt = pytest.importorskip('numpy.testing')
scipy = pytest.importorskip('scipy')

import networkx as nx
from networkx.generators.degree_seq import havel_hakimi_graph


class TestGraphMatrix(object):

    @classmethod
    def setup_class(cls):
        deg = [3, 2, 2, 1, 0]
        cls.G = havel_hakimi_graph(deg)
        cls.OI = numpy.array([[-1, -1, -1, 0],
                              [1, 0, 0, -1],
                              [0, 1, 0, 1],
                              [0, 0, 1, 0],
                              [0, 0, 0, 0]])
        cls.A = numpy.array([[0, 1, 1, 1, 0],
                             [1, 0, 1, 0, 0],
                             [1, 1, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        cls.WG = havel_hakimi_graph(deg)
        cls.WG.add_edges_from((u, v, {'weight': 0.5, 'other': 0.3})
                              for (u, v) in cls.G.edges())
        cls.WA = numpy.array([[0, 0.5, 0.5, 0.5, 0],
                              [0.5, 0, 0.5, 0, 0],
                              [0.5, 0.5, 0, 0, 0],
                              [0.5, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0]])
        cls.MG = nx.MultiGraph(cls.G)
        cls.MG2 = cls.MG.copy()
        cls.MG2.add_edge(0, 1)
        cls.MG2A = numpy.array([[0, 2, 1, 1, 0],
                                [2, 0, 1, 0, 0],
                                [1, 1, 0, 0, 0],
                                [1, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0]])
        cls.MGOI = numpy.array([[-1, -1, -1, -1, 0],
                                [1, 1, 0, 0, -1],
                                [0, 0, 1, 0, 1],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0]])
        cls.no_edges_G = nx.Graph([(1, 2), (3, 2, {'weight': 8})])
        cls.no_edges_A = numpy.array([[0, 0], [0, 0]])

    def test_incidence_matrix(self):
        "Conversion to incidence matrix"
        I = nx.incidence_matrix(self.G,
                                nodelist=sorted(self.G),
                                edgelist=sorted(self.G.edges()),
                                oriented=True).todense().astype(int)
        npt.assert_equal(I, self.OI)
        I = nx.incidence_matrix(self.G,
                                nodelist=sorted(self.G),
                                edgelist=sorted(self.G.edges()),
                                oriented=False).todense().astype(int)
        npt.assert_equal(I, numpy.abs(self.OI))

        I = nx.incidence_matrix(self.MG,
                                nodelist=sorted(self.MG),
                                edgelist=sorted(self.MG.edges()),
                                oriented=True).todense().astype(int)
        npt.assert_equal(I, self.OI)
        I = nx.incidence_matrix(self.MG,
                                nodelist=sorted(self.MG),
                                edgelist=sorted(self.MG.edges()),
                                oriented=False).todense().astype(int)
        npt.assert_equal(I, numpy.abs(self.OI))

        I = nx.incidence_matrix(self.MG2,
                                nodelist=sorted(self.MG2),
                                edgelist=sorted(self.MG2.edges()),
                                oriented=True).todense().astype(int)
        npt.assert_equal(I, self.MGOI)
        I = nx.incidence_matrix(self.MG2,
                                nodelist=sorted(self.MG),
                                edgelist=sorted(self.MG2.edges()),
                                oriented=False).todense().astype(int)
        npt.assert_equal(I, numpy.abs(self.MGOI))

    def test_weighted_incidence_matrix(self):
        I = nx.incidence_matrix(self.WG,
                                nodelist=sorted(self.WG),
                                edgelist=sorted(self.WG.edges()),
                                oriented=True).todense().astype(int)
        npt.assert_equal(I, self.OI)
        I = nx.incidence_matrix(self.WG,
                                nodelist=sorted(self.WG),
                                edgelist=sorted(self.WG.edges()),
                                oriented=False).todense().astype(int)
        npt.assert_equal(I, numpy.abs(self.OI))

        # npt.assert_equal(nx.incidence_matrix(self.WG,oriented=True,
        #                                  weight='weight').todense(),0.5*self.OI)
        # npt.assert_equal(nx.incidence_matrix(self.WG,weight='weight').todense(),
        #              numpy.abs(0.5*self.OI))
        # npt.assert_equal(nx.incidence_matrix(self.WG,oriented=True,weight='other').todense(),
        #              0.3*self.OI)

        I = nx.incidence_matrix(self.WG,
                                nodelist=sorted(self.WG),
                                edgelist=sorted(self.WG.edges()),
                                oriented=True,
                                weight='weight').todense()
        npt.assert_equal(I, 0.5 * self.OI)
        I = nx.incidence_matrix(self.WG,
                                nodelist=sorted(self.WG),
                                edgelist=sorted(self.WG.edges()),
                                oriented=False,
                                weight='weight').todense()
        npt.assert_equal(I, numpy.abs(0.5 * self.OI))
        I = nx.incidence_matrix(self.WG,
                                nodelist=sorted(self.WG),
                                edgelist=sorted(self.WG.edges()),
                                oriented=True,
                                weight='other').todense()
        npt.assert_equal(I, 0.3 * self.OI)

        # WMG=nx.MultiGraph(self.WG)
        # WMG.add_edge(0,1,weight=0.5,other=0.3)
        # npt.assert_equal(nx.incidence_matrix(WMG,weight='weight').todense(),
        #              numpy.abs(0.5*self.MGOI))
        # npt.assert_equal(nx.incidence_matrix(WMG,weight='weight',oriented=True).todense(),
        #              0.5*self.MGOI)
        # npt.assert_equal(nx.incidence_matrix(WMG,weight='other',oriented=True).todense(),
        #              0.3*self.MGOI)

        WMG = nx.MultiGraph(self.WG)
        WMG.add_edge(0, 1, weight=0.5, other=0.3)
        I = nx.incidence_matrix(WMG,
                                nodelist=sorted(WMG),
                                edgelist=sorted(WMG.edges(keys=True)),
                                oriented=True,
                                weight='weight').todense()
        npt.assert_equal(I, 0.5 * self.MGOI)
        I = nx.incidence_matrix(WMG,
                                nodelist=sorted(WMG),
                                edgelist=sorted(WMG.edges(keys=True)),
                                oriented=False,
                                weight='weight').todense()
        npt.assert_equal(I, numpy.abs(0.5 * self.MGOI))
        I = nx.incidence_matrix(WMG,
                                nodelist=sorted(WMG),
                                edgelist=sorted(WMG.edges(keys=True)),
                                oriented=True,
                                weight='other').todense()
        npt.assert_equal(I, 0.3 * self.MGOI)

    def test_adjacency_matrix(self):
        "Conversion to adjacency matrix"
        npt.assert_equal(nx.adj_matrix(self.G).todense(), self.A)
        npt.assert_equal(nx.adj_matrix(self.MG).todense(), self.A)
        npt.assert_equal(nx.adj_matrix(self.MG2).todense(), self.MG2A)
        npt.assert_equal(nx.adj_matrix(self.G, nodelist=[0, 1]).todense(), self.A[:2, :2])
        npt.assert_equal(nx.adj_matrix(self.WG).todense(), self.WA)
        npt.assert_equal(nx.adj_matrix(self.WG, weight=None).todense(), self.A)
        npt.assert_equal(nx.adj_matrix(self.MG2, weight=None).todense(), self.MG2A)
        npt.assert_equal(nx.adj_matrix(self.WG, weight='other').todense(), 0.6 * self.WA)
        npt.assert_equal(nx.adj_matrix(self.no_edges_G, nodelist=[1, 3]).todense(), self.no_edges_A)
