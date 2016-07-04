# Fusion360 ucf exporter

# sketch_var is a fusion sketch object
# returnValue = sketch_var.saveAsDXF(fullFilename)

#ucf-fusion-loader.
#Author-Harry Keen
#Description-Fusion360 addin to export ultimate CAD format json files.

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

IMPORT = ADDIN_PATH + "/leg.json"
EXPORT = ADDIN_PATH + "/leg_export.json"
SKETCHES_LOC = ADDIN_PATH + "/sketches/"

def run(context):
  
  try:

    app = adsk.core.Application.get()
    ui = app.userInterface

    # Get import manager
    # importManager = app.importManager

    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    # Get the root component of the active design
    rootComp = design.rootComponent
    features = rootComp.features

    # Might have to set the "timeline" back to zero.

    # Set top level dict
    json_export = {'units': 'millimeters', 'sketches': {}, 'features': {}}

    feature_ind = 0
    combine_ind = 0
    sketch_ind = 0

    for extrude in features.extrudeFeatures:

      #   "feature_1": {
      #   "type": "extrude",
      #   "name": "extrude_1",
      #   "base_sketch": "LEG_OUTER_sketch",
      #   "distance": 18.0,
      #   "direction": [ 0.0, 0.0, 1.0]
      # },

      feature_ind += 1
      combine_ind += 1

      feature_key = 'feature_' + str(feature_ind)
      json_feature = {}

      json_feature['type'] = 'extrude'
      
      extrude.bodies.item(0).name = 'extrude_' + str(combine_ind)
      json_feature['name'] = 'extrude_' + str(combine_ind)
      
      profile = extrude.profile

      if type(profile) == adsk.core.ObjectCollection:
        sketch = profile.item(0).parentSketch
      else:
        sketch = profile.parentSketch
      
      json_feature['base_sketch'] = sketch.name

      json_feature['distance'] = 10 * extrude.extentDefinition.distance.value

      direction = sketch.referencePlane.geometry.normal.asArray()
      json_feature['direction'] = direction

      json_export['features'][feature_key] = json_feature


    for combine in features.combineFeatures:

        # "feature_5": {
        #   "type": "combine",
        #   "name": "combine_2",
        #   "solid_1": "extrude_1",
        #   "solid_2": "extrude_3",
        #   "union": false,
        #   "intersect": false,
        #   "cut": true
        # }

      feature_ind += 1
      combine_ind += 1

      feature_key = 'feature_' + str(feature_ind)
      json_feature = {}

      json_feature['type'] = 'combine'
      json_feature['name'] = 'combine_' + str(combine_ind)

      target_body = combine.targetBody
      json_feature['solid_1'] = target_body.name

      tool_bodies = combine.toolBodies
      # Get 'extrude_X' string of tool body - may need to do some regexing to get rid of end number
      json_feature['solid_2'] = tool_bodies.item(0).name

      # Set all operation types to false
      json_feature['union'] = False
      json_feature['intersect'] = False
      json_feature['cut'] = False

      # Get operation type
      if combine.operation == 0:
        json_feature[feature_key]['union'] = True
      elif combine.operation == 2:
        json_feature['intersect'] = True
      else:
        json_feature['cut'] = True

      json_export['features'][feature_key] = json_feature

    for sketch in rootComp.sketches:

      #   "sketch_1": {
      #   "name": "LEG_12_POCKETS_sketch",
      #   "location": "/sketches/sketch_1"
      # },

      sketch_ind += 1

      sketch_key = 'sketch_' + str(sketch_ind)
      json_sketch = {}

      json_sketch['name'] = sketch.name

      json_sketch['location'] = 'sketches/' + sketch.name

      # add sketch to json_export

      json_export['sketches'][sketch_key] = json_sketch

      # Actually save out the skecth profile as a dxf.
      sketch.saveAsDXF(SKETCHES_LOC + sketch.name + '.dxf')


    print(json.dumps(json_export, sort_keys=True, indent=2 * ' '))

    with open(EXPORT, 'w') as outfile:
      # data = json.dumps(json_export, sort_keys=True, indent=2 * ' ')
      json.dump(json_export, outfile, indent=2 * ' ')


  except:
    if ui:
      print('Failed:\n{}'.format(traceback.format_exc()))
      #ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


