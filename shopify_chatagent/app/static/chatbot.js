(function () {
    const assistantName = "Chatiz"; // <-- Change the name here

    // Create floating button
    const chatButton = document.createElement("div");
    chatButton.id = "chat-button";
    chatButton.style.position = "fixed";
    chatButton.style.bottom = "20px";
    chatButton.style.right = "20px";
    chatButton.style.width = "60px";
    chatButton.style.height = "60px";
    chatButton.style.background = "#4F46E5";
    chatButton.style.borderRadius = "50%";
    chatButton.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
    chatButton.style.cursor = "pointer";
    chatButton.style.zIndex = "9999";
    chatButton.style.display = "flex";
    chatButton.style.alignItems = "center";
    chatButton.style.justifyContent = "center";
    chatButton.style.color = "#fff";
    chatButton.style.fontSize = "30px";
    chatButton.innerHTML = "💬";

    document.body.appendChild(chatButton);

    // Create chat box (hidden initially)
    const chatBox = document.createElement("div");
    chatBox.id = "chat-box";
    chatBox.style.position = "fixed";
    chatBox.style.bottom = "90px";
    chatBox.style.right = "20px";
    chatBox.style.width = "320px";
    chatBox.style.height = "420px";
    chatBox.style.background = "white";
    chatBox.style.border = "1px solid #ccc";
    chatBox.style.borderRadius = "10px";
    chatBox.style.zIndex = "9999";
    chatBox.style.display = "none";
    chatBox.style.flexDirection = "column";
    chatBox.style.boxShadow = "0 8px 20px rgba(0,0,0,0.2)";
    chatBox.style.overflow = "hidden";

    chatBox.innerHTML = `
        <div style="background:#4F46E5;color:white;padding:10px;font-weight:bold;font-size:16px;">
            ${assistantName}
        </div>
        <div id="chat-messages" style="flex:1;padding:10px;overflow-y:auto;background:#f9f9f9;"></div>
        <div style="display:flex;border-top:1px solid #ccc;">
            <input id="chat-input" style="flex:1;padding:10px;border:none;outline:none;" placeholder="Type message..." />
            <button id="chat-send" style="background:#4F46E5;color:white;border:none;padding:0 15px;cursor:pointer;">Send</button>
        </div>
    `;

    document.body.appendChild(chatBox);

    // Toggle chat box visibility
    chatButton.onclick = () => {
        chatBox.style.display = chatBox.style.display === "none" ? "flex" : "none";
        document.getElementById("chat-input").focus();
    };

    const sessionId = "session_" + Math.random().toString(36).substring(2);

    async function sendMessage() {
        const input = document.getElementById("chat-input");
        const message = input.value.trim();
        if (!message) return;

        const messages = document.getElementById("chat-messages");
        messages.innerHTML += `<div><b>You:</b> ${message}</div>`;
        input.value = "";
        messages.scrollTop = messages.scrollHeight;

        try {
            const response = await fetch("https://lithophytic-unbeneficially-nadia.ngrok-free.dev/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            messages.innerHTML += `<div><b>${assistantName}:</b> ${data.reply}</div>`;
            messages.scrollTop = messages.scrollHeight;
        } catch (err) {
            messages.innerHTML += `<div style="color:red;"><b>${assistantName}:</b> Unable to connect</div>`;
            messages.scrollTop = messages.scrollHeight;
        }
    }

    // Send message on button click
    document.getElementById("chat-send").onclick = sendMessage;

    // Send message on Enter key
    document.getElementById("chat-input").addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
})();