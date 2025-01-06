import "./style.css";
import { Map, View } from "ol";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { useGeographic } from "ol/proj.js";

useGeographic();

const canada = [-106, 51];

/* create a new view, centered in Canada 
  ref: https://openlayers.org/en/latest/examples/geographic.html */
const map = new Map({
  target: "map",
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
  ],
  view: new View({
    center: canada,
    zoom: 4,
  }),
});
