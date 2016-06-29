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

    # print(json.dumps(data, sort_keys=True, indent=4 * ' '))

    # for n in data.keys():
    #   print(n)

    # print('-------')

    # for feature in data['features'].keys():
    #   print(data['features'][feature]['type'])

    # Import all sketches
    for sketch in data['sketches']:
      sketch_name = data['sketches'][sketch]['name']
      
      # Get dxf2d import options
      sketch_loc = SKETCHES_LOC + sketch_name + '.dxf'#'sketch_2.dxf'
      # returnValue = importManager_var.createDXF2DImportOptions(filename, planarEntity)
      dxf2dOptions = importManager.createDXF2DImportOptions(sketch_loc, rootComp.xYConstructionPlane)
      
      # Import dxf file to root component
      importManager.importToTarget(dxf2dOptions, rootComp)

      # Rename sketch
      for sketch in rootComp.sketches:
        if 'sketch' not in sketch.name:
          sketch.name = sketch_name

    # Extrude all extrusion features
    for feature in data['features']:
      feature = data['features'][feature]

      if feature['type'] == 'extrude':
        
        # Run extrude
        # Get base_sketch
        for sketch in rootComp.sketches:

          if sketch.name == feature['base_sketch']:

            base_sketch = sketch
            break

        # Get profiles
        # Create an object collection to use an input.
        profiles = adsk.core.ObjectCollection.create()
        
        # Add all of the profiles to the collection.
        for prof in base_sketch.profiles:
          profiles.add(prof)

        # Define Fusion type of extrude
        # Currently only going to use new_bodies and then combines to get any subtraction

        # Create extrusion input
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    
        # Define distance of extrude
        distance = adsk.core.ValueInput.createByReal(feature['distance'] / 10)
        # Set the distance extent to be symmetric
        extInput.setDistanceExtent(True, distance)

        # Set the extrude to be a solid
        # extInput.isSolid = True

        # extent_def = adsk.fusion.ExtentDirections.PositiveExtentDirection

        # Set direction
        # extInput.setAllExtent(1)

        # Create the extrusion
        ext = extrudes.add(extInput)

  except:
    if ui:
      print('Failed:\n{}'.format(traceback.format_exc()))
      #ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

