// get user input from register.html
const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback');
const emailField=document.querySelector('#emailField');
const emailFeedbackArea=document.querySelector('.emailFeedBackArea');
const usernamesuccessOutput = document.querySelector('.usernamesuccessOutput');
const emailsuccessOutput = document.querySelector('.emailsuccessOutput');
const showPasswordTog = document.querySelector('.showPasswordToggle');
const passwordField= document.querySelector('#passwordField');
const submitButton= document.querySelector('.submit-btn');
let emailValid = true;
let passwordValid = true;
let usernameValid = true;
const handleToggleInput = (e) => {
    if(showPasswordTog.textContent==='SHOW'){
        showPasswordTog.textContent = "'HIDE";
        passwordField.setAttribute("type", "text");
    }else{
        showPasswordTog.textContent="SHOW"
        passwordField.setAttribute("type", "password");
    }
    
}

showPasswordTog.addEventListener('click',  handleToggleInput);

emailField.addEventListener('keyup', (e) =>{
    // console.log('77777', 7777777)
    const emailVal= e.target.value;

    // email feedback of checking availability
    emailsuccessOutput.style.display = "block"
    emailsuccessOutput.textContent=`Checking ${emailVal}`

    emailField.classList.remove('is-invalid'); //bootstrap
    emailFeedbackArea.style.display="none";
    
    // submitButton.disabled = false;

    //Email is valid until told otherwise
    emailValid = true;

    // If one text is invalid, disable button
    if(usernameValid == false || usernameValid == false){
        submitButton.disabled = true;
    }else{
        submitButton.disabled = false;
    }

    if(emailVal.length > 0)
    {
        fetch('/authentication/validate-email', {
                body: JSON.stringify({
                    email: emailVal
                }),
                method: 'POST',
            }
        ).then(res => res.json())
        .then(data =>{
            // Once email is found, checking is gone
            emailsuccessOutput.style.display = "none"

            // show error in frontend
            if(data.email_error){
                emailValid = false;
                submitButton.disabled = true;
                emailField.classList.add('is-invalid'); //bootstrap
                emailFeedbackArea.style.display="block";
                emailFeedbackArea.innerHTML=`<p> ${data.email_error} </p>`;
            }
        });
    }
});

// once user types something
usernameField.addEventListener('keyup', (e) => {
    // console.log('77777', 7777777)
    const usernameVal= e.target.value;

    // username feedback of checking availability
    usernamesuccessOutput.style.display = "block"
    usernamesuccessOutput.textContent=`Checking ${usernameVal}`

    //Error is remove if not found inavailable
    usernameField.classList.remove('is-invalid'); //bootstrap
    feedbackArea.style.display="none";

    // submitButton.disabled = false;

    //Username is valid until told otherwise
    usernameValid = true;

    // If one text is invalid, disable button
    if(passwordValid == false || emailValid == false){
        submitButton.disabled = true;
    }else{
        submitButton.disabled = false;
    }
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
            // Once username is found, checking is gone
            usernamesuccessOutput.style.display = "none"

            // show error in frontend
            if(data.username_error){
                // submitButton.removeAttribute('disabled');
                submitButton.disabled = true;
                usernameValid = false;
                usernameField.classList.add('is-invalid'); //bootstrap
                feedbackArea.style.display="block";
                feedbackArea.innerHTML=`<p> ${data.username_error} </p>`;
            }
        });
    }
});