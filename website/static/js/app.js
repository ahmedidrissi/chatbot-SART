const msgerForm = get(".msger-form");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

// Chatbot icons by Icons8 from https://icons8.com/icon/79UfeEN6JkZ8/chatbot
// User icon by Icons8 from https://icons8.com/icon/kDoeg22e5jUY/male-user
const BOT_IMG = "https://img.icons8.com/fluency/48/null/chatbot.png";
const PERSON_IMG = "https://img.icons8.com/fluency/48/null/user-male-circle.png";
const BOT_NAME = "SART";
const PERSON_NAME = "User";

var greet = false;

window.addEventListener('load', function() {
  document.querySelector('.msg-info-time').textContent = formatDate(new Date());
});

msgerForm.addEventListener('submit', async event => {
  event.preventDefault();
  
  var msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  if (recognition.lang == 'fr-FR') {
    msgText = await translateMessage(msgText, 'en');
    console.log(msgText);
  }

  fetch('http://localhost:5005/webhooks/rest/webhook', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'sender' : 'user', 'message' : msgText })
  })
  .then(response => response.json())
  .then(data => {
    let promises = data.map(item => item.text);
    return Promise.all(promises);
  })
  .then(botResponses => {
    botResponses.forEach(async botResp => {
      if (recognition.lang == 'fr-FR') {
        botResp = await translateMessage(botResp, 'fr');
        if (!botResp) {
          botResp = "Pouvez-vous répétez s'il vous plaît."
        }
      }
      appendMessage(BOT_NAME, BOT_IMG, "left", botResp);
      utterance.text = botResp;
      synthesis.speak(utterance);
    });
  })
  .catch(async error => {
    console.error(error);
    let botResp = "Can you repeat please?";
    if (recognition.lang == 'fr-FR') {
      botResp = "Pouvez-vous répétez s'il vous plaît.";
    }
    appendMessage(BOT_NAME, BOT_IMG, "left", botResp);
    utterance.text = botResp;
    synthesis.speak(utterance);
  });
});

function greetUser() {
  if (!greet) {
    let msg = "Hi, I'm SART! Go ahead and send me a message.";
    
    if (recognition.lang == 'fr-FR') {
      msg = "Bonjour, je suis SART! Allez-y et envoyez-moi un message.";
    }

    setTimeout(() => {
      appendMessage(BOT_NAME, BOT_IMG, "left", msg);
    }, 1000);

    utterance.text = msg;
    synthesis.speak(utterance);
    greet = true;
  }
}

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  let msgHTML = `
    <div class="msg ${side}-msg">
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

function translateMessage(message, language) {
  let result = fetch('/index', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'userMessage' : message, 'lang' : language
    })
  })
  .then(response => response.json())
  .then(data => {
    return data.translatedMessage;
  })
  .catch(error => {
    console.error('Error:', error);
  });
  return result;
}