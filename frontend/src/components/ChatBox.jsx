import React, { useState } from "react";
import { ChatFeed, Message } from "react-chat-ui";

function ChatBox() {
    const [messages, setMessages] = useState([
        new Message({ id: 1, message: "Hola" })
    ]);
    const [input, setInput] = useState([
        ""
    ])

    const handleSend = async () => {
        console.log("Handle send called with input:", input);
        if (!input.trim()) return;
        const newMessage = new Message({ id: 0, message: input });
        setMessages([...messages, newMessage]);
        setInput("");
        try {
            const response = await axios.post("http://localhost:8000/api/chat", {
                message: input
            });

            const reply = response.data.reply;


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

    }

    return (
        <div>
            <ChatFeed
                messages={messages}
                isTyping={false}
                hasInputField={false}
                showSenderName
                bubblesCentered={false}
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