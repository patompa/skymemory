#! /usr/bin/env python3
from chunklocator import ChunkLocator
import math
import default_config

class Simulator:
  def __init__(self, config):
    self.config = config
    self.max_sats = self.config["MAX_SATELLITES"]
    self.max_orbs = self.config["MAX_ORBS"]
    self.v = 2.998*10**8
    self.re = 6371*10**3
    self.altitude = self.config["ALTITUDE"]
    self.dm = (self.re+self.altitude)*math.sqrt(2*(1-math.cos(2*math.pi/self.max_sats))) 
    self.dn = (self.re+self.altitude)*math.sqrt(2*(1-math.cos(2*math.pi/self.max_orbs))) 
    self.center_sat = self.config["CENTER_SATELLITE"]
    self.center_orb = self.config["CENTER_ORB"]
    self.strategy = self.config["STRATEGY"]
    self.servers = self.config["SERVERS"]
    self.on_board = self.config["STRATEGY"] == "hop"
    self.chunklocator = ChunkLocator((self.center_sat,self.center_orb),strategy=self.strategy,
                                     servers=self.servers,tot_sats=self.max_sats, tot_orbs=self.max_orbs)
    self.positions = self.chunklocator.positions
    self.chunk_size = self.config["CHUNK_SIZE_BYTES"] 
    self.kvc_size = config["KVC_BYTES"] 
    self.chunk_processing_time = config["CHUNK_PROCESSING_TIME"] 

    
  def get_times(self):
    chunks = math.ceil(self.kvc_size/self.chunk_size)  
    for c in range(0,chunks):
      index = c % self.servers
      if not "chunks" in self.positions[index]:
        self.positions[index]["chunks"] = 0
      self.positions[index]["chunks"] += 1
    times = []
    for pos in self.positions:
      times.append(self.latency(pos["sat"],pos["orb"])+self.chunk_processing_time*pos["chunks"])
    return times  

  def latency(self,sat,orb):
    return self.distance(sat,orb)/self.v

  def distance(self,sat,orb): 
    if self.on_board:
      return self.delta_orb(orb)*self.dn + self.delta_sat(sat)*self.dm
    D = math.sqrt((self.delta_orb(orb)*self.dn)**2+(self.delta_sat(sat)*self.dm)**2)
    return math.sqrt(D**2+self.altitude**2)

  def delta_sat(self,sat):
    return min(abs(self.center_sat-sat),self.max_sats-abs(sat-self.center_sat))

  def delta_orb(self,orb):
    return min(abs(self.center_orb-orb),self.max_orbs-abs(orb-self.center_orb))

if __name__ == "__main__":
  simulator = Simulator(default_config.config)
  print(max(simulator.get_times()))
