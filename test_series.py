from __future__ import print_function

import hashlib
import numpi_series as numpy  # Module to test

def logistic_map(x, r=4.-1./32):
    """Logistic map r*x*(1-x)"""
    return r * x * ( 1. - x )
def generate_numbers(n, r=4.-1./32, x0=0.5, n0=0):
    """Generates reproducible vector of values between 0 and 1"""
    for k in range(n0):
        x0 = logistic_map( x0, r=r)
    x = numpy.zeros(n)
    x[0] = x0
    for k in range(1,n):
        x[k] = logistic_map( x[k-1], r=r)
    return x
def compare_numbers(x, y, good_hash=None, quiet=False):
    # Compare hashes
    status = True
    # Numerical test
    error = ( x - y )
    n = numpy.count_nonzero( error )
    if n>0:
        if not quiet: print(' X There were %i differences detected (out of %i) or %3.4f%% hits.'%(n,error.size,(100.*n)/error.size))
        k = numpy.nonzero( error )[0]
        if not quiet: print('   First few values ...')
        frac = error / x
        for j in range( min(n, 5) ):
            i = k[j]
            a,b,e,f = x[i],y[i],error[i],frac[i]
            if not quiet: print('      x(%i)=%23.15e y(%i)=%23.15e error=%.5e frac. err.=%.2e'%(i,a,i,b,e,f))
        print('   Largest fractional error = %.2e'%numpy.abs( frac ).max() )
        status = False
    # Bitwise (hash) test
    hx = hashlib.sha256( numpy.array( x ) ).hexdigest()
    hy = hashlib.sha256( numpy.array( y ) ).hexdigest()
    print('   hash(x) =', hx, 'min=%.15e max=%.15e'%(x.min(), x.max()))
    if hx != hy and status:
        print('   hash(y) =', hy, 'min=%.15e max=%.15e'%(y.min(), y.max()))
        print(' X Hashes do not match (i.e. bits differ).')
        status = False
    # Recorded hash
    if good_hash is not None:
        if hx == good_hash:
            print('   Hash matches recorded hash.')
        else:
            print('   hash(R) =', good_hash)
            print(' X Hash does NOT match recorded hash!')
            status = False
    return status
def writefile(filename, vals):
    f = netCDF4.Dataset(filename, 'w', clobber=True, format='NETCDF3_CLASSIC')
    v = f.createDimension('n', len(vals) )
    v = f.createVariable('results', 'f8', ('n',))
    v[:] = numpy.array(vals)[:]
    f.close()

N = 1024*1024
x01 = generate_numbers(N, r=4.-1./(1024*1024*1024*1024)) # Reproducible numbers between 0..1

print('Generated test numbers: ', end='')
for k in range(4): print( '%.15e'%x01[k], end=', ' )
print('...')
x01_hash = 'e6eb0684e329098c7c3fd2514e14436d27dfc13395237b179168ec34030e0c11'
assert compare_numbers(x01, x01, good_hash=x01_hash), 'Generated test numbers did not reproduce!'

# Generate better numbers
x01 = generate_numbers(N, r=4.-1./(1024*1024*1024*1024), n0=987654) # Reproducible numbers between 0..1
print('Generated test numbers: ', end='')
for k in range(4): print( '%.15e'%x01[k], end=', ' )
print('...')
x01_hash = 'b0e634899b6519687c044e0310b2ac9bf0e56704dcd70696749a9b84da2e3661'
assert compare_numbers(x01, x01, good_hash=x01_hash), 'Generated test numbers did not reproduce!'

# Floating point range

print('Check that maximum floating point number (numpy.finfo.max) is bitwise as expected')
x = numpy.array([numpy.finfo(float).max])
max_hash = 'dd46fdd197731f40f29d789fd02be525b10ff16ea3b7830c9f2c5b28131420ff'
assert compare_numbers(x, x, good_hash=max_hash), 'numpy.finfo.mas did not reproduce'

print('Check that floating point epsilon (numpy.finfo.eps) is bitwise as expected')
x = numpy.array([numpy.finfo(float).eps])
max_hash = '78902dbbf3ee23e635e0b63fd65aea1e80d4a8b08559ea0bb884c7eb872e15d8'
assert compare_numbers(x, x, good_hash=max_hash), 'numpy.finfo.eps did not reproduce'

# Special values

print('Check that PI (numpy.pi) is bitwise as expected')
x = numpy.array([numpy.pi])
pi_hash = '8b5319c77d1df2dcfcc3c1d94ab549a29d2b8b9f61372dc803146cbb1d2800b9'
assert compare_numbers(x, x, good_hash=pi_hash), 'numpy.pi did not reproduce'

