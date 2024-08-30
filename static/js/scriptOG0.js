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



document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('transferForm');
    const progressBarContainer = document.querySelector('.progress-bar__container');
  
    form.addEventListener('submit', (event) => {
      event.preventDefault(); // Prevent form submission for demo purposes
  
      progressBarContainer.style.display = 'block'; // Show the progress bar
  
      fetch('/start')  // Start the testint increment on the server
          .then(() => {
              updateProgressBar();  // Start updating the progress bar
          });
    });
  });