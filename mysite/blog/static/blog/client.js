console.log(window.location.pathname)

const API_URL = 'http://localhost:8000/like'; //post request against this URL

function sendSearchRequest() {

}

function doButtonStuff() {
    for (const btn of document.querySelectorAll('.vote')) {
        btn.addEventListener('click', event => {
          const element = event.currentTarget;
          console.log(element.matches('.already'));
          if (event.currentTarget.classList.contains('already')) {
            console.log("already on!");
            event.currentTarget.classList.toggle('already');

          } else {
              event.currentTarget.classList.toggle('on');
              console.log("not on!");

          }



        });
    }
}

window.onload = function () {
    doButtonStuff();
};


//get endpoint to do GET request to nodejs server
function listAllPosts() {
    fetch(API_URL)
        .then(response => response.json())
        .then(mews => {
            mews.reverse();
            mews.forEach(mew => {
                const div = document.createElement('div');

                const header = document.createElement('h3');
                header.textContent = mew.name;
                
                const contents = document.createElement('p');
                contents.textContent = mew.content;

                const date = document.createElement('small');
                console.log(mew.date);
                date.textContent = new Date(mew.date);

                div.appendChild(header);
                div.appendChild(contents);
                div.appendChild(date);

                mewsElement.appendChild(div);
                loadingElement.style.display = 'none';

            })
        })
}