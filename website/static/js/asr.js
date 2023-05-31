const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
const recognition = new SpeechRecognition();

const synthesis = window.speechSynthesis;
const utterance = new SpeechSynthesisUtterance();
synthesis.cancel();

recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

function changeLanguage(lang) {
    recognition.lang = lang;
    let voices = speechSynthesis.getVoices();

    if (lang === "en-US") {
        utterance.voice = voices[1];
    } else {
        utterance.voice = voices[4];
    }        
};

document.querySelector("#mic").onclick = () => {
    const mic = document.querySelector('#mic').classList;
    if (mic.contains("mic-off")) {
        recognition.start();
    }
};

recognition.onstart = () => {
    const mic = document.querySelector('#mic').classList;
    const mic_icon = document.querySelector('#mic-icon').classList;
    mic.remove("mic-off");
    mic_icon.remove("bi-mic-mute-fill");
    mic.add("mic-on");
    mic_icon.add("bi-mic-fill");
    document.querySelector("#input").placeholder = "Listening...";
};

recognition.onerror = () => {
    alert("Speech Recognition Error !");
    console.log("Speech Recognition Error");
};

recognition.onend = () => {
    document.querySelector("#input").placeholder = "Enter your message...";
    const mic = document.querySelector('#mic').classList;
    const mic_icon = document.querySelector('#mic-icon').classList;
    mic.remove("mic-on");
    mic_icon.remove("bi-mic-fill");
    mic.add("mic-off");
    mic_icon.add("bi-mic-mute-fill");
    console.log("Speech Recognition Ended");
};

recognition.onresult = (event) => {
    document.querySelector("#input").value = event.results[0][0].transcript;
    document.querySelector('#send').click();
}; 

recognition.onspeechend = () => {
    recognition.stop();
};