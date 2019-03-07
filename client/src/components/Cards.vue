<template>
  <div class="container">
    <div class="row">
      <b-card-group deck>
        <b-card v-for="(Theory, index) in storedTheories" :key="index"
          :title=Theory.title
          :sub-title=Theory.author
          img-src="https://picsum.photos/600/300/?image=25"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 20rem;"
          class="mb-2"
        >
          🔥x{{ Theory.positive }}, 💀x{{ Theory.negative }}
          <br/>
          <br/>

          <b-button href="#" variant="primary">Go somewhere</b-button>
        </b-card>
      </b-card-group>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

function genPosNeg(singleTheory) {
  let countPositives = 0;
  let countNegatives = 0;
  singleTheory.bets.forEach((element) => {
    if (element.betAmount > 0) {
      countPositives += element.betAmount;
    } else {
      countNegatives += Math.abs(element.betAmount);
    }
  });
  return [countPositives, countNegatives];
}
/* Vue Architecture */

export default {
  data() {
    return {
      storedTheories: [],
    };
  },
  methods: {
    getTheories() {
      const path = 'http://localhost:5000/Theories';
      axios.get(path)
        .then((res) => {
          /* eslint no-param-reassign: "error" */
          res.data.Theories.forEach((element) => {
            const temp = genPosNeg(element);
            element.positive = temp[0];
            element.negative = temp[1];
          });
          this.storedTheories = res.data.Theories;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getTheories();
  },
};
</script>
