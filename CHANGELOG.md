# Goblin Changelog

## v2.2.3

* Fixed bug when mapping an edge's properties introduced as a regression in newer gremlinpython versions.

## v2.2.2

* updated to use aiobremlin v3.3.4 in order to get the correct dependency tree.

## v2.2.1

* Fixed dependency requirement allowing Goblin to run on python v3.7+.

## v2.2.0

* Added Immutable meta-property
* Added optimistic locking on-creation.
* Fixed incorrect hashable id handling on Janusgraph.
* Updated to run on newer versions of gremlin-python, 3.4.3 is the latest compatible version.
