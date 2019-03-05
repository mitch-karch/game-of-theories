<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Theories</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button"
                class="btn btn-success btn-sm"
                v-b-modal.book-modal>Add Theory</button>
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
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>{{ "👍".repeat(book.positive) }}</td>
              <td>{{ "👎".repeat(book.negative) }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.book-update-modal
                        @click="editBook(book)">Update</button>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteBook(book)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal"
             id="book-modal"
             title="Add a new book"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-theory-group"
                      label="Theory:"
                      label-for="form-theory-input">
            <b-form-textarea id="form-theory-input"
                             type="text"
                             v-model="addBookForm.theory"
                             rows="3"
                             max-rows="6">
            </b-form-textarea>
        </b-form-group>
        <b-form-group id="form-votes-group"
                      label="Votes:"
                      label-for="form-votes-input">
            <div v-for="voter in players" :key="voter.name">
                {{voter.name}} assigned tokens: {{voter.tempToken}}
                <b-form-input :name="voter.name"
                              :key="voter.name"
                              id="form-votes-input"
                              type="range"
                              placeholder=0
                              min=-5
                              max=5
                              step=1
                              v-model.number="voter.tempToken">
                </b-form-input>
            </div>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editBookModal"
             id="book-update-modal"
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
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-edit-theory-group"
                      label="Theory:"
                      label-for="form-edit-theory-input">
            <b-form-textarea id="form-edit-theory-input"
                             type="text"
                             v-model="editForm.theory"
                             rows="3"
                             max-rows="6">
            </b-form-textarea>
        </b-form-group>
        <b-form-group id="form-edit-votes-group"
                      label="Votes:"
                      label-for="form-edit-votes-input">
            <div v-for="voter in editForm.bets" :key="voter.player">
                {{voter.player}} assigned tokens: {{voter.betAmount}}
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
import Alert from './Alert';

function genPosNeg(singleBook) {
  let countPositives = 0;
  let countNegatives = 0;
  singleBook.bets.forEach((element) => {
    if (element.betAmount > 0) {
      countPositives += element.betAmount;
    } else {
      countNegatives += Math.abs(element.betAmount);
    }
  });
  return [countPositives, countNegatives];
}

export default {
  data() {
    return {
      books: [],
      players: [],
      tempBetList: [],
      addBookForm: {
        title: '',
        author: '',
        theory: '',
      },
      editForm: {
        id: '',
        title: '',
        author: '',
        theory: '',
        bets: [],
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          /* eslint no-param-reassign: "error" */
          res.data.books.forEach((element) => {
            const temp = genPosNeg(element);
            element.positive = temp[0];
            element.negative = temp[1];
          });
          this.books = res.data.books;
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
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book removed!';
          this.showMessage = true;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    editBook(book) {
      this.editForm = book;
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.theory = '';
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.theory = '';
      this.editForm.bets = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        theory: this.addBookForm.theory,
      };
      this.players.forEach((element) => {
        const player = element.name;
        const betAmount = element.tempToken;
        this.tempBetList.push({ player, betAmount });
      });
      payload.bets = this.tempBetList;
      this.tempBetList = [];
      this.addBook(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        theory: this.editForm.theory,
        bets: this.editForm.bets,
      };
      this.updateBook(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks(); // why?
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
  },
  created() {
    this.getBooks();
    this.getPlayers();
  },
};


</script>
