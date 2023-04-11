try {
    const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    //let final_transcript = "";

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    function changeLanguage(lang) {
        recognition.lang = lang;
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

} catch (error) {
    alert("Speech Recognition is not available in your brower :(");
    console.log("Speech Recognition Not Available");
}