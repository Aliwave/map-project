<template>
  <div class="menu-container">
    <label
      >File
      <input
        class="mainupload-btn"
        type="file"
        ref="file"
        name="file"
        id="file"
      />
      <button v-on:click="submitFile()">Submit</button>
    </label>
    <!-- <form action="http://127.0.0.1:5000/uploaddb" method="post" enctype="multipart/form-data">
      <p><input type="file" name="file">
         <input type="submit" value="Upload"></p>
    </form> -->
    {{ msg }}
  </div>
</template>

<script>
import axios from 'axios';
/* eslint-disable */
export default {
  name: "MainMenu",
  data() {
    return {
      file: "",
      msg: "",
    };
  },
	watch:{

	},
  methods: {
    submitFile() {
			this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append("file", this.file);
      alert(formData.toString());
      axios
        .post("http://127.0.0.1:5000/uploaddb", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
					//надо придумать как обновлять вопросы после загрузки базы данных!!!
        })
        .then((res) => {
          this.msg = res.data;
					console.log(res);
        })
        .catch((error) => {
          // eslint-disable
          console.log(error);
        });
    },
  },
  created() {
    //this.getMessage();
  },
};

</script>

<style>
.menu-container {
	min-height:40px;
	display:flex;
	align-items:center;
	justify-content: center;
}
</style>