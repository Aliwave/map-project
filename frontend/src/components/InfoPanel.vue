<template>
  <div :mapkey="mapkey" class="info-container">
    <div class="info-header">
      <h2>Статистика:</h2>
    </div>
    <div class="info-lists-wrapper">
      <div
        v-if="
          selectedQues.length >= 1 &&
          selectedReg.length == 1 &&
          data !== undefined
        "
        class="info-list-block"
      >
        <div v-for="(elem, index) in selectedQues" :key="index" id="chart">
          <p v-if="data[elem] !== undefined">
            {{ elem }} (<a class="toMap__link" @click="oneQuestionChange(elem)"
              >на карту</a
            >)
          </p>
          <apexchart
            v-if="data[elem] !== undefined"
            type="pie"
            :width="`${1200}px`"
            height="290px"
            :options="
              getPieChartOptions(data[elem][selectedReg[0].region].labels)
            "
            :series="data[elem][selectedReg[0].region].data"
          ></apexchart>
        </div>
      </div>
      <div
        v-if="selectedReg.length > 1 && selectedQues.length >= 1"
        class="info-list-block multi-ques-block"
      >
        <div
          v-for="(quesItem, index) in selectedQues"
          :key="index"
          class="info-list-block reg-list-block"
        >
          <p v-if="data[quesItem] !== undefined">
            {{ quesItem }} (<a
              class="toMap__link"
              @click="oneQuestionChange(quesItem)"
              >на карту</a
            >)
          </p>
          <ul v-if="data[quesItem] !== undefined" class="info-list">
            <li v-for="regItem in selectedReg" :key="regItem.id">
              {{ regItem.region }}
              <span class="mini-bar"
                ><apexchart
                  type="bar"
                  height="15px"
                  width="100%"
                  :options="chartOptions"
                  :series="
                    getBarSeries(
                      data[quesItem][regItem.region].labels,
                      data[quesItem][regItem.region].data
                    )
                  "
                ></apexchart
              ></span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from 'axios';
import VueApexCharts from "vue-apexcharts";
/* eslint-disable */
export default {
  name: "InfoPanel",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      chartOptions: {
        chart: {
          type: "bar",
          width: "100%",
          height: "100%",
          stacked: true,
          stackType: "100%",
          toolbar: {
            show: false,
          },
          sparkline: {
            enabled: true,
          },
          offsetX: 0,
          offsetY: 0,
        },
        theme: {
          mode: "dark",
        },
        legend:{
          width: '200px',
        },
        dataLabels: {
          enabled: true,
          formatter: function (val, opts) {
            if (val < 2) {
              return "";
            }
            return val.toFixed(1) + "%";
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
            barHeight: "100%",
          },
        },
        tooltip: {
          enabled: true,
          x: {
            show: false,
          },
          y: {
            formatter: function (val) {
              return val;
            },
          },
          style: {
            fontSize: "12px",
            fontFamily: undefined,
            color: "#fff",
          },
        },
        fill: {
          colors: this.colors,
          opacity: 1,
        },
        states: {
          active: {
            allowMultipleDataPointsSelection: false,
            filter:{
              type:"darken",
              value: 0.15,
            }
          },
          hover: {
            filter: {
              type: "none",
              value: 0.05,
            },
          },
        },
      },
      piechartOptions: {
        colors: this.colors,
        chart: {
          width: "1200px",
          type: "pie",
          background: "#282b38",
          offsetX: -50,
        },
        theme: {
          mode: "dark",
        },
        states: {
          active: {
            allowMultipleDataPointsSelection: false,
            filter:{
              type:"darken",
              value: 0.15,
            }
          },
          hover: {
            filter: {
              type: "none",
              value: 0.05,
            },
          },
        },
        labels: [""],
        tooltip: {
          enabled: true,
          fillSeriesColor: false,
        },
        legend: {
          show: true,
        },
        dataLabels: {
          enabled: true,
        },
        stroke: {
          show: true,
          width: 0,
        },
      },
    };
  },
    props: {
    queslist:Array,
    regions:Array,
    selectedReg:Array,
    selectedQues:Array,
    data:Object,
    mapkey:Number,
    colors:Array,
    },
  methods: {
    getPieChartOptions(labels) {
      let piechartOpt = Object.assign({}, this.piechartOptions);
      piechartOpt.labels = labels;
      if (labels[0] == "Нет данных") {
        piechartOpt.colors = ["#ccc"];
      }
      return piechartOpt;
    },
    getBarSeries(labels, series) {
      let temp = [];
      for (let i = 0; i < labels.length; i++) {
        let tempItem = {};
        tempItem["name"] = labels[i];
        tempItem["data"] = [series[i]];
        temp.push(tempItem);
      }
      return temp;
    },
    oneQuestionChange(oneQues) {
      this.$emit("oneQuesChange", oneQues);
    },
  },
  created() {
  },
  mounted() {},
};
</script>
<style>
p {
  margin: 0;
}
.info-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding-top: 5px;
}

.info-header span {
  padding-left: 10px;
}

.info-container h2 {
  margin: 0;
  padding: 0;
  padding-left: 12px;
  padding-bottom: 2px;
  line-height: 20px;
}

.info-list {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  column-gap: 15px;
  padding: 0;
}

.info-list li {
  padding-bottom: 5px;
  display: flex;
  justify-content: space-between;
  min-width: 250px;
  max-width: 370px;
}
.info-lists-wrapper {
  display: flex;
  justify-content: space-around;
  padding-bottom: auto;
}

.mini-bar {
  display: inline-block;
  background-color: transparent;
  width: 700px;
  height: 15px;
  margin-left: 5px;
}
.apexcharts-tooltip {
  background: #f3f3f3;
  color: #000;
}

.reg-list-block {
  border: 2px solid #13c6e9;
  border-radius: 11px;
  position: relative;
  padding: 15px 10px 10px 10px;
  margin: 10px 0;
  width: 100%;
}

.reg-list-block .info-list {
  width: 100%;
  grid-template-columns: 1fr 1fr;
}

.reg-list-block .info-list li {
  max-width: none;
}

.reg-list-block p {
  background-color: #282b38;
  position: absolute;
  top: -10px;
  left: 10px;
  padding: 0 5px;
}

.multi-ques-block {
  width: calc(100vw - 60px);
  margin-left: -20px;
}

.multi-ques-block p {
  margin: 0;
  /* max-width: 400px; */
}
/* .multi-ques-block .chart {
  max-width: 450px;
} */

.toMap__link {
  text-decoration: underline;
  cursor: pointer;
  color: #ffc0cb;
}
.toMap__link:hover {
  color: #d6a3ab;
}
.toMap__link:active {
  color: #b8989d;
}
</style>