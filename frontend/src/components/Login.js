import React, { useState } from 'react';

const API_BASE = ''; // CRA dev server proxies /api/* to Django on :8000

function Login({ onLogin }) {
    const [pin, setPin] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleKeyClick = (digit) => {
        if (pin.length < 4) {
            setPin(pin + digit);
            setError('');
        }
    };

    const handleLogin = async () => {
        if (pin.length !== 4) {
            setError('Please enter a 4-digit PIN');
            return;
        }
        setLoading(true);
        setError('');
        try {
            const res = await fetch(`${API_BASE}/api/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pin, terminal: '420' }),
            });
            const data = await res.json();
            if (!res.ok) {
                setError(data.detail || 'Login failed');
                setLoading(false);
                return;
            }
            // Stash token for later API calls
            localStorage.setItem('accubuds_token', data.token);
            onLogin({
                id: data.user_id,
                name: data.username,
                terminalNumber: data.terminal || '420',
                token: data.token,
            });
        } catch (e) {
            setError('Network error: ' + e.message);
        } finally {
            setLoading(false);
        }
    };

    const handleClear = () => {
        setPin('');
        setError('');
    };

    const handleBackspace = () => {
        setPin(pin.slice(0, -1));
        setError('');
    };

    return (
        <div className="login-screen">
            <h1>AccuBuds POS</h1>
            <div className="pin-display">{'*'.repeat(pin.length)}</div>
            {error && <div className="login-error">{error}</div>}
            <div className="keypad">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((digit) => (
                    <button key={digit} onClick={() => handleKeyClick(digit)} disabled={loading}>
                        {digit}
                    </button>
                ))}
                <button onClick={handleBackspace} disabled={loading}>⌫</button>
                <button onClick={() => handleKeyClick(0)} disabled={loading}>0</button>
                <button onClick={handleClear} disabled={loading}>C</button>
            </div>
            <button onClick={handleLogin} disabled={loading || pin.length !== 4}>
                {loading ? 'Signing in…' : 'Login'}
            </button>
            <p className="hint">Demo PINs: 1234 (techjuan), 0420 (budtender1), 9999 (manager)</p>
        </div>
    );
}

export default Login;
