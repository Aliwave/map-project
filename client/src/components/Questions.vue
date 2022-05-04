<template>
  <div class="quescontainer sidebar">
    <h2>Вопросы:</h2>
    <!-- <span class="notification" v-if="Warnin">Выбрано макс. допустимое кол-во вопросов!</span> -->
    <form action="">
      <ul>
        <li v-for="(element, index) in queslist" :key="index">
          <input
            type="checkbox"
            name="questions"
            :id="'question_' + index"
            :value="element.question"
            :checked="element.selected == true"
            @click="selectQuestion(element)"
            :disabled="disabledQues(element)"
          />
          <label :for="'question_' + index">{{ element.question }}</label>
        </li>
        <!-- <li><input type="radio" name="questions" id="0"> <label for="0">Test 1</label></li>
        <li><input type="radio" name="questions" id="1"> <label for="1">Test 2</label></li>
        <li><input type="radio" name="questions" id="2"> <label for="2">Test 3</label></li> -->
      </ul>
    </form>
  </div>
</template>

<script>
// import axios from 'axios';
/* eslint-disable */
export default {
  name: "Questions",
  data() {
    return {
      msg: "",
    };
  },
  props: ["queslist"],
  computed: {
    // Warnin:function(){
    //   if (this.queslist.filter((value) => value.selected == true).length == 4) {
    //     return true;
    //   } else {
    //     return false;
    //   }
    // }
  },
  methods: {
    disabledQues(element) {
      if (
        this.queslist.filter((value) => value.selected == true).length == 1 &&
        element.selected == true
      ) {
        return true;
      } else {
        if (
          this.queslist.filter((value) => value.selected == true).length == 4 &&
          element.selected == false
        ) {
          return true;
        } else {
          return false;
        }
      }
    },
    // showWarn() {
    //   if (this.queslist.filter((value) => value.selected == true).length == 4) {
    //     return true;
    //   } else {
    //     return false;
    //   }
    // },
    selectQuestion(element) {
      element.selected = !element.selected;
      this.$emit("selectQ", element.question, element.selected);
    },
  },
  created() {
    //this.getMessage();
  },
};
</script>

<style scoped>
.notification {
  font-size: 12px;
  text-align: center;
}
</style>