from __future__ import print_function

# The following import allows all the numpy modules/functions to be accessed
# as if they were in this module. i.e.
#   import pnumpy as np
# will work as if it read "import numpy as np"
from numpy import *

# The following import gives this script hidden access to numpy
import ignore_this as _numpy

global __default_bits
__default_bits = 0

def round_lastbits(x, bits=None):
    if bits is None:
        bits = __default_bits
        if bits==0: return x # Only return unrounded argument if bits==None and __default_bits==0
    else:
        assert bits>=0, 'Optional argument "bits" must be non-negative'
    bits = int(bits)
    if type(x) is ndarray:
        m,e = frexp( x ) # Mantissa and twos exponent
        if x.dtype == 'float64':
            bits_to_shift = finfo(x.dtype).nmant + 1 - bits
            m = array( m * ( 2**(bits_to_shift) ) ,dtype=float).round() * ( 2**(-bits_to_shift))
            return ldexp( m, e )
        raise Exception('Operation not permitted on ndarray dtype "'+x.dtype+'"')
    elif type(x) == float:
        return float( round_lastbits( array([x], dtype=float), bits=bits ) )
    raise Exception('Operation not permitted on type "'+str(type(x))+'"')

def set_rounding_bits(bits):
    global __default_bits
    __default_bits = int(bits)

def sin(*args, bits=None, **kwargs):
    if bits is None: bits = __default_bits
    return round_lastbits( _numpy.sin( *args, **kwargs ), bits=bits )

def cos(*args, bits=None, **kwargs):
    if bits is None: bits = __default_bits
    return round_lastbits( _numpy.cos( *args, **kwargs ), bits=bits )

def tan(*args, bits=None, **kwargs):
    if bits is None: bits = __default_bits
    return round_lastbits( _numpy.tan( *args, **kwargs ), bits=bits )

def arcsin(*args, bits=None, **kwargs):
    if bits is None: bits = __default_bits
    return round_lastbits( _numpy.arcsin( *args, **kwargs ), bits=bits )

def arccos(*args, bits=None, **kwargs):
    if bits is None: bits = __default_bits
    return round_lastbits( _numpy.arccos( *args, **kwargs ), bits=bits )

def arctan(*args, bits=None, **kwargs):
    if bits is None: bits = __default_bits
    return round_lastbits( _numpy.arctan( *args, **kwargs ), bits=bits )
