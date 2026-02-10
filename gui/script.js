async function analyzeLog() {
    const stderr = document.getElementById("stderr").value;
    const stdout = document.getElementById("stdout").value;
    const exitCode = parseInt(document.getElementById("exitCode").value);

    if (isNaN(exitCode)) {
        alert("Please enter a valid exit code");
        return;
    }

    const payload = {
        stderr: stderr,
        stdout: stdout,
        exit_code: exitCode
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        document.getElementById("output").textContent =
            JSON.stringify(data, null, 2);

        document.getElementById("result").classList.remove("hidden");

    } catch (error) {
        alert("Failed to connect to backend");
    }
}
