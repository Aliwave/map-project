<template>
  <div :key="mapkey" class="maps" style="height: 590px; width: 100%">
    <div style="height: 590px; width: 100%">
      <l-map
        v-if="geojson"
        class="leaf-map"
        style="height: 590px"
        :zoom="zoom"
        :center="center"
        ref="map"
        @ready="doOnReady()"
      >
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-polygon
          v-for="(polygon, index) in geojson.features"
          :key="index"
          :lat-lngs="polygon.geometry.coordinates"
          :color="'blue'"
          :fillColor="getColor(polygon)"
          :fillOpacity="0.6"
          :weight="getWeight(polygon)"
          @click="selectRegion(polygon)"
          @mouseenter="showName(polygon.properties.name)"
          @mouseleave="showName('')"
        >
        </l-polygon>
        <l-control
          v-if="data[this.question] !== undefined && this.customdatabool == false"
          position="bottomleft"
          ref="mapLegend"
          :disableScrollPropagation="true"
        >
          <div v-if="customdataLength == 0" class="legend">
            <!-- показать/скрыть легенду??? -->
            <h4>{{ question }}</h4>
            <div
              v-for="(value, index) in data[this.question]['Вся область']
                .labels"
              :key="index"
            >
              <i :style="`background: ${colors[index]}`"></i
              ><span>{{ value }}</span
              ><br />
            </div>
          </div>
        </l-control>
      </l-map>
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
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import VueApexCharts from "vue-apexcharts";
import { latLng, icon } from "leaflet";
import "leaflet.minichart";
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

  data() {
    return {
      chartLegend: null,
      series: [44, 55, 13, 43, 22],
      staticAnchor: [51.504, -0.159],
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
      position: {
        lat: 60.504,
        lng: 40,
      },
      map: null,
      coordsReg: {
        "ЗАТО Первомайский": [59.066419, 49.289217],
        "Свечинский район": [58.31021, 47.579042],
        "Кикнурский район": [57.34431, 47.010453],
        "Сунский район": [57.840365, 50.029674],
        "Опаринский район": [59.734253, 47.73285],
        "Подосиновский район": [60.216626, 47.252207],
        "Пижанский район": [57.419815, 48.471736],
        "Оричевский район": [58.329683, 48.930272],
        "Куменский район": [58.121419, 49.982991],
        "г. Котельнич": [58.302995, 48.319589],
        "Орловский район": [58.702629, 48.72439],
        "Даровской район": [59.068802, 47.686161],
        "Верхошижемский район": [57.984808, 49.092291],
        "Верхнекамский район": [59.899958, 52.679556],
        "Афанасьевский район": [58.852121, 53.402029],
        "г. Киров": [58.588299, 49.493535],
        "Юрьянский район": [59.023595, 48.922109],
        "Белохолуницкий район": [59.019354, 51.072924],
        "Котельничский район": [57.978983, 47.977148],
        "Арбажский район": [57.756938, 48.28354],
        "Тужинский район": [57.568888, 47.719134],
        "г. Вятские Поляны": [56.233142, 51.059474],
        "г. Кирово-Чепецк": [58.539774, 50.001871],
        "г. Слободской": [58.723668, 50.201684],
        "Советский район": [57.508447, 48.93577],
        "Омутнинский район": [58.729728, 52.218458],
        "Унинский район": [57.620405, 51.485407],
        "Богородский район": [57.809651, 50.776884],
        "Зуевский район": [58.372918, 51.023483],
        "Фаленский район": [58.061897, 51.572728],
        "Немский район": [57.548261, 50.40853],
        "Кильмезский район": [57.025784, 51.051089],
        "Лебяжский район": [57.313174, 49.422578],
        "Уржумский район": [57.010833, 49.94703],
        "Нолинский район": [57.599807, 49.724752],
        "Санчурский район": [56.941978, 47.268686],
        "Нагорский район": [59.619158, 50.762036],
        "Мурашинский район": [59.419933, 48.768273],
        "Лузский район": [60.757818, 47.875677],
        "Яранский район": [57.17497, 47.8949],
        "Малмыжский район": [56.556455, 50.694009],
        "Вятскополянский район": [56.182254, 51.25171],
        "Шабалинский район": [58.251727, 46.708323],
        "Слободской район": [58.908901, 50.064315],
        "Кирово-Чепецкий район": [58.362835, 50.309529],
      },
      charts: {},
      customdataLength: Object.keys(this.customdata).length,
      customdatabool: false,
    };
  },
  props: {
    geojson: Object,
    selectedReg: Array,
    selectedQuestions: Array,
    data: Object,
    mapkey: Number,
    question: String,
    colors: Array,
    customdata: Object,
  },
  watch: {},
  computed: {},
  methods: {
    // con(name) {
    //   console.log(name);
    // },
    getColor(polygon) {
      let regName = polygon.properties.name;
      if (this.data[this.question] == undefined) {
        return this.colors[0];
      }
      if (this.data[this.question][regName].labels[0] === "Нет данных") {
        return "black";
      }
      this.data[this.question][regName];
      let regionData = this.data[this.question][regName];
      let maxItemIndex = regionData.data.indexOf(
        Math.max.apply(null, regionData.data)
      );
      return this.colors[maxItemIndex];
    },
    getPopUpDiv(key, data, labels) {
      let str = '<p style="margin:0;">' + key + "</p>";
      if (data.length != 0) {
        for (let i = 0; i < data.length; i++) {
          let color = labels[0] != "Нет данных" ? this.colors[i] : "#ccc";
          str +=
            "<div>" +
            '<div style="display:inline-block;width: 10px;height:10px;margin-right: 5px;' +
            "background-color:" +
            color +
            '">' +
            '</div><span class="popup__label">' +
            data[i] +
            "</span></div>";
        }
      }
      return str;
    },
    getCustomTooltip(key, data, labels) {
      let str = '<p style="margin:0;">' + key + "</p>";
      for (let i = 0; i < data.length; i++) {
        let color = labels[0] != "Нет данных" ? this.colors[i] : "#ccc";
        str +=
          "<div>" +
          '<div style="display:inline-block;width: 10px;height:10px;margin-right: 5px;' +
          "background-color:" +
          this.colors[i] +
          '">' +
          '</div><span class="popup__label">' +
          labels[i] +
          " " +
          data[i] +
          "</span></div>";
      }
      return str;
    },

    doOnReady() {
      this.map = this.$refs.map.mapObject;
      for (const [key, value] of Object.entries(this.coordsReg)) {
        this.charts[key] = L.minichart(value, {
          type: "pie",
          data:
            this.data[this.question] != undefined
              ? this.data[this.question][key].data
              : [0],
          colors: this.colors, // this.data[this.question][key].labels[0]!="Нет данных" ? this.chartsColors : "rgba(255, 255, 255,0);",
          width:
            this.data[this.question][key].labels[0] != "Нет данных" ? 25 : 0,
          maxValues: [1000000],
        })
          .bindPopup(() => {
            if (this.data[this.question] !== undefined) {
              return this.getPopUpDiv(
                key,
                this.data[this.question][key].data,
                this.data[this.question][key].labels
              );
            } else {
              return "no data";
            }
          })
          .bindTooltip("<div>" + key + "</div>");
        this.map.addLayer(this.charts[key]);
      }
    },
    updateMap(oneQues) {
      for (const [key, value] of Object.entries(this.coordsReg)) {
        this.charts[key].setOptions({
          data:
            this.data[oneQues] != undefined
              ? this.data[oneQues][key].data
              : [0],
          colors:
            this.data[oneQues] != undefined
              ? this.data[oneQues][key].labels[0] != "Нет данных"
                ? this.colors
                : "red"
              : "black",
          width:
            this.data[oneQues] != undefined
              ? this.data[oneQues][key].labels[0] != "Нет данных"
                ? 25
                : 0
              : 0,
          labels: "none",
        });
        this.charts[key].setPopupContent(() => {
          if (this.data[oneQues] !== undefined) {
            return this.getPopUpDiv(
              key,
              this.data[oneQues][key].data,
              this.data[oneQues][key].labels
            );
          } else {
            return "no data";
          }
        });
        this.charts[key].setTooltipContent("<div>" + key + "</div>");
        this.$refs.map.mapObject.addLayer(this.charts[key]);
      }
      this.customdatabool = false;
    },
    updateMapOnCustomData(customData) {
      for (const [key, value] of Object.entries(this.coordsReg)) {
        if (key in customData) {
          this.charts[key].setOptions({
            data: customData[key],
            colors: "blue",
            width: 25,
            labels: "auto",
            labelStyle: "font-family:serif",
          });
          // this.charts[key].setPopupContent(
          //   this.getPopUpDiv(key, customData[key].data, customData[key].labels)
          // );
          // this.charts[key].setTooltipContent(
          //   this.getCustomTooltip(
          //     key,
          //     customData[key].data,
          //     customData[key].labels
          //   )
          // );
          this.charts[key].setPopupContent(this.getPopUpDiv(key, [], []));
        } else {
          this.charts[key].setOptions({
            width: 0,
          });
          this.charts[key].setPopupContent(this.getPopUpDiv(key, [], []));
        }
        // this.charts[key].setOptions({
        //   data: this.customdata[key],
        //   colors:
        //     this.data[oneQues][key].labels[0] != "Нет данных"
        //       ? this.colors
        //       : "red",
        //   width: this.data[oneQues][key].labels[0] != "Нет данных" ? 25 : 0,
        // });
        //this.charts[key].setTooltipContent(this.getPopUpDiv(key,this.data[oneQues][key].data));
        this.$refs.map.mapObject.addLayer(this.charts[key]);
      }
      this.customdatabool = true;
      // console.log(Object.keys(this.customdata).length);
      // if (Object.keys(this.customdata).length === 0) {
      //   console.log("emp[ty");
      // }
    },
    chartHide() {
      this.chartLegend = "";
    },
    chartShow(e) {
      if (window.timer) clearTimeout(window.timer);
      window.timer = setTimeout(() => {
        this.chartLegend =
          document.querySelector(".apexcharts-legend").innerHTML;
      }, 300);
      // console.log(e.target);
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
      this.panel.x = e.pageX;
      this.panel.y = e.pageY;
    },
    getWeight(polygon) {
      if (polygon.properties.selected) return 3;
      return 1;
    },
    getPieChartOptions(labels) {
      let piechartOpt = Object.assign({}, this.piechartOptions);
      piechartOpt.labels = labels;
      return piechartOpt;
    },
  },
  async created() {},
  mounted() {
    window.addEventListener("mousemove", this.mouseIsMoving);
    // console.log(this.$refs["leaflet-icon"]);
    // var chart = new ApexCharts(this.$refs["leaflet-icon"],this.piechartOptions);
    // chart.render();
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

.popup__color {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 5px;
}
/* .popup__label {

} */
p {
  padding: 0;
  margin: 0;
}

.legend {
  padding: 6px 8px;
  font: 12px Arial, Helvetica, sans-serif;
  background: white;
  background: rgba(255, 255, 255, 0.8);
  /*box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);*/
  /*border-radius: 5px;*/
  line-height: 20px;
  color: #555;
  max-height: 300px;
  max-width: 530px;
  overflow-y: scroll;
}
.legend h4 {
  text-align: center;
  font-size: 14px;
  margin: 2px 5px 2px;
  color: #777;
}

.legend span {
  position: relative;
  bottom: 3px;
}

.legend i {
  width: 18px;
  height: 18px;
  float: left;
  margin: 0 8px 0 0;
  opacity: 1;
}

.legend i.icon {
  background-size: 18px;
  background-color: rgba(255, 255, 255, 1);
}

text.leaflet-clickable.leaflet-interactive:after {
  content: "%";
}
</style>