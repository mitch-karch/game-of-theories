<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Theories</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <addTheory @theorySubmitted="getTheories"></addTheory>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">It Is Known</th>
              <th scope="col">You Know Nothing</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(Theory, index) in Theories" :key="index">
              <td>{{ Theory.title }}</td>
              <td>{{ Theory.author }}</td>
              <td>{{ "🔥".repeat(Theory.positive) }}</td>
              <td>{{ "💀".repeat(Theory.negative) }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.Theory-update-modal
                        @click="editTheory(Theory)">Update</button>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteTheory(Theory)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <editTheory @theoryUpdated="getTheories" v-bind:passedTheory="this.theory"></editTheory>
</div>
</template>

<script>
import axios from 'axios';

import AddTheory from './AddTheory';
import EditTheory from './EditTheory';
import Alert from './Alert';

/* Helper Functions */
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
      Theories: [],
      theory: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    addTheory: AddTheory,
    editTheory: EditTheory,
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
          this.Theories = res.data.Theories;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
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
    editTheory(Theory) {
      this.theory = Theory;
    },
    onDeleteTheory(Theory) {
      this.removeTheory(Theory.id);
    },
  },
  created() {
    this.getTheories();
  },
};
</script>
