all: a-test1.nc a-test2.nc
	hostname
	python --version
	pip list | egrep "python|numpy|scipy|netCDF4"
	md5sum *.nc

test1.nc test2.nc:
	python test.py
	
%.cdl: %.nc
	ncdump $< > $@

a-%.nc: %.cdl
	ncgen -o $@ -k1 $<

clean:
	\rm *.nc
