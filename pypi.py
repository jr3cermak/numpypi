import math

def reciprocal(x, n=9, verbose=False):
    """Returns 1/x"""
    # https://en.wikipedia.org/wiki/Division_algorithm
    m,e = math.frexp(x) # Mantissa and exponent in base-2
    r=m*(2**(1-e)) # First quess
    if verbose: print('reciprocal:',r,' first guess')
    for iter in range(n):
        rn = r * ( 2 - x*r )
        if verbose: print('reciprocal:',rn,'(%i)'%iter)
        if abs(rn-r)==0: break
        r = rn
    return r

def sqrt(x, n=9, verbose=False):
    """Returns sqrt(x)"""
    # https://en.wikipedia.org/wiki/Methods_of_computing_square_roots
    m,e = math.frexp(x) # Mantissa and exponent in base-2
    r = 2**(int(e/2)) # First quess
    if verbose: print('sqrt:',r,' first guess')
    for iter in range(n):
        rn = 0.5 * ( r + x/r )
        if verbose: print('sqrt:',rn,'(%i)'%iter)
        if abs(rn-r)==0: break
        r = rn
    return r
