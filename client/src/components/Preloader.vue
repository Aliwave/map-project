<template>
  <div class="container">
    <div class="clear-loading loading-effect-1">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="loader-text">Загрузка...</div>
  </div>
</template>

<script>
// import axios from 'axios';
/* eslint-disable */
export default {
  name: "Preloader",
  data() {
    return {

    };
  },
  methods: {},
  created() {

  },
};
</script>

<style scoped>
.container {
  width: 100%;
  height:100%;
  margin: 0 auto;
	position:fixed;
  top:0;
  left:0;
	background-color: #282b38;
	z-index: 99999999;
	text-align: center;
	display:flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}
.loader-text {
	font-size: 30px;
	padding-top:20px;
	width: 100%;
	text-align:center;
}
.clear-loading {
  text-align: center;
  margin: 0 20px;
  position: relative;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  -ms-box-sizing: border-box;
  -o-box-sizing: border-box;
  box-sizing: border-box;
  display: inline-block;
}
/* Loading Effect One */
.loading-effect-1 {
  width: 100px;
  height: 100px;
}
.loading-effect-1 span {
  display: block;
  -webit-border-radius: 50%;
  -moz-border-radius: 50%;
  -ms-border-radius: 50%;
  -o-border-radius: 50%;
  border-radius: 50%;
  border: 4px solid #fff;
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-transform: translate(-50%, -50%);
  -moz-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  -o-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
.loading-effect-1 span:first-child {
  width: 100%;
  height: 100%;
  border-color: #639dd4;
  border-left-color: transparent;
  top: 0;
  left: 0;
  -webkit-animation: effect-1-1 4s infinite linear;
  -moz-animation: effect-1-1 4s infinite linear;
  -ms-animation: effect-1-1 4s infinite linear;
  -o-animation: effect-1-1 4s infinite linear;
  animation: effect-1-1 4s infinite linear;
}
.loading-effect-1 span:nth-child(2) {
  width: 75%;
  height: 75%;
  border-color: #aaa5d3;
  border-right-color: transparent;
  top: 12.5%;
  left: 12.5%;
  -webkit-animation: effect-1-2 3s infinite linear;
  -moz-animation: effect-1-2 3s infinite linear;
  -ms-animation: effect-1-2 3s infinite linear;
  -o-animation: effect-1-2 3s infinite linear;
  animation: effect-1-2 3s infinite linear;
}
.loading-effect-1 span:last-child {
  width: 50%;
  height: 50%;
  border-color: #7072e7;
  border-bottom-color: transparent;
  top: 25%;
  left: 25%;
  -webkit-animation: effect-1-1 4s infinite linear;
  -moz-animation: effect-1-1 4s infinite linear;
  -ms-animation: effect-1-1 4s infinite linear;
  -o-animation: effect-1-1 4s infinite linear;
  animation: effect-1-1 4s infinite linear;
}
@-webkit-keyframes effect-1-1 {
  from {
    -webkit-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes effect-1-1 {
  from {
    -webkit-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-webkit-keyframes effect-1-2 {
  from {
    -webkit-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(-360deg);
    -moz-transform: rotate(-360deg);
    -ms-transform: rotate(-360deg);
    -o-transform: rotate(-360deg);
    transform: rotate(-360deg);
  }
}
@keyframes effect-1-2 {
  from {
    -webkit-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(-360deg);
    -moz-transform: rotate(-360deg);
    -ms-transform: rotate(-360deg);
    -o-transform: rotate(-360deg);
    transform: rotate(-360deg);
  }
}
</style>