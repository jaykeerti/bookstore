import React, { Component } from "react";
import BookDataService from "../services/book.service";

//This component is used to add/save exixsting book data
export default class AddBook extends Component {
  constructor(props) {
    super(props);
    this.onChangeBookId = this.onChangeBookId.bind(this);
    this.onChangeQuantity = this.onChangeQuantity.bind(this);
    this.saveBook = this.saveBook.bind(this);
    this.newBook = this.newBook.bind(this);

    this.state = {
      bookid: '',
      quantity: 0,
      submitted: false
    };
  }

  onChangeBookId(e) {
    this.setState({
      bookid: e.target.value
    });
  }

  onChangeQuantity(e) {
    this.setState({
      quantity: e.target.value
    });
  }

  saveBook() {
    var data = {
      bookid: this.state.bookid,
      quantity: this.state.quantity
    };

    BookDataService.create(data)
      .then(response => {
        this.setState({
          bookid: response.data.bookid,
          quantity: response.data.quantity,
          submitted: true
        });
        console.log(response.data);
      })
      .catch(e => {
        console.log(e);
      });
  }

  newBook() {
    this.setState({
      bookid: '',
      quantity: 0,
      submitted: false
    });
  }

  render() {
    return (
      <div className="submit-form">
        {this.state.submitted ? (
          <div>
            <h4>You submitted successfully!</h4>
            <button className="btn btn-success" onClick={this.newBook}>
              Add
            </button>
          </div>
        ) : (
          <div>
            <div className="form-group">
              <label htmlFor="title">Book Id</label>
              <input
                type="text"
                className="form-control"
                id="bookid"
                required
                value={this.state.bookid}
                onChange={this.onChangeBookId}
                name="bookid"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Quantity</label>
              <input
                type="number"
                className="form-control"
                id="quantity"
                required
                value={this.state.quantity}
                onChange={this.onChangeQuantity}
                name="quantity"
              />
            </div>

            <button onClick={this.saveBook} className="btn btn-success">
              Submit
            </button>
          </div>
        )}
      </div>
    );
  }
}