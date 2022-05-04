<template>
  <transition name="fade">
    <div id="regionsList" class="regionscontainer sidebar">
      <h2>Районы:</h2>
      <form action="">
        <ul>
          <li v-for="(element, index) in regions" :key="index">
            <input
              type="checkbox"
              name="regions"
              :id="'region_' + index"
              :value="element.region"
              :checked="element.selected"
              @click="selectReg(element)"
              :disabled="index == 0 && element.selected == true ? true : false"
            />
            <label :for="'region_' + index"
              >{{ element.region }}
              <!-- <span style="font-size: 10px">{{ element.selected }}</span> -->
            </label>
          </li>
          <!-- <li><input type="radio" name="regions" id="testregion2">
        <label for="testregion2">Test 2</label></li>
        <li><input type="radio" name="regions" id="testregion3">
        <label for="testregion3">Test 3</label></li>@click="selectRegion(regions,element)"  -->
        </ul>
      </form>
    </div>
  </transition>
</template>

<script>
// import axios from 'axios';
/* eslint-disable */
export default {
  name: "Regions",
  data() {
    return {
      msg: "",
    };
  },
  props: ["regions"],
  methods: {
    // getCheck(element){
    //   if(element.selected){

    //   }
    // }
    selectReg(element) {
      element.selected = !element.selected;
      this.$emit("selectR", element.region, element.selected);
    },
  },
  created() {},
};
</script>

<style>
.regionListTemplate {
  position: relative;
}
.regionListToggle {
  position: absolute;
  display: block;
  top: -30px;
  left: 0;
}
</style>