import React, { Component } from "react";
import BookDataService from "../services/book.service";
import { Link } from "react-router-dom";
import '../App.css';

//This is used to list/search books
export default class BooksList extends Component {
  constructor(props) {
    super(props);
    this.onChangeSearchTitle = this.onChangeSearchTitle.bind(this);
    this.retrieveBooks = this.retrieveBooks.bind(this);
    this.refreshList = this.refreshList.bind(this);
    this.searchTitle = this.searchTitle.bind(this);
    this.addToCart = this.addToCart.bind(this);
    this.onEnterPress = this.onEnterPress.bind(this);

    this.state = {
      books: [],
      searchTitle: ""
    };
  }

  componentDidMount() {
    this.retrieveBooks();
  }

  onChangeSearchTitle(e) {
    const searchTitle = e.target.value;

    this.setState({
      searchTitle: searchTitle
    });
  }

  retrieveBooks() {
    BookDataService.getAll()
      .then(response => {
        this.setState({
          books: response.data
        });
        console.log(response.data);

      })
      .catch(e => {
        console.log(e);
      });
  }

  refreshList() {
    this.retrieveBooks();
  }

  searchTitle() {
    BookDataService.findByTitle(this.state.searchTitle)
      .then(response => {
        this.setState({
          books: response.data
        });
        console.log(response.data);
      })
      .catch(e => {
        console.log(e);
      });
  }



  onEnterPress = (e) => {
    if(e.keyCode == 13 && e.shiftKey == false) {
      e.preventDefault();
      this.searchTitle();
    }
  }

  addToCart(){
    alert("Book has been addded")
  }

  render() {
    const { searchTitle, books } = this.state;
   
    return (
      <div className="">
        <div className="col-md-8">
          <div className="input-group mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Search by title"
              value={searchTitle}
              onChange={this.onChangeSearchTitle}
              onKeyDown={this.onEnterPress}
            />
            <div className="input-group-append">
              <button
                className="btn btn-outline-secondary"
                type="button"
                onClick={this.searchTitle}
                
              >
                Search
              </button>
            </div>
          </div>
        </div>
        <div className="row  match-height">
            {books &&
              books.map((book, index) => (
              <div className="col-md-2  py-2"  key={index}>
                <div className="card card-body h-100">
                <img style={{display: "block", margin: "0 auto 10px", maxHeight: "200px"}} className="img-fluid" 
                src={book.thumbnail} alt=""/>
                <h6 style={{textAlign:"center"}}><a href={book.link}>{book.title}</a></h6>
                { book.quantity > 0  ? <p style={{textAlign:"center",color:"green"}}>Available : {book.quantity}</p> : <p style={{textAlign:"center",color:"red"}}>Sold Out</p>}
                { book.quantity > 0  ? <button onClick={this.addToCart}>Book Now</button> : '' }
                  
                </div>
              </div>
              ))}
        
        </div>
      </div>
    );
  }
}
