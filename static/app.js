class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            handleClick: document.querySelector('.message_button')
        }

        this.state = false;
        this.messages = [];
    }


    display() {
        const {openButton, chatBox, sendButton, handleClick} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        handleClick.addEventListener('click', () =>   setInterval(vibrate, 0))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
    
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
    
            if (msg2.message.startsWith("Thanks for sharing the details")) {
              const form = document.createElement('form');
              form.classList.add('my-form-class');
              form.innerHTML = `
              <div class="Form" >
                <p>I did'nt get you please fill the details below our team will contact you</p>
                <label for="name">Name:      <input type="text" id="name" name="name" required></label></br>
                <label for="email">Email:    <input type="email" id="email" name="email" required></label></br>
                <label for="message">Number: <input type="number" name="message" id="message" required></label><br><br>
                <button class="button" type="submit">Submit</button>
              </div>
              `;
    
              const messagesDiv = chatbox.querySelector('.chatbox__messages');
              messagesDiv.appendChild(form);
              //document.querySelector('.chatbox__messages').appendChild(form);
    
              form.addEventListener('submit', (event) => {
                event.preventDefault();
                const name = event.target.elements.name.value;
                const email = event.target.elements.email.value;
                const message = event.target.elements.message.value;
                const detailsMsg = { name: "Sam", message: `Name: ${name} <br/> Email: ${email} <br/> Number : ${message}` };
                this.messages.push(detailsMsg);
                this.updateChatText(chatbox);
                form.remove();
              });
            } else {
              this.updateChatText(chatbox);
            }
            textField.value = ''
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
    
    

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
            
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

setInterval(function(){
    var myDiv = document.getElementById("myDiv");
    myDiv.classList.add("vibrate");
    setTimeout(function() {
      myDiv.classList.remove("vibrate");
    }, 3000);
  }, 2000);

  var myDiv = document.getElementById("myDiv");

myDiv.addEventListener("click", function() {
  myDiv.style.animation = "none";
});
 
const chatbox = new Chatbox();
chatbox.display();
