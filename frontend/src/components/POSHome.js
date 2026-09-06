import React, { useState, useEffect } from 'react';

const TOKEN = () => localStorage.getItem('accubuds_token') || '';
const authHeaders = () => ({
    'Content-Type': 'application/json',
    Authorization: `Token ${TOKEN()}`,
});

function POSHome({ user, onSignOff }) {
    const [products, setProducts] = useState([]);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [availableAmounts, setAvailableAmounts] = useState([]);
    const [productTypes, setProductTypes] = useState([]);

    useEffect(() => {
        fetch('/api/products/', { headers: authHeaders() })
            .then(r => r.json())
            .then(data => setProducts(data))
            .catch(err => console.error('Failed to load products', err));
    }, []);

    const completeSale = async () => {
        if (!selectedProduct) return;
        try {
            const res = await fetch('/api/sales/process_sale/', {
                method: 'POST',
                headers: authHeaders(),
                body: JSON.stringify({
                    product_id: selectedProduct.id,
                    patient_id: 1, // demo — patient picker is a future enhancement
                    user_id: user.id,
                    quantity: 1,
                    terminal_number: user.terminalNumber,
                }),
            });
            const data = await res.json();
            alert(data.status === 'ok' ? `Sale #${data.sale_id} complete — total $${data.total}` : 'Sale failed: ' + data.detail);
        } catch (e) {
            alert('Network error: ' + e.message);
        }
    };

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
                <button onClick={onSignOff}>Sign Off</button>
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
                        <button onClick={completeSale} disabled={!selectedProduct}>Complete Sale</button>
                <button onClick={() => setSelectedProduct(null)}>Remove</button>
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
