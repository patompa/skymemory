#! /usr/bin/env python3
from simulator import Simulator
import default_config
import copy
import numpy as np
import math



strategies = "rotation","hop","hop_rotation"

parameters = {}

parameters["KVC_BYTES"] = list(range(2**20,22*(2**20),2**20))
parameters["SERVERS"] = [9,25,49,81]
parameters["CHUNK_PROCESSING_TIME"] = (np.array(list(range(1,11)))/500).tolist()
parameters["ALTITUDE"] = list(range(160000,2000000,220000))


def runsim(strategy,param):
  results = []
  for p in parameters[param]:
    config = copy.deepcopy(default_config.config)
    config["STRATEGY"] = strategy
    config[param] = p  
    print(f"{strategy} {param} {p}")
    for v in parameters.keys():
      if v == param:
        continue    
      config[v] = parameters[v][-1]  
    sim = Simulator(config)
    times = sim.get_times()   
    max_time = np.max(times)
    min_time = np.min(times)
    avg_time = np.mean(times)
    std_time = np.std(times)
    se_time = np.std(times)/math.sqrt(len(times))
    results.append({"times": {"max": max_time,"min": min_time,"avg":avg_time,"std":std_time,"se":se_time},
                    "param": p})
  with open(f"results/{strategy}.{param}.dat","w") as f:
    out = f"{param}\tMAX\tMIN\tAVG\tSTD\tSE\n"
    f.write(out)  
    for result in results:
      out = f"{result['param']}\t"
      out += f"{result['times']['max']}\t{result['times']['min']}\t"
      out += f"{result['times']['avg']}\t{result['times']['std']}\t"
      out += f"{result['times']['se']}\n"
      f.write(out)  

for strategy in strategies:
  for param in parameters.keys():
    runsim(strategy, param)







