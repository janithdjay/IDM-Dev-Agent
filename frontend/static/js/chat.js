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

    function renderMessage(role, text, metadata = null) {

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

                navigator.clipboard.writeText(text).catch(console.error);

                copy.textContent = "Copied!";

                setTimeout(() => {

                    copy.textContent = "Copy";

                }, 1500);

            };

            bubble.prepend(copy);

            if (metadata && metadata.metrics) {

                const details =
                    document.createElement("details");

                details.className = "diagnostics";

                const summary =
                    document.createElement("summary");

                summary.textContent =
                    "Diagnostics";

                details.appendChild(summary);

                const table =
                    document.createElement("table");

                table.innerHTML = `

                        <tr>

                        <td class="metric-label">Intent</td>

                        <td>${metadata.intent}</td>

                        </tr>

                        <tr>

                        <td class="metric-label">Resolved Symbol</td>

                        <td>${metadata.symbol}</td>

                        </tr>

                        <tr>

                        <td class="metric-label">Context Size</td>

                        <td>${metadata.metrics.context_chars} chars</td>

                        </tr>

                        <tr>

                        <td class="metric-label">Prompt Size</td>

                        <td>${metadata.metrics.prompt_chars} chars</td>

                        </tr>

                        <tr>

                        <td class="metric-label">Model</td>

                        <td>${metadata.metrics.model}</td>

                        </tr>

                        <tr>

                        <td class="metric-label">LLM Time</td>

                        <td>${metadata.metrics.llm_ms} ms</td>

                        </tr>

                        <tr>

                        <td class="metric-label">Total Time</td>

                        <td>${metadata.metrics.total_ms} ms</td>

                        </tr>

                        `;

                details.appendChild(table);

                bubble.appendChild(details);

            }

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

                msg.text,

                msg.metadata || null

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

                text: data.answer,

                metadata: {

                    intent: data.intent,

                    symbol: data.symbol,

                    metrics: data.metrics

                }

            });

            saveHistory();

            renderMessage(
                "assistant",
                data.answer,
                data
            );

        }
        catch {

            loadingWrapper.remove();

            history.push({

                role: "assistant",

                text: "**Error contacting agent.**"

            });

            saveHistory();

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

        try {
            history = JSON.parse(stored);
        }
        catch {
            history = [];
        }

    }

    redrawConversation();

});