<template>
  <div class="info-container">
    <div class="info-header">
      <!-- <h2>Статистика по районам:</h2> -->
    </div>
    <div class="info-lists-wrapper">
      <!-- Выбор одного вопроса и одного района или Выбор одного вопроса и всей области -->
      <!-- <div class="info-list-block"> 
        <div id="chart">
          <apexchart type="pie" width="1200px" height="240px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
      </div> -->
      <!-- Выбор нескольких вопросов и одного района или Выбор нескольких вопросов и всей области -->
      <!-- <div class="info-list-block multi-ques-block"> 
        <div id="chart">
          <p>Если причиной невозможности иметь детей являются (станет) «отсутствие партнера» или «проблемы со здоровьем», готовы ли Вы обратиться за медицинской помощью и сделать ЭКО (искусственное оплодотворение)?</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
        <div id="chart1">
          <p>Вопрос 1</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
        <div id="chart2">
          <p>Вопрос 1</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
        <div id="chart3">
          <p>Вопрос 1</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
      </div> -->

      <div class="info-list-block multi-ques-block"> 
        <div class="chart" id="chart">
          <p>Если причиной невозможности иметь детей являются (станет) «отсутствие партнера» или «проблемы со здоровьем», готовы ли Вы обратиться за медицинской помощью и сделать ЭКО (искусственное оплодотворение)?</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
        <div id="chart1">
          <p>Вопрос 1</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
        <div id="chart2">
          <p>Вопрос 1</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
        </div>
        <div id="chart3">
          <p>Вопрос 1</p>
          <apexchart type="pie" :width="`${1200}px`" height="290px" :options="piechartOptions" :series="pieseries"></apexchart>
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
      series: [
        {
          name: "Marine",
          data: [15],
        },
        {
          name: "Striking",
          data: [5],
        },
        {
          name: "Strikin",
          data: [8],
        },
        {
          name: "Striki",
          data: [9],
        },
        // {
        //   name: "Strik Calf",
        //   data: [30],
        // },
        // {
        //   name: "Strilf",
        //   data: [7],
        // },
        // {
        //   name: "Stralf",
        //   data: [23],
        // },
        // {
        //   name: "Stlf",
        //   data: [22],
        // },
        // {
        //   name: "alf",
        //   data: [21],
        // },
        // {
        //   name: "Sf",
        //   data: [20],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
        // {
        //   name: "S",
        //   data: [17],
        // },
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

      pieseries: [1428,430,905,51,154,196,1373,423,502,557,207,782,133,143,132,275,99,188,45,28,150,863,519,289,101,511,128],
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
          width: '100%',
          type: 'pie',
          background: '#282b38',
          offsetX: -50,
        },
        labels: [
          'Уже есть столько детей, сколько хотелось бы',
          'Отсутствие тех, кто будет регулярно помогать и сидеть с ребенком',
          'Нет соответствующих жилищных условий',
          'Возможные трудности при обучении. Я - студентка',
          'Желание построить карьеру',
          'Отсутствие постоянной работы',
          'Низкая заработная плата',
          'Иметь детей (больше детей) не позволяет здоровье',
          'Дети являются финансовой нагрузкой для всей семьи',
          'Отсутствие нормальной медицины в регионе',
          'Нет партнера для рождения детей',
          'По причине большой обеспокоенности за будущее детей',
          'Ваш муж (партнер) больше не хочет иметь детей',
          'Вы не сможете достаточно заботиться и уделять внимание своим старшим детям',
          'Детей трудно воспитывать и контролировать',
          'Отсутствие качественного школьного образования в регионе',
          'Трудно хорошо заботиться о семье и заниматься домашним хозяйством',
          'По причине страха беременности и родов',
          'Невозможно проводить много времени с мужем, когда есть дети',
          'Ребенок доставляет много хлопот',
          'С детьми не настолько свободен, чтобы делать, что хочешь',
          'Недостаточная материальная поддержка государством семей с детьми',
          'Трудность (невозможность) устроить детей в детское дошкольное учреждение с 1,5 лет',
          'Трудность (невозможность) устроить детей в детское дошкольное учреждение с 3-х лет',
          'Желание «пожить для себя» или вообще отказ от рождения детей',
          'Ничего не помешает, планируем иметь (еще) детей',
          'Другое',

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
        theme:{
          mode: 'dark',
        },
        tooltip:{
          enabled: true,
          fillSeriesColor: true,
        },
        legend: {
          show:true,
          // position: 'bottom'
        },
        dataLabels:{
          enabled:true,
          // enabled: false,
        },
        stroke: {
          show:true,
          width: 2
        }
      },
    };
  },
  props: ["queslist", "regions","selectedReg","selectedQues"],
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
  },
  created() {
    //this.getMessage();
  },
  mounted(){
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
  width: 180px;
  height: 15px;
  margin-left: 5px;
}
.apexcharts-tooltip {
  background: #f3f3f3;
  color: #000;
}

.multi-ques-block {
  /* display:flex; */
}

.multi-ques-block p {
  margin: 0;
  /* max-width: 400px; */
}
/* .multi-ques-block .chart {
  max-width: 450px;
} */
</style>