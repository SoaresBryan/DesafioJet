document.addEventListener('DOMContentLoaded', function () {
    const loginScreen = document.getElementById('login-screen');
    const chatScreen = document.getElementById('chat-screen');
    const loginButton = document.getElementById('login-button');
    const logoutButton = document.getElementById('logout-button');
    const userIdInput = document.getElementById('user-id-input');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatWindow = document.getElementById('chat-window');

    let userId = null; // Variável global para armazenar o ID do usuário

    // Login do usuário
    loginButton.addEventListener('click', function () {
        const inputId = userIdInput.value.trim();
        if (inputId) {
            console.log(`ID do usuário inserido: ${inputId}`);
            userId = inputId; // Armazena o ID do usuário

            // Esconde a tela de login e mostra a tela de chat
            loginScreen.style.display = 'none'; // Esconde a tela de login
            chatScreen.style.display = 'flex'; // Mostra a tela de chat
        } else {
            alert('Por favor, insira um ID de usuário válido.');
        }
    });

    // Logout do usuário
    logoutButton.addEventListener('click', function () {
        userId = null; // Reseta o ID do usuário
        userIdInput.value = ''; // Limpa o campo de entrada
        chatWindow.innerHTML = ''; // Limpa o histórico de mensagens

        // Volta para a tela de login
        loginScreen.style.display = 'flex'; // Mostra a tela de login
        chatScreen.style.display = 'none'; // Esconde a tela de chat
    });

    // Enviar mensagem
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    // Função para enviar a mensagem
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            appendMessage('user', message); // Adiciona a mensagem do usuário na tela
            messageInput.value = ''; // Limpa o campo de entrada

            if (!userId) {
                console.error('Erro: ID do usuário não encontrado.');
                appendMessage('bot', 'Erro: ID do usuário não definido. Por favor, faça login novamente.');
                return;
            }

            // Envia a mensagem para o backend
            fetch(`/api/chat?mensagem=${encodeURIComponent(message)}`, {
                method: 'POST',
                headers: {
                    'user-id': userId // Cabeçalho com o ID do usuário
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro HTTP: ${response.status}`);
                    }
                    return response.text(); // Lê a resposta como texto simples
                })
                .then(data => {
                    appendMessage('bot', data); // Adiciona a resposta do bot na tela
                })
                .catch(error => {
                    console.error('Erro ao enviar mensagem:', error);
                    appendMessage('bot', 'Erro ao enviar mensagem.');
                });
        }
    }

    // Função para adicionar mensagens ao chat
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.innerText = text;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Rolagem automática para a última mensagem
    }
});
