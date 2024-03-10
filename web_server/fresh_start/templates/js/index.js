document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const input = document.getElementById('name');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const name = input.value; // Get the input value
        const data = { name: name }; // Prepare the data object

        // Send a POST request
        fetch('/', { // You should replace '/' with the URL you wish to send the request to
            method: 'POST', // Set the request method to POST
            headers: {
                'Content-Type': 'application/json', // Specify the content type as JSON
            },
            body: JSON.stringify(data), // Convert the JavaScript object to a JSON string
        })
        .then(response => response.json()) // Convert the response to JSON
        .then(data => {
            console.log('Success:', data); // Handle success
        })
        .catch((error) => {
            console.error('Error:', error); // Handle errors
        });
    });
});