const cameFromShoppingCart = true;
        const isAuthorised = false;
    
    
    
        function authPageFormSent(authPageForm) {
            if (accountLogged == true) {
                window.location.href = "../pages/shopping-cart.html";
            };
        }
    
        const UnvalidateInput = (input, p, text) => {
            input.classList.remove('field-yellow');
            input.classList.add('field-red');
            p.innerText = text;
            p.style.color = 'red';
        }
    
        const ValidateInput = (input, p, text) => {
            input.classList.remove('field-red');
            input.classList.add('field-yellow');
            p.innerText = text;
            p.style.color = 'black';
        }
    
        const ValidateName = (name) => {
            return (name.length >= 6 ? true : false);
        }
    
        const ValidateTelephone = (telephone) => {
            // eslint-disable-next-line no-useless-escape
            return telephone.match(/^[\d\+][\d\(\)\ -]{4,14}\d$/);
        }
    
        const ValidateEmail = (email) => {
            // eslint-disable-next-line no-useless-escape
            if(email.match(/^[\w]{1}[\w-\.]*@[\w-]+\.[a-z]{2,4}$/i))
                return true;
            return false;
        };
    
        const ValidateBirthday = (birthday) => {
            return (birthday.length == 10 ? true : false);
        }
    
        const ValidatePassword = (password) => {
            return (password.length >= 6 ? true : false);
        }
    
        const CheckName = () => {
            let nameInput = document.getElementById('authorization-field-name');
            let nameText = document.getElementById('authorization-p-name');
            let name = nameInput.value;
            if (!ValidateName(name)) {
                UnvalidateInput(nameInput, nameText, 'Имя не менее 6 символов');
                return false;
            } else {
                ValidateInput(nameInput, nameText, 'Ваше имя');
                return true;
            }
        }
    
        const CheckTelephone = () => {
            let telephoneInput = document.getElementById('authorization-field-phone');
            let telephoneText = document.getElementById('authorization-p-phone');
            let telephone = telephoneInput.value;
            if (!ValidateTelephone(telephone)) {
                UnvalidateInput(telephoneInput, telephoneText, 'Неправильный номер');
                return false;
            } else {
                ValidateInput(telephoneInput, telephoneText, 'Ваш телефон для связи');
                return true;
            }
        }
    
        const CheckEmail = () => {
            let emailInput = document.getElementById('authorization-field-email');
            let emailText = document.getElementById('authorization-p-email');
            let email = emailInput.value;
            if (!ValidateEmail(email)) {
                UnvalidateInput(emailInput, emailText, 'Неправильная почта');
                return false;
            } else {
                ValidateInput(emailInput, emailText, 'Ваша электронная почта');
                return true;
            }
        }
    
        const CheckBirthday = () => {
            let birthdayInput = document.getElementById('authorization-field-birthday');
            let birthdayText = document.getElementById('authorization-p-birthday');
            let birthday = birthdayInput.value;
            if (!ValidateBirthday(birthday)) {
                UnvalidateInput(birthdayInput, birthdayText, 'Неправильная дата рождения');
                return false;
            } else {
                ValidateInput(birthdayInput, birthdayText, 'Дата рождения');
                return true;
            }
        }
    
        const CheckPassword = () => {
            let passwordInput = document.getElementById('authorization-field-password');
            let passwordText = document.getElementById('authorization-p-password');
            let password = passwordInput.value;
            if (!ValidatePassword(password)) {
                UnvalidateInput(passwordInput, passwordText, 'Пароль не менее 6 символов');
                return false;
            } else {
                ValidateInput(passwordInput, passwordText, 'Введите пароль');
                return true;
            }
        }
        function rara(){
            console.log("aaaaaaaaaaaaaaaa")
        }
        function createUser(event) {
            // if(!CheckName() || !CheckTelephone() || !CheckEmail() || !CheckBirthday() || !CheckPassword()) {
            //     return;
            // }
            let username = document.getElementById('authorization-field-name').value;
            let phone_number = document.getElementById('authorization-field-phone').value;
            let email = document.getElementById('authorization-field-email').value;
            let birthdate = document.getElementById('authorization-field-birthday').value;
            let password = document.getElementById('authorization-field-password').value;
    
            let xhr = new XMLHttpRequest();
            let url = "http://127.0.0.1:8000/auth/jwt/register";
            
            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-Type", "application/json");
    
            xhr.onreadystatechange = function () {
            if (xhr.status === 201) {
                window.location.href = '/login'
            } else if (xhr.status === 400){
                let emailInput = document.getElementById('authorization-field-email');
                let emailText = document.getElementById('authorization-p-email');
                UnvalidateInput(emailInput, emailText, 'Уже зарегистрирован');
    
                
            } else {
                event.preventDefault();
                event.stopPropagation();
                console.log('Error');
            }
            
            }
    
            var data = JSON.stringify({ "username": username, "email": email, "password": password, "phone_number": phone_number, "birthdate": birthdate, "role_id": 0});
    
            xhr.send(data);
        }
    