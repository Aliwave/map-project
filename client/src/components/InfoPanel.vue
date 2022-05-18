<template>
  <div :mapkey="mapkey" v-if="data !== undefined" class="info-container">
    <div class="info-header">
      <h2>Статистика:</h2>
    </div> 
    <div v-if="data !== null" class="info-lists-wrapper">
      <!-- Выбор одного вопроса и одного района или Выбор одного вопроса и всей области -->
      <!-- <div v-if="data.length == 1 && data[0].regions.length == 1" class="info-list-block"> 
        <div id="chart">
          <p>{{data[0].question}}</p>
          <apexchart type="pie" width="1200px" height="240px"
          :options="getPieChartOptions(data[0].regions[0].labels)" 
          :series="data[0].regions[0].data"></apexchart>
        </div>
      </div> -->

      <!-- Выбор одного вопроса и одного района или Выбор одного вопроса и всей области -->
      <div v-if="selectedQues.length == 1 && selectedReg.length == 1 && data !== undefined" class="info-list-block"> 
        <div v-if="data[selectedQues[0]] !== null" id="chart">
          <p>{{selectedQues[0]}} (<span class="toMap__link" @click="oneQuestionChange(selectedQues[0])">на карту</span>)</p>
          <apexchart v-if="data[selectedQues[0]] != undefined" type="pie" width="1200px" height="240px"
          :options="getPieChartOptions(data[selectedQues[0]][selectedReg[0].region].labels)" 
          :series="data[selectedQues[0]][selectedReg[0].region].data"></apexchart>
        </div>
        <div v-else>Загрузка...</div>
      </div>

      <!-- Выбор нескольких вопросов и одного района или Выбор нескольких вопросов и всей области -->
      <div v-if="selectedQues.length > 1 && selectedReg.length == 1 && data !== undefined" class="info-list-block"> 
        <div v-for="(elem,index) in selectedQues" :key="index" id="chart">
          <p v-if="data[elem] !== undefined">{{elem}} (<a class="toMap__link" @click="oneQuestionChange(elem)">на карту</a>)</p>
          <p v-else>Загрузка...</p>
          <apexchart v-if="data[elem] !== undefined" type="pie" :width="`${1200}px`" height="290px" 
          :options="getPieChartOptions(data[elem][selectedReg[0].region].labels)" 
          :series="data[elem][selectedReg[0].region].data"></apexchart>
        </div>
      </div>
      <!-- Выбор одного вопроса и нескольких районов или Выбор нескольких вопросов и нескольких районов -->
      <div v-if="selectedReg.length > 1 && selectedQues.length >= 1" class="info-list-block multi-ques-block">
        <div v-for="(quesItem,index) in selectedQues" :key="index" class="info-list-block reg-list-block">
          <p v-if="data[quesItem] !== undefined">{{quesItem}} (<a class="toMap__link" @click="oneQuestionChange(quesItem)">на карту</a>)</p>
          <p v-else>Загрузка...</p>
          <ul v-if="data[quesItem] !== undefined" class="info-list">
            <li v-for="(regItem,index) in selectedReg" :key="index">
              {{regItem.region}}
              <span class="mini-bar"
                ><apexchart
                  type="bar"
                  height="15px"
                  width="100%"
                  :options="chartOptions"
                  :series="getBarSeries(
                    data[quesItem][regItem.region].labels,data[quesItem][regItem.region].data
                  )"
                ></apexchart
              ></span>
            </li>
          </ul>
        </div>
      </div>
      <!-- Выбор одного вопроса и нескольких районов или Выбор нескольких вопросов и нескольких районов -->
      <!-- <div v-if="selectedReg.length > 1 && selectedQues.length >= 1" class="info-list-block multi-ques-block">
        <div v-for="(quesItem,index) in data" :key="index" class="info-list-block reg-list-block">
          <p>{{quesItem.question}}</p>
          <ul class="info-list">
            <li v-for="(regItem,index) in quesItem.regions" :key="index">
              {{regItem.name}}
              <span class="mini-bar"
                ><apexchart
                  type="bar"
                  height="15px"
                  width="100%"
                  :options="chartOptions"
                  :series="getBarSeries(regItem.labels,regItem.data)"
                ></apexchart
              ></span>
            </li>
          </ul>
        </div>
      </div> -->
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
        dataLabels: {
          enabled: true,
          formatter: function(val,opts){
            if(val < 2){
              return "";
            }
            return val.toFixed(1)+"%";
          }
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
          colors: [
            "#86007e",
            "#588539",
            "#cc9915",
            "#523690",
            "#c44112",
            "#aa2048",
            "#80419c",
            "#9e92fa",
            "#89204e",
            "#e80a2c",
            "#c4d9a8",
            "#4f8897",
            "#ff9a7e",
            "#d5a916",
            "#e56b74",
            "#3293c6",
            "#83e690",
            "#bc8d9d",
            "#8fa807",
            "#4d84b6",
            "#5d4319",
            "#2a6e3e",
            "#549466",
            "#4d9eb3",
            "#18b47a",
            "#73b223",
            "#73705b",
            "#f2c19b",
            "#1b4e7b",
            "#9dae6b",
            "#85dbc3",
            "#42a4d8",
            "#945d01",
            "#de9bfe",
            "#f5dd30",
            "#ce5b9b",
            "#ff0dc0",
            "#3fdb89",
            "#682d44",
            "#898e7a",
            "#6d4fd",
            "#487e54",
            "#fc05d3",
            "#2d2e1c",
            "#39371c",
            "#4ed56f",
            "#935b96",
            "#1112e4",
            "#d68b26",
            "#282f2b",
          ],
          opacity: 1,
        },
      },
      piechartOptions: {
        colors: [
          "#86007e",
          "#588539",
          "#cc9915",
          "#523690",
          "#c44112",
          "#aa2048",
          "#80419c",
          "#9e92fa",
          "#89204e",
          "#e80a2c",
          "#c4d9a8",
          "#4f8897",
          "#ff9a7e",
          "#d5a916",
          "#e56b74",
          "#3293c6",
          "#83e690",
          "#bc8d9d",
          "#8fa807",
          "#4d84b6",
          "#5d4319",
          "#2a6e3e",
          "#549466",
          "#4d9eb3",
          "#18b47a",
          "#73b223",
          "#73705b",
          "#f2c19b",
          "#1b4e7b",
          "#9dae6b",
          "#85dbc3",
          "#42a4d8",
          "#945d01",
          "#de9bfe",
          "#f5dd30",
          "#ce5b9b",
          "#ff0dc0",
          "#3fdb89",
          "#682d44",
          "#898e7a",
          "#6d4fd",
          "#487e54",
          "#fc05d3",
          "#2d2e1c",
          "#39371c",
          "#4ed56f",
          "#935b96",
          "#1112e4",
          "#d68b26",
          "#282f2b",
        ],
        chart: {
          width: "100%",
          // type: "pie",
          background: "#282b38",
          offsetX: -50,
        },
        // responsive: [{
        //   breakpoint: 480,
        //   options: {
        //     chart: {
        //       width: 200
        //     },
        //     legend: {
        //       position: 'bottom'
        //     }
        //   }
        // }],
        theme: {
          mode: "dark",
        },
        labels: [""],
        tooltip: {
          enabled: true,
          fillSeriesColor: true,
        },
        legend: {
          show: true,
          // position: 'bottom'
        },
        dataLabels: {
          enabled: true,
          // enabled: false,
        },
        stroke: {
          show: true,
          width: 0,
        },
      },
    };
  },
  props: ["queslist", "regions", "selectedReg", "selectedQues","data","mapkey"],
  methods: {
    getPieChartOptions(labels){
      let piechartOpt = Object.assign({}, this.piechartOptions);;
      piechartOpt.labels = labels;
      if(labels[0]=="Нет данных"){
        piechartOpt.colors = ['#ccc'];
      }
      return piechartOpt;
    },
    getBarSeries(labels,series){
      let temp = [];
      for(let i=0;i<labels.length;i++){
        let tempItem = {};
        tempItem['name'] = labels[i];
        tempItem['data'] = [series[i]];
        temp.push(tempItem);
      }
      return temp;
    },
    oneQuestionChange(oneQues){
      this.$emit("oneQuesChange",oneQues);
    },
    // getreg() {
    //   console.log(this.selectedReg);
    // },
  },
  created() {
    //this.getMessage();
  },
  mounted() {
  },
};
</script>
<style>
p{
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
  /* grid-template-rows: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr; */
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
  cursor:pointer;
  color: #ffc0cb;
}
.toMap__link:hover {
  color: #d6a3ab;
}
.toMap__link:active {
  color: #b8989d;
}
</style>