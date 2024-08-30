function updateProgressBar() {
    fetch('/progress')
        .then(response => response.json())
        .then(data => {
            const testint = data.testint;
            const progressBar = document.querySelector('.progress-bar');
            const progressBarText = document.querySelector('.progress-bar__text');
            
            // Update the text immediately
            progressBarText.innerText = `${testint}%`;
            
            // Update the width of the progress bar
            gsap.to(progressBar, {
                width: `${testint}%`,
                duration: 1.0,
                backgroundColor: testint >= 100 ? '#4895ef' : '#e76f51'
            });

            if (testint < 101) {
                setTimeout(updateProgressBar, 100); // Poll every 0.5 second
            } else {
                progressBarText.innerText = "Uploaded Successfully!";
                progressBar.style.backgroundColor = '#4895ef'; // Ensure the final color
            }
        });
}

// Start the progress bar when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetch('/start')  // Start the testint increment on the server
        .then(() => {
            updateProgressBar();  // Start updating the progress bar
        });
});




//for authentication of Password and RSA Key File
    document.getElementById('loginform').addEventListener('submit', function(event) {
        // Get the password and file input elements
        var password = document.getElementById('password').value.trim();
        var keyfile = document.getElementById('keyfile').files.length;
        var os = document.getElementById('os').value;
        var isOsSelected = os !== "";


        // Check if either password or keyfile is provided
        if (!password && !keyfile) {
            alert('Please enter a password or upload an RSA key file.');
            event.preventDefault(); // Prevent form submission
        }


        if (!isOsSelected) {
            alert('Please enter a password or upload an RSA key file.');
            // osErrorMessage.style.display = 'block';
            event.preventDefault(); // Prevent form submission
        } 



    });




    document.getElementById('folderInput').addEventListener('change', function(event) {
        const files = event.target.files;
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '';  // Clear previous file list
        
        if (files.length === 0) {
            document.getElementById('folderPath').textContent = 'No folder selected';
            return;
        }

        // Display file paths
        let filePaths = new Set(); // Use Set to avoid duplicates
        for (const file of files) {
            filePaths.add(file.webkitRelativePath);
        }

        document.getElementById('folderPath').textContent = 'Selected folder contents:';
        filePaths.forEach(path => {
            const li = document.createElement('li');
            li.textContent = path;
            fileList.appendChild(li);
        });
    });