from __future__ import print_function

import hashlib
import numpy
import pintrinsics
import netCDF4
import struct

def test(fn, val, label, prod=''):
    if val is None:
        res = fn()
    else: 
        res = fn(val)
    i = struct.unpack( 'q', struct.pack('d',res) )
    h = hashlib.sha224( str(i).encode('utf-8') ).hexdigest()
    print(prod, label, '\t', h, 'x =', str(val), 'fn() =', str(res))
    return res

def writefile(filename, vals):
    f = netCDF4.Dataset(filename, 'w', clobber=True, format='NETCDF3_CLASSIC')
    v = f.createDimension('n', len(vals) )
    v = f.createVariable('results', 'f8', ('n',))
    v[:] = numpy.array(vals)[:]
    f.close()

P = []
for a in range(1,11):
  P.append( test( pintrinsics.reciprocal, .125*a, '1/x    ', prod='pintrinsics') )
for a in range(1,11):
  P.append( test( pintrinsics.sqrt, .25*a, 'sqrt(x)', prod='pintrinsics') )
P.append( test( pintrinsics.pi, None, 'pi    ', prod='pintrinsics') )
pi = pintrinsics.pi()
for a in range(1,11):
  P.append( test( pintrinsics.sine, 0.025*pi*a, 'sin(x)', prod='pintrinsics') )
  P.append( test( pintrinsics.cosine, 0.025*pi*a, 'cos(x)', prod='pintrinsics') )
writefile('test1.nc', P)

def recip(x):
    return (1./numpy.array(x))
def pifn():
    return numpy.pi

P = []
for a in range(1,11):
  P.append( test( recip, .125*a, '1/x    ', prod='numpy') )
for a in range(1,11):
  P.append( test( numpy.sqrt, .25*a, 'sqrt(x)', prod='numpy') )
P.append( test( pifn, None, 'pi    ', prod='numpy') )
pi = pifn()
for a in range(1,11):
  P.append( test( numpy.sin, 0.025*pi*a, 'sin(x)', prod='numpy') )
  P.append( test( numpy.cos, 0.025*pi*a, 'cos(x)', prod='numpy') )
writefile('test2.nc', P)
