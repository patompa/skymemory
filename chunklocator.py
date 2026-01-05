import math
class ChunkLocator:
  def __init__(self, center, strategy="rotation", servers=9, tot_sats=19, tot_orbs=5):
    self.center = center
    self.strategy = strategy
    self.servers = servers
    self.center_sat = self.center[0]
    self.tot_sats = tot_sats
    self.tot_orbs = tot_orbs
    self.positions = self.get_positions()

  def get_positions(self):
    if self.strategy == "hop_rotation":
      return self.get_hop_rotation_positions()
    elif self.strategy == "rotation":
      return self.get_rotation_positions()
    elif self.strategy == "hop":
      return self.get_hop_positions()
    return []

  def add_hop(self, sat, orb, positions,bounds=None):
    if len(positions) < self.servers:
      chunk = len(positions)+1
      chunk_key = f"{sat}.{orb}"
      if chunk_key in positions:
        return False
      if not bounds is None and not self.is_in_bounds(sat,orb,bounds):
        return False
      positions[chunk_key] = {"sat": sat, "orb": orb, "chunk": chunk}
      return True
    return False

  def add_neighbors(self, sat, orb, positions,bounds=None):
      north_orb = orb - 1
      north_sat = sat
      if north_orb < 1:
        north_orb = self.tot_orbs

      east_orb = orb
      east_sat = sat+1
      if east_sat > self.tot_sats:
        east_sat = 1

      south_orb = orb+1
      south_sat = sat
      if south_orb > self.tot_orbs:
        south_orb = 1

      west_orb = orb
      west_sat = sat-1
      if west_sat < 1:
        weat_sat = self.tot_sats

      explore = []
      if self.add_hop(north_sat, north_orb, positions,bounds=bounds):
        explore.append([north_sat,north_orb])
      if self.add_hop(east_sat, east_orb, positions,bounds=bounds):
        explore.append([east_sat,east_orb])
      if self.add_hop(south_sat, south_orb, positions,bounds=bounds):
        explore.append([south_sat,south_orb])
      if self.add_hop(west_sat, west_orb, positions,bounds=bounds):
        explore.append([west_sat,west_orb])
      return explore


  def populate_neighbors(self,sat,orb,positions,bounds=None):
      to_explore = []
      if self.add_hop(sat,orb,positions,bounds=bounds):
        to_explore.append([sat,orb])
     
      while len(to_explore) > 0 and len(positions) < self.servers:
        next_explore = []
        for explore in to_explore:
          next_explore +=  self.add_neighbors(explore[0],explore[1],positions,bounds=bounds)
        to_explore = next_explore
     
  def get_hop_positions(self):
    orb = self.center[1]
    sat = self.center_sat
    positions = {}
    self.populate_neighbors(sat,orb,positions)
    return list(map(lambda x: x[1],sorted(positions.items(),key=lambda kv: kv[1]["chunk"])))

  def is_in_bounds(self,x,y,bounds):
    if bounds[0] < bounds[1]:
        in_x_bounds = (x >= bounds[0] and x <= bounds[1]) 
    else:
        in_x_bounds = (x >= bounds[0] or x <= bounds[1])

    if bounds[2] < bounds[3]:
        in_y_bounds = (y >= bounds[2] and y <= bounds[3]) 
    else:
        in_y_bounds = (y >= bounds[2] or y <= bounds[3]) 
    return in_x_bounds and in_y_bounds 


  def get_hop_rotation_positions(self):
    orb = self.center[1]
    sat = self.center_sat
    min_orb, max_orb = self.get_min_max_orb()
    min_sat, max_sat = self.get_min_max_sat()
    positions = {}
    self.populate_neighbors(sat,orb,positions, bounds=[min_sat,max_sat,min_orb,max_orb])
    return list(map(lambda x: x[1],sorted(positions.items(),key=lambda kv: kv[1]["chunk"])))


  def get_rotation_positions(self):
    min_orb, max_orb = self.get_min_max_orb()
    min_sat, max_sat = self.get_min_max_sat()
    sat = min_sat
    orb = min_orb
    positions = []
    for chunk in range(1, self.servers+1):
      positions.append({"sat": sat, "orb":orb, "chunk": chunk})
      sat += 1
      if sat > max_sat:
        sat = min_sat
        orb += 1
        if orb > max_orb:
          orb = 1
    return positions 

  def update_center(self):
    self.center_sat -= 1
    if self.center_sat < 1:
      self.center_sat = self.tot_sats

  def get_min_max_orb(self):
    center_orb = self.center[1]
    rows = math.ceil(math.sqrt(self.servers))
    min_orb = center_orb - int((rows - 1)/2)
    max_orb = center_orb + int((rows  -  1)/2)
    if min_orb < 1:
      min_orb = self.tot_orbs - abs(min_orb)
    if max_orb > self.tot_orbs:
      max_orb = 1 + (max_orb - self.tot_orbs)
    return min_orb, max_orb

  def get_min_max_sat(self):
    cols = math.ceil(math.sqrt(self.servers))
    max_sat = self.center_sat + int((cols  -  1)/2)
    min_sat = self.center_sat - int((cols  -  1)/2)
    if min_sat < 1:
      min_sat = self.tot_sats - abs(min_sat)
    if max_sat > self.tot_sats:
      max_sat = 1 + (max_sat - self.tot_sats)
    return min_sat, max_sat

  def rotate_once(self):
    old_min_sat, old_max_sat = self.get_min_max_sat()
    print(f"Before center {self.center_sat} min_sat {old_min_sat} max_sat {old_max_sat}")
    self.update_center()
    min_sat, max_sat = self.get_min_max_sat()
    print(f"After center {self.center_sat} min_sat {min_sat} max_sat {max_sat}")
    for pos in self.positions:
      if pos["sat"] == old_max_sat:
        pos["sat"] = min_sat

  def rotate(self,rotations):
    real_rotations = rotations % self.tot_sats
    for i in range(0,real_rotations):
      self.rotate_once()

  def get_chunk(self,chunk):
    chunk_pos = (chunk-1) % self.servers
    return self.positions[chunk_pos]

if __name__ == "__main__":
  pos = ChunkLocator((4,3))
  print(f"Before Rotation positions {pos.positions}")
  pos.rotate(20)
  print(f"After Rotation positions {pos.positions}")
  print(pos.get_chunk(12))

  print("Hop Layout")
  pos = ChunkLocator((4,3),strategy="hop")
  print(pos.positions)

  print("Hop Rotation Layout")
  pos = ChunkLocator((4,3),strategy="hop_rotation")
  print(pos.positions)

