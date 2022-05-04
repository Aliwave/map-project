<template>
  <div id="app">
    <transition name="fade">
      <Preloader v-if="preloader"></Preloader>
    </transition>
    <div class="menu-container">
      <button @click="showQuesList = !showQuesList;" class="toggleSidebar">Вопросы</button>
      <div>
        <label
          >File
          <input
            class="mainupload-btn"
            type="file"
            ref="file"
            name="file"
            id="file"
          />
          <button @click="submitFile()">Submit</button>
        </label>
        {{ msg }}
      </div>
      <button @click="showRegionList = !showRegionList;" class="toggleSidebar">Районы</button>
    </div>
    <div class="map-container">
      <transition name="fade">
        <Questions v-if="showQuesList" :queslist="queslist" @selectQ="selectQues"></Questions>
      </transition>

      <Map
        :geojson="geodata"
        :selectedReg="selectedRegions"
        @selectM="selectionRegionList"
        :selectedQuestions="selectedQuestions"
        :key="mapkey"
      ></Map>
      <transition name="fade">
        <Regions v-if="showRegionList" :regions="regdata" @selectR="selectionRegionList"></Regions>
      </transition>
    </div>
    <InfoPanel
      :queslist="queslist"
      :selectedReg="selectedRegions"
      :selectedQues="selectedQuestions"
      :regions="regdata"
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
      selectedRegions: ["Вся область"],
      selectedQuestions: [],
      file: "",
      msg: "",
      preloader: true,
      mapkey: 0,
      showQuesList: true,
      showRegionList: true,
    };
  },
  methods: {
    // forceRender(){
    //   this.mapkey +=1;
    // },
    async submitFile() {
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append("file", this.file);
      await axios
        .post("http://127.0.0.1:5000/api/uploaddb", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          //надо придумать как обновлять вопросы после загрузки базы данных!!!
        })
        .then((res) => {
          console.log(res);
          this.msg = res.data.msg;
          let queslist = [];
          res.data.queslist.forEach((question, index) => {
            if (index == 0) {
              this.selectedQuestion = question;
              queslist.push({ id: index, question: question, selected: true });
              return;
            }
            queslist.push({ id: index, question: question, selected: false });
          });
          this.queslist = queslist;
        })
        .catch((error) => {
          // eslint-disable
          console.log(error);
        });
      console.log(this.queslist);
    },
    getData(Region, Question) {
      const path = "http://localhost:5000/data";
      const data = { selectedQuestion: Question, selectedRegion: Region };
      axios
        .post(path, data, { headers: { "Access-Control-Allow-Origin": "*" } })
        .then((response) => console.log(response))
        .catch((error) => console.log(error));
    },
    selectQues(element, selected) {
      if (selected == true) {
        this.selectedQuestions.push(element);
        this.mapkey++;
      } else {
        this.selectedQuestions.splice(
          this.selectedQuestions.indexOf(element),
          1
        );
        this.mapkey--;
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
      }
      // this.getData(this.selectedRegion, this.selectedQuestion);
    },
  },
  async created() {
    //получение данных и их обработка👌
    const path = "http://localhost:5000/api/regions";
    let regions = [];
    await axios
      .get(path)
      .then((res) => {
        regions = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
    const path1 = "http://localhost:5000/api/questions";
    let questions = [];
    await axios
      .get(path1)
      .then((res) => {
        questions = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
    const path2 = "http://localhost:5000/api/geojson";
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
        queslist.push({ id: index, question: question, selected: true });
        return;
      }
      queslist.push({ id: index, question: question, selected: false });
    });
    this.queslist = queslist;

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
};
</script>

<style>
@import url("http://fonts.cdnfonts.com/css/circe");
/*@import url('../static/normalize.css');*/
html {
  width: 100vw;
  /* overflow-x: hidden; */
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
  display:block;
  z-index:99999;
  background-color:#282b38;
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

.regionscontainer{
  top:0;
  right:0;
}
.quescontainer {
  top:0;
  left:0;
}
</style>
