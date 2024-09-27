import React, { useState, useEffect } from 'react';

function POSHome({ user }) {
    const [products, setProducts] = useState([]);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [availableAmounts, setAvailableAmounts] = useState([]);
    const [productTypes, setProductTypes] = useState([]);

    useEffect(() => {
        // Fetch products from the Django API
        fetch('/api/products/')
            .then(response => response.json())
            .then(data => setProducts(data));
    }, []);

    const handleProductSelect = (product) => {
        setSelectedProduct(product);
        
        // Determine available amounts and product types
        if (product.item_type === 'Flower') {
            setProductTypes(['Flower']);
            setAvailableAmounts([1, 3.5, 7, 14, 28].filter(amount => amount <= product.quantity));
        } else {
            setProductTypes([product.item_type]);
            setAvailableAmounts([]);  // Assuming other types don't have weight options
        }
    };

    return (
        <div className="pos-home">
            <header>
                <div>{new Date().toLocaleDateString()}</div>
                <div>{new Date().toLocaleTimeString()}</div>
                <div>Terminal: {user.terminalNumber}</div>
                <div>User: {user.name}</div>
            </header>
            <aside>
                <button>Home</button>
                <button>New Patient</button>
                <button>Search by Symptoms</button>
                <button>Reports</button>
                <button>Products</button>
                <button>Timeclock</button>
                <button>Sign Off</button>
            </aside>
            <main>
                <div className="display-screen">
                    {/* Display screen where sales information will be shown */}
                </div>
                <div className="product-controls">
                    <div className="row">
                        <select onChange={(e) => handleProductSelect(products.find(p => p.id === parseInt(e.target.value)))}>
                            <option>Select Product</option>
                            {products.map(product => (
                                <option key={product.id} value={product.id}>{product.name}</option>
                            ))}
                        </select>
                        <div className="product-info">
                            {selectedProduct && (
                                <div>
                                    <p>{selectedProduct.name}</p>
                                    <p>Price: ${selectedProduct.recommended_sell_price}</p>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="row">
                        <button disabled={!productTypes.includes('Flower')}>Flower</button>
                        <button disabled={!productTypes.includes('Concentrates')}>Concentrates</button>
                        <button disabled={!productTypes.includes('Edibles')}>Edibles</button>
                        <button disabled={!productTypes.includes('Cartridges')}>Cartridges</button>
                        <button>Remove</button>
                    </div>
                    <div className="row">
                        {[1, 3.5, 7, 14, 28].map(amount => (
                            <button key={amount} disabled={!availableAmounts.includes(amount)}>{amount}g</button>
                        ))}
                    </div>
                    <div className="row">
                        <button>Placeholder 1</button>
                        <button>Placeholder 2</button>
                        <button>Placeholder 3</button>
                        <button>Placeholder 4</button>
                        <button>Placeholder 5</button>
                    </div>
                </div>
                <div className="numeric-keypad">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map(number => (
                        <button key={number}>{number}</button>
                    ))}
                    <button>Credit Card</button>
                    <button>Gift Card</button>
                    <button>Fast Cash</button>
                </div>
            </main>
        </div>
    );
}

export default POSHome;
