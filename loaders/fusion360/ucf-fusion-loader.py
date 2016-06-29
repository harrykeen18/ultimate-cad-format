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

import simplejson as json

IMPORT = "/Users/harry/Documents/github/ultimate-cad-format/template.json"
DIR_LOC = "/Users/harry/Documents/github/ultimate-cad-format/loaders/fusion360/"
SKETCHES_LOC = DIR_LOC + "sketches/"

def run(context):
  
  try:

    app = adsk.core.Application.get()
    ui = app.userInterface

    # Get import manager
    importManager = app.importManager

    # Create a document.
    #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    # Get the root component of the active design
    rootComp = design.rootComponent

    with open(IMPORT) as data_file:    
      data = json.load(data_file)

    print(json.dumps(data, sort_keys=True, indent=4 * ' '))

    # for n in data.keys():
    #   print(n)

    # print('-------')

    # for feature in data['features'].keys():
    #   print(data['features'][feature]['type'])

    # Import all sketches

    for sketch in data['sketches']:
      print(data['sketches'][sketch]['name'])
      
      # Get dxf2d import options
      dxf2dFileName = SKETCHES_LOC + data['sketches'][sketch]['name'] + '.dxf'#'sketch_2.dxf'
      
      # returnValue = importManager_var.createDXF2DImportOptions(filename, planarEntity)
      dxf2dOptions = importManager.createDXF2DImportOptions(dxf2dFileName, rootComp.xYConstructionPlane)
      
      # Import dxf file to root component
      importManager.importToTarget(dxf2dOptions, rootComp)


    # # Create sketch
    # sketches = rootComp.sketches
    # sketch = sketches.add(rootComp.xZConstructionPlane)
    # sketchCircles = sketch.sketchCurves.sketchCircles
    # centerPoint = adsk.core.Point3D.create(0, 0, 0)
    # circle = sketchCircles.addByCenterRadius(centerPoint, 5.0)
    
    # # Get the profile defined by the circle
    # prof = sketch.profiles.item(0)

    # # Create an extrusion input
    # extrudes = rootComp.features.extrudeFeatures
    # extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    
    # # Define that the extent is a distance extent of 5 cm
    # distance = adsk.core.ValueInput.createByReal(5)
    # # Set the distance extent to be symmetric
    # extInput.setDistanceExtent(True, distance)
    # # Set the extrude to be a surface one
    # extInput.isSolid = False

    # # Create the extrusion
    # ext = extrudes.add(extInput)
    
    # # Get the body created by the extrusion
    # body = ext.bodies.item(0)
    
    # # Create another sketch
    # sketchVertical = sketches.add(rootComp.yZConstructionPlane)
    # sketchCirclesVertical = sketchVertical.sketchCurves.sketchCircles
    # centerPointVertical = adsk.core.Point3D.create(0, 1, 0)
    # cicleVertical = sketchCirclesVertical.addByCenterRadius(centerPointVertical, 0.5)
    
    # # Get the profile defined by the vertical circle
    # profVertical = sketchVertical.profiles.item(0)
    
    # # Create an extrusion input
    # extInput1 = extrudes.createInput(profVertical, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    
    # # Define that the extent is one side to
    # # Leave the direction determined automatically
    # extInput1.setOneSideToExtent(body, False)
    # # Define the taper angle of 4 degree
    # extInput1.taperAngle = adsk.core.ValueInput.createByString('4 deg')
    
    # # Create the extrusion
    # ext1 = extrudes.add(extInput1)


  except:
    if ui:
    #print('Failed:\n{}'.format(traceback.format_exc()))
      ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

