'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { User, Session } from '@supabase/supabase-js'
import { API_BASE } from '@/app/lib/api'

interface AuthContextType {
  user: User | null
  session: Session | null
  loading: boolean
  signUp: (email: string, password: string, fullName: string, businessName: string) => Promise<{ error: any }>
  signIn: (email: string, password: string) => Promise<{ error: any }>
  signInWithGoogle: () => Promise<{ error: any }>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  session: null,
  loading: true,
  signUp: async () => ({ error: null }),
  signIn: async () => ({ error: null }),
  signInWithGoogle: async () => ({ error: null }),
  signOut: async () => {},
})

export const useAuth = () => useContext(AuthContext)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession()
      .then(({ data: { session } }) => {
        console.log('AuthContext: initial session', session)
        setSession(session)
        setUser(session?.user ?? null)
        setLoading(false)
      })
      .catch((err) => {
        console.error('AuthContext: getSession error', err)
        setLoading(false)
      })

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      console.log('AuthContext: onAuthStateChange', event, session)
      setSession(session)
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  const signUp = async (email: string, password: string, fullName: string, businessName: string) => {
    try {
      // Call backend signup endpoint
      const response = await fetch(`${API_BASE}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          password,
          full_name: fullName,
          business_name: businessName,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        return { error: new Error(data.detail || 'Signup failed') }
      }

      // Do not auto sign in; require email verification if configured.
      return { error: null }
    } catch (error: any) {
      return { error: new Error(error.message || 'Signup failed') }
    }
  }

  const signIn = async (email: string, password: string) => {
    try {
      console.log('AuthContext: Attempting to sign in with Supabase...');
      const { data, error } = await supabase.auth.signInWithPassword({ email, password });
      console.log('AuthContext: Supabase response:', {
        hasData: !!data,
        hasUser: !!data?.user,
        hasSession: !!data?.session,
        error: error?.message,
      });

      if (error) {
        const message = error.message || 'Login failed';
        const normalized = message.toLowerCase();
        if (normalized.includes('confirm') || normalized.includes('verified') || normalized.includes('unconfirmed')) {
          return { error: new Error('Your email is not confirmed yet. Please verify the email sent to you before logging in.') };
        }

        console.error('AuthContext: Sign in error:', error);
        return { error };
      }

      console.log('AuthContext: Sign in successful, user:', data.user?.email);
      return { error: null };
    } catch (err: any) {
      console.error('AuthContext: Sign in exception:', err);
      return { error: new Error(err.message || 'An unexpected error occurred') };
    }
  }

  const signOut = async () => {
    await supabase.auth.signOut()
  }

  const signInWithGoogle = async () => {
    try {
      // Get the app origin dynamically
      const appOrigin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:4000';
      
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${appOrigin}/auth/callback`,
        },
      });
      
      return { error };
    } catch (err: any) {
      return { error: { message: err.message || 'Google sign in failed' } };
    }
  }

  return (
    <AuthContext.Provider value={{ user, session, loading, signUp, signIn, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}
