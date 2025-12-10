# %%
from build123d import *
from ocp_vscode import *

# %%
width = 106
height = 56
depth = 10
corner_radius = 6
thickness = 0.8
lip = 1
inr = 0.8

# %%

with BuildSketch(Plane.XY) as footprint:
  RectangleRounded(width, height, corner_radius)

cutouts = Part() + [
  # MicroSD card slot
  Pos(-35,-28,-1.5) * Rot(90,0,0) * extrude(
    offset(SlotOverall(12,1.5),0.5),amount=thickness,both=True),

  # USB-C port
  Pos(23,-28,1.5) * Rot(90,0,0) * extrude(
    offset(SlotOverall(8.4,2.6),0.5),amount=thickness,both=True),

  # Power switch
  Pos(53,-15,0.5) * Rot(0,90,0) * extrude(
    offset(RectangleRounded(3, 5, 0.2),0.5),amount=thickness,both=True),
] + [
  # Shoulder buttons
  pos * Rot(90,0,0) * extrude(
    offset(RectangleRounded(6, 4, 0.2),0.5),amount=thickness,both=True)
  for pos in [Pos(33,28,0.5), Pos(-33,28,0.5)]
]

with BuildPart() as case:
  extrude(footprint.sketch, amount=depth/2, both=True)
  offset(amount=thickness)
  offset(extrude(offset(footprint.sketch, amount=-inr), amount=(depth-inr)/2, both=True),amount=inr, mode=Mode.SUBTRACT)
  extrude(offset(footprint.sketch, amount=-lip), amount=depth,mode=Mode.SUBTRACT)
  add(cutouts,mode=Mode.SUBTRACT)

# %%
show(case,reset_camera=Camera.KEEP)

exporter = Mesher()
exporter.add_shape(case.part)
exporter.write("trimui-model-s.3mf")
# %%
