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
			handleResponse(data);
		});
}

function handleResponse(response) {
	if (response.success) {
		alert(response.message);
		window.location.href = "/auth/login";
	} else {
		alert(response.message);
	}
}
