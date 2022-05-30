import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import $ from 'jquery'
import chart_class from './Components/allcharts';
import request_class from './Components/Axios'
import {upload1res, upload2res} from './Components/Axios'



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

var chart = new chart_class();
chart.notes_chart();
chart.velocity_chart();


var uploadbutton1 = document.getElementById('uploadbutton1')
var uploadbutton2 = document.getElementById('uploadbutton2')
var dropdownitem1 = document.getElementById('dropdownitem1')
var dropdownitem2 = document.getElementById('dropdownitem2')
var dropdownmenubutton = document.getElementById('dropdownMenuButton')
var transferbutton = document.getElementById('transfer-button')
var uploadbutton = document.getElementById('upload-button')
var playbutton = document.getElementById('play-button')


var upload1_file
var upload2_file

export var upload_count1 = 0
export var upload_count2 = 0

uploadbutton1.addEventListener("click", upload1)
uploadbutton2.addEventListener("click", upload2)
$("#upload1").on("change", upload_func1)
$("#upload2").on("change", upload_func2)
$("#download-button").on("click", download_func)
dropdownitem1.addEventListener("click", dropdownitem_select1)
dropdownitem2.addEventListener("click", dropdownitem_select2)
dropdownmenubutton.addEventListener("click", dropdownmenu_display)
transferbutton.addEventListener("click", transfer_func)
playbutton.addEventListener("click", play_func)

var request_func = new request_class();
request_func.init();

function upload1() {
  document.getElementById('upload1').click();
  }
function upload2() {
  document.getElementById('upload2').click();
  }
function upload_func1(){
  upload1_file = $('#upload1').prop('files');
  console.log(upload1_file[0])
  if (upload1_file[0] !== undefined){
    document.getElementById('dropdownMenuButton').textContent = upload1_file[0].name
    document.getElementById('dropdownitem1').textContent = upload1_file[0].name
    upload_count1++
    let formdata = new FormData();
    formdata.append("upload1", upload1_file[0])
    
    $('#spinner-corner').show()
    $('#upload-button').attr('disabled', true)
    $('#dropdown').attr('disabled', true)
    $('#dropdownMenuButton').attr('disabled', true)
    $('#transfer-button').attr('disabled', true)
    request_func.upload_visual(formdata, 1)
  }
}
function upload_func2(){
  upload2_file = $('#upload2').prop('files');
  if (upload2_file[0] !== undefined){
    document.getElementById('dropdownMenuButton').textContent = upload2_file[0].name
    document.getElementById('dropdownitem2').textContent = upload2_file[0].name
    upload_count2++
    let formdata = new FormData();
    formdata.append("upload2", upload2_file[0])

    $('#spinner-corner').show()
    $('#upload-button').attr('disabled', true)
    $('#dropdown').attr('disabled', true)
    $('#dropdownMenuButton').attr('disabled', true)
    $('#transfer-button').attr('disabled', true)
    request_func.upload_visual(formdata, 2)
  }
}

export function transfer_button_appear(count1, count2){
  if(count1 >= 1 && count2 >= 1){
    $("#upload-button").css({"right": "150px"})
    $("#transfer-button").css({"position":"absolute", "display": "block", "bottom": "1px", "opacity": "100", "transition": "all 0.5s"})
  }
}

function dropdownitem_select1(){
  document.getElementById('dropdownMenuButton').textContent = document.getElementById('dropdownitem1').textContent
  try{
    chart.update_notes_chart(upload1res)
  }
  catch(e){
    console.log(e.message)
  }
}
function dropdownitem_select2(){
  document.getElementById('dropdownMenuButton').textContent = document.getElementById('dropdownitem2').textContent
  try{
    chart.update_notes_chart(upload2res)
  }
  catch(e){
    console.log(e.message)
  }
}
function dropdownmenu_display(){
  return undefined
}

function transfer_func(){
  

  $('#transfer-button').prop('disabled', true);
  $('#dropdown').prop('disabled', true);
  $('#transfer-button').append(document.createTextNode("ing"));

  $("#transfer-button").removeClass("transfer-button-property")
  $("#progress-outer").removeClass("progress-outer-property")

  $('#transfer-button').addClass('transfer-button-property2')
  $("#progress-outer").addClass("progress-outer-property2")

  $('#upload-button').text('Cancel');
  $('#upload-button').removeClass("dropdown-toggle")
  $('#upload-button').removeAttr("data-bs-toggle")
  $('#upload-button').css({"right":"85px", "transition": "all 0.5s"})

  $("#progress-text").text(0)
  $("#progressbar").css('width', `${0}%`)

  //request_func.transfer_algo()
  uploadbutton.addEventListener("click", cancel_transfer_func)


  
  let formdata = new FormData();
  formdata.append("upload1", upload1_file[0])
  formdata.append("upload2", upload2_file[0])

  request_func.postfile(formdata, 40);
  
  request_func.progress()

}

function cancel_transfer_func(){

  uploadbutton.removeEventListener("click", cancel_transfer_func)
  //uploadbutton.addEventListener("click", transfer_func)
}



function play_func(){

  let formdata = new FormData();
  formdata.append("midi_convert", upload1_file[0])
  
}

export function temp_transferbuttonaddeventlistener(){
  transferbutton.addEventListener("click", transfer_func)
}

export function download_func(){
  request_func.download_request()
}
