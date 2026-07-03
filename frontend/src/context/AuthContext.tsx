import React, { createContext, useContext, useEffect, useState } from 'react';
import { API_BASE } from '../config';

interface AuthContextType {
    accessToken: string | null;
    isLoading: boolean;
    login: (username: string, password: string) => Promise<void>;
    register: (username: string, email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetch(`${API_BASE}/auth/refresh/`, {
            method: 'POST',
            credentials: 'include',
        })
            .then((response) => (response.ok ? response.json() : null))
            .then((data) => {
                if (data) setAccessToken(data.access);
            })
            .finally(() => setIsLoading(false));
    }, []);

    const login = async (username: string, password: string) => {
        const response = await fetch(`${API_BASE}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password }),
        });
        if (!response.ok) throw new Error('Login failed');
        const data = await response.json();
        setAccessToken(data.access);
    };

    const register = async (username: string, email: string, password: string) => {
        const response = await fetch(`${API_BASE}/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password }),
        });
        if (!response.ok) throw new Error('Registration failed');
    };

    const logout = async () => {
        await fetch(`${API_BASE}/auth/logout/`, {
            method: 'POST',
            credentials: 'include',
        });
        setAccessToken(null);
    };

    return (
        <AuthContext.Provider value={{ accessToken, isLoading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
