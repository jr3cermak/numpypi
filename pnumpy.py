from __future__ import print_function

# The following import allows all the numpy modules/functions to be accessed
# as if they were in this module. i.e.
#   import pnumpy as np
# will work as if it read "import numpy as np"
from numpy import *

# The following import gives this script hidden access to numpy
import ignore_this as _numpy

global __default_bits
__default_bits = None

def round_lastbits(x, bits=None):
    if bits is None:
        bits = __default_bits
    else:
        assert bits>=0, 'Optional argument "bits" must be non-negative'
    if bits is None: return x # Return un-rounded argument if bits==None and __default_bits==None
    bits = int(bits)
    if type(x) is ndarray:
        m,e = frexp( x ) # Mantissa and twos exponent
        if x.dtype == 'float64':
            bits_to_shift = finfo(x.dtype).nmant + 1 - bits
            m = array( m * ( 2**(bits_to_shift) ) ,dtype=float).round() * ( 2**(-bits_to_shift))
            return ldexp( m, e )
        raise Exception('Operation not permitted on ndarray dtype "'+x.dtype+'"')
    elif type(x) == float or type(x) == _numpy.float64:
        return float( round_lastbits( array([x], dtype=float), bits=bits ) )
    raise Exception('Operation not permitted on type "'+str(type(x))+'"')

def set_rounding_bits(bits):
    global __default_bits
    __default_bits = int(bits)

def unset_rounding_bits():
    global __default_bits
    __default_bits = None

def sin(*args, **kwargs):
    global __default_bits
    return round_lastbits( _numpy.sin( *args, **kwargs ), bits=__default_bits )

def cos(*args, **kwargs):
    global __default_bits
    return round_lastbits( _numpy.cos( *args, **kwargs ), bits=__default_bits )

def tan(*args, **kwargs):
    global __default_bits
    return round_lastbits( _numpy.tan( *args, **kwargs ), bits=__default_bits )

def arcsin(*args, **kwargs):
    global __default_bits
    return round_lastbits( _numpy.arcsin( *args, **kwargs ), bits=__default_bits )

def arccos(*args, **kwargs):
    global __default_bits
    return round_lastbits( _numpy.arccos( *args, **kwargs ), bits=__default_bits )

def arctan(*args, **kwargs):
    global __default_bits
    return round_lastbits( _numpy.arctan( *args, **kwargs ), bits=__default_bits )
