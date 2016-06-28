#ucf-fusion-loader.
#Author-Harry Keen
#Description-Fusion360 addin to load and build ultimate CAD format json files.

import adsk.core, adsk.fusion, adsk.cam, traceback

#import system modules
import os, sys 

#get the path of add-in
ADDIN_PATH = os.path.dirname(os.path.realpath(__file__))
#print(ADDIN_PATH)

#add the path to the searchable path collection
if not ADDIN_PATH in sys.path:
  sys.path.append(ADDIN_PATH)

import json

def run(context):
  
  try:

  app = adsk.core.Application.get()
    ui = app.userInterface

    design = app.activeProduct

    #get the root component of the active design.
    rootComp = design.rootComponent


  except:
    if ui:
    #print('Failed:\n{}'.format(traceback.format_exc()))
      ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

