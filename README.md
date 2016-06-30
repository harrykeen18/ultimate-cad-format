# Manifesto

![alt-text](https://imgs.xkcd.com/comics/standards.png)

## But seriously

Collaborative CAD design between remote designers such as those in the [Opendesk](www.opendesk.cc) network using different CAD systems is currenly very difficult. Proprietry formats inhibit intelligent model sharing and git versioning.

So we're all agreed, proprietry CAD formats suck. Transferring data from one system to another is based in the dark ages. The best current solution is to transfer models via dumb solid formats such as `.stp` or `.iges`. It's time we did something about it. The new ***Ultimate CAD Format*** will be:

* universal
* opensource
* `json` format (see /template.json or below)

Almost all CAD systems have api calls that run modelling commands. This format defines system that describes a "history tree" of modelling features and their base skecth geometry. This can be read by addins unique to each CAD system to construct an "inteligent" model of features from scratch.

This system relies on the development of individual:

* loaders - translator of json to proprietry format
* exporters - translator of proprietry format to json format

for each current CAD system.

The system will begin with basic modelling features such as extrudes, combines with simple `.dxf` base sketch geometry based on lines and arcs.

```
{
  "units": "millimeters",
  "sketches": {
    "sketch_1": {
      "name": "sketch_1",
      "location": "/sketches/sketch_1"
    },
    "sketch_2": {
      "name": "sketch_2",
      "location": "/sketches/sketch_2"
    }
  },
  "features": {
    "feature_1": {
      "type": "extrude",
      "name": "extrude_1",
      "distance": 10.0,
      "direction": [ 0.0, 0.0, 1.0]
    },
    "feature_2": {
      "type": "extrude",
      "name": "extrude_2",
      "distance": 10.0,
      "direction": [ 0.0, 1.0, 1.0]
    },
    "feature_3": {
      "type": "combine",
      "name": "combine_1",
      "solid_1": "extrude_1",
      "solid_2": "extrude_2",
      "union": true,
      "intersect": false,
      "cut": false
    },
    "feature_4": {
      "type": "combine",
      "name": "combine_2",
      "solid_1": "extrude_1",
      "solid_2": "extrude_2",
      "union": false,
      "intersect": true,
      "cut": false
    }
  }
}
```