import React from 'react';
import axios from 'axios';

export default class ProductList extends React.Component {
    state = {
        products: [],
    };

    componentDidMount() {
        axios.get(`https://jsonplaceholder.typicode.com/photos`).then((response) => {
            const productsResponse = response.data;
            this.setState({ products: productsResponse });
        });
    }

    render() {
        return (
            <div className="grid-container">
                {
                    this.state.products.map (
                        product => <div key={product.id} className="grid-item">
                                        <img src={product.url} width="200px"/><br/>
                                        <h3>{product.title}</h3>
                                    </div>
                    )
                } 
            </div>
        )
    }
}