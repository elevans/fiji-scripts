#@ CommandService cmd
#@ UIService ui
#@ ImgPlus img

from de.csbdresden.stardist import StarDist2D

# run StarDist2D on the input img
res = cmd.run(StarDist2D, False,
              "input", img,
              "modelChoice", "Versatile (fluorescent nuclei)",
              ).get()

# get index/label image and show
label = res.getOutput("label")
ui.show(label)