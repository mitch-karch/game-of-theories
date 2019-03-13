<template>
  <div>
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
                        v-model="passedTheory.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
            <b-form-select id="form-author-edit-input"
                          v-model="passedTheory.author"
                          required
                          :options=player_list>
            </b-form-select>
          </b-form-group>
        <b-form-group id="form-edit-proposedTheory-group"
                      label="proposedTheory:"
                      label-for="form-edit-proposedTheory-input">
            <b-form-textarea id="form-edit-proposedTheory-input"
                             type="text"
                             v-model="passedTheory.proposedTheory"
                             rows="3"
                             max-rows="6">
            </b-form-textarea>
        </b-form-group>
        <b-form-group id="form-edit-votes-group"
                      label="Votes:"
                      label-for="form-edit-votes-input">
          <votingSlides v-bind:players="passedTheory.bets"></votingSlides>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
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
  props: ['passedTheory'],
  data() {
    return {
      player_list: [],
    };
  },
  methods: {
    getPlayers() {
      const path = 'http://localhost:5000/players';
      axios.get(path)
        .then((res) => {
          this.player_list = genAuthorList(res.data.players);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTheoryModal.hide();
      const payload = {
        title: this.passedTheory.title,
        author: this.passedTheory.author,
        proposedTheory: this.passedTheory.proposedTheory,
        bets: this.passedTheory.bets,
      };
      this.updateTheory(payload, this.passedTheory.id);
    },
    updateTheory(payload, TheoryID) {
      const path = `http://localhost:5000/Theories/${TheoryID}`;
      axios.put(path, payload)
        .then(() => {
          this.$emit('theoryUpdated');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.$emit('submissionFail');
        });
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTheoryModal.hide();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTheoryModal.hide();
      this.getTheories();
    },
  },
  created() {
    this.getPlayers();
  },
  components: {
    votingSlides: VotingSlides,
  },
};
</script>
