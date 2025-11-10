# %%
from build123d import *
from ocp_vscode import *

# %%
top_l = 81
top_d = 8.1
mid_d = 6
bottom_l = 96
tip_d = 3.33
screw_d = 3
screw_l = 6

top_off = 7
bottom_off = 3.5

# %%
with BuildPart() as top:
  Cone(mid_d/2,top_d/2,top_l)

with BuildPart() as top_str:
  Cylinder(top_d/2,top_l)

with BuildPart() as bottom:
  Cone(tip_d/2,mid_d/2,bottom_l-tip_d/2)
  with Locations((0,0,-bottom_l/2+tip_d/4)):
    Sphere(tip_d/2)
  with Locations((0,0,bottom_l/2-tip_d/2)):
    Cylinder(screw_d/2,screw_l,align=(Align.CENTER,Align.CENTER,Align.MIN))

with BuildPart() as bottom_str:
  Cylinder(mid_d/2,bottom_l-tip_d/2)
  with Locations((0,0,bottom_l/2-tip_d/2)):
    Cylinder(screw_d/2,screw_l,align=(Align.CENTER,Align.CENTER,Align.MIN))

with BuildPart() as combo:
  with Locations(
    (0,top_off),
    Location((0,-top_off),(0,180,0))):
    add(top)
  with Locations(
    (bottom_off,0,-screw_l/3),
    Location((-bottom_off,0,screw_l/3),(0,180,0))):
    add(bottom)

with BuildPart() as combo_neg:
  with Locations((0,top_off)):
    add(top_str)
  with Locations(Location((0,-top_off,0),(0,180,0))):
    add(top)
  with Locations((bottom_off,0,-screw_l/3)):
    add(bottom_str)
  with Locations(Location((-bottom_off,0,screw_l/3),(0,180,0))):
    add(bottom)

with BuildPart() as tophalf:
  with BuildSketch():
    Ellipse(7,12)
  with BuildSketch(Pos(0,0,41)):
    Ellipse(7,12)
  with BuildSketch(Pos(0,0,45)):
    Ellipse(7,5)
  with BuildSketch(Pos(0,0,52)):
    Ellipse(6,3)
  loft(ruled=True)
  fillet(tophalf.edges().group_by(Axis.Z)[-1], radius=1.5)
  add(combo_neg,mode=Mode.SUBTRACT)

show(tophalf)

exporter = Mesher()
exporter.add_shape(tophalf.part)
exporter.write("chopstickholder.3mf")
# %%
