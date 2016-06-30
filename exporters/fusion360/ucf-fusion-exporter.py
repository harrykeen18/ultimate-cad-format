# Fusion360 ucf exporter

# sketch_var is a fusion sketch object
# returnValue = sketch_var.saveAsDXF(fullFilename)

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

IMPORT = "/Users/harry/Documents/github/ultimate-cad-format/loaders/fusion360/leg.json"
EXPORT = "/Users/harry/Documents/github/ultimate-cad-format/loaders/fusion360/leg_export.json"
DIR_LOC = "/Users/harry/Documents/github/ultimate-cad-format/loaders/fusion360/"
SKETCHES_LOC = DIR_LOC + "sketches/"

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

    # Set top level dict
    json_export = {'units': '', 'sketches': {}, 'features': {}}

    feature_ind = 0
    combine_ind = 0

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
      json_feature = {feature_key: {}}

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

    # print(json.dumps(json_export, sort_keys=True, indent=2 * ' '))

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
      json_feature = {feature_key: {}}

      json_feature['type'] = 'extrude'
      json_feature['name'] = 'extrude_' + str(combine_ind)

      name = extrude.profile.parentSketch.name


  except:
    if ui:
      print('Failed:\n{}'.format(traceback.format_exc()))
      #ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


