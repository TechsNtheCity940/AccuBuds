import React, { useState } from 'react';
import Login from './components/Login';
import POSHome from './components/POSHome';
import './App.css';
import './components/Login.css';
import './components/POSHome.css';


function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);

    const handleLogin = (pin) => {
        // Simulate an API call to verify the pin and get user details
        // Replace with real API call
        const user = { name: 'Tech Juan', terminalNumber: 420 };
        setCurrentUser(user);
        setLoggedIn(true);
    };

    return (
        <div className="App">
            {loggedIn ? <POSHome user={currentUser} /> : <Login onLogin={handleLogin} />}
        </div>
    );
}

export default App;
