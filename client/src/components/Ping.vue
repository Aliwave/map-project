<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';
/* eslint-disable */
export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path =  process.env.SERVER_URL+'/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-выключение следующей строки
          console.log(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
