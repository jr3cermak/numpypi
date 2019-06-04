import pintrinsics

re = pintrinsics.reciprocal(.3, verbose=True)
sq = pintrinsics.sqrt(12.25, verbose=True)
pi = pintrinsics.pi(verbose=True)
si = pintrinsics.sine(0.25*pi, verbose=True)
co = pintrinsics.cosine(0.25*pi, verbose=True)

print()
print(re,sq,pi,si,co)
