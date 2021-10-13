[![basic tests](https://github.com/adcroft/numpypi/actions/workflows/basic_tests.yml/badge.svg)](https://github.com/adcroft/numpypi/actions/workflows/basic_tests.yml)

# Portable intrinsics for numpy (numpypi)

## Warnings!

- This is not meant to be a replacement for numpy.
- These portable intrinsic functions are not efficient.
- These modules are unsafe in that they try to wrap numpy and replace certain functions so you can not readily tell where the function comes from.
- Only a subset of intrinsic functions are implemented as portable.

##

- Provides portable intrinsic functions that return the same bitwise floating-point values on different platforms.

## Why?

- We need some way to obtain bitwise-the-same floating-point values in certain non-time-critical calculations.

## How?

- Using just "+", "-", "*", and "1/" operations one can "hope" to obtain the same results on different platofrms if they adhere to recommendations in IEEE 754 (https://en.wikipedia.org/wiki/IEEE_754).
- Avoid `z=a/b` by using `d=1/b ; z=a*d`.
- Evaluate intrinsic functions using series or root-finding, rather than the c-library version of the functions.
- Retain accuracy in series by summing from smallest terms first.

## Where?

- Works on Linux, Windows and Mac and for both python2 and python3.
- Regularly tested with Travis-CI and on various linux platforms.

## Test?

```bash
python test_series.py
```

## To use

In python

```python
import numpypi_series
```

or (be careful!)

```python
import numpypi_series as numpy
```
