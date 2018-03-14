#!/usr/bin/env python
#------------------------------------------------------------------------------
# File: analyze.py
# Description: analyze BDT/MLP produced by TMVA
# Created: 07-Apr-2017 HBP (error-rate vs # trees example for Meena)
#------------------------------------------------------------------------------
import os, sys
from ROOT import *
from math import *
# to get do
# git clone https://github.com/hbprosper/histutil.git
# source histutil/setup.sh
from histutil import *
from time import sleep
#------------------------------------------------------------------------------
# read training and test data, assuming that the multivariate discriminant
# was trained with SplitMode=Block in TMVA
#------------------------------------------------------------------------------
def readData(filename, variables, mvd, ntrain, ntest, gap=0,
             treename='Analysis'):
    
    ntuple = Ntuple(filename, treename)
    size   = len(ntuple)
    print 'reading file: %s\tnumber of rows: %d' % (filename, size)

    index  = 0
    # ---------------------------------    
    # get training data
    # ---------------------------------
    print "  train data"
    traindata = []
    count  = 0
    while index < size:
        ntuple.read(index)
        index += 1

        # we need to call this here to in order to create
        # new instances of vdata
        vdata = vector('double')(len(variables))
        for ii, name in enumerate(variables): vdata[ii] = ntuple(name)
        traindata.append(vdata)
        
        if count % 100 == 0:
            print '%5d\t%10.3f' % (count, mvd(vdata))

        # stop when we have accumulated enough training
        # data then skip 
        count += 1
        if count >= ntrain:
            index += gap
            break
    # ---------------------------------
    # get test data
    # ---------------------------------    
    print "  test data"
    testdata = []
    count  = 0
    while index < size:
        ntuple.read(index)
        index += 1
        
        vdata = vector('double')(len(variables))
        for ii, name in enumerate(variables): vdata[ii] = ntuple(name)
        testdata.append(vdata)
        
        if count % 100 == 0:
            print '%5d\t%10.3f' % (count, mvd(vdata))
        
        count += 1
        if count >= ntest:
            break
    return (traindata, testdata)
#------------------------------------------------------------------------------
def main():

    # load BDT (C++ wrapped version)    
    gSystem.Load("lib/libmvd.so")

    # instantiate
    bdt = myBDT()
    
    print "number of trees: %6d" % bdt.size()
    print "summed weights:  %10.3f" % bdt.summedWeights()
    
    print "variables"
    vs = bdt.variables()
    for ii in xrange(vs.size()):
        print "\t%5d\t%s" % (ii, vs[ii])

    print
    print 'variable ranking by frequency'
    R = bdt.ranking()
    top = R[0].first
    for ii in xrange(R.size()):
        print '%5d\t%10.3f\t%s' % \
          (ii, R[ii].first/top, R[ii].second)

    print
    ntrees = 5
    print 'first %d trrees' % ntrees
    for itree in xrange(ntrees):
        print
        bdt.printTree(itree)

    # ---------------------------------        
    # Get training and test data for
    # background and signal
    # ---------------------------------    
    ntrain = 800
    ntest  = 200
    ngap   = 0
    
    trainBdata, testBdata = readData('badwine.root',  vs, bdt,
                                      ntrain, ntest, ngap)
    
    trainSdata, testSdata = readData('goodwine.root',vs, bdt,
                                      ntrain, ntest, ngap)
    #--------------------------------------------------------------------------
    # plot some stuff
    #--------------------------------------------------------------------------
    setStyle()
    
    # plot frequency based ranking
    
    hrank = TH1F('hrank', 'rank by frequency', len(vs), 0, len(vs))
    hrank.SetMinimum(0)
    hrank.SetMaximum(1)
    hrank.SetFillColor(kBlue)
    hrank.SetFillStyle(3001)
    hrank.GetYaxis().SetTitle('relative rank')
    hrank.GetYaxis().SetTitleOffset(0.9)
    hrank.GetXaxis().SetLabelSize(0.05)
    
    for ii in xrange(vs.size()):
        hrank.GetXaxis().SetBinLabel(ii+1, vs[ii])
        hrank.SetBinContent(ii+1, R[ii].first/top)
        hrank.SetBinError(ii+1, 0)
        
    canvas = TCanvas('fig_ranking', 'ranking', 10, 10, 800, 400)
    canvas.cd()
    canvas.SetLeftMargin(0.10)
    canvas.SetBottomMargin(0.18)
    canvas.SetRightMargin(0.05)
    hrank.Draw('hist')
    canvas.Update()
    gSystem.ProcessEvents()
    canvas.SaveAs('.png')

    # Plot error rate vs. forest size

    xmin = 0
    xmax = min(400, bdt.size())
    xbins= 100
    ymin = 0.0
    ymax = 0.3    
    nstep  = 1
    numTrees = range(0, xmax+nstep, nstep)
    numTrees[0] = 1

    # setup plot for error rate
    
    cerr = TCanvas('fig_errorRate', 'error rate', 10, 520, 800, 400)
    cerr.SetLeftMargin(0.10)
    cerr.SetBottomMargin(0.18)
    cerr.SetRightMargin(0.05)
    
    hfmt = mkhist1('h', 'number of trees', 'error rate', xbins, xmin, xmax)
    hfmt.SetMinimum(ymin)
    hfmt.SetMaximum(ymax)
    hfmt.GetYaxis().SetTitleOffset(0.9)
       
    gtrain = mkgraph(None, None, 'number of trees', 'error rate', xmin, xmax,
                     color=kRed, lwidth=2)

    gtest = mkgraph(None, None, 'number of trees',  'error rate', xmin, xmax,
                    color=kBlue, lwidth=2)

    lg = mklegend(0.62, 0.68, 0.20, 0.20)
    lg.AddEntry(gtest, 'test data', 'l')
    lg.AddEntry(gtrain, 'training data', 'l')
    
    cerr.cd()
    hfmt.Draw()
    lg.Draw()
    cerr.Update()
    gSystem.ProcessEvents()

    # loop over different numbers of trees
    np = 0
    for nt in numTrees:

        # compute error rate on training sample
        trainError = 0.0
        for d in trainBdata:
            if bdt(d, nt) > 0: trainError += 1.0
        for d in trainSdata:
            if bdt(d, nt) < 0: trainError += 1.0
        trainError /= len(trainBdata)+len(trainSdata)

        # compute error rate on test sample
        testError = 0.0
        for d in testBdata:
            if bdt(d, nt) > 0: testError += 1.0
        for d in testSdata:
            if bdt(d, nt) < 0: testError += 1.0
        testError /= len(testBdata)+len(testSdata)       
        
        #print "%5d\t%10.3f\t%10.3f" % (nt, trainError, testError)

        # update plot
        np += 1
        gtrain.SetPoint(np, nt, trainError)
        gtest.SetPoint(np, nt, testError)
        cerr.cd()
        gtrain.Draw('l same')
        gtest.Draw('l same')
        cerr.Update()
        gSystem.ProcessEvents()
    #--------------------------------------------------------------------------
    cerr.cd()
    addTitle(' error rate vs number of trees')
    cerr.Update()
    gSystem.ProcessEvents()
    cerr.SaveAs(".png")

    sleep(5)
#------------------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\nciao"
