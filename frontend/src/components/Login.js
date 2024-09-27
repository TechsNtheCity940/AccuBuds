import React, { useState } from 'react';

function Login({ onLogin }) {
    const [pin, setPin] = useState('');

    const handleKeyClick = (digit) => {
        if (pin.length < 4) {
            setPin(pin + digit);
        }
    };

    const handleLogin = () => {
        if (pin.length === 4) {
            onLogin(pin);
        } else {
            alert("Please enter a 4-digit PIN");
        }
    };

    const handleClear = () => {
        setPin('');
    };

    return (
        <div className="login-screen">
            <h1>AccuBuds POS</h1>
            <div className="pin-display">{'*'.repeat(pin.length)}</div>
            <div className="keypad">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map((digit) => (
                    <button key={digit} onClick={() => handleKeyClick(digit)}>{digit}</button>
                ))}
            </div>
            <button onClick={handleLogin}>Login</button>
            <button onClick={handleClear}>Clear</button>
        </div>
    );
}

export default Login;
