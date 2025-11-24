import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useToast } from "@/hooks/use-toast";
import { Scale, Send, LogOut, User, Bot, Loader2 } from "lucide-react";
import { sendQuestion, sendFeedback } from "./chatService"; // new service (relative path)
import { Database } from "@/integrations/supabase/types"; // if you have types, optional

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  simpleExplanation?: string;
  legalExplanation?: string;
}

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [userEmail, setUserEmail] = useState("");
  const navigate = useNavigate();
  const { toast } = useToast();
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkUser = async () => {
      const {
        data: { session },
      } = await supabase.auth.getSession();
      if (!session) {
        navigate("/auth");
      } else {
        setUserEmail(session.user.email || "");
      }
    };
    checkUser();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (!session) {
        navigate("/auth");
      }
    });

    return () => subscription.unsubscribe();
  }, [navigate]);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate("/auth");
  };

  // top of file: add imports

  // --- inside component replace the existing handleSend with this ---
  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    // push user message
    setMessages((prev) => [...prev, userMessage]);
    const questionText = input;
    setInput("");
    setLoading(true);

    try {
      // call backend
      const data = await sendQuestion(questionText);

      // backend may return { simple, legal } OR { answer }
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.simple || data.answer || "No answer",
        simpleExplanation: data.simple || data.answer || "",
        legalExplanation:
          data.legal || data.legalExplanation || data.sections || "",
      };

      // save message to state
      setMessages((prev) => [...prev, botMessage]);

      // optional: store chat in Supabase for chat history
      try {
        const user = supabase.auth.getUser
          ? (await supabase.auth.getUser()).data.user
          : null;
        if (user) {
          await supabase.from("chats").insert([
            {
              user_id: user.id,
              question: questionText,
              answer_simple: botMessage.simpleExplanation,
              answer_legal: botMessage.legalExplanation,
              created_at: new Date().toISOString(),
            },
          ]);
        }
      } catch (dbErr) {
        console.warn("Failed to save chat history:", dbErr);
      }
    } catch (err: any) {
      // push an error assistant message
      const errMsg: Message = {
        id: (Date.now() + 2).toString(),
        role: "assistant",
        content: `Error: ${err.message || err}`,
        simpleExplanation: `Error: ${err.message || err}`,
        legalExplanation: "",
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/95 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-hero rounded-lg">
              <Scale className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">
                LegalAI Assistant
              </h1>
              <p className="text-xs text-muted-foreground">Powered by AI</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground hidden sm:block">
              {userEmail}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={handleSignOut}
              className="gap-2"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <div className="container mx-auto px-4 py-6 h-[calc(100vh-180px)] flex flex-col">
        <ScrollArea className="flex-1 pr-4" ref={scrollAreaRef}>
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <Card className="p-8 max-w-md text-center bg-gradient-card border-border/50">
                <Scale className="w-16 h-16 mx-auto mb-4 text-primary" />
                <h2 className="text-2xl font-bold mb-2">Welcome to LegalAI</h2>
                <p className="text-muted-foreground">
                  Ask any question about Indian legal laws, IPC sections, or
                  legal concepts. I'll provide both simple and detailed legal
                  explanations.
                </p>
              </Card>
            </div>
          ) : (
            <div className="space-y-4 pb-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 animate-fade-in ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {message.role === "assistant" && (
                    <div className="w-8 h-8 rounded-full bg-gradient-hero flex items-center justify-center flex-shrink-0">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                  )}
                  <div
                    className={`max-w-[80%] ${
                      message.role === "user" ? "order-first" : ""
                    }`}
                  >
                    {message.role === "user" ? (
                      <Card className="p-4 bg-primary text-primary-foreground">
                        <p className="text-sm">{message.content}</p>
                      </Card>
                    ) : (
                      <Card className="p-4 bg-card border-border/50">
                        <Tabs defaultValue="simple" className="w-full">
                          <TabsList className="grid w-full grid-cols-2 mb-3">
                            <TabsTrigger value="simple" className="text-xs">
                              Simple Explanation
                            </TabsTrigger>
                            <TabsTrigger value="legal" className="text-xs">
                              Legal Format
                            </TabsTrigger>
                          </TabsList>
                          <TabsContent value="simple" className="mt-0">
                            <p className="text-sm whitespace-pre-line text-foreground">
                              {message.simpleExplanation}
                            </p>
                          </TabsContent>
                          <TabsContent value="legal" className="mt-0">
                            <p className="text-sm whitespace-pre-line text-foreground font-mono">
                              {message.legalExplanation}
                            </p>
                          </TabsContent>
                        </Tabs>
                        <div className="flex gap-2 mt-2">
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={async () => {
                              await sendFeedback({
                                user: userEmail || null,
                                question: message.content,
                                rating: "up",
                              });
                              toast({ title: "Thanks for the feedback!" });
                            }}
                          >
                            👍 Helpful
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={async () => {
                              await sendFeedback({
                                user: userEmail || null,
                                question: message.content,
                                rating: "down",
                              });
                              toast({
                                title: "Feedback recorded",
                                variant: "destructive",
                              });
                            }}
                          >
                            👎 Not helpful
                          </Button>
                        </div>
                      </Card>
                    )}
                  </div>
                  {message.role === "user" && (
                    <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
                      <User className="w-5 h-5 text-secondary-foreground" />
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div className="flex gap-3 animate-fade-in">
                  <div className="w-8 h-8 rounded-full bg-gradient-hero flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                  <Card className="p-4 bg-card border-border/50">
                    <Loader2 className="w-5 h-5 animate-spin text-primary" />
                  </Card>
                </div>
              )}
            </div>
          )}
        </ScrollArea>

        {/* Input Area */}
        <div className="mt-4 flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask about IPC sections, legal rights, or any legal question..."
            className="flex-1 bg-card border-border/50"
            disabled={loading}
          />
          <Button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-gradient-hero hover:opacity-90 transition-opacity"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
