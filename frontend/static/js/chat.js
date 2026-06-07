document.addEventListener("DOMContentLoaded", () => {

    const chatWindow = document.getElementById("chat-window");
    const input = document.getElementById("chat-input");
    const button = document.getElementById("send-button");

    function scrollBottom() {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function createMessage(role, text) {

        const wrapper = document.createElement("div");
        wrapper.className =
            role === "user"
                ? "user-message"
                : "assistant-message";

        const avatar = document.createElement("div");
        avatar.className = "avatar";

        avatar.textContent =
            role === "user"
                ? "👤"
                : "🤖";

        const bubble = document.createElement("div");
        bubble.className = "bubble";

        bubble.textContent = text;

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);

        chatWindow.appendChild(wrapper);

        scrollBottom();

        return bubble;
    }

    async function sendMessage() {

        const message = input.value.trim();

        if (message.length === 0)
            return;

        createMessage(
            "user",
            message
        );

        input.value = "";

        const loadingBubble = createMessage(
            "assistant",
            "Thinking..."
        );

        try {

            const response = await fetch(
                "/agent/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        message: message
                    })
                }
            );

            const data = await response.json();

            loadingBubble.textContent =
                data.answer;

        }

        catch (err) {

            loadingBubble.textContent =
                "Error contacting agent.";

            console.error(err);

        }

        scrollBottom();

    }

    button.addEventListener(
        "click",
        sendMessage
    );

    input.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
                && !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();

            }

        }
    );

});