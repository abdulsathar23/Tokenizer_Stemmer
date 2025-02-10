document.getElementById('submitButton').addEventListener('click', function() {
    const name = document.getElementById('name').value;
    const rollno = document.getElementById('rollno').value;
    const inputText = document.getElementById('inputText').value;
    
    if (name.trim() === "" || rollno.trim() === "" || inputText.trim() === "") {
        alert("Please fill out all fields.");
        return;
    }

    fetch('/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'name=' + encodeURIComponent(name) + '&rollno=' + encodeURIComponent(rollno) + '&text=' + encodeURIComponent(inputText),
    })
    .then(response => response.json())
    .then(data => {
        // Displaying user info
        document.getElementById('userName').textContent = data.Name;
        document.getElementById('userRollNo').textContent = data['Roll Number'];
        document.getElementById('userDate').textContent = data.Date;

        // Clearing the previous table content
        const resultTable = document.getElementById('resultTable').getElementsByTagName('tbody')[0];
        resultTable.innerHTML = ''; 

        // Adding the tokenization and stemming results
        data.Results.forEach(item => {
            const row = resultTable.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            cell1.textContent = item.Tokenization;
            cell2.textContent = item.Stemming;
        });
    })
    .catch(error => console.error('Error:', error));
});
