document.addEventListener("DOMContentLoaded", () => {

    const STORAGE_KEY = "idm_dev_agent_chat";

    const chatWindow =
        document.getElementById("chat-window");

    const input =
        document.getElementById("chat-input");

    const button =
        document.getElementById("send-button");

    const newChatButton =
        document.getElementById("new-chat-button");

    let history = [];

    function saveHistory() {

        localStorage.setItem(

            STORAGE_KEY,

            JSON.stringify(history)

        );

    }

    function scrollBottom() {

        chatWindow.scrollTop =
            chatWindow.scrollHeight;

    }

    function renderMessage(role, text) {

        const wrapper =
            document.createElement("div");

        wrapper.className =
            role === "user"
                ? "user-message"
                : "assistant-message";

        const avatar =
            document.createElement("div");

        avatar.className = "avatar";

        avatar.textContent =
            role === "user"
                ? "👤"
                : "🤖";

        const bubble =
            document.createElement("div");

        bubble.className = "bubble";

        if (role === "assistant") {

            bubble.innerHTML =
                marked.parse(text);

            bubble.querySelectorAll("pre code")
                .forEach(block => {

                    hljs.highlightElement(block);

                });

            const copy =
                document.createElement("button");

            copy.className =
                "copy-button";

            copy.textContent = "Copy";

            copy.onclick = () => {

                navigator.clipboard.writeText(text);

            };

            bubble.prepend(copy);

        }
        else {

            bubble.textContent = text;

        }

        wrapper.appendChild(avatar);

        wrapper.appendChild(bubble);

        chatWindow.appendChild(wrapper);

        scrollBottom();

    }

    function redrawConversation() {

        chatWindow.innerHTML = "";

        if (history.length === 0) {

            renderMessage(

                "assistant",

                "# Welcome\n\nAsk me anything about your project."

            );

            return;

        }

        history.forEach(msg => {

            renderMessage(

                msg.role,

                msg.text

            );

        });

    }

    async function sendMessage() {

        const message =
            input.value.trim();

        if (!message)
            return;

        history.push({

            role: "user",

            text: message

        });

        saveHistory();

        renderMessage(

            "user",

            message

        );

        input.value = "";

        const loadingWrapper =
            document.createElement("div");

        loadingWrapper.className =
            "assistant-message";

        loadingWrapper.innerHTML =

            '<div class="avatar">🤖</div><div class="bubble">Thinking...</div>';

        chatWindow.appendChild(

            loadingWrapper

        );

        scrollBottom();

        try {

            const response =
                await fetch(

                    "/agent/chat",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":

                                "application/json"

                        },

                        body: JSON.stringify({

                            message

                        })

                    }

                );

            const data =
                await response.json();

            loadingWrapper.remove();

            history.push({

                role: "assistant",

                text: data.answer

            });

            saveHistory();

            renderMessage(

                "assistant",

                data.answer

            );

        }

        catch {

            loadingWrapper.remove();

            renderMessage(

                "assistant",

                "**Error contacting agent.**"

            );

        }

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

    newChatButton.onclick = () => {

        if (

            confirm(

                "Start a new conversation?"

            )

        ) {

            history = [];

            saveHistory();

            redrawConversation();

        }

    };

    const stored =
        localStorage.getItem(
            STORAGE_KEY
        );

    if (stored) {

        history =
            JSON.parse(stored);

    }

    redrawConversation();

});