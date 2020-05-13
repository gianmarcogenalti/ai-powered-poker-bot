# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:16:39 2020

@author: Francesco
"""


class SubGameResolver:
    #subinfoset contiene la lista degli infoset che sono nel sotto gioco
    def __init__(self,abs_infosets,SubInfosets,nodes):
        self.infosets = abs_infosets
        self.SubInfoset=Subinfosets
        self.nodes= nodes 
        
        
   def  new_strategy:
       for absInfo in self.SubInfoset:
           for idaction in range(len( self.SubInfoset.Actions[absInfo])):
               #qui calcolo i regret di ogni azione con funzioni che devo ancora fare e aggiorno R poi aggiorno le strategie
              r(idaction,absInfo)=ComputeRegret(absInfo,idaction,sigma)
              R(idaction,absInfo)=R(idaction,absInfo)+r
              R_plus(idaction,absInfo)=max(R(idaction,absInfo),0)
        Updatesigma(R_plus)