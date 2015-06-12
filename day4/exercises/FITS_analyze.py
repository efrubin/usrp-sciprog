#!/usr/bin/env python

import astropy.io.fits
import numpy as np



def getMagnitudes(table, magzero, fields):
    '''returns a dict of arrays of magnitudes. inputs are table (FITS table), magzero (magnitude zero point), 
    and d (a dictionary mapping the name of a filter to the flux column)'''

    magtable = {}
    mask =np.ones(len(table), dtype=bool)
    for k,v in fields.items():


        mask = np.logical_and(mask, np.isfinite(table[v]))

        mask = np.logical_and(mask, table[v]>0.0)


    table = table[mask]

    for k, v in fields.items():

        magtable[k] = -2.5 * np.log10(table[v]) + magzero

    #build a mask - look through each set of values in the dictionary and make an array of isnot(isnan)

    #for k, v in magtable.items():

        #print  np.logical_not(np.isnan(magtable[v]))

    return magtable
