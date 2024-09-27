import React, { useState, useEffect } from 'react';

function POS() {
    const [products, setProducts] = useState([]);
    const [patients, setPatients] = useState([]);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [selectedPatient, setSelectedPatient] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [totalPrice, setTotalPrice] = useState(0);

    useEffect(() => {
        // Fetch products and patients from the Django API
        fetch('/api/products/')
            .then(response => response.json())
            .then(data => setProducts(data));

        fetch('/api/patients/')
            .then(response => response.json())
            .then(data => setPatients(data));
    }, []);

    useEffect(() => {
        if (selectedProduct) {
            setTotalPrice(selectedProduct.sell_price * quantity);
        }
    }, [selectedProduct, quantity]);

    const handleSubmit = (event) => {
        event.preventDefault();

        const saleData = {
            product: selectedProduct.id,
            patient: selectedPatient.id,
            quantity: quantity,
            total_price: totalPrice,
        };

        fetch('/api/sales/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(saleData),
        })
            .then(response => response.json())
            .then(data => {
                alert('Sale completed successfully!');
            });
    };

    return (
        <div>
            <h2>Process a Sale</h2>
            <form onSubmit={handleSubmit}>
                <label>Product:</label>
                <select onChange={e => setSelectedProduct(products.find(p => p.id === parseInt(e.target.value)))}>
                    <option>Select a product</option>
                    {products.map(product => (
                        <option key={product.id} value={product.id}>{product.name}</option>
                    ))}
                </select>

                <label>Patient:</label>
                <select onChange={e => setSelectedPatient(patients.find(p => p.id === parseInt(e.target.value)))}>
                    <option>Select a patient</option>
                    {patients.map(patient => (
                        <option key={patient.id} value={patient.id}>{patient.patient_name}</option>
                    ))}
                </select>

                <label>Quantity:</label>
                <input type="number" value={quantity} onChange={e => setQuantity(parseInt(e.target.value))} min="1" />

                <label>Total Price:</label>
                <input type="text" value={totalPrice.toFixed(2)} readOnly />

                <button type="submit">Complete Sale</button>
            </form>
        </div>
    );
}

export default POS;
