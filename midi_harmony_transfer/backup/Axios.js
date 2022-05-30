// import React, { Component } from 'react'
// import axios, { Axios } from 'axios'
var react = require('react')
var axios = require('axios')

class httprequest extends react.Component {
    
    state={
        dataS:[]
    }
    componentDidMount(){

        
        
        axios.get('http://127.0.0.1:8000/')
        .then((res) =>{
            this.setState({
                dataS:res.data
            })
            console.log(res.data);
        })

        console.log("pass!")
        axios.post(`http://127.0.0.1:8000/`, {
            'user': 'thisisloong',
            'description': 'thisistimeframe',
            'completed': 'thisisresult',
        },
        {
            headers: {
                "Authorization": `AUTHORIZATION_KEY`,
                "Content-Type": 'application/json'
            }
        }
    )
    .then((res) => console.log(res))
    .catch((error) => console.log(error))
    
        
    }

    postfile(file) {
        console.log("postfile")


        axios.post(`http://127.0.0.1:3000/`, {
            'user': 'thisisloong',
            'description': 'thisistimeframe',
            'completed': 'thisisresult',
        },
        {
            headers: {
                "Authorization": `AUTHORIZATION_KEY`,
                "Content-Type": 'application/json'
            }
        }
    )
    .then((res) => console.log(res))
    .catch((error) => console.log(error))


        

        // return "undefined"
    }

    render() {
        return (
            "undefined"
        )
    }

    
}

export default Axios