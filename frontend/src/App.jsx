import { useState } from 'react';
import ProductList from './components/ProductList';
import UserList from './components/UserList';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('products');

  return (
    <div className="app">
      <header className="app-header">
        <h1>CRUD Application</h1>
        <p>Manage Products and Users</p>
      </header>

      <nav className="tabs">
        <button
          className={`tab ${activeTab === 'products' ? 'active' : ''}`}
          onClick={() => setActiveTab('products')}
        >
          Products
        </button>
        <button
          className={`tab ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'products' && <ProductList />}
        {activeTab === 'users' && <UserList />}
      </main>
    </div>
  );
}

export default App;
