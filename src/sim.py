"""
Module for adding data simulation support to AntennaArrays.  For most classes,
this means adding gain/amplitude information (as a function of frequency).

Author: Aaron Parsons
Date: 11/07/06
Revisions:
    12/05/06    arp Conjugated sim_data (-2pi1j, instead of 2pi1j).
    01/01/07    arp Added gain information for antennas.  Expanded sim_data to 
                    have optional compute of gradient.
    03/02/07    arp Changed sim_data to do 1 baseline at a time.  Substantial
                    restructuring of parameter passing.  More documentation.
    05/15/07    arp Split part of Antennas into PhsAntennas to have more
                    streamlined support for phasing antenna data.
    10/10/07    arp Switched bandpass parameterization from polynomial to
                    splines.
    12/12/07    arp Switched bp again, this time to interpolation from a
                    decimated bandpass.
    03/06/08    arp Vectorized simulation w/ 4x increase in speed and
                    support for pixel-based simulation.
"""

import ant, numpy as n, ephem, coord, healpix

#  ____           _ _       ____            _       
# |  _ \ __ _  __| (_) ___ | __ )  ___   __| |_   _ 
# | |_) / _` |/ _` | |/ _ \|  _ \ / _ \ / _` | | | |
# |  _ < (_| | (_| | | (_) | |_) | (_) | (_| | |_| |
# |_| \_\__,_|\__,_|_|\___/|____/ \___/ \__,_|\__, |
#                                             |___/ 

class RadioBody:
    """A class redefining ephem's sense of brightness for radio astronomy."""
    def __init__(self, janskies, mfreq, index, angsize):
        """janskies:     source strength
        mfreq:    frequency (in GHz) where strength was measured
        index:   index of power-law spectral model of source emission"""
        try: len(janskies)
        except: janskies = [janskies]
        try: len(index)
        except: index = [index]
        self._janskies = janskies
        self.mfreq = mfreq
        self._index = index
        self.angsize = angsize
    def compute(self, observer):
        self.janskies = n.clip(n.polyval(self._janskies, 
                (observer.sidereal_time()-self.ra+n.pi) % (2*n.pi)), 0, n.Inf)
        self.index = n.polyval(self._index, observer.sidereal_time())

#  ____           _ _       _____ _              _ ____            _       
# |  _ \ __ _  __| (_) ___ |  ___(_)_  _____  __| | __ )  ___   __| |_   _ 
# | |_) / _` |/ _` | |/ _ \| |_  | \ \/ / _ \/ _` |  _ \ / _ \ / _` | | | |
# |  _ < (_| | (_| | | (_) |  _| | |>  <  __/ (_| | |_) | (_) | (_| | |_| |
# |_| \_\__,_|\__,_|_|\___/|_|   |_/_/\_\___|\__,_|____/ \___/ \__,_|\__, |
#                                                                    |___/ 

class RadioFixedBody(ant.RadioFixedBody, RadioBody):
    """A class adding simulation capability to ant.RadioFixedBody"""
    def __init__(self, ra, dec, janskies, mfreq=.150, 
            index=-1., angsize=0., name='', **kwargs):
        ant.RadioFixedBody.__init__(self, ra, dec, name=name)
        RadioBody.__init__(self, janskies, mfreq, index, angsize)
    def compute(self, observer):
        ant.RadioFixedBody.compute(self, observer)
        RadioBody.compute(self, observer)

#  ____           _ _      ____                  _       _ 
# |  _ \ __ _  __| (_) ___/ ___| _ __   ___  ___(_) __ _| |
# | |_) / _` |/ _` | |/ _ \___ \| '_ \ / _ \/ __| |/ _` | |
# |  _ < (_| | (_| | | (_) |__) | |_) |  __/ (__| | (_| | |
# |_| \_\__,_|\__,_|_|\___/____/| .__/ \___|\___|_|\__,_|_|
#                               |_|                        

class RadioSpecial(ant.RadioSpecial, RadioBody):
    """A class adding simulation capability to ant.RadioSun"""
    def __init__(self,name,janskies,mfreq=.150,index=-1.,angsize=0.,**kwargs):
        ant.RadioSpecial.__init__(self, name)
        RadioBody.__init__(self, janskies, mfreq, index, angsize)
    def compute(self, observer):
        ant.RadioSpecial.compute(self, observer)
        RadioBody.compute(self, observer)

#  ____            ____      _        _             
# / ___| _ __ ___ / ___|__ _| |_ __ _| | ___   __ _ 
# \___ \| '__/ __| |   / _` | __/ _` | |/ _ \ / _` |
#  ___) | | | (__| |__| (_| | || (_| | | (_) | (_| |
# |____/|_|  \___|\____\__,_|\__\__,_|_|\___/ \__, |
#                                             |___/ 

class SrcCatalog(ant.SrcCatalog):
    """A class adding simulation capability to SrcCatalog"""
    def get_fluxes(self):
        return n.array([s.janskies for s in self.values()])
    def get_indices(self):
        return n.array([s.index for s in self.values()])
    def get_mfreqs(self):
        return n.array([s.mfreq for s in self.values()])
    def get_angsizes(self):
        return n.array([s.angsize for s in self.values()])

#  ____
# | __ )  ___  __ _ _ __ ___
# |  _ \ / _ \/ _` | '_ ` _ \
# | |_) |  __/ (_| | | | | | |
# |____/ \___|\__,_|_| |_| |_|

class BeamFlat(ant.Beam):
    def response(self, xyz):
        return n.ones((self.afreqs.size, xyz.shape[1]))

class Beam2DGaussian(ant.Beam):
    """A 2D Gaussian beam pattern, with default setting for a flat beam."""
    def __init__(self, freqs, xwidth=n.Inf, ywidth=n.Inf):
        ant.Beam.__init__(self, freqs)
        self.update(xwidth=xwidth, ywidth=ywidth)
    def update(self, xwidth=None, ywidth=None):
        """Set the width in the x and y directions of the gaussian beam."""
        if not xwidth is None: self.xwidth = xwidth
        if not ywidth is None: self.ywidth = ywidth
    def response(self, xyz):
        """Return the beam response across the active band for the specified
        topocentric coordinates (with z = up, x = east). 2nd axis should be 
        multiple coordinates.  Returns 'x' pol (rotate pi/2 for 'y')."""
        x,y,z = xyz
        x,y = n.arcsin(x)/self.xwidth, n.arcsin(y)/self.ywidth
        resp = n.sqrt(n.exp(-(x**2 + y**2)))
        resp = n.resize(resp, (self.afreqs.size, resp.size))
        return resp

class BeamPolynomial(ant.Beam):
    """A Beam model that uses a 2D polynomial in cos(2*n*az) for first axis,
    and in freq**n for second axis."""
    def __init__(self, freqs, poly_azfreq=n.array([[.5]])):
        self.poly = poly_azfreq
        ant.Beam.__init__(self, freqs)
        self.update(poly_azfreq)
    def select_chans(self, active_chans):
        ant.Beam.select_chans(self, active_chans)
        self.update()
    def update(self, poly_azfreq=None):
        """Set the width in the x and y directions of the gaussian beam."""
        if poly_azfreq is None: poly_azfreq = self.poly
        elif len(poly_azfreq.shape) == 1: poly_azfreq.shape = self.poly.shape
        self.poly = poly_azfreq
        f = n.resize(self.afreqs, (self.poly.shape[1], self.afreqs.size))
        f = f**n.array([range(self.poly.shape[1])]).transpose()
        self.sigma = n.dot(self.poly, f)
    def response(self, top):
        """Return the beam response across the active band for the specified
        topocentric coordinates (with z = up, x = east). 2nd axis should be 
        multiple coordinates.  Returns 'x' pol (rotate pi/2 for 'y')."""
        az,alt = coord.top2azalt(top)
        zang = n.pi/2 - alt
        if zang.size == 1:
            zang = n.array([zang]); zang.shape = (1,)
            az = n.array([az]); az.shape = (1,)
        a = 2 * n.arange(self.poly.shape[0], dtype=n.float)
        a.shape = (1,) + a.shape; az.shape += (1,); zang.shape += (1,)
        a = n.cos(n.dot(az, a))
        a[:,0] = 0.5
        s = n.dot(a, self.sigma)
        return n.sqrt(n.exp(-(zang/s)**2)).transpose()

