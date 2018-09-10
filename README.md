[![CircleCI](https://circleci.com/gh/cmedinaarmas/srtmlib/tree/master.svg?style=svg)](https://circleci.com/gh/cmedinaarmas/srtmlib/tree/master)
# SRTM Lib
SRTM Lib is a tool to decode data generated from NASA's Shuttle Radar Topography Mission [SRTM](https://www2.jpl.nasa.gov/srtm/).
## Tile class
The Tile class decodes data from a single file and represents heights contained in a 1 degree tile (~ 111 km depending on latitude). Results for `n27_e085_1arc_v3.bil`, a 1-arc-second accuracy (30 meters) file, rendered in two formats are presented below: Height and Wrapped height.
<p align="center">
  <img src="docs/block.png">
</p>

## Mosaic class

The Mosaic class joins multiple tiles into a single array. Missing tiles are treated as void spaces. :construction:
