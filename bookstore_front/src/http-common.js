import axios from "axios";

export default axios.create({
  baseURL: "https://bookshotapi.herokuapp.com/api",
  headers: {
    "Content-type": "application/json"
  }
});