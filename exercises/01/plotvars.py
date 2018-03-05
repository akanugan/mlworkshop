#!/usr/bin/env python
#------------------------------------------------------------------
# Description: Wine tasting
#------------------------------------------------------------------
import os,sys,csv
from math import *
from ROOT import *
from histutil import *
from time import sleep
from string import *
from array import array
#------------------------------------------------------------------
VARS = '''
acetic
citric
suger
salt
SO2free
SO2tota
pH
sulfate
alcohol
quality
'''
VARS = map(strip, split(strip(VARS),'\n'))
#------------------------------------------------------------------
def main():
    setStyle()
    
    filename = 'wine.dat'
    table = Table(filename)

    # format [(name1, count1), (name1, count2), ..]
    variables = table.variables()
    hsig = []
    hbkg = []
    msize= 0.15
    for ii in xrange(len(variables)-2):
        varx = variables[ii][0]
        for jj in xrange(ii+1, len(variables)-2):
            vary = variables[jj][0]
            hs = mkhist2('hs_%d_%d'  % (ii, jj),
                         varx, vary,
                         20,-2, 2, 20,-2, 2)
            hs.SetMarkerColor(kCyan+1)
            hs.SetMarkerSize(msize)
            
            hs.GetXaxis().CenterTitle()
            hs.GetXaxis().SetTitleSize(0.10)
            hs.GetXaxis().SetTitleOffset(0.2)
            
            hs.GetYaxis().CenterTitle()
            hs.GetYaxis().SetTitleSize(0.10)
            hs.GetYaxis().SetTitleOffset(0.2)
            
            hsig.append(hs)
                                    
            hb = mkhist2('hb_%d_%d'  % (ii, jj),
                         varx, vary,
                         20,-2, 2, 20,-2, 2)
            hb.SetMarkerColor(kMagenta+1)
            hb.SetMarkerSize(msize)

            hb.GetXaxis().CenterTitle()
            hb.GetXaxis().SetTitleSize(0.12)
            hb.GetXaxis().SetTitleOffset(0.55)

            hb.GetYaxis().CenterTitle()
            hb.GetYaxis().SetTitleSize(0.12)
            hb.GetYaxis().SetTitleOffset(0.55)                        
            hbkg.append(hb)
    if len(hsig) != 36: sys.exit('huh?!')
                
    canvas = TCanvas('fig_allvars', '', 10, 10, 900, 900)
    canvas.Divide(6, 6)
    
    for index, row in enumerate(table):
        target = row('target')
        ih = 0
        for ii in xrange(len(variables)-2):
            x = row(variables[ii][0])
            for jj in xrange(ii+1, len(variables)-2):
                y = row(variables[jj][0])
                if target > 0:
                    hsig[ih].Fill(x, y)
                else:
                    hbkg[ih].Fill(x, y)
                ih += 1
        if index % 100 == 0:
            for ih in xrange(len(hsig)):
                canvas.cd(ih+1)
                hbkg[ih].Draw('p')
                hsig[ih].Draw('p same')
            canvas.Update()

    for ih in xrange(len(hsig)):
        canvas.cd(ih+1)
        hbkg[ih].Draw('p')
        hsig[ih].Draw('p same')
    canvas.Update()
    canvas.SaveAs('.png')
    sleep(10)            
try:
    main()
except KeyboardInterrupt:
    print "\nciao!"
    
    
