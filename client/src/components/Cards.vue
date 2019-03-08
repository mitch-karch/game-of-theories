<template>
  <div class="container">
    <h1>Game of Theories</h1>
    <h3>Card View</h3>
    <hr>
    <addTheory @theorySubmitted="getTheories"></addTheory>
    <br><br>
    <editTheory @theoryUpdated="getTheories" v-bind:passedTheory="this.theory"></editTheory>
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
          <button type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.Theory-update-modal
                  @click="editTheory(Theory)">Update</button>
          <button type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteTheory(Theory)">Delete</button>
        </b-card>
      </b-card-group>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AddTheory from './AddTheory';
import EditTheory from './EditTheory';

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
      theory: [],
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
    editTheory(Theory) {
      this.theory = Theory;
    },
    removeTheory(TheoryID) {
      const path = `http://localhost:5000/Theories/${TheoryID}`;
      axios.delete(path)
        .then(() => {
          this.getTheories();
          this.message = 'Theory removed!';
          this.showMessage = true;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
          this.getTheories();
        });
    },
    onDeleteTheory(Theory) {
      this.removeTheory(Theory.id);
    },


  },
  created() {
    this.getTheories();
  },
  components: {
    addTheory: AddTheory,
    editTheory: EditTheory,
  },
};
</script>
