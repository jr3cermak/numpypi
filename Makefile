all: a-test1.nc a-test2.nc test1.cdl test2.cdl
	hostname
	python --version
	pip list | egrep "numpy|scipy|netCDF4"
	md5sum *.nc

check: a-test1.nc a-test2.nc test1.nc test2.nc
	md5sum -c test.md5

test1.nc test2.nc:
	python test.py
	
%.cdl: %.nc
	ncdump $< > $@

a-%.nc: %.cdl
	ncgen -o $@ -k1 $<

clean:
	@rm -f *.nc *.cdl
