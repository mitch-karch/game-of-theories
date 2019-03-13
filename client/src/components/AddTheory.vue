<template>
  <div>
    <button type="button"
            class="btn btn-success btn-sm"
            v-b-modal.Theory-modal>Add Theory</button>
    <b-modal ref="addTheoryModal"
             id="Theory-modal"
             title="Add a new Theory"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
        <b-form-input id="form-title-input"
                        type="text"
                        v-model="addTheoryForm.title"
                        required
                        placeholder="Enter title">
        </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
          <b-form-select id="form-author-input"
                          v-model="addTheoryForm.author"
                          required
                          :options=player_list>
          </b-form-select>
        </b-form-group>
        <b-form-group id="form-proposedTheory-group"
                      label="proposedTheory:"
                      label-for="form-proposedTheory-input">
          <b-form-textarea id="form-theory-input"
                             type="text"
                             v-model="addTheoryForm.proposedTheory"
                             rows="3"
                             max-rows="6">
          </b-form-textarea>
        </b-form-group>
        <b-form-group id="form-votes-group"
                      label="Votes:"
                      label-for="form-votes-input">
          <votingSlides v-bind:players="addTheoryForm.players"></votingSlides>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import VotingSlides from './VotingSlides';

function genAuthorList(playerObject) {
  const tempAuthorList = [];
  playerObject.forEach((element) => {
    tempAuthorList.push(element.name);
  });
  return tempAuthorList;
}

export default{
  data() {
    return {
      addTheoryForm: {
        title: '',
        author: '',
        proposedTheory: '',
        players: [],
      },
      player_list: [],
      showMessage: false,
      tempBetList: [],
    };
  },
  methods: {
    addTheory(payload) {
      const path = 'http://localhost:5000/Theories';
      axios.post(path, payload)
        .then(() => {
          this.showMessage = true;
          this.$emit('theorySubmitted');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    getPlayers() {
      const path = 'http://localhost:5000/players';
      axios.get(path)
        .then((res) => {
          this.player_list = genAuthorList(res.data.players);
          this.addTheoryForm.players = res.data.players;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTheoryModal.hide();
      const payload = {
        title: this.addTheoryForm.title,
        author: this.addTheoryForm.author,
        proposedTheory: this.addTheoryForm.proposedTheory,
      };
      this.addTheoryForm.players.forEach((element) => {
        const name = element.name;
        const betAmount = element.betAmount;
        this.tempBetList.push({ name, betAmount });
      });
      payload.bets = this.tempBetList;
      this.tempBetList = [];
      this.addTheory(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTheoryModal.hide();
      this.initForm();
    },
    initForm() {
      this.addTheoryForm.title = '';
      this.addTheoryForm.author = '';
      this.addTheoryForm.proposedTheory = '';
    },
  },
  created() {
    this.getPlayers();
    this.initForm();
  },
  components: {
    votingSlides: VotingSlides,
  },
};
</script>
