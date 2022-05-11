<template>
  <div class="info-container">
    <div class="info-header">
      <!-- <h2>Статистика по районам:</h2> -->
    </div>
    <div class="info-lists-wrapper">
      <!-- Выбор одного вопроса и одного района или Выбор одного вопроса и всей области -->
      <div v-if="selectedQues.length == 1 && selectedReg.length == 1" class="info-list-block"> 
        <div id="chart">
          <p>{{selectedQues[0]}}</p>
          <apexchart type="pie" width="1200px" height="240px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
      </div>

      <!-- Выбор нескольких вопросов и одного района или Выбор нескольких вопросов и всей области -->
      <div v-if="selectedQues.length > 1 && selectedReg.length == 1" class="info-list-block"> 
        <div v-for="(elem,index) in selectedQues" :key="index" id="chart">
          <p>{{elem}}</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
      </div>

      <!-- Выбор одного вопроса и нескольких районов или Выбор нескольких вопросов и нескольких районов -->
      <div v-if="selectedReg.length > 1 && selectedQues.length >= 1" class="info-list-block multi-ques-block">
        <div v-for="(elem,index) in selectedQues" :key="index" class="info-list-block reg-list-block">
          <p>{{elem}}</p>
          <ul class="info-list">
            <li v-for="(elem,index) in selectedReg" :key="index">
              {{elem.region}}
              <span class="mini-bar"
                ><apexchart
                  type="bar"
                  height="15px"
                  width="100%"
                  :options="chartOptions"
                  :series="series"
                ></apexchart
              ></span>
            </li>
          </ul>
        </div>
      </div>
      <!-- <div v-for="(elem,index) in selectedReg" @click="getreg()" :key="index">
        {{elem.region}}
      </div>
      <div v-for="(elem,index) in selectedQues" @click="getreg()" :key="index">
        {{elem}}
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
      series: [
        {
          name: "Уже есть столько детей, сколько хотелось бы",
          data: [1428],
        },
        {
          name: "Отсутствие тех, кто будет регулярно помогать и сидеть с ребенком",
          data: [430],
        },
        {
          name: "Нет соответствующих жилищных условий",
          data: [905],
        },
        {
          name: "Возможные трудности при обучении. Я - студентка",
          data: [51],
        },
        {
          name: "Желание построить карьеру",
          data: [154],
        },
        {
          name: "Отсутствие постоянной работы",
          data: [196],
        },
        {
          name: "Низкая заработная плата",
          data: [1373],
        },
        {
          name: "Иметь детей (больше детей) не позволяет здоровье",
          data: [423],
        },
        {
          name: "Дети являются финансовой нагрузкой для всей семьи",
          data: [502],
        },
        {
          name: "Отсутствие нормальной медицины в регионе",
          data: [557],
        },
        {
          name: "Нет партнера для рождения детей",
          data: [207],
        },
        {
          name: "По причине большой обеспокоенности за будущее детей",
          data: [782],
        },
        {
          name: "Ваш муж (партнер) больше не хочет иметь детей",
          data: [133],
        },
        {
          name: "Вы не сможете достаточно заботиться и уделять внимание своим старшим детям",
          data: [143],
        },
        {
          name: "Детей трудно воспитывать и контролировать",
          data: [132],
        },
        {
          name: "Отсутствие качественного школьного образования в регионе",
          data: [275],
        },
        {
          name: "Трудно хорошо заботиться о семье и заниматься домашним хозяйством",
          data: [99],
        },
        {
          name: "По причине страха беременности и родов",
          data: [188],
        },
        {
          name: "Невозможно проводить много времени с мужем, когда есть дети",
          data: [45],
        },
        {
          name: "Ребенок доставляет много хлопот",
          data: [28],
        },
        {
          name: "С детьми не настолько свободен, чтобы делать, что хочешь",
          data: [150],
        },
        {
          name: "Недостаточная материальная поддержка государством семей с детьми",
          data: [863],
        },
        {
          name: "Трудность (невозможность) устроить детей в детское дошкольное учреждение с 1,5 лет",
          data: [519],
        },
        {
          name: "Трудность (невозможность) устроить детей в детское дошкольное учреждение с 3-х лет",
          data: [289],
        },
        {
          name: "Желание «пожить для себя» или вообще отказ от рождения детей",
          data: [101],
        },
        {
          name: "Ничего не помешает, планируем иметь (еще) детей",
          data: [511],
        },
        {
          name: "Другое",
          data: [128],
        },
      ],
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
            console.log(opts);
            console.log(val);
            if(val < 2){
              return "";
            }
            return val.toFixed(0)+"%";
          }
        },
        plotOptions: {
          bar: {
            horizontal: true,
            barHeight: "100%",
          },
        },
        // stroke: {
        //   width: 1,
        //   colors: ["#fff"],
        // },
        // title: {
        //   text: '100% Stacked Bar'
        // },
        // xaxis: {
        //   show: false,
        //   labels: {
        //     show: false,
        //   },
        //   axisBorder: {
        //     show: false,
        //   },
        //   axisTicks: {
        //     show: false,
        //   },
        //   crosshairs: {
        //     show: false,
        //   },
        // },
        // grid: {
        //   show: false,
        //   padding: {
        //     top: 0,
        //     right: 0,
        //     bottom: 0,
        //     left: 0,
        //   },
        // },
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

      pieseries: [
        1428, 430, 905, 51, 154, 196, 1373, 423, 502, 557, 207, 782, 133, 143,
        132, 275, 99, 188, 45, 28, 150, 863, 519, 289, 101, 511, 128,
      ],
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
          type: "pie",
          background: "#282b38",
          offsetX: -50,
        },
        labels: [
          "Уже есть столько детей, сколько хотелось бы",
          "Отсутствие тех, кто будет регулярно помогать и сидеть с ребенком",
          "Нет соответствующих жилищных условий",
          "Возможные трудности при обучении. Я - студентка",
          "Желание построить карьеру",
          "Отсутствие постоянной работы",
          "Низкая заработная плата",
          "Иметь детей (больше детей) не позволяет здоровье",
          "Дети являются финансовой нагрузкой для всей семьи",
          "Отсутствие нормальной медицины в регионе",
          "Нет партнера для рождения детей",
          "По причине большой обеспокоенности за будущее детей",
          "Ваш муж (партнер) больше не хочет иметь детей",
          "Вы не сможете достаточно заботиться и уделять внимание своим старшим детям",
          "Детей трудно воспитывать и контролировать",
          "Отсутствие качественного школьного образования в регионе",
          "Трудно хорошо заботиться о семье и заниматься домашним хозяйством",
          "По причине страха беременности и родов",
          "Невозможно проводить много времени с мужем, когда есть дети",
          "Ребенок доставляет много хлопот",
          "С детьми не настолько свободен, чтобы делать, что хочешь",
          "Недостаточная материальная поддержка государством семей с детьми",
          "Трудность (невозможность) устроить детей в детское дошкольное учреждение с 1,5 лет",
          "Трудность (невозможность) устроить детей в детское дошкольное учреждение с 3-х лет",
          "Желание «пожить для себя» или вообще отказ от рождения детей",
          "Ничего не помешает, планируем иметь (еще) детей",
          "Другое",
        ],
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
          width: 2,
        },
      },
    };
  },
  props: ["queslist", "regions", "selectedReg", "selectedQues"],
  methods: {
    // getMessage() {
    //   const path = 'http://localhost:5000/ping';
    //   axios.get(path)
    //     .then((res) => {
    //       this.msg = res.data;
    //     })
    //     .catch((error) => {
    //       // eslint-выключение следующей строки
    //       console.log(error);
    //     });
    // },
    getreg() {
      console.log(this.selectedReg);
    },
  },
  created() {
    //this.getMessage();
  },
  mounted() {
    console.log(this.selectedReg);
    console.log(this.selectedQues);
  },
};
</script>
<style>
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
  padding-bottom: 5px;
}

.info-list {
  max-height: 400px;
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
</style>