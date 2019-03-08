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
    <b-modal ref="editTheoryModal"
             id="Theory-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
            <b-form-select id="form-author-edit-input"
                          v-model="editForm.author"
                          required
                          :options=player_list>
            </b-form-select>
          </b-form-group>
        <b-form-group id="form-edit-proposedTheory-group"
                      label="proposedTheory:"
                      label-for="form-edit-proposedTheory-input">
            <b-form-textarea id="form-edit-proposedTheory-input"
                             type="text"
                             v-model="editForm.proposedTheory"
                             rows="3"
                             max-rows="6">
            </b-form-textarea>
        </b-form-group>
        <b-form-group id="form-edit-votes-group"
                      label="Votes:"
                      label-for="form-edit-votes-input">
            <div v-for="voter in editForm.bets" :key="voter.player">
                {{voter.player}} assigned tokens: {{ voter.betAmount }} {{
                voter.betAmount > 0
                ? "🔥".repeat(voter.betAmount) : "💀".repeat(Math.abs(voter.betAmount)) }}
                <b-form-input :name="voter.name"
                              :key="voter.name"
                              id="form-votes-input"
                              type="range"
                              placeholder=0
                              min=-5
                              max=5
                              step=1
                              v-model.number="voter.betAmount">
                </b-form-input>
            </div>
        </b-form-group>

        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
</div>
</template>

<script>
import axios from 'axios';

import AddTheory from './AddTheory';
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

function genAuthorList(playerObject) {
  const tempAuthorList = [];
  playerObject.forEach((element) => {
    tempAuthorList.push(element.name);
  });
  return tempAuthorList;
}

/* Vue Architecture */
export default {
  data() {
    return {
      Theories: [],
      players: [],
      player_list: [],
      tempBetList: [],
      addTheoryForm: {
        title: '',
        author: '',
        proposedTheory: '',
      },
      editForm: {
        id: '',
        title: '',
        author: '',
        proposedTheory: '',
        bets: [],
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    addTheory: AddTheory,
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
    getPlayers() {
      const path = 'http://localhost:5000/players';
      axios.get(path)
        .then((res) => {
          this.players = res.data.players;
          this.player_list = genAuthorList(this.players);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addTheory(payload) {
      const path = 'http://localhost:5000/Theories';
      axios.post(path, payload)
        .then(() => {
          this.getTheories();
          this.message = 'Theory added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTheories();
        });
    },
    updateTheory(payload, TheoryID) {
      const path = `http://localhost:5000/Theories/${TheoryID}`;
      axios.put(path, payload)
        .then(() => {
          this.getTheories();
          this.message = 'Theory updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTheories();
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
      this.editForm = Theory;
    },
    initForm() {
      this.addTheoryForm.title = '';
      this.addTheoryForm.author = '';
      this.addTheoryForm.proposedTheory = '';
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.proposedTheory = '';
      this.editForm.bets = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTheoryModal.hide();
      const payload = {
        title: this.addTheoryForm.title,
        author: this.addTheoryForm.author,
        proposedTheory: this.addTheoryForm.proposedTheory,
      };
      this.players.forEach((element) => {
        const player = element.name;
        const betAmount = element.tempToken;
        this.tempBetList.push({ player, betAmount });
      });
      payload.bets = this.tempBetList;
      this.tempBetList = [];
      this.addTheory(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTheoryModal.hide();
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        proposedTheory: this.editForm.proposedTheory,
        bets: this.editForm.bets,
      };
      this.updateTheory(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTheoryModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTheoryModal.hide();
      this.initForm();
      this.getTheories(); // why?
    },
    onDeleteTheory(Theory) {
      this.removeTheory(Theory.id);
    },
  },
  created() {
    this.getTheories();
    this.getPlayers();
  },
};


</script>
