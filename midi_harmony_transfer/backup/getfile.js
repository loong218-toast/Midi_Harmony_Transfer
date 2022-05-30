// import postfile from 'Axios'

function getfile(){
    let file = document.getElementById('upload1');

    console.log(file.files[0]);
    console.log(typeof file.files[0]);

    var axios = require("./Axios.js")
    axios.postfile(file.files[0]);


}