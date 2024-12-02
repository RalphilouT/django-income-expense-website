// get user input from register.html
const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback')
// once user types something
usernameField.addEventListener('keyup', (e) => {
    console.log('77777', 7777777)
    const usernameVal= e.target.value;

    // usernameField.classList.remove('is-invalid') //bootstrap
    // feedbackArea.style.display="none"
    usernameField.classList.remove('is-invalid') //bootstrap
    feedbackArea.style.display="none"
    if(usernameVal.length > 0)
    {
        fetch('/authentication/validate-username', {
                body: JSON.stringify({
                    username: usernameVal
                }),
                method: 'POST',
            }
        ).then(res => res.json())
        .then(data =>{
            // show error in frontend
            if(data.username_error){
                usernameField.classList.add('is-invalid') //bootstrap
                feedbackArea.style.display="block"
                feedbackArea.innerHTML=`<p> ${data.username_error} </p>`
            }
        });
    }
})