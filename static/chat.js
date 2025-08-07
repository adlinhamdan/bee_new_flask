function sendMessage() {
  const message = messageInput.value.trim();

  if (message !== "") {
    addMessage(message, true);

    fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    })
      .then(response => response.json())
      .then(data => {
        messageInput.value = "";
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("mt-3", "p-3", "rounded", "bot-message");

        // Defensive: Only show code if content is a non-empty string
        let content = "No response from backend.";
        if (data && typeof data.response === 'string' && data.response.length > 0) {
          content = data.response;
        }

        const hasCodeBlock = typeof content === 'string' && content.includes("```");
        if (hasCodeBlock) {
          // If the content has code block, wrap it in a <pre><code> element
          const codeContent = content.replace(/```([\s\S]+?)```/g, '</p><pre><code>$1</code></pre><p>');
          messageDiv.innerHTML = `<img src="/static/images/gpt.jpg" class="bot-icon"><p>${codeContent}</p>`;
        } else {
          messageDiv.innerHTML = `<img src="/static/images/gpt.jpg" class="bot-icon"><p>${content}</p>`;
        }
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(error => {
        console.error(error);
        // Show error in chat
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("mt-3", "p-3", "rounded", "bot-message");
        messageDiv.innerHTML = `<img src="/static/images/gpt.jpg" class="bot-icon"><p>Error: ${error}</p>`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
      });
  }
}
