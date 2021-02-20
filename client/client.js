const form = document.querySelector('form');
const loadingElement = document.querySelector('.loading');
const mewsElement = document.querySelector('.mews');
const API_URL = 'http://localhost:5000/mews'; //post request against this URL

loadingElement.style.display = '';

listAllMews();

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const name = formData.get('name');
    const content = formData.get('content');

    const mew = {
        name, 
        content
    };

    form.style.display = 'none';
    loadingElement.style.display = '';
    
    //SUBMIT FORM
    fetch(API_URL, {
        method:'POST',
        body: JSON.stringify(mew),
        headers: {
            'content-type': 'application/json'
        }
    }).then(response => response.json())
      .then(createdMew => {
        
        console.log(createdMew);
        form.reset()
        setTimeout(() => {
            form.style.display="";
        }, 30000);
        form.style.display = '';
        loadingElement.style.display='none';
        listAllMews();
      });
});

//get endpoint to do GET request to nodejs server
function listAllMews() {
    mewsElement.innerHTML = '';
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