class BeamCosSeries(ant.Beam):
    def __init__(self, freqs, poly_cos=n.array([[0., 1.]]), 
            poly_wid=n.array([0., 1.])):
        self.poly_cos = poly_cos
        self.poly_wid = poly_wid
        ant.Beam.__init__(self, freqs)
        self.update(poly_cos, poly_wid)
    def select_chans(self, active_chans):
        ant.Beam.select_chans(self, active_chans)
        self.update()
    def update(self, poly_cos=None, poly_wid=None):
        """Set the width in the x and y directions of the gaussian beam."""
        if poly_cos is None: poly_cos = self.poly_cos
        elif len(poly_cos.shape) == 1: poly_cos.shape = self.poly_cos.shape
        if poly_wid is None: poly_wid = self.poly_wid
        self.poly_cos = poly_cos
        self.poly_wid = poly_wid
    def response(self, top):
        az,alt = coord.top2azalt(top)
        zang = n.pi/2 - alt
        if zang.size == 1:
            zang = n.array([zang]); zang.shape = (1,)
            az = n.array([az]); az.shape = (1,)
        wid = 2 * n.arange(self.poly_wid.shape[0], dtype=n.float)
        wid.shape = (1,) + wid.shape
        az.shape += (1,)
        wid = n.dot(n.cos(n.dot(az, wid)), self.poly_wid)
        x = n.cos(wid * zang)**2
        a = 2 * n.arange(self.poly_cos.shape[0], dtype=n.float)
        a.shape = (1,) + a.shape; zang.shape += (1,)
        p = n.dot(n.cos(n.dot(az, a)), self.poly_cos)
        rv = n.polyval(p.transpose(), x.transpose())
        rv.shape = (1,) + rv.shape
        return rv.clip(0, n.Inf)

class BeamAlm(ant.Beam):
    def __init__(self, freqs, lmax=8, mmax=8, deg=7, nside=64, coeffs={}):
        self.alm = [healpix.Alm(lmax,mmax) for i in range(deg+1)]
        self.hmap = [healpix.HealpixMap(nside,scheme='RING',interp=True)
            for a in self.alm]
        ant.Beam.__init__(self, freqs)
        self.update(coeffs)
    def update(self, coeffs={}):
        for c in coeffs:
            if c >= len(self.alm): continue
            self.alm[-1-c].set_data(coeffs[c])
            self.hmap[-1-c].from_alm(self.alm[-1-c])
    def response(self, top):
        top = [healpix.mk_arr(c, dtype=n.double) for c in top]
        px,wgts = self.hmap[0].crd2px(*top, **{'interpolate':1})
        poly = n.array([n.sum(h.map[px] * wgts, axis=-1) for h in self.hmap])
        rv = n.polyval(poly, n.reshape(self.afreqs, (self.afreqs.size, 1)))
        return rv

#     _          _                         
#    / \   _ __ | |_ ___ _ __  _ __   __ _ 
#   / _ \ | '_ \| __/ _ \ '_ \| '_ \ / _` |
#  / ___ \| | | | ||  __/ | | | | | | (_| |
# /_/   \_\_| |_|\__\___|_| |_|_| |_|\__,_|

class Antenna(ant.Antenna):
    """A representation of the physical location and beam pattern of an
    individual antenna in an array."""
    def __init__(self, x, y, z, beam, delay=0., offset=0., bp_r=n.array([1]),
            bp_i=n.array([0]), amp=1, pointing=(0.,n.pi/2,0), **kwargs):
        """x, y, z:    Antenna coordinates in equatorial (ns) coordinates
        beam:       Object with function 'response(xyz=None, azalt=None)'
        delay:      Cable/systematic delay in ns
        bp_r:       Polynomial modeling the real component of the passband
        bp_i:       Polynomial modeling the imag component of the passband
        pointing:   Antenna pointing=(az, alt).  Default is zenith"""
        ant.Antenna.__init__(self, x,y,z, beam=beam, delay=delay, offset=offset)
        # Implement a flat passband of ones if no bp is provided
        self.update_gain(bp_r, bp_i, amp)
        self.update_pointing(*pointing)
    def select_chans(self, active_chans=None):
        ant.Antenna.select_chans(self, active_chans)
        self.update_gain()
    def update_gain(self, bp_r=None, bp_i=None, amp=None):
        if not bp_r is None:
            try: len(bp_r)
            except: bp_r = [bp_r]
            self.bp_r = bp_r
        if not bp_i is None:
            try: len(bp_i)
            except: bp_i = [bp_i]
            self.bp_i = bp_i
        if not amp is None: self.amp = amp
        bp = n.polyval(self.bp_r, self.beam.afreqs) + \
             1j*n.polyval(self.bp_i, self.beam.afreqs)
        #bp *= n.exp(1j*self.offset)
        self.gain = self.amp * bp
    def update_pointing(self, az=0, alt=n.pi/2, twist=0):
        """Set the antenna beam to point at (az, alt) with the specified
        right-hand twist to the polarizations.  Polarization y is assumed
        to be +pi/2 azimuth from pol x."""
        y, z = n.array([0,1,0]), n.array([0,0,1])
        rot = coord.rot_m(twist, z)
        rot = n.dot(rot, coord.rot_m(alt-n.pi/2, y))
        rot = n.dot(rot, coord.rot_m(-az, z))
        self.rot_pol_x = rot
        self.rot_pol_y = n.dot(coord.rot_m(-n.pi/2, z), rot)
    def bm_response(self, top, pol='x'):
        top = n.array(top)
        top = {'x':top, 'y':n.dot(self.rot_pol_y, top)}[pol]
        x,y,z = top
        return self.beam.response((x,y,z))
    def response(self, top, pol='x'):
        """Return the total antenna response to the specified topocentric 
        coordinates (with z = up, x = east).  This includes beam response and
        per-frequency gain.  1st axis should be xyz, 2nd axis should be 
        multiple coordinates."""
        beam_resp = self.bm_response(top, pol=pol)
        gain = self.gain
        if len(beam_resp.shape) == 2: gain = n.reshape(gain, (gain.size, 1))
        return beam_resp * gain

#     _          _                            _                         
#    / \   _ __ | |_ ___ _ __  _ __   __ _   / \   _ __ _ __ __ _ _   _ 
#   / _ \ | '_ \| __/ _ \ '_ \| '_ \ / _` | / _ \ | '__| '__/ _` | | | |
#  / ___ \| | | | ||  __/ | | | | | | (_| |/ ___ \| |  | | | (_| | |_| |
# /_/   \_\_| |_|\__\___|_| |_|_| |_|\__,_/_/   \_\_|  |_|  \__,_|\__, |
#                                                                 |___/ 

class AntennaArray(ant.AntennaArray):
    """A class which adds simulation functionality to AntennaArray."""
    def set_jultime(self, t=None):
        ant.AntennaArray.set_jultime(self, t=t)
        self.eq2top_m = coord.eq2top_m(-self.sidereal_time(), self.lat)
        self._cache = None
    def sim_cache(self, s_eqs, fluxes, indices=0., mfreqs=n.array([.150]), 
            angsizes=None):
        # Get topocentric coordinates of all srcs
        src_top = n.dot(self.eq2top_m, s_eqs)
        # Throw out everything that is below the horizon
        valid = n.logical_and(src_top[2,:] > 0, fluxes > 0)
        if n.all(valid == 0):
            self._cache = {'I_sf': 0, 's_eqs': s_eqs, 
                    's_top': s_eqs, 's_sz':angsizes}
        else:
            fluxes = fluxes.compress(valid)
            indices = indices.compress(valid)
            mfreqs = mfreqs.compress(valid)
            if not angsizes is None: angsizes = angsizes.compress(valid)
            src_top = src_top.compress(valid, axis=1)
            s_eqs = s_eqs.compress(valid, axis=1)
            # Get src fluxes vs. freq
            fluxes.shape = (fluxes.size, 1)
            mfreqs.shape = (mfreqs.size, 1)
            indices.shape = (indices.size, 1)
            freqs = n.resize(self.ants[0].beam.afreqs, 
                (fluxes.size, self.ants[0].beam.afreqs.size))
            self._cache = {
                'I_sf':fluxes * (freqs / mfreqs)**indices,
                's_eqs': s_eqs,
                's_top': src_top,
                's_sz': angsizes
            }
    def sim(self, i, j, pol='xx'):
        """Simulate visibilites for the (i,j) baseline based on source
        locations (in equatorial coordinates), fluxes, spectral indices,
        the frequencies at which fluxes were measured, and the polarization."""
        assert(pol in ('xx','yy','xy','yx'))
        if self._cache is None:
            raise RuntimeError('sim_cache() must be called before the first sim() call at each time step.')
        # Check that we have cached results needed.  If not, cache them.
        for c,p in zip([i,j], pol):
            if not self._cache.has_key(c): self._cache[c] = {}
            if not self._cache[c].has_key(p):
                x,y,z = self._cache['s_top']
                resp = self.ants[c].response((x,y,z), pol=p).transpose()
                self._cache[c][p] = resp
        I_sf = self._cache['I_sf']
        s_eqs = self._cache['s_eqs']
        GAi_sf = self._cache[i][pol[0]]
        GAj_sf = self._cache[j][pol[1]]
        s_sz = self._cache['s_sz']
        # Get the phase of each src vs. freq, also does resolution effects
        E_sf = n.conjugate(self.gen_phs(s_eqs.transpose(), i, j, angsize=s_sz))
        E_sf.shape = I_sf.shape
        # Combine and sum over sources
        GBIE_sf = GAi_sf * n.conjugate(GAj_sf) * I_sf * E_sf
        #GBIE_sf = GAi_sf * GAj_sf * I_sf * E_sf
        Vij_f = GBIE_sf.sum(axis=0)
        return Vij_f