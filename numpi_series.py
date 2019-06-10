import math

def reciprocal(x, n=9, verbose=False):
    """Returns 1/x"""
    # https://en.wikipedia.org/wiki/Division_algorithm
    m,e = math.frexp(x) # Mantissa and exponent in base-2
    r=(2**(-e)) # First quess
    if verbose: print('reciprocal:',r,' first guess')
    for iter in range(n):
        rn = r * ( 2 - x*r )
        if verbose: print('reciprocal:',rn,'(%i)'%iter)
        if rn==r: break
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
        if rn==r: break
        r = rn
    return r

def pi_v0(n=5, verbose=False):
    """Returns pi"""
    # https://en.wikipedia.org/wiki/Approximations_of_%CF%80#Modern_algorithms
    root2 = sqrt(2)
    if verbose: print('pi: sqrt(2) =',root2)
    y,a = root2 - 1, 6 - 4*root2
    if verbose: print('pi: y,a =',y,a,'first guess')
    for k in range(n):
        y2 = y*y
        y4 = y2*y2
        f = sqrt( sqrt( 1 - y4 ) )
        f = (1-y**4)**0.25
        r = reciprocal( 1 + f, n=20)
        yn = ( 1 - f ) * r
        yn = ( 1 - f) / ( 1 + f )
        yp1 = 1 + yn
        yp12 = yp1 * yp1
        an = a*( yp12*yp12 ) - ( yn * ( 1 + yn * ( 1 + yn ) ) ) * ( 2**(2*k+3) )
        # an = a*( 1 + yn )**4 - ( 2**(2*k+3) ) * yn * (1+yn+yn**2)
        if verbose: print('pi: y,a =',yn,an,'(%i)'%k)
        if an==a: break
        y,a = yn,an
    return reciprocal(a, n=20)

def pi(n=5, verbose=False):
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

def sine(x, n=20, verbose=False, efficient=False):
    """Returns sin(x)"""
    assert n<21,'n must be >0 and <21'
    # https://en.wikipedia.org/wiki/Sine#Series_definition
    C=[0.16666666666666667,0.05,0.023809523809523808,0.013888888888888889,0.00909090909090909,0.00641025641025641,0.004761904761904762,0.003676470588235294,0.0029239766081871343,0.002380952380952381,0.001976284584980237,0.0016666666666666667,0.0014245014245014246,0.0012315270935960591,0.001075268817204301,0.000946969696969697,0.0008403361344537816,0.0007507507507507507,0.0006747638326585695]
    if efficient:
        ro,f,s = x,1.,-1.
        for i in range(1,n):
            k = 2*i + 1
            #f = f * pypi.reciprocal( (k-1)*k ) # These should be pre-computed
            f = f * C[i-1]
            r = ro + x**k * f * s
            if verbose: print('sine:',r,'(%i)'%i)
            #if r==ro: break
            ro,s = r, -s
    else:
        f,r,s = [1.]*(n),0.,1.
        if n%2==0: s=-1.
        for i in range(1,n):
            f[i] = f[i-1] * C[i-1]
        for i in range(n-1,0,-1):
            k = 2*i + 1
            r = r + x**k * f[i] * s
            if verbose: print('sine:',r,'(%i)'%i)
            s = -s
        r = r + x
        if verbose: print('sine:',r,'(%i)'%i)
    return r

def cosine(x, n=21, verbose=False):
    """Returns cos(x)"""
    # https://en.wikipedia.org/wiki/Trigonometric_functions#Power_series_expansion
    C=[0.5,0.08333333333333333,0.03333333333333333,0.017857142857142856,0.011111111111111111,0.007575757575757576,0.005494505494505495,0.004166666666666667,0.0032679738562091504,0.002631578947368421,0.0021645021645021645,0.0018115942028985507,0.0015384615384615385,0.0013227513227513227,0.0011494252873563218,0.0010080645161290322,0.00089126559714795,0.0007936507936507937,0.0007112375533428165,0.000641025641025641]
    ro,f,s = 1,1.,-1.
    for i in range(1,n):
        k = 2*i
        #f = f * pypi.reciprocal( (k-1)*k ) # These should be pre-computed
        f = f * C[i-1]
        r = ro + x**k * f * s
        if verbose: print('cosine:',r,'(%i)'%i)
        if r==ro: break
        ro,s = r, -s
    return r
