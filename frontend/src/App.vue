<template>
  <div id="app">
    <transition name="fade">
      <Preloader v-if="preloader"></Preloader>
    </transition>
    <div class="menu-container">
      <!-- <button @click="showMain()" class="toggleSidebar">Вопросы</button> -->
      <button @click="showQuesList = !showQuesList" class="toggleSidebar">
        Вопросы
      </button>
      <div>
        <label
          >Выберите файл с данными опроса(формат xlsx):
          <input
            class="mainupload-btn"
            type="file"
            ref="file"
            name="file"
            id="file"
            accept=".xlsx"
          />
          <button @click="submitFile()">Отправить</button>
        </label>
      </div>
      <button @click="showRegionList = !showRegionList" class="toggleSidebar">
        Районы
      </button>
    </div>
    <div class="map-container">
      <transition name="fade">
        <Questions
          v-if="showQuesList"
          :queslist="queslist"
          @selectQ="selectQues"
          :data="mainData"
          :queskey="queskey"  
          @selectCriteria="selectCriteria"
          :criteriaData="criteriaData"
          @customOnMap="customOnMap"
        ></Questions>
      </transition>

      <Map
        :geojson="geodata"
        :selectedReg="selectedRegions"
        @selectM="selectionRegionList"
        :selectedQuestions="selectedQuestions"
        :data="mainData"
        :question="oneQuestion"
        ref="mapComp"
        :colors="chartColors"
        :customdata="customData"
      ></Map>
      <transition name="fade">
        <Regions
          v-if="showRegionList"
          :regions="regdata"
          @selectR="selectionRegionList"
        ></Regions>
      </transition>
    </div>
    <InfoPanel
      :queslist="queslist"
      :selectedReg="selectedRegions"
      :selectedQues="selectedQuestions"
      :regions="regdata"
      :data="mainData"
      @oneQuesChange="oneQuestionChangeMain"
      :colors="chartColors"
      :mapkey="mapkey"
      :chartkey="chartkey"
      ref="infopanel"
    ></InfoPanel>
    <div></div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import Map from "./components/Map"
import Questions from "./components/Questions";
import Regions from "./components/Regions";
import InfoPanel from "./components/InfoPanel";
import Preloader from "./components/Preloader";

