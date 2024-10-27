async function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch('/api/logreg/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        alert(data.message); // Display success message
        location.replace("/");
    } else {
        const error = await response.json();
        alert(error.message); // Display error message if login failed
    }
}
async function signup() {
    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;
    const role = document.getElementById("userRole").value;
    console.log(username)
    console.log(password)
    console.log(role)
    try {
        const response = await fetch('/api/logreg/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Include cookies with the request
            body: JSON.stringify({ username, password, role })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message); // Success message for user creation
        } else {
            alert(data.message); // Error message, e.g., insufficient permissions
        }
    } catch (error) {
        console.error( error);
        alert(`Виникла помилка під час реєстрації. ${error}`);
    }
}
async function get_password() {
    const username = document.getElementById("loginUsername").value;
    const response = await fetch('/api/logreg/get-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username })
    });

    if (response.ok) {
        const data = await response.json();
        alert("Ваш пароль: " + data); 
        // Redirect to another page or perform additional actions if needed
    } else {
        const error = await response.json();
        alert(error.message); // Display error message if login failed
    }
}