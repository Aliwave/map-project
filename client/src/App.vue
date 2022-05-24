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
      @customDataChange="customDataChange"
      :mapkey="mapkey"
      :chartkey="chartkey"
      :multiple="multiple"
      ref="infopanel"
    ></InfoPanel>
    <div></div>
    <!-- <Ping></Ping> -->
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import Map from "./components/Map";
import Ping from "./components/Ping";
import MainMenu from "./components/MainMenu";
import Questions from "./components/Questions";
import Regions from "./components/Regions";
import InfoPanel from "./components/InfoPanel";
import Preloader from "./components/Preloader";

export default {
  components: { Map, Ping, MainMenu, Regions, Questions, InfoPanel, Preloader },
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
      msg: "",
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
      multiple: false,
      chartkey: 0,
      msg1: ""
    };
  },
  methods: {
    async getid() {
      const path = process.env.SERVER_URL + "/api/session";
      await axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
        async getid1() {
      const path = process.env.SERVER_URL + "/api/session1";
      await axios
        .get(path)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // forceRender(){
    //   this.mapkey +=1;
    // },
    // showMain(){
    //   //this.mainData[0].question получение вопроса
    //   //this.mainData[0].regions[0].name получение названия региона
    //   //this.mainData[0].regions[0].labels получение вариантов ответа
    //   //this.mainData[0].regions[0].data получение данных
    //   console.log(this.mainData[0].regions.length);
    //   console.log(this.mainData.length);
    // },
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
          this.msg1 = res.data.msg;
          let queslist = [];
          this.selectedQuestions = [];
          res.data.queslist.forEach((question, index) => {
            if (index == 0) {
              this.selectedQuestion = question;
              queslist.push({ id: index, question: question, selected: true });
              this.selectedQuestions.push(question);
              return;
            }
            queslist.push({ id: index, question: question, selected: false });
            
          });
          this.queslist = queslist;
          this.mainData = {};
          // this.selectQues(this.selectedQuestion,true);
          // this.oneQuestionChangeMain(this.selectedQuestion);
          this.getData(this.regdata, this.selectedQuestions);
          //this.$refs.mapComp.updateMapOnCustomData(this.customData);
          this.oneQuestionChangeMain(this.selectedQuestion);
        })
        .catch((error) => {
          // eslint-disable
          console.log(error);
        });
        this.preloader =false;
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
          //console.log(this.mainData);
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
        if (this.selectedRegions[0] == "Вся область") {
          //this.customData[region].data.splice(this.customData[region].labels.indexOf(queslabel),1);
          this.customData.forEach(function (value) {});
        } else {
        }
        //console.log(this.mainData[element]);
        //this.mapkey--;
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
        this.multiple = false;
        this.customData = {};
        this.$refs.mapComp.updateMapOnCustomData(this.customData);
        this.mapkey++;
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
          this.multiple = false;
          this.customData = {};
          this.mapkey++;
          this.$refs.mapComp.updateMapOnCustomData(this.customData);
        }
        if (this.regdata.filter((value) => value.selected == true).length > 1) {
          this.multiple = true;
          this.mapkey++;
        }
        // this.customData = {};
        // this.$refs.mapComp.updateMapOnCustomData(this.customData);
      }
      this.selectedRegions = this.regdata.filter(
        (value) => value.selected == true
      );
      if (selected == false) {
        delete this.customData[element];
        this.$refs.mapComp.updateMapOnCustomData(this.customData);
      }
      // this.regdata.forEach((obj)=>{
      //   if(obj.selected == true){
      //     this.selectedRegions.push(obj.region);
      //   }
      // });
      // this.mapkey++;
      // this.getData(this.selectedRegions, this.selectedQuestions);
      this.chartkey++;
    },
    oneQuestionChangeMain(oneQues) {
      this.oneQuestion = oneQues;
      // console.log(this.oneQuestion);
      this.$refs.mapComp.updateMap(oneQues);
    },
    addRegionToCustom(data, region, queslabel) {
      if (this.customData[region] === undefined) {
        //создаем регион если не было
        this.customData[region] = {
          labels: [],
          data: [],
        };
        this.customData[region].labels.push(queslabel);
        this.customData[region].data.push(data);
      } else {
        if (this.customData[region].labels.indexOf(queslabel) === -1) {
          //добавляем данные если не было
          this.customData[region].labels.push(queslabel);
          this.customData[region].data.push(data);
        } else {
          //удаляем данные если пришло заново
          this.customData[region].data.splice(
            this.customData[region].labels.indexOf(queslabel),
            1
          );
          this.customData[region].labels.splice(
            this.customData[region].labels.indexOf(queslabel),
            1
          );
          //удаляем регион из списка, если все данные пусты
          if (this.customData[region].labels.length === 0) {
            delete this.customData[region];
          }
        }
      }
    },
    customDataChange(data, region, label, question) {
      let queslabel = question + " / " + label;
      if (region === "Вся область") {
        this.regdata.forEach((element) => {
          if (
            this.mainData[question][element.region].labels.indexOf(label) !== -1
          ) {
            let dataIndex =
              this.mainData[question][element.region].labels.indexOf(label);
            let regionData =
              this.mainData[question][element.region].data[dataIndex];
            let labelData =
              this.mainData[question][element.region].labels[dataIndex];
            this.addRegionToCustom(regionData, element.region, queslabel);
          }
          //console.log(element.region);
        });
        //console.log(this.mainData);
      } else {
        this.addRegionToCustom(data, region, queslabel);
      }
      Object.keys(this.customData);
      this.$refs.mapComp.updateMapOnCustomData(this.customData);
    },
  },
  computed: {},
  created: async function () {
    //получение данных и их обработка👌
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
      //быть может стоит перенести обработку на сервер 🤔
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
