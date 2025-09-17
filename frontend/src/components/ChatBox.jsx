import React, { useState } from "react";
import axios from "axios";
import { ChatFeed, Message } from "react-chat-ui";

function ChatBox() {
    const bubbleStyles = {
        userBubble: {
            backgroundColor: "#0078fe",
            color: "#fff",
            fontSize: "16px",
            borderRadius: "18px",
            padding: "10px 16px",
            margin: "8px 0",
            maxWidth: "70%",
        },
        chatbubble: {
            backgroundColor: "#5b5b5cff",
            color: "#222",
            fontSize: "16px",
            borderRadius: "18px",
            padding: "10px 16px",
            margin: "8px 0",
            maxWidth: "70%",
        }
    };

    const [messages, setMessages] = useState([
        new Message({ id: 1, message: "Hola" })
    ]);
    const [input, setInput] = useState([""]);
    const [typing, setTyping] = useState(false); // Add typing state

    const handleSend = async () => {
        console.log("Handle send called with input:", input);
        if (!input.trim()) return;
        const newMessage = new Message({ id: 0, message: input });
        setMessages([...messages, newMessage]);
        setInput("");
        setTyping(true);
        try {

            const response = await axios.post("http://localhost:8000/api/chat", {
                messages: [{ "role": "user", "content": input }]
            });

            const reply = response.data.message;


            // Add bot's reply
            const botMessage = new Message({ id: 1, message: reply, sender: "bot" });
            setMessages((prevMessages) => [...prevMessages, botMessage]);
        } catch (error) {
            console.error("Error sending message:", error);
            const errorMessage = new Message({
                id: 1,
                message: "Oops! Something went wrong.",
                sender: "bot",
            });
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        }
        setTyping(false);

    }

    return (
        <div>
            <ChatFeed
                messages={messages}
                isTyping={typing}
                hasInputField={false}
                showSenderName
                bubblesCentered={false}
                bubbleStyles={bubbleStyles}
            />
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        handleSend();
                    }
                }}
                placeholder="Escriba su mensaje..."
            />

        </div>
    );
}

export default ChatBox;