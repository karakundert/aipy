#! /usr/bin/env python
"""
This is a general-purpose script for making images from MIRIAD UV files.  Data
(optionally selected for baseline, channel) are read from the file, phased
to a provided position, normalized for passband/primary beam effects, gridded
to a UV matrix, imaged, and optionally deconvolved by a corresponding PSF to
produce a clean image.

Author: Aaron Parsons
"""

import aipy as a, numpy as n, pylab as p, sys, optparse, ephem

o = optparse.OptionParser()
o.set_usage('plot_img.py [options] *.uv')
o.set_description(__doc__)
a.scripting.add_standard_options(o, ant=True, pol=True, chan=True, loc=True,
    src=True, dec=True)
o.add_option('-r', '--residual', dest='residual', action='store_true',
    help='Display only the residual in the 4th panel (otherwise display sum of clean image and residual).')
o.add_option('-d', '--deconv', dest='deconv', default='mem',
    help='Attempt to deconvolve the dirty image by the dirty beam using the specified deconvolver (none,mem,lsq,cln,ann).')
o.add_option('--var', dest='var', type='float', default=1.,
    help='Starting guess for variance in maximum entropy fit (defaults to variance of dirty image.')
o.add_option('--tol', dest='tol', type='float', default=1e-6,
    help='Tolerance for successful deconvolution.  For annealing, interpreted as cooling speed.')
o.add_option('--maxiter', dest='maxiter', type='int', default=200,
    help='Number of allowable iterations per deconvolve attempt.')
o.add_option('--skip_amp', dest='skip_amp', action='store_true',
    help='Do not use amplitude information to normalize visibilities.')
o.add_option('--skip_bm', dest='skip_bm', action='store_true',
    help='Do not weight visibilities by the strength of the primary beam.')
o.add_option('--size', dest='size', type='int', default=200,
    help='Size of maximum UV baseline.')
o.add_option('--res', dest='res', type='float', default=0.5,
    help='Resolution of UV matrix.')
o.add_option('--no_w', dest='no_w', action='store_true',
    help="Don't use W projection.")
o.add_option('--dyn_rng', dest='dyn_rng', type='float', default=3.,
    help="Dynamic range in color of image (log).")
o.add_option('--phs', dest='phs', action='store_true',
    help="If plotting the UV matrix, show phases.")
o.add_option('--buf_thresh', dest='buf_thresh', default=1.8e6, type='float',
    help='Maximum amount of data to buffer before gridding.  Excessive gridding takes performance hit, but if buffer exceeds memory available... ouch.')
opts, args = o.parse_args(sys.argv[1:])

# Parse command-line options
uv = a.miriad.UV(args[0])
a.scripting.uv_selector(uv, opts.ant, opts.pol)
aa = a.loc.get_aa(opts.loc, uv['sdf'], uv['sfreq'], uv['nchan'])
chans = a.scripting.parse_chans(opts.chan, uv['nchan'])
aa.select_chans(chans)
src = a.scripting.parse_srcs(opts.src)
if opts.no_w: im = a.img.Img(opts.size, opts.res)
else: im = a.img.ImgW(opts.size, opts.res)
DIM = int(opts.size/opts.res)
p1,p2 = opts.pol
del(uv)

cnt, curtime = 0, None
# Gather data
uvw, dat, wgt = [], [], []
cache = {}
for filename in args:
    sys.stdout.write('.'); sys.stdout.flush()
    uv = a.miriad.UV(filename)
    a.scripting.uv_selector(uv, opts.ant, opts.pol)
    for (crd,t,(i,j)),d,f in uv.all(raw=True):
        if curtime != t:
            curtime = t
            cnt = (cnt + 1) % opts.decimate
            if cnt == 0:
                aa.set_jultime(t)
                src.compute(aa)
                top = a.coord.azalt2top((src.az,src.alt))
                cache = {}
        if cnt != 0: continue
        d = d.take(chans)
        f = f.take(chans)
        if not opts.skip_amp:
            d /= aa.ants[i].gain * n.conjugate(aa.ants[j].gain)
        try:
            d = aa.phs2src(d, src, i, j)
            xyz = aa.gen_uvw(i,j,src=src)
            if not opts.skip_bm:
                # Cache beam response, since it is an expensive operation
                if not cache.has_key(i): cache[i] = {}
                if not cache[i].has_key(p1):
                    r = aa.ants[i].bm_response(top, pol=p1)
                    cache[i][p1] = r.flatten()
                if not cache.has_key(j): cache[j] = {}
                if not cache[j].has_key(p2):
                    r = aa.ants[j].bm_response(top, pol=p2)
                    cache[j][p2] = r.flatten()
                # Calculate beam strength for weighting purposes
                w = cache[i][p1] * cache[j][p2]
                # For optimal SNR, down-weight data that is already attenuated 
                # by beam  by another factor of the beam response (modifying 
                # weight accordingly).
                #d *= w; w *= w
            else: w = n.ones(d.shape, dtype=n.float)
        except(a.ant.PointingError): continue
        valid = n.logical_not(f)
        d = d.compress(valid)
        if len(d) == 0: continue
        dat.append(d)
        uvw.append(xyz.compress(valid, axis=0))
        wgt.append(w.compress(valid))
        if len(dat) * len(chans) > opts.buf_thresh:
            sys.stdout.write('|'); sys.stdout.flush()
            dat = n.concatenate(dat)
            uvw = n.concatenate(uvw); uvw.shape = (uvw.size / 3, 3)
            wgt = n.concatenate(wgt).flatten()
            uvw,dat,wgt = im.append_hermitian(uvw,dat,wgt)
            im.put(uvw, dat, wgt)
            uvw, dat, wgt = [], [], []

if len(uvw) == 0: raise ValueError('No data to plot')
# Grid data into UV matrix
sys.stdout.write('|\n'); sys.stdout.flush()
dat = n.concatenate(dat)
uvw = n.concatenate(uvw); uvw.shape = (uvw.size / 3, 3)
wgt = n.concatenate(wgt).flatten()
uvw,dat,wgt = im.append_hermitian(uvw,dat,wgt)
im.put(uvw, dat, wgt)

im_img = im.image((DIM/2, DIM/2))
bm_img = im.bm_image()
bm_gain = n.sqrt((bm_img**2).sum())

if opts.deconv == 'mem':
    cl_img,info = a.deconv.maxent_findvar(im_img, bm_img, f_var0=opts.var,
        maxiter=opts.maxiter, verbose=True, tol=opts.tol)
elif opts.deconv == 'lsq':
    cl_img,info = a.deconv.lsq(im_img, bm_img, 
        maxiter=opts.maxiter, verbose=True, tol=opts.tol)
elif opts.deconv == 'cln':
    cl_img,info = a.deconv.clean(im_img, bm_img, 
        maxiter=opts.maxiter, verbose=True, tol=opts.tol)
elif opts.deconv == 'ann':
    cl_img,info = a.deconv.anneal(im_img, bm_img, maxiter=opts.maxiter, 
        cooling=lambda i,x: opts.tol*(1-n.cos(i/50.))*(x**2), verbose=True)

print 'Gain of dirty beam:', bm_gain
bm_img = im.bm_image((DIM/2,DIM/2))

if opts.deconv != 'none':
    rs_img = info['res'] / bm_gain
    if not opts.residual: rs_img += cl_img

    # Generate a little info about where the strongest src is
    eq = im.get_eq(ra=src.ra, dec=src.dec, center=(DIM/2,DIM/2))
    ra,dec = a.coord.eq2radec(eq)
    x_ind,y_ind = n.indices(cl_img.shape)
    print 'Phase center:', (src.ra, src.dec)
    # Print top 10 srcs
    if not opts.residual: top10_img = rs_img
    else: top10_img = cl_img
    src_locs = list(top10_img.argsort(axis=None)[-10:])
    src_locs.reverse()
    print 'Flux in central 3px x 3px of image:',
    print rs_img[DIM/2-1:DIM/2+2,DIM/2-1:DIM/2+2].sum()
    print 'Top 10 sources in field:'
    for i, src_loc in enumerate(src_locs):
        src_ra,src_dec = ra.flat[src_loc], dec.flat[src_loc]
        eq = ephem.Equatorial(src_ra, src_dec, epoch=aa.epoch)
        eq = ephem.Equatorial(eq, epoch=ephem.J2000)
        x,y = x_ind.flat[src_loc], y_ind.flat[src_loc]
        print '#%2d:' % (i+1), eq.get(), 'J2000,',
        print 'px:', (y, x),
        print 'Jy: %5.1f' % top10_img.flat[src_loc]

p.subplot(221)
plt1_img = n.log10(im_img.clip(1e-15,n.Inf))
mx = plt1_img.max()
p.imshow(plt1_img, vmin=mx-opts.dyn_rng, vmax=mx, aspect='auto')
p.colorbar(shrink=.5, fraction=.05)
p.title('Dirty Image')

p.subplot(222)
plt2_img = n.log10(bm_img.clip(1e-15,n.Inf))
mx = plt2_img.max()
p.imshow(plt2_img, vmin=mx-opts.dyn_rng, vmax=mx, aspect='auto')
p.colorbar(shrink=.5, fraction=.05)
p.title('Dirty Beam')

p.subplot(223)
if opts.deconv != 'none':
    plt3_img = n.log10(cl_img.clip(1e-15,n.Inf))
    p.title('%s Image' % opts.deconv.upper())
else:
    if opts.phs: plt3_img = n.angle(im.uv)
    else: plt3_img = n.log10(n.abs(im.uv))
    p.title('UV Sampling')
mx = plt3_img.max()
p.imshow(plt3_img, vmin=mx-opts.dyn_rng, vmax=mx, aspect='auto')
p.colorbar(shrink=.5, fraction=.05)

p.subplot(224)
if opts.deconv != 'none':
    plt4_img = n.log10(n.abs(rs_img).clip(1e-15,n.Inf))
    p.title('Residual Image')
else:
    plt4_img = n.log10(n.abs(im.bm))
    p.title('Beam Sampling')
mx = plt4_img.max()
p.imshow(plt4_img, vmin=mx-opts.dyn_rng, vmax=mx, aspect='auto')
p.colorbar(shrink=.5, fraction=.05)

p.show()