export default {
  components: { Map, Regions, Questions, InfoPanel, Preloader },
  name: "App",
  data() {
    return {
      geodata: null,
      regdata: null,
      queslist: null,
      selectedRegions: [],
      selectedQuestions: [],
      oneQuestion: "",
      file: "",
      preloader: true,
      mapkey: 0,
      showQuesList: true,
      showRegionList: true,
      mainData: {},
      chartColors: [
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
      customData: {},
      criteriaData:{},
      chartkey: 0,
      queskey: 0,
      customOnMapBool: false
    };
  },
  methods: {
    customOnMap(){
      this.$refs.mapComp.updateMapOnCustomData(this.customData);
    },
    selectCriteria(element,label){
      if(this.criteriaData[element] === undefined){
        this.criteriaData[element] = [];
        this.criteriaData[element].push(label);
      }else{
        if(this.criteriaData[element].indexOf(label) === -1){
          this.criteriaData[element].push(label);
        }else{
          this.criteriaData[element].splice(
            this.criteriaData[element].indexOf(label),
            1
          );
        }
        if(this.criteriaData[element].length === 0){
          delete this.criteriaData[element];
        }
      }
      this.getCritData(this.criteriaData);
      this.customOnMapBool = true;
    },
    async submitFile() {
      this.preloader = true;
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append("file", this.file);
      await axios
        .post(process.env.SERVER_URL + "/api/uploaddb", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          let queslist = [];
          this.selectedQuestions = [];
          res.data.queslist.forEach((question, index) => {
            if (index == 0) {
              this.oneQuestion = question;
              queslist.push({ id: index, question: question, selected: true });
              this.selectedQuestions.push(question);
              return;
            }
            queslist.push({ id: index, question: question, selected: false });
          });
          this.queslist = queslist;
          this.mainData = {};
          this.customData = {};
          this.criteriaData = {};
        })
        .catch((error) => {
          // eslint-disable
          console.log(error);
        });
        await this.getData(this.regdata, this.selectedQuestions); 
        this.$refs.mapComp.updateMap(this.oneQuestion);
        this.preloader =false;
        this.mapkey++;
    },

    async getData(Region, Question) {
      const path = process.env.SERVER_URL + "/api/data";
      const data = { selectedQuestions: Question, selectedRegions: Region };
      await axios
        .post(path, data)
        .then((response) => {
          this.mainData[
            this.selectedQuestions[this.selectedQuestions.length - 1]
          ] = response.data;
          this.mapkey++;
          this.queskey++;
        })
        .catch((error) => console.log(error));
    },
    async getCritData(CritData){
      const path = process.env.SERVER_URL + "/api/dataCrit";
      const data = { selectedQuestions: CritData, selectedRegions: this.regdata };
      await axios
        .post(path, data)
        .then((response) => {
          this.customData = response.data;
          if(this.customOnMapBool == true){
            this.$refs.mapComp.updateMapOnCustomData(this.customData);
          }
        })
        .catch((error) => console.log(error));
    },
    async selectQues(element, selected) {
      if (selected == true) {
        this.selectedQuestions.push(element);
        //this.mapkey++;
      } else {
        this.selectedQuestions.splice(
          this.selectedQuestions.indexOf(element),
          1
        );
        delete this.criteriaData[element];
        this.getCritData(this.criteriaData);
      //   if (this.selectedRegions[0] == "Вся область") {
      //     //this.customData[region].data.splice(this.customData[region].labels.indexOf(queslabel),1);
      //     this.customData.forEach(function (value) {});
      //   } else {
      //   }
      //   //console.log(this.mainData[element]);
      //   //this.mapkey--;
      }
      if (this.mainData[element] === undefined) {
        this.preloader = true;
        await this.getData(this.regdata, this.selectedQuestions);
        this.preloader = false;
      }
    },

    selectionRegionList(element, selected) {
      if (element == "Вся область") {
        this.regdata.forEach((obj) => {
          obj.selected = false;
          if (obj.region == "Вся область") {
            obj.selected = true;
          }
        });
        this.geodata.features.forEach((obj) => {
          obj.properties.selected = false;
        });
      } else {
        this.regdata.forEach((obj) => {
          if (obj.region == element) {
            obj.selected = selected;
          }
          if (obj.region == "Вся область") {
            obj.selected = false;
          }
        });
        this.geodata.features.forEach((obj) => {
          if (obj.properties.name == element) {
            obj.properties.selected = selected;
          }
        });
        if (
          this.regdata.filter((value) => value.selected == true).length == 0
        ) {
          this.regdata[0].selected = true;
        }
        if (this.regdata.filter((value) => value.selected == true).length > 1) {
        }
      }
      this.selectedRegions = this.regdata.filter(
        (value) => value.selected == true
      );
      this.mapkey++;
      this.chartkey++;
    },
    oneQuestionChangeMain(oneQues) {
      this.oneQuestion = oneQues;
      this.$refs.mapComp.updateMap(oneQues);
      this.customOnMapBool = false;
    },
  },
  computed: {},
  created: async function () {
    //получение данных и их обработка
    const path = process.env.SERVER_URL + "/api/regions";
    let regions = [];
    await axios
      .get(path)
      .then((res) => {
        regions = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
    const path1 = process.env.SERVER_URL + "/api/questions";
    let questions = [];
    await axios
      .get(path1)
      .then((res) => {
        questions = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
    const path2 = process.env.SERVER_URL + "/api/geojson";
    let geodata = [];
    await axios
      .get(path2)
      .then((res) => {
        geodata = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
    let reglist = [];
    regions.forEach((region, index) => {
      if (region == "Вся область") {
        this.selectedRegions.push({
          id: index,
          region: region,
          selected: true,
        });
        reglist.push({ id: index, region: region, selected: true });
        return;
      }
      reglist.push({ id: index, region: region, selected: false });
    });

    this.regdata = reglist;

    let queslist = [];
    questions.forEach((question, index) => {
      if (index == 0) {
        this.selectedQuestions.push(question);
        this.oneQuestion = question;
        queslist.push({ id: index, question: question, selected: true });
        return;
      }
      queslist.push({ id: index, question: question, selected: false });
    });
    this.queslist = queslist;
    await this.getData(this.regdata, this.selectedQuestions);
    geodata = JSON.parse(geodata);
    geodata.features.forEach((obj) => {
      switch (obj.properties.name) {
        case "городской округ Котельнич":
          obj.properties.name = "г. Котельнич";
          break;
        case "городской округ Киров":
          obj.properties.name = "г. Киров";
          break;
        case "городской округ Вятские Поляны":
          obj.properties.name = "г. Вятские Поляны";
          break;
        case "городской округ Кирово-Чепецк":
          obj.properties.name = "г. Кирово-Чепецк";
          break;
        case "городской округ Слободской":
          obj.properties.name = "г. Слободской";
          break;
        case "Кумёнский район":
          obj.properties.name = "Куменский район";
          break;
        case "Фалёнский район":
          obj.properties.name = "Фаленский район";
          break;
        default:
          obj.properties.name = obj.properties.name;
          break;
      }
      obj.properties["selected"] = false;
      obj.properties["color"] = "blue";
      obj.properties["weight"] = 1;
    });
    this.geodata = geodata;
    this.preloader = false;
  },
  mounted() {},
};
</script>

<style>
@import url("http://fonts.cdnfonts.com/css/circe");
/*@import url('../static/normalize.css');*/
html {
  width: 100vw;
  overflow-x: hidden;
  /* overflow-y:hidden; */
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

body {
  margin: 0;
  background-color: #282b38;
}
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-family: "Circe", Helvetica, Arial, sans-serif;
  color: #13c6e9;
  background-color: #282b38;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.map-container {
  display: flex;
  min-width: 100vw;
  justify-content: center;
  height: 100%;
  position: relative;
}

.sidebar {
  box-sizing: border-box;
  border-top: 2px solid rgba(19, 198, 233, 0.5);
  border-bottom: 2px solid rgba(19, 198, 233, 0.5);
  min-width: 210px;
  max-width: 420px;
  width: 15%;
  overflow-y: scroll;
  max-height: 590px;
  position: absolute;
  display: block;
  z-index: 99999;
  background-color: #282b38;
}

.sidebar h2 {
  font-size: 18px;
  padding-left: 10px;
  margin: 0px;
  padding-top: 5px;
  padding-bottom: 5px;
}

ul {
  list-style: none;
  padding: 0px;
  padding-left: 15px;
  font-size: 16px;
  margin: 0px;
}

.sidebar ul li {
  padding-bottom: 10px;
}

input[type="radio"] {
  margin-right: 5px;
}

.menu-container {
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0px 30px;
}

.toggleSidebar {
  width: 100px;
  background-color: #282b38;
  border: 2px solid #13c6e9;
  border-radius: 5px;
  height: 35px;
  font-size: 20px;
  color: #13c6e9;
  cursor: pointer;
}

.toggleSidebar:active {
  color: #0b7c92;
}

.regionscontainer {
  top: 0;
  right: 0;
}
.quescontainer {
  top: 0;
  left: 0;
}
</style>
