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

        // Use data.response (not data.content!)
        const content = data && data.response ? data.response : "No response from backend.";

        // Defensive: Only check .includes if content is a string
        const hasCodeBlock = typeof content === 'string' && content.includes("```");
        if (hasCodeBlock) {
          // If the content has code block, wrap it in a <pre><code> element
          const codeContent = content.replace(/```([\s\S]+?)```/g, '</p><pre><code>$1</code></pre><p>');
          messageDiv.innerHTML = `<img src="{{ url_for('static', filename='images/gpt.jpg') }}" class="bot-icon"><p>${codeContent}</p>`;
        } else {
          messageDiv.innerHTML = `<img src="{{ url_for('static', filename='images/gpt.jpg') }}" class="bot-icon"><p>${content}</p>`;
        }
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(error => {
        console.error(error);
        // Show error in chat
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("mt-3", "p-3", "rounded", "bot-message");
        messageDiv.innerHTML = `<img src="{{ url_for('static', filename='images/gpt.jpg') }}" class="bot-icon"><p>Error: ${error}</p>`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
      });
  }
}
