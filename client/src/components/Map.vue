<template>
  <div class="maps" style="height: 590px; width: 100%">
    <div
      v-for="(ques, index) in selectedQuestions"
      :key="index"
      style="position: relative"
      :style="`height:590px;width:${100 / selectedQuestions.length}%`"
    >
      <l-map
        v-if="geojson"
        class="leaf-map"
        style="height: 590px"
        :zoom="zoom"
        :center="center"
      >
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-polygon
          v-for="(polygon, index) in geojson.features"
          :key="index"
          :lat-lngs="polygon.geometry.coordinates"
          :color="'blue'"
          :fillColor="polygon.properties.color"
          :weight="getWeight(polygon)"
          @click="selectRegion(polygon)"
          @mouseenter="showName(polygon.properties.name)"
          @mouseleave="showName('')"
        >
          <!-- <l-tooltip>{{ polygon.properties.name }}</l-tooltip> -->
        </l-polygon>
        <l-marker @click="showName('Тест')" :lat-lng="[60.504, 40]">
          <!-- <l-icon :lat-lng="[60.504, 40]"> 
          
          </l-icon> -->
            <apexchart
              type="pie"
              height="50px"
              width="50px"
              :options="chartOptions"
              :series="series"
            ></apexchart>
         </l-marker>
        <!-- <apexchart
        style="position:absolute;"
              type="pie"
              height="50px"
              width="50px"
              :options="chartOptions"
              :series="series"
            ></apexchart> -->
      </l-map>
      <span
        style="
          position: absolute;
          opacity: 0.8;
          z-index: 999;
          font-size: 15px;
          background-color: white;
          border: 1px #aaa solid;
          border-radius: 5px;
          padding: 3px 5px;
          color: #000;
          display: block;
          top: 5px;
          left: 50px;
        "
        >{{ ques }}</span
      >
    </div>
    <div
      v-if="panel.text"
      :style="'left: ' + panel.x + 'px; top: ' + panel.y + 'px'"
      style="
        opacity: 0.8;
        position: absolute;
        z-index: 999999;
        border: 1px #aaa solid;
        background-color: white;
        padding: 3px 5px;
        border-radius: 5px;
        box-shadow: 0.2em 0.2em 4px rgba(122, 122, 122, 0.5);
        font-size: 14px;
        color: #000;
      "
    >
      {{ panel.text }}
    </div>
    <!-- <apexchart
      type="pie"
      height="50px"
      width="50px"
      :options="chartOptions"
      :series="series"
      @click="showName('test')"
    ></apexchart> -->
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import VueApexCharts from "vue-apexcharts";
import { latLng, icon } from "leaflet";
import {
  LMap,
  LTileLayer,
  LMarker,
  LGeoJson,
  LPolygon,
  LControl,
  LTooltip,
  LLayerGroup,
  LIcon,
} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPolygon,
    LGeoJson,
    LControl,
    LTooltip,
    LLayerGroup,
    apexchart: VueApexCharts,
    LIcon,
  },
  props: ["geojson", "selectedReg", "selectedQuestions", "mapkey"],
  data() {
    return {
      series: [44, 55, 13, 43, 22],
      staticAnchor: [51.504, -0.159],
      chartOptions: {
        chart: {
          width: 50,
          type: "pie",
        },
        chart: {
          width: "100%",
          sparkline: {
            enabled: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        legend: {
          show: false,
        },
        tooltip: {
          enabled: true,
          x: {
            show: false,
          },
          y: {
            formatter: function (val) {
              return val + "K";
            },
          },
          style: {
            fontSize: "12px",
            fontFamily: undefined,
            color: "#fff",
          },
        },
      },
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 6,
      center: [59, 50],
      // markerLatLng: [51.504, -0.159]
      regname: null,
      latLng: null,
      region: this.selectedReg,
      color: "blue",
      panel: {
        text: "",
        x: -600,
        y: 0,
      },
    };
  },
  watch: {},
  computed: {},
  methods: {
    con(name){
      console.log(name);
    },
    showName(name) {
      if (window.timer) clearTimeout(window.timer);
      if (name == "") {
        this.panel.text = "";
      } else {
        window.timer = setTimeout(() => {
          this.panel.text = name;
        }, 300);
      }
    },
    selectRegion: function (polygon) {
      polygon.properties.selected = !polygon.properties.selected;
      this.$emit(
        "selectM",
        polygon.properties.name,
        polygon.properties.selected
      );
    },
    mouseIsMoving(e) {
      this.panel.x = e.pageX + 10;
      this.panel.y = e.pageY + 20;
    },
    getWeight(polygon) {
      if (polygon.properties.selected) return 3;
      return 1;
    },
  },
  created() {},
  mounted() {
    window.addEventListener("mousemove", this.mouseIsMoving);
  },
};
</script>
<style scoped>
.maps {
  display: flex;
}

.mega {
  z-index: 9999999;
}
</style>