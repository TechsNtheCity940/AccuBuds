import React, { useState } from 'react';
import Login from './components/Login';
import POSHome from './components/POSHome';
import './App.css';
import './components/Login.css';
import './components/POSHome.css';


function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);

    const handleLogin = (user) => {
        setCurrentUser(user);
        setLoggedIn(true);
    };

    const handleSignOff = () => {
        const token = localStorage.getItem('accubuds_token');
        if (token) {
            // Best-effort logout; ignore errors
            fetch('/api/logout/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token }),
            }).finally(() => {
                localStorage.removeItem('accubuds_token');
                setCurrentUser(null);
                setLoggedIn(false);
            });
        } else {
            setCurrentUser(null);
            setLoggedIn(false);
        }
    };

    return (
        <div className="App">
            {loggedIn
                ? <POSHome user={currentUser} onSignOff={handleSignOff} />
                : <Login onLogin={handleLogin} />}
        </div>
    );
}

export default App;
