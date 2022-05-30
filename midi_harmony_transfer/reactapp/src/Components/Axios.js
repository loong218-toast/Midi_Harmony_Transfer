import React from 'react';
import axios from 'axios';
import qs from 'qs';
import chart_class from './allcharts';
import $ from 'jquery'
import {transfer_button_appear, temp_transferbuttonaddeventlistener} from '../index'
import {upload_count1} from '../index'
import {upload_count2} from '../index'
import {download_func} from '../index'


export var res
export var upload1res
export var upload2res

var transfer_progress

export default class request_class extends React.Component {

    //Initialization
    init(){
        let data = {
            'init': 'yes',
        }
        let config = {
            headers: {
                "Content-Type": 'application/json'
            }
        }
        axios.post('http://127.0.0.1:8000/', data, config)
        .then((res) =>{
            //console.log(res);
        })
        
    }

    //Post file to backend
    async postfile(file) {

    let config = {
        headers: {
            "Content-Type": 'multipart/form-data'
        }
    }

    await axios.post('http://127.0.0.1:8000', file, config)
    .then(function (res) {console.log(res)})
    .catch((error) => console.log(error))
        
    }

    //File upload and update visual when file is uploaded
    upload_visual(upload, value){
    let config = {
        headers: {
            "Content-Type": 'multipart/form-data'
        }
    }
    axios.post('http://127.0.0.1:8000', upload, config)
    .then(function(res) {
        var chart = new chart_class()
        var data = res.data
        if (value === 1){
            upload1res = data
        }
        if (value === 2){
            upload2res = data
        }

        chart.update_notes_chart(data)
        $('#spinner-corner').hide()
        $('#upload-button').attr('disabled', false)
        $('#transfer-button').attr('disabled', false)
        $('#dropdownMenuButton').attr('disabled', false)
        $('#transfer-button').attr('disabled', false)
        temp_transferbuttonaddeventlistener()
        transfer_button_appear(upload_count1, upload_count2)
    })
    .catch((error) => console.log(error))
    }

    //Download completed midi file from backend
    download_request(){

        axios.get('http://127.0.0.1:8000', {responseType: 'blob'}).then((res) =>{
            var blob = new Blob([res.data], {type: "audio/midi"});
            let objectURL = window.URL.createObjectURL(blob);

            let anchor = document.getElementById('download-link')
            anchor.href = objectURL;
            document.getElementById('download-link').click();
        })
        
    }

    // transfer progress
    progress(){
        let data = {
            'progress': 'yes',
        }

        let data2 = {
            'noprogress': 'yes',
        }

        let config = {
            headers: {
                "Content-Type": 'application/json'
            }
        }

        var temp_click_disable = true
        $('#upload-button').on('click', function temp_click(){
            // Cancel button
            if (temp_click_disable === true){
                stop = 0;
                i = 1000;
                $('#upload-button').prop('disabled', true);
            }
        })
        
        var stop = 1

        for(var i = 0;i < 50000; i++){
                
                transfer_progress = setTimeout(timer, i * 3000);

            }

        function timer() {
            if (stop === 1){
                //console.log("progressing");
                axios.post('http://127.0.0.1:8000', qs.stringify(data) , config)
                .then(function(res) {
                    // Updating visual of progress bar
                    temp_click_disable = true
                    $("#progress-text").text(res.data)
                    $("#progressbar").css('width', `${res.data}%`)
                    if (res.data === 100){
                        stop = 2
                    }
                })
                .catch((error) => console.log(error))
            }
            else{
                // Cancel or finish progress
                console.log("cancelled");
                var id = window.setTimeout(function() {}, 0);
                while (id--) {
                    window.clearTimeout(id);
                }
                axios.post('http://127.0.0.1:8000', qs.stringify(data2) , config)
                .then(function(res) {console.log(res)

                    temp_click_disable = false

                    $('#transfer-button').prop('disabled', false);
                    $("#transfer-button").removeClass("transfer-button-property2")
                    $("#transfer-button").addClass("transfer-button-property")
                    $("#progress-outer").removeClass("progress-outer-property2")
                    $("#progress-outer").addClass("progress-outer-property")
                    
                    $('#upload-button').css({"right":"140px", "transition": "all 0.5s"})
                    $('#upload-button').attr('data-bs-toggle', 'dropdown')
                    $('#upload-button').addClass("dropdown-toggle")
                    $('#upload-button').text('Choose Files');
                    let text = $('#transfer-button').text().replace("ing", "")
                  
                    $('#transfer-button').text(text)
                    console.log($('#transfer-button').text().replace("ing", ""))
                    $('#upload-button').attr('disabled', false);
                    $('#dropdownMenuButton').attr('disabled', false)

                    if (stop === 2){
                        // Show download button
                        // This feature is temporarily disabled due to aesthetic issue
                        // Instead, file will automatically download itself

                        // console.log('completed')
                        // $('#download-button').css({'visibility':'visible'})
                        // $('#download-button').attr('disabled', false)
                        // $("#download-button").removeClass("download-button-property")
                        // $("#download-button").addClass("download-button-property2")
                        // $("#upload-button").prop("onclick", null).off("click");

                        download_func()
                        
                    }
                })
                .catch((error) => console.log(error))
            }
        }
    }

    render() {
        return (
            "undefined"
        )
    }

}
