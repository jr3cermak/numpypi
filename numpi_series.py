from __future__ import print_function

# The following import allows all the numpy modules/functions to be accessed
# as if they were in this module. i.e.
#   import numpi as np
# will work as if it read "import numpy as np"
from numpy import *

# The following import gives this script hidden access to numpy
import ignore_this as _numpy

def abs(x):
    return _numpy.numpy.abs(x)

def reciprocal(x, n=9, verbose=False):
    """Returns 1/x"""
    # https://en.wikipedia.org/wiki/Division_algorithm
    m,e = frexp(x) # Mantissa and exponent in base-2
    r = ldexp(1.,-e) # First quess
    s,x = copysign(1., x), abs(x)
    for iter in range(n):
        r = r * ( 2. - x * r )
    return r * s

def sqrt(x, n=9, verbose=False):
    """Returns sqrt(x)"""
    # https://en.wikipedia.org/wiki/Methods_of_computing_square_roots
    m,e = frexp(x) # Mantissa and exponent in base-2
    r = ldexp(1.,(e/2).astype(int)) # First quess
    for iter in range(n):
        r = 0.5 * ( r + x / r )
    return r

def calc_pi(n=5, verbose=False):
    """Returns pi"""
    # https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm
    root2 = sqrt(2.)
    a,b,t,p,rn = 1, reciprocal(root2, n=20), 0.25, 1, 0
    an = 0.5 * ( a + b )
    for iter in range(n):
        bn = sqrt( a*b )
        tn = t - p * ( a - an )**2
        pn = 2 * p
        a,b,t,p = an,bn,tn,pn
        an = 0.5 * ( a + b )
        if verbose:
            r = an**2 * reciprocal(t)
            print('pi:',r,'(%i)'%iter)
        if an==a: break
    r = an**2 * reciprocal(t)
    return r
pi = calc_pi()

def sin(a):
    """Returns sin(x)"""
    # https://en.wikipedia.org/wiki/Sine#Series_definition
    one_eighty = calc_pi()
    three_sixty = 2.*one_eighty
    ninety = 0.5*one_eighty
    x = 1. * a
    fs = 1. + 0. * x
    # Anything < -90 reflect to >-90...
    j = ( x < -ninety )
    x[j] = -one_eighty - x[j]
    # Anything > 360 shift to range 0...360
    j = ( x > three_sixty )
    n = floor( x / three_sixty )
    x[j] = x[j] - n[j] * three_sixty
    # Anything in range 180...360 shift to 0...180
    j = ( x >= one_eighty )
    x[j] = x[j] - one_eighty
    fs[j] = -1.
    # Anything in range 90...180 reflect to 90...0
    j = ( x > ninety )
    x[j] = one_eighty - x[j]
    C=[0.16666666666666667,0.05,0.023809523809523808,0.013888888888888889,0.00909090909090909,0.00641025641025641,0.004761904761904762,0.003676470588235294,0.0029239766081871343,0.002380952380952381,0.001976284584980237,0.0016666666666666667,0.0014245014245014246,0.0012315270935960591,0.001075268817204301,0.000946969696969697,0.0008403361344537816,0.0007507507507507507,0.0006747638326585695]
    n = len(C)
    f,r,s = [1.]*(n),0.,1.
    if n%2==0: s=-1.
    for i in range(1,n):
        f[i] = f[i-1] * C[i-1]
    for i in range(n-1,0,-1):
        k = 2*i + 1
        r,s = r + x**k * f[i] * s,-s
#   term,f,r,s,xx = [1.]*(n),1.,0.,1.,x
#   for i in range(1,n):
#       xx = xx * (x*x)
#       f = f * C[i-1]
#       term[i],s = xx * f * s,-s
#   for i in range(n-1,0,-1):
#       r = r + term[i]
    return ( r + x ) * fs

def cos(a):
    """Returns cos(x)"""
    # https://en.wikipedia.org/wiki/Trigonometric_functions#Power_series_expansion
    one_eighty = calc_pi()
    three_sixty = 2.*one_eighty
    ninety = 0.5*one_eighty
    x = 1. * a
    fs = 1. + 0. * x
    # Anything < 0 reflect to >0...
    j = ( x < 0 )
    x[j] = -x[j]
    # Anything > 360 shift to range 0...360
    j = ( x > three_sixty )
    n = floor( x / three_sixty )
    x[j] = x[j] - n[j] * three_sixty
    # Anything in range 180...360 shift to 0...180
    j = ( x >= one_eighty )
    x[j] = x[j] - one_eighty
    fs[j] = -1.
    # Anything in range 90...180 reflect to 90...0
    j = ( x > ninety )
    x[j] = one_eighty - x[j]
    fs[j] = -fs[j]
    # Use sin(90-x) for 45...90
    j = ( x >= 0.5*ninety )
    c = sin(ninety-x)
    C=[0.5,0.08333333333333333,0.03333333333333333,0.017857142857142856,0.011111111111111111,0.007575757575757576,0.005494505494505495,0.004166666666666667,0.0032679738562091504,0.002631578947368421,0.0021645021645021645,0.0018115942028985507,0.0015384615384615385,0.0013227513227513227,0.0011494252873563218,0.0010080645161290322,0.00089126559714795,0.0007936507936507937,0.0007112375533428165,0.000641025641025641]
    n = len(C)
    r,f,s = 1,1.,-1.
    for i in range(1,n):
        k = 2*i
        #f = f * pypi.reciprocal( (k-1)*k ) # These should be pre-computed
        f = f * C[i-1]
        r,s = r + x**k * f * s, -s
    r[j] = c[j]
    return r * fs
