# %%
from build123d import *
from ocp_vscode import *

# %%
width = 106
height = 56
depth = 10
corner_radius = 6
thickness = 0.8
lip = 1.6
intr = 1.6
inbr = 0.8

# %%

with BuildSketch(Plane.XY) as footprint:
  RectangleRounded(width, height, corner_radius)

cutouts = Part() + [
  # MicroSD card slot
  Pos(-35.25,-28,-1.8) * Rot(90,0,0) * extrude(
    offset(SlotOverall(12,1.5),0.5),amount=thickness,both=True),

  # USB-C port
  Pos(23.5,-28,1.2) * Rot(90,0,0) * extrude(
    offset(SlotOverall(8.4,2.6),0.5),amount=thickness,both=True),

  # Power switch
  Pos(53,-14.5,0.5) * Rot(0,90,0) * extrude(
    offset(RectangleRounded(3, 5, 0.2),2),amount=thickness,both=True),
] + [
  # Shoulder buttons
  pos * Rot(90,0,0) * extrude(
    offset(RectangleRounded(6, 4, 0.2),2),amount=thickness,both=True)
  for pos in [Pos(32.75,28,0.2), Pos(-33.25,28,0.2)]
]

inside = extrude(footprint.sketch, amount=depth/2+0.4, both=True)
inside = chamfer(inside.edges().group_by(Axis.Z)[-1], length=intr)
inside = fillet(inside.edges().group_by(Axis.Z)[0], radius=inbr)

with BuildPart() as case:
  extrude(footprint.sketch, amount=depth/2, both=True)
  offset(amount=thickness)
  add(inside,mode=Mode.SUBTRACT)
  extrude(offset(footprint.sketch, amount=-lip), amount=depth,mode=Mode.SUBTRACT)
  add(cutouts,mode=Mode.SUBTRACT)

# %%
show(case,reset_camera=Camera.KEEP)

exporter = Mesher()
exporter.add_shape(case.part)
exporter.write("trimui-model-s.3mf")
# %%
