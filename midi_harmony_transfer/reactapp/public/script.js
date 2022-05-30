// import postfile from './Axios'
// import axios from 'axios';

function upload() {
  document.getElementById('upload1').click();
  postfile();
  }
  
function upload2() {
  document.getElementById('upload2').click();
}
  
function samples() {
  return undefined;
}
  
function getfile(){
  let file = document.getElementById('upload1');
  
  console.log(file.files[0]);
  console.log(typeof file.files[0]);

  
  }

function postfile(){
  var axios = require('axios')

  console.log("postfile")


  axios.post(`http://127.0.0.1:3000/`, {
      'user': 'thisisloong',
      'description': 'thisistimeframe',
      'completed': 'thisisresult',
  },
  {
      headers: {
          "Authorization": `AUTHORIZATION_KEY`,
          "Content-Type": 'multipart/form-data'
      }
  }
)
.then((res) => console.log(res))
.catch((error) => console.log(error))
}


