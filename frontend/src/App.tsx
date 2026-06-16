import {useEffect, useState} from 'react';
import './App.css';
import type {Category} from './types';

function App() {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/finances/categories/')
      .then(response => response.json())
      .then(data => setCategories(data))
      .catch(error => console.error('Error fetching categories:', error));
  }, []);

  return (
    <div className="App">
      <h1>Finance Dashboard</h1>
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
    </div>
  )
}

export default App;