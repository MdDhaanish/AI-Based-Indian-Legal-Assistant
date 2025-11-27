import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { Scale, Sparkles } from "lucide-react";
import axios from "axios";


declare global {
  interface Window {
    google: any;
  }
}

const google = window.google;

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const Auth = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // important: allow cookie to be set
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || "Login failed");
      }

      const data = await res.json();
      // store token (optional - cookie is already set by backend)
      localStorage.setItem("auth_token", data.token);
      localStorage.setItem("user_name", data.user?.name || "");
      localStorage.setItem("user_email", data.user?.email || "");
      localStorage.setItem("token", data.token);
      navigate("/chat", { replace: true });

      // redirect to chat page
      //setTimeout(() => navigate("/chat"), 50);
    } catch (err: any) {
      setError(err.message || "Login error");
    } finally {
      setLoading(false);
    }
  };
  
  
async function handleGoogleLoginResponse(response: any) {
  try {
    const backendResponse = await axios.post(`${API_URL}/auth/google`, {
      id_token: response.credential
    });

    if (backendResponse.data.success) {
      localStorage.setItem("auth_token", backendResponse.data.token);
      localStorage.setItem("user_email", backendResponse.data.email || "");
      localStorage.setItem("user_name", backendResponse.data.name || "");
      navigate("/chat", { replace: true });
    }
  } catch (err) {
    console.log(err);
  }
}

// Google One-Tap
useEffect(() => {
  /* global google */
  google.accounts.id.initialize({
    client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
    callback: handleGoogleLoginResponse,
  });

  google.accounts.id.renderButton(
    document.getElementById("googleLoginDiv"),
    { theme: "outline", size: "large" }
  );
}, []);



  const handleSignUp = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);
  setError(null);

  try {
    const res = await fetch(`${API_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        email,
        password,
      }),
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt);
    }

    toast({
      title: "Account created",
      description: "You can now sign in",
    });

  } catch (err: any) {
    setError(err.message || "Signup failed");
  } finally {
    setLoading(false);
  }
};



  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-background to-muted">
      <div className="w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="p-3 bg-gradient-hero rounded-xl">
              <Scale className="w-8 h-8 text-white" />
            </div>
            <Sparkles className="w-6 h-6 text-accent" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-hero bg-clip-text text-transparent mb-2">
            LegalAI Assistant
          </h1>
          <p className="text-muted-foreground">
            Your intelligent guide to legal knowledge
          </p>
        </div>

        <Card className="p-6 shadow-lg border-border/50 backdrop-blur-sm bg-card/95">
          <Tabs defaultValue="signin" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-6">
              <TabsTrigger value="signin">Sign In</TabsTrigger>
              <TabsTrigger value="signup">Sign Up</TabsTrigger>
            </TabsList>

            <TabsContent value="signin">
              <div id="googleLoginDiv" className="flex justify-center mb-4">

              <div style={{ textAlign: "center", marginBottom: "18px" }}>
              <div style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "10px",
                  padding: "10px 18px",
                  background: "white",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                  boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
                  textDecoration: "none",
                  color: "#222",
                  fontWeight: "500",
                  cursor: "pointer"
                }}>
                <img src="https://developers.google.com/identity/images/g-logo.png" width="20"/>
                <span style={{ fontWeight: "600" }}>Continue with Google</span>
              </div>
              </div>
              </div>
              <form onSubmit={handleSignIn} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="signin-email">Email</Label>
                  <Input
                    id="signin-email"
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="transition-all focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="signin-password">Password</Label>
                  <Input
                    id="signin-password"
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="transition-all focus:ring-2 focus:ring-primary"
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full bg-gradient-hero hover:opacity-90 transition-opacity"
                  disabled={loading}
                >
                  {loading ? "Signing in..." : "Sign In"}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="signup">
              <form onSubmit={handleSignUp} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="signup-name">Name</Label>
                  <Input
                    id="signup-name"
                    type="text"
                    placeholder="Enter your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    className="transition-all focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="signup-email">Email</Label>
                  <Input
                    id="signup-email"
                    type="email"
                    value={email}
                    placeholder="Enter your email"
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="transition-all focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="signup-password">Password</Label>
                  <Input
                    id="signup-password"
                    type="password"
                    placeholder="Create a password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={6}
                    className="transition-all focus:ring-2 focus:ring-primary"
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full bg-gradient-hero hover:opacity-90 transition-opacity"
                  disabled={loading}
                >
                  {loading ? "Creating account..." : "Create Account"}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </Card>

        <p className="text-center text-sm text-muted-foreground mt-6">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
};

export default Auth;