print('Check numpy intrinsics for special values')
x = numpy.array([ numpy.sin([numpy.pi/4]), numpy.cos([numpy.pi/4]), numpy.tan(numpy.array([numpy.pi/4])) ])
y = numpy.array([ numpy.sqrt([2])/2, numpy.sqrt([2])/2,  1.0 ])
assert not compare_numbers(x, y, quiet=True), 'numpy intrinsics unexpectedly matched!'

# Ranges to test direct series

print('Check numpi intrinsic sin() for range +/- pi/4')
x = numpy.sin( (x01 - 0.5)*numpy.pi*0.5 )
sin_hash = '0c10836887ea83a871533c38fb118d6a0c762f194c39a014fb77e566c39a5737'
assert compare_numbers(x, x, good_hash=sin_hash), 'numpi intrinsic sin() failed to reproduce recorded hash!'

print('Check numpi intrinsic cos() for range +/- pi/4')
x = numpy.cos( (x01 - 0.5)*numpy.pi*0.5 )
cos_hash = '12162e89f1131bcf065ccdfccdb1b6989891b1a14eae82cd2c22d97eb358c526'
assert compare_numbers(x, x, good_hash=cos_hash), 'numpi intrinsic cos() failed to reproduce recorded hash!'

print('Check numpi intrinsic tan() for range +/- pi/8')
x = numpy.tan( (x01 - 0.5)*numpy.pi*0.25 )
tan_hash = '7a11adc32645edcb323291748a3ba61540d1e88100eb27fc18eac3d5bcde57d2'
assert compare_numbers(x, x, good_hash=tan_hash), 'numpi intrinsic tan() failed to reproduce recorded hash!'

# Range +/- pi/2

print('Check numpi intrinsic sin() for range +/- pi/2')
x = numpy.sin( (x01 - 0.5)*numpy.pi )
sin_hash = '335315f32056ec05061d21ede987e0fa2b5ca2a182005fd907fe939a9030382a'
assert compare_numbers(x, x, good_hash=sin_hash), 'numpi intrinsic sin() failed to reproduce recorded hash!'
#assert x.min() >= -1., 'numpi sin(x)<-1 !'
#assert x.max() <= 1., 'numpi sin(x)<-1 !'

print('Check numpi intrinsic cos() for range +/- pi/2')
x = numpy.cos( (x01 - 0.5)*numpy.pi )
cos_hash = '2bfab3ef5e79c893ca72efbf033d73dd2c099245e3d229478b4a0af8b1f99330'
assert compare_numbers(x, x, good_hash=cos_hash), 'numpi intrinsic cos() failed to reproduce recorded hash!'
#assert x.min() >= -1., 'numpi cos(x)<-1 !'
#assert x.max() <= 1., 'numpi cos(x)<-1 !'

print('Check numpi intrinsic tan() for range +/- pi/2')
x = numpy.tan( (x01 - 0.5)*numpy.pi )
tan_hash = '4f92be23557c12cca0426de0da530cfde43de1bd73502dac23b7ad896a4f62fd'
assert compare_numbers(x, x, good_hash=tan_hash), 'numpi intrinsic tan() failed to reproduce recorded hash!'

#print('Check numpi intrinsic arcsin() for range of values')
#x = numpy.arcsin( 2.*x01 - 1. )
#arcsin_hash = '0c8cc44f1b24b2fd2c18dccc0638a9f54758ebfdcdc21d600c7f1b2e647baf4a'
#assert compare_numbers(x, x, good_hash=arcsin_hash), 'numpi intrinsic arcsin() failed to reproduce recorded hash!'
#
#print('Check numpi intrinsic arccos() for range of values')
#x = numpy.arccos( 2.*x01 - 1. )
#arccos_hash = '2db2ba8daaa85a5365cd0ae6b8bb90749f4fc29b61ffb8a9d0ca959b47014787'
#assert compare_numbers(x, x, good_hash=arccos_hash), 'numpi intrinsic arccos() failed to reproduce recorded hash!'
#
#print('Check numpi intrinsic arctan() for range of values')
#x = numpy.arctan( 2.*x01 - 1. )
#arctan_hash = '51c4c9529631a1026159dd9479b4216de65807fd08b9c0a79f4ca44e686f8ae4'
#assert compare_numbers(x, x, good_hash=arctan_hash), 'numpi intrinsic arctan() failed to reproduce recorded hash!'
