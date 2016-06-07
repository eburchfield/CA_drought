# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 15:35:31 2016

@author: Emily Burchfield
"""
import numpy as np
from osgeo import osr, gdal
from gdal import *
import matplotlib.mlab as ml

#XYZ (long, lat, data) format ascii file without header information
#first load xyz into GIS to construct raster from point centroids

d = '/data/emily/WF/kate/spi'
infile = d + "/SPI20091.asc"
outfile = d + '/test4.tif'
refIm = '/data/emily/WF/kate/spi/refIm.tif'

def ascii_to_tiff(infile, outfile, refIm):
	"""
	Transform an XYZ ascii file without a header to a projected GeoTiff
	
	:param infile (str): path to infile ascii location
	:param outfile (str): path to final GTiff
	:param refIm (str): path to a reference image made from the lat lon pair centriods
	
	"""
	
    im = gdal.Open(refIm)
    ima = gdal.Open(refIm).ReadAsArray()
    row = ima.shape[0]; col = ima.shape[1]
     
    indata = np.genfromtxt(infile, delimiter=",", skip_header = True, dtype=None)
    lon = indata[:,0] #x
    lat = indata[:,1] #y
    data = indata[:,2]

    #create grid
    xmin, xmax, ymin, ymax = [min(lon), max(lon), min(lat), max(lat)]
    xi = np.linspace(xmin, xmax, col)
    yi = np.linspace(ymin, ymax, row)
    xi, yi = np.meshgrid(xi, yi)

    #linear interpolation
    zi = ml.griddata(lon, lat, data, xi, yi, interp = 'linear')
    final_array = np.asarray(np.rot90(np.transpose(zi)))

    #projection
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(outfile, col, row, 1, gdal.GDT_Float32)
    dst_ds.GetRasterBand(1).WriteArray(final_array)
    prj = im.GetProjection()
    dst_ds.SetProjection(prj)
    
    gt = im.GetGeoTransform()
    dst_ds.SetGeoTransform(gt)
    dst_ds = None

    final_tif = gdal.Open(outfile, GA_ReadOnly).ReadAsArray()
    return final_tif    
    
    
