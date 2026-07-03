import React, { useState } from 'react';
import type { Category } from '../types';
import { useAuth } from '../context/AuthContext';
import { API_BASE } from '../config';

interface TransactionFormProps {
    categories: Category[];
    onSuccess: () => void;
}

function TransactionForm({ categories, onSuccess }: TransactionFormProps) {
    const { accessToken } = useAuth();
    const [formData, setFormData] = useState({
        amount: '',
        date: '',
        description: '',
        category: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE}/finances/transactions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${accessToken}`,
                },
                body: JSON.stringify(formData),
            });
            if (!response.ok) throw new Error('Failed to create transaction');
            setFormData({ amount: '', date: '', description: '', category: '' });
            onSuccess();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="number"
                step="0.01"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                placeholder="Amount"
                required
            />
            <input
                type="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Description"
                required
            />
            <select name="category" value={formData.category} onChange={handleChange} required>
                <option value="">Select a category</option>
                {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
            </select>
            <button type="submit">Add Transaction</button>
        </form>
    );
}

export default TransactionForm;