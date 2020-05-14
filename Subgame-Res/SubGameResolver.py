# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:16:39 2020

@author: Francesco
"""


class SubGameResolver:
    #subinfoset contiene la lista degli infoset che sono nel sotto gioco
    def __init__(self,abs_infosets,SubInfosets):
        self.infosets = abs_infosets
        self.SubInfoset=Subinfosets
        self.sigma= abs_infosets.Actions_Probs
        self.R= initR(self)
        self.R_plus= abs_infosets.Actions_Probs
        
   def  new_strategy(self,subInfosets):
       for absInfo in SubInfoset:
           mixed=0
           for idaction in range(len( SubInfoset.Actions[absInfo])):
              mixed+=self.infosets.Exp_Ut[idaction]*self.sigma[absInfo][idaction]
           for idaction in range(len( SubInfoset.Actions[absInfo])):
              r=self.ComputeRegret(absInfo,idaction,mixed)
              self.R[absInfo][idaction]+=r
              self.R_plus[absInfo][idaction]=max(self.R[absInfo][idaction],0)
           self.Updatesigma(absInfo)
   
    def  ComputeRegret(self,absInfo,idaction,mixed):
        return self.infosets.Exp_Ut[absInfo][idaction]-mixed
   
    def  Updatesigma(self,absInfo):
        sm=sum(self.R_plus[absInfo])
        if not sm:
           for idaction in range(len( SubInfoset.Actions[absInfo])):
               self.sigma[absInfo][idaction]=R_plus[idaction]/sm
        else:
           for idaction in range(len( SubInfoset.Actions[absInfo])):
               self.sigma[absInfo][idaction]=1/len(self.sigma[absInfo])
        