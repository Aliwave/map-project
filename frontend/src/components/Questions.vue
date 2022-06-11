<template>
  <div :key="queskey" class="quescontainer sidebar">
    <h2>Вопросы: (<a class="toMap__link" @click="customDataOnMap()">на карту</a>)</h2>
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
          <div v-if="element.selected == true && data[element.question] !== undefined">
            <ul
              v-for="(label, index1) in data[element.question]['Вся область'].labels"
              :key="index1"
            >
              <input
                v-if="label != 'Другое'"
                type="checkbox"
                name="questions"
                :id="'question_' + index+'label_'+index1"
                :value="label"
                :checked="criteriaData[element.question] !== undefined && criteriaData[element.question].indexOf(label) !== -1"
                @click="selectCriteria(element.question,label)"
              />
              <label v-if="label != 'Другое'" :for="'question_' + index+'label_'+index1">{{ label}}</label>
            </ul>
          </div>
        </li>
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
  props: {
    queslist: Array,
    data: Object,
    queskey: Number,
    criteriaData: Object
  },
  computed: {
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
    selectQuestion(element) {
      element.selected = !element.selected;
      this.$emit("selectQ", element.question, element.selected);
    },
    selectCriteria(element,label){
      this.$emit("selectCriteria",element,label);
    },
    customDataOnMap(){
      this.$emit("customOnMap");
    }
  },
  created() {
  },
};
</script>

<style scoped>
.notification {
  font-size: 12px;
  text-align: center;
}
</style>