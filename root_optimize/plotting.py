from __future__ import absolute_import
from __future__ import print_function

import csv
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def init_palette():
  from rootpy.plotting.style import set_style, get_style
  atlas = get_style('ATLAS')
  atlas.SetPalette(51)
  set_style(atlas)
  return True

def nbins(start, stop, step):
    return abs(int( (stop - start) / step ))

def init_canvas(x, y, name="c", topMargin=0.07, rightMargin=0.16):
    c = ROOT.TCanvas("c", "", 0, 0, x, y)
    c.SetTopMargin(topMargin)
    c.SetRightMargin(rightMargin)
    return c

def axis_labels(x_label="m_{#tilde{g}} [GeV]", y_label="m_{#tilde{#chi}^{0}_{1}} [GeV]", z_label="", title=""):
    return ';'.join([x_label, y_label, z_label, title])

def init_hist(label, x_min, x_max, y_min, y_max, bin_size, name="grid"):
    return ROOT.TH2F(name,
                axis_labels(z_label=label),
                nbins(x_min, x_max, bin_size),
                x_min,
                x_max,
                nbins(y_min, y_max, bin_size),
                y_min,
                y_max)

def fill_hist(hist,plot_array,label,skipNegativeSig=True):

  for i in range(len(plot_array[label])):
      g = int(plot_array['mgluino'][i])
      l = int(plot_array['mlsp'][i])
      z = plot_array[label][i]
      sig = plot_array['sig'][i]
      b = hist.FindFixBin(g,l)
      if(sig>0) or not(skipNegativeSig):
        xx=ROOT.Long(0)
        yy=ROOT.Long(0)
        zz=ROOT.Long(0)
        hist.GetBinXYZ(b,xx,yy,zz)
        z_old =  hist.GetBinContent(xx,yy)
        newz = max(z_old,z) #for significances this makes sense. For the other quantities not so much. Oh well.
        hist.SetBinContent(b,newz)
      else:
        hist.SetBinContent(b,0.01)

def draw_hist(hist, nSigs=1):
    hist.SetMarkerSize(800)
    hist.SetMarkerColor(ROOT.kWhite)
    #gStyle.SetPalette(51)
    ROOT.gStyle.SetPaintTextFormat("1.{0:d}f".format(nSigs));
    hist.Draw("TEXT45 COLZ")

def draw_labels(lumi):
    txt = ROOT.TLatex()
    txt.SetNDC()
    txt.DrawText(0.32,0.87,"Internal")
    txt.DrawText(0.2,0.82,"Simulation")
    #txt.SetTextSize(0.030)
    txt.SetTextSize(18)
    txt.DrawLatex(0.16,0.95,"#tilde{g}-#tilde{g} production, #tilde{g} #rightarrow t #bar{t} + #tilde{#chi}^{0}_{1}")
    txt.DrawLatex(0.62,0.95,"L_{int} = %d fb^{-1}, #sqrt{s} = 13 TeV"% lumi)
    txt.SetTextFont(72)
    txt.SetTextSize(0.05)
    txt.DrawText(0.2,0.87,"ATLAS")
    txt.SetTextFont(12)
    txt.SetTextAngle(38)
    txt.SetTextSize(0.02)
    txt.DrawText(0.33,0.63,"Kinematically Forbidden")

def draw_text(path):

    if path is None:
        return

    txt = TLatex()
    txt.SetNDC()
    txt.SetTextSize(0.030)

    with open(path,'r') as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            txt.DrawLatex(float(row[0]), float(row[1]), row[2])

def draw_line(x_min, x_max, y_max, topmass=173.34):
  l=ROOT.TLine(1000,1000,2000,2000)
  l.SetLineStyle(2)
  l.DrawLine(x_min,x_min-2*topmass,y_max+2*topmass,y_max)

from array import *
def get_run1(filename,linestyle,linewidth,linecolor):
  x = array('f')
  y = array('f')
  n = 0
  with open(filename,'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ' ')
    for row in reader:
      n += 1
      x.append(float(row[0]))
      y.append(float(row[1]))

  gr = ROOT.TGraph(n,x,y)
  gr.SetLineColor(linecolor)
  gr.SetLineWidth(linewidth)
  gr.SetLineStyle(linestyle)
  return gr

def draw_run1_text(color):
    txt = ROOT.TLatex()
    txt.SetNDC()
    txt.SetTextFont(22)
    txt.SetTextSize(0.04)
    txt.SetTextColor(color)
    txt.DrawText(0.2,0.2,"Run 1 Limit")

def exclusion():
  x = array('d',[1400,1600,1600,1400])
  y = array('d',[600,600,800,600])
  p=ROOT.TPolyLine(4,x,y)
  p.SetFillColor(1)
  p.SetFillStyle(3001)
  #p.DrawPolyLine(4,x,y)
  return p