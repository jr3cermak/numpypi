import pypi

re = pypi.reciprocal(.3, verbose=True)
sq = pypi.sqrt(12.25, verbose=True)
pi = pypi.pi(verbose=True)
si = pypi.sine(0.25*pi, verbose=True)
co = pypi.cosine(0.25*pi, verbose=True)

print()
print(re,sq,pi,si,co)
