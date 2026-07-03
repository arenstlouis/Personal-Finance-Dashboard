import {useEffect, useState} from 'react';
import './App.css';
import type {Category} from './types';
import { useAuth } from './context/AuthContext';
import { API_BASE } from './config';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import TransactionForm from './components/TransactionForm';

function App() {
  const { accessToken, isLoading, logout } = useAuth();
  const [categories, setCategories] = useState<Category[]>([]);
  const [showSignup, setShowSignup] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/finances/categories/`)
      .then(response => response.json())
      .then(data => setCategories(data))
      .catch(error => console.error('Error fetching categories:', error));
  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (!accessToken) {
    return (
      <div className="App">
        {showSignup ? <SignupForm /> : <LoginForm />}
        <button onClick={() => setShowSignup(!showSignup)}>
          {showSignup ? 'Already have an account? Log in' : "Don't have an account? Sign up"}
        </button>
      </div>
    );
  }

  return (
    <div className="App">
      <h1>Finance Dashboard</h1>
      <button onClick={logout}>Log Out</button>
      <div className = "card">
      <h2>Categories</h2>
      <ul>
        {categories.map(category => (
          <li key={category.id}>
            <span style={{color: category.color}}>{category.icon}</span> {category.name}
          </li>
        ))}
      </ul>
      </div>
      <TransactionForm categories={categories} onSuccess={() => alert('Transaction added!')} />
    </div>
  )
}

export default App;
