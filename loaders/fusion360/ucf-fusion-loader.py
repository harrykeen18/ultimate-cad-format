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

IMPORT = ADDIN_PATH + "/leg_export.json"
SKETCHES_LOC = ADDIN_PATH + "/sketches/"

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
        # extInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.JoinFeatureOperation)

        # Define distance of extrude
        distance = adsk.core.ValueInput.createByReal(feature['distance'])
        # Set the distance extent to be symmetric
        extInput.setDistanceExtent(False, distance)

        # Set the extrude to be a solid
        # extInput.isSolid = True

        # Set direction
        extInput.setAllExtent = 1

        # Create the extrusion
        ext = extrudes.add(extInput)

        # Rename sketch
        for body in rootComp.bRepBodies:
          if 'extrude' not in body.name:
            body.name = feature['name']

    # Apply combines
    for feature in data['features']:
      feature = data['features'][feature]

      if feature['type'] == 'combine':

        # Define target_body
        for body in rootComp.bRepBodies:
          if body.name == feature['solid_1']:
            target_body = body

        # Get tool_bodies
        # Create an object collection to use an input.
        tool_bodies = adsk.core.ObjectCollection.create()
        
        # Add all of the tool_bodies to the collection.
        for body in rootComp.bRepBodies:
          # if body.name == feature['solid_2']:
          if feature['solid_2'] in body.name:
            tool_bodies.add(body)

        # Create combine input
        combines = rootComp.features.combineFeatures
        combInput = combines.createInput(target_body, tool_bodies)

        # Keep tool bodies
        combInput.isKeepToolBodies = False

        # Cut operation
        combInput.operation = 1

        # Create the extrusion
        comb = combines.add(combInput)

        # Was going to rename but actually target body may have other combine features applied to it.
        # for body in rootComp.bRepBodies:
        #   if body.name == target_body.name:
        #     body.name = feature['name'] 

    # 28160 mm / 1108mm = 25.4 -> need to scale down to mm

  except:
    if ui:
      print('Failed:\n{}'.format(traceback.format_exc()))
      #ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

