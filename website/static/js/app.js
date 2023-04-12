const msgerForm = get(".msger-form");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

// Chatbot icons by Icons8 from https://icons8.com/icon/79UfeEN6JkZ8/chatbot
// User icon by Icons8 from https://icons8.com/icon/kDoeg22e5jUY/male-user
const BOT_IMG = "https://img.icons8.com/fluency/48/null/chatbot.png";
const PERSON_IMG = "https://img.icons8.com/fluency/48/null/user-male-circle.png";
const BOT_NAME = "SART";
const PERSON_NAME = "User";

window.addEventListener('load', function() {
  document.querySelector('.msg-info-time').textContent = formatDate(new Date());
});

msgerForm.addEventListener('submit', event => {
  event.preventDefault();
  
  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  fetch('http://localhost:5005/webhooks/rest/webhook', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'sender' : 'user', 'message' : msgText })
  })
  .then(response => response.json())
  .then(data => {
    const botResp = data[0]['text'];
    const delay = botResp.split(" ").length * 100;

    setTimeout(() => {
      appendMessage(BOT_NAME, BOT_IMG, "left", botResp);
    }, delay);
  })
  .catch(error => console.error(error));
});


function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img"><img src="${img}" alt="bot"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}