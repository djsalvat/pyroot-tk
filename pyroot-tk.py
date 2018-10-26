import ROOT

def mr_legend(hist_list,text_list,size=(0.6,0.6,0.95,0.9)):
        '''Take a list of histograms and list of collated legend labels
        (strings). A legend is generated and returned. The optional
        size setting expects a tuple (xlo,ylo,xhi,yhi).
        '''
        leg = ROOT.TLegend(*size)
        for hist,text in zip(hist_list,text_list):
                leg.AddEntry(hist,text)
        return leg

def Integralv(self,lo,hi):
        '''adds a method to histogram classes to get integral
        based on the axis value instead of the bin numbers.
        '''
        return self.Integral(self.FindBin(lo),self.FindBin(hi))
ROOT.TH1.Integralv = Integralv

def IntegralvAndError(self,lo,hi,err):
        '''adds a method to histogram classes to get integral
        based on the axis value instead of the bin numbers.
        '''
        return self.IntegralAndError(self.FindBin(lo),self.FindBin(hi),err)
ROOT.TH1.IntegralvAndError = IntegralvAndError

def Snip(self,lo,hi,label=''):
        '''adds a method to histogram classes to cut out part of Y axis.
        '''
        newhist = self.Clone(self.GetName()+label+'_snip_'+str(lo)+'_'+str(hi)).ProjectionX()
        tmphist = self.Clone(self.GetName()+label+'_snip_'+str(lo)+'_'+str(hi)+'_tmp')
        tmphist.GetYaxis().SetRangeUser(lo,hi)
        newhist.Add(tmphist.ProjectionX(),-1.0)
        return newhist
ROOT.TH1.Snip = Snip

def Slice(self,lo,hi,label=''):
        '''adds a method to histogram classes to select part of Y axis.
        '''
        newhist = self.Clone(self.GetName()+label+'_slice_'+str(lo)+'_'+str(hi))
        newhist.GetYaxis().SetRangeUser(lo,hi)
        return newhist.ProjectionX()
ROOT.TH1.Slice = Slice

def AddSmart(self,hist,c):
        '''Same as the usual "Add" method, but instead it returns
        a new histogram as a result, with an auto-generated name
        '''
        newhist = self.Clone(self.GetName()+'_plus_'+str(c)+'*'+hist.GetName())
        newhist.Add(hist,c)
        return newhist
ROOT.TH1.AddSmart = AddSmart

def Shift(self,c):
        for b in range(self.GetNbinsX()+1):
                self.SetBinContent(b,self.GetBinContent(b)+c)
ROOT.TH1.Shift = Shift

def make_residual(hist,func,restype='normed',label=''):
        '''takes a histogram and a tf1 and returns a residual histogram.
        restype can be 'normed' (default) which plots (y-f(x))/sigma,
        'unnormed' which plots (y-f(x)), or 'relative' which plots (y-f(x))/f(x).
        '''
        hist_ = ROOT.TH1D(hist.GetName()+label+'_res',';'+hist.GetXaxis().GetTitle(),
                          hist.GetNbinsX(),hist.GetXaxis().GetBinLowEdge(0),
                          hist.GetXaxis().GetBinUpEdge(hist.GetNbinsX()))
        for b in range(1,hist.GetNbinsX()+1):
                content = hist.GetBinContent(b)
                funcval = func.Eval(hist.GetBinCenter(b))
                err = hist.GetBinError(b)
                if restype=='normed':
                        if err > 0.0:
                                hist_.SetBinContent(b,(content-funcval)/err)
                                hist_.SetBinError(b,1.0)
                        else:
                                hist_.SetBinContent(b,0.0)
                                hist_.SetBinError(b,0.0)
                elif restype=='unnormed':
                        hist_.SetBinContent(b,content-funcval)
                        hist_.SetBinError(b,err)
                elif restype=='relative':
                        hist_.SetBinContent(b,(content-funcval)/funcval)
                        hist_.SetBinError(b,err/funcval)
        return hist_
        
