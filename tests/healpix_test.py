# -*- coding: utf-8 -*-
import unittest, aipy.healpix as h, numpy as n


class TestHealpix(unittest.TestCase):
    def setUp(self):
        self.hpb = h.HealpixBase()
        self.hpm = h.HealpixMap(nside=256)
    def test_fromhpm(self):
        """Test HEALpix from_hpm functional attribute"""
        hpm2 = h.HealpixMap(nside=64)
        self.hpm.map = n.ones(shape = self.hpm.map.shape)
        hpm2.from_hpm(self.hpm)
        self.assertEqual(n.sum(self.hpm.get_map()), n.sum(hpm2.get_map()))
        self.hpm.map[::2] = 0
        hpm2.from_hpm(self.hpm)
        self.assertEqual(n.sum(self.hpm.get_map()), n.sum(hpm2.get_map()))
        for m in xrange(len(self.hpm.get_map())):
            N = m**2
            if N <= m:
                self.hpm.map[N] = m
            else:
                break
        hpm2.from_hpm(self.hpm)
        self.assertEqual(n.sum(self.hpm.get_map()), n.sum(hpm2.get_map()))

if False:
  class TestMemLeaks(unittest.TestCase):
    def setUp(self):
        self.hpb = h.HealpixBase(nside=256)
    def test_create(self):
        while True: hpb = h.HealpixBase(nside=256)
    def test_crd2pix(self):
        one = 0.99
        x = n.arange(-one, one, .01, dtype=n.double)
        y = n.zeros_like(x)
        z = n.sqrt(1 - x**2 - y**2)
        while True: crds = self.hpb.crd2px(x, y, z)

class TestSuite(unittest.TestSuite):
    """A unittest.TestSuite class which contains all of the aipy._healpix unit tests."""

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(TestHealpix))
        #self.addTests(loader.loadTestsFromTestCase(TestMemLeaks))

if __name__ == '__main__':
    unittest.main()

#hp = aipy._healpix.HealpixBase(2**6, 'NEST')
#print hp.order(), hp.nside(), hp.npix(), hp.scheme()
#px = numpy.arange(hp.npix())
#px = hp.nest_ring_conv(px, 'RING')
#hp.set_nside_scheme(hp.nside(), 'RING')
#px = numpy.arange(10)
#x,y,z = hp.px2crd(px, ncrd=3)
#th,phi = hp.px2crd(px, ncrd=2)
#assert(numpy.all(px == hp.crd2px(x,y,z, interpolate=0)))
#px2,wgt = hp.crd2px(x,y,z, interpolate=1)
#z[-1] = numpy.Inf
#try: hp.crd2px(x,y,z[:-1])
#except(RuntimeError): pass
#assert(numpy.all(px == hp.crd2px(th, phi, interpolate=0)))
#px2,wgt = hp.crd2px(th, phi, interpolate=1)
