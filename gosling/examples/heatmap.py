"""
Hi-C Heatmap
==============
"""
# category: basic marks
import gosling as gos
 
size = 500
data = gos.matrix("https://server.gosling-lang.org/api/v1/tileset_info/?d=hffc6-microc-hg38")
# data = gos.matrix('/path/to/dataset.cool') # local dataset
    
track = gos.Track(data).mark_bar().encode(
  x=gos.X("xs:G", axis="bottom"),
  xe="xe:G",
  y=gos.Y("ys:G", axis="left"),
  ye="ye:G",
  color=gos.Color("value:Q", range="warm", legend=True),
).properties(width=size, height=size)

track.view()
