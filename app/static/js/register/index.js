document.addEventListener("DOMContentLoaded", () => {
	document
		.getElementById("register-button")
		.addEventListener("click", register);
});

function register() {
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
			console.log(data);
		});
}

function handleResponse(response) {
	if (response.success) {
		window.location.href = "/auth/login";
	} else {
		alert(response.message);
	}
}
