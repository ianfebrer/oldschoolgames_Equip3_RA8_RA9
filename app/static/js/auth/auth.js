function register(event) {
	event.preventDefault();
	const username = document.getElementById("username").value;
	const password = document.getElementById("password").value;
	fetch("/auth/api/register", {
		method: "POST",
		body: JSON.stringify({ username: username, password: password }),
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then((response) => response.json())
		.then((data) => {
			handleResponseRegister(data);
		});
}

function login(event) {
	event.preventDefault();
	const username = document.getElementById("username").value;
	const password = document.getElementById("password").value;
	fetch("/auth/api/login", {
		method: "POST",
		body: JSON.stringify({ username: username, password: password }),
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then((response) => response.json())
		.then((data) => {
			handleResponseLogin(data);
		});
}

function handleResponseRegister(response) {
	if (response.success) {
		alert(response.message);
		window.location.href = "/auth/login";
	} else {
		alert(response.message);
	}
}

function handleResponseLogin(response) {
	if (response.success) {
		alert(response.message);
		window.location.href = "/";
	} else {
		alert(response.message);
	}
}
