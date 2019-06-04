from __future__ import print_function

import hashlib
import numpy
import pintrinsics
import scipy.io.netcdf

def test(fn, val, label, prod=''):
    if val is None:
        res = fn()
    else: 
        res = fn(val)
    s = str(res)
    h = hashlib.sha224( s.encode('utf-8') ).hexdigest()
    print(prod, label, '\t', h, 'x =', str(val), 'fn() =', s)
    return res

def writefile(filename, vals):
    f = scipy.io.netcdf.netcdf_file(filename, 'w')
    v = f.createDimension('n', len(vals) )
    v = f.createVariable('results', 'f8', ('n',))
    v[:] = numpy.array(vals)[:]
    f.close()

P = [0.] * (5)
P[0] = test( pintrinsics.reciprocal, .3, '1/x    ', prod='pintrinsics')
P[1] = test( pintrinsics.sqrt, 12.25, 'sqrt(x)', prod='pintrinsics')
P[2] = test( pintrinsics.pi, None, 'pi    ', prod='pintrinsics')
pi = pintrinsics.pi()
P[3] = test( pintrinsics.sine, 0.25*pi, 'sin(x)', prod='pintrinsics')
P[4] = test( pintrinsics.cosine, 0.25*pi, 'cos(x)', prod='pintrinsics')
writefile('test1.nc', P)

def recip(x):
    return (1./numpy.array(x))
def pifn():
    return numpy.pi

P[0] = test( recip, .3, '1/x    ', prod='numpy')
P[1] = test( numpy.sqrt, 12.25, 'sqrt(x)', prod='numpy')
P[2] = test( pifn, None, 'pi    ', prod='numpy')
pi = pifn()
P[3] = test( numpy.sin, 0.25*pi, 'sin(x)', prod='numpy')
P[4] = test( numpy.cos, 0.25*pi, 'cos(x)', prod='numpy')
writefile('test2.nc', P)
