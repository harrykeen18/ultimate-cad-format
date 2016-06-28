# Manifesto

Proprietry CAD formats suck. Transferring data from one system to another is based in the dark ages. The best current solution is to transfer models via dumb solid formats such as `.stp` or `.iges`. It's time we did something about it. This format will be:

* universal
* opensource
* `json` format

Almost all CAD systems have api calls that run modelling commands. This format defines system that describes a "history tree" of modelling features and their base skecth geometry. This can be read by addins unique to each CAD system to construct an "inteligent" model of features from scratch.

This system relies on the development of individual:

* loaders - translator of json to proprietry format
* exporters - translator of proprietry format to json format

for each current CAD system.

The system will begin with basic modelling features such as extrudes, combines with simple base sketch geometry based on lines and arcs.
