document.addEventListener("DOMContentLoaded", () => {

    const chatWindow = document.getElementById("chat-window");
    const input = document.getElementById("chat-input");
    const button = document.getElementById("send-button");

    function scrollBottom() {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function addMessage(role, text) {

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

        if (role === "assistant") {

            bubble.innerHTML =
                marked.parse(text);

            bubble.querySelectorAll("pre code")
                .forEach(block => {
                    hljs.highlightElement(block);
                });

            const copyButton =
                document.createElement("button");

            copyButton.className = "copy-button";
            copyButton.innerText = "Copy";

            copyButton.onclick = () => {

                navigator.clipboard.writeText(text);

                copyButton.innerText = "Copied";

                setTimeout(() => {

                    copyButton.innerText = "Copy";

                }, 1500);

            };

            bubble.prepend(copyButton);

        }
        else {

            bubble.textContent = text;

        }

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);

        chatWindow.appendChild(wrapper);

        scrollBottom();

        return bubble;

    }

    async function sendMessage() {

        const message = input.value.trim();

        if (!message)
            return;

        addMessage("user", message);

        input.value = "";

        const loading =
            addMessage(
                "assistant",
                "Thinking..."
            );

        try {

            const response =
                await fetch("/agent/chat", {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        message

                    })

                });

            const data =
                await response.json();

            loading.innerHTML =
                marked.parse(data.answer);

            loading.querySelectorAll("pre code")
                .forEach(block => {

                    hljs.highlightElement(block);

                });

        }

        catch {

            loading.innerHTML =
                "<b>Error contacting agent.</b>";

        }

        scrollBottom();

    }

    button.onclick = sendMessage;

    input.addEventListener(
        "keydown",
        e => {

            if (
                e.key === "Enter"
                &&
                !e.shiftKey
            ) {

                e.preventDefault();

                sendMessage();

            }

        }

    );

});