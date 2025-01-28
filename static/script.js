document.getElementById('generateBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default form submission

    const genre = document.getElementById('genre').value;
    const topic = document.getElementById('topic').value;

    if (!genre || !topic) {
        alert("Please enter both genre and topic!");
        return;
    }

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Changed to form data
        },
        body: new URLSearchParams({ // Use URLSearchParams for form data
            genre: genre,
            topic: topic
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) }); // Handle non-2xx responses
        }
        return response.json();
    })
    .then(data => {
        if (data.book_idea) {
            window.location.href = `/results?genre=${encodeURIComponent(data.genre)}&topic=${encodeURIComponent(data.topic)}&book_idea=${encodeURIComponent(data.book_idea)}`; //Corrected URL and added genre and topic
        } else {
            alert('Error generating book idea: ' + data.error);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});