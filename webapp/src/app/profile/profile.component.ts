import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './profile.html',
  styleUrls: ['./profile.css'] // Corrected from 'styleUrl' to 'styleUrls'
})

export class ProfileComponent {
  title = 'MusMix';
  constructor(private router: Router) { }
  ngOnInit() {
    this.checkForCookie();
    this.getProfileData();
  }
  async getProfileData(){ 
    // Get details from cookies
    var details = "";
    const cookieName = "login=";
    const allCookies = document.cookie.split(';');
    for (let i = 0; i < allCookies.length; i++) {
      let c = allCookies[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(cookieName) === 0) { details = c.substring(cookieName.length, c.length); }
    }
    try {
      const response = await fetch('https://198.199.84.208:5000/getProfileData', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ details })
        });
      
      if (response.ok) {
        const result = await response.json();
        (document.getElementById('description') as HTMLInputElement).value = result.message;
        console.log("description set");
      } else {
        console.log("description not set yet");
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  async setProfileData(event: Event){
    event.preventDefault(); 
    const description = (document.getElementById('description') as HTMLInputElement).value;
    // Get details from cookies
    var details = "";
    const cookieName = "login=";
    const allCookies = document.cookie.split(';');
    for (let i = 0; i < allCookies.length; i++) {
      let c = allCookies[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(cookieName) === 0) { details = c.substring(cookieName.length, c.length); }
    }
    try {
      const response = await fetch('https://musmix.site/setProfileData', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ description, details })
        });
      
      if (response.ok) {
          alert('Data set successfully!');
      } else {
          alert('Error during data upload.');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  async checkForCookie() {
    var details = "";
    const cookieName = "login=";
    const allCookies = document.cookie.split(';');
    for (let i = 0; i < allCookies.length; i++) {
      let c = allCookies[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(cookieName) === 0) { details = c.substring(cookieName.length, c.length); }
    }
    if (details === "") {
        // Cookie not found -- Redirect to login
        alert('Not logged in!');
        this.router.navigate(['/login']);
        return;
    }
    alert('Logged In!');
    // Cookies found -- Run as normal
    const user = document.getElementById('username') as HTMLInputElement;
    let str = details.replace(/"/g, '').split(" ").filter(part => part !== "")[0]; // Remove the quotes from the beginning and end
    user.innerHTML  = `<h4>${str}</h4>`;
    user.style.display = 'block';
    //(document.getElementById('output') as HTMLInputElement).style.display = 'flex';
  }
}
// upload.ts

// Ensure the DOM is fully loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', () => {
  const photoInput = document.getElementById('photoInput') as HTMLInputElement;
  photoInput.addEventListener('change', previewPhoto);
});

function previewPhoto(event: Event): void {
  const input = event.target as HTMLInputElement;
  const fileNameDisplay = document.getElementById('fileName') as HTMLParagraphElement;

  if (input.files && input.files[0]) {
      const file = input.files[0];
      fileNameDisplay.textContent = `Selected file: ${file.name}`;
      const reader = new FileReader();

      reader.onload = (e: ProgressEvent<FileReader>) => {
          const profilePhoto = document.getElementById('profilePhoto') as HTMLImageElement;
          if (e.target && typeof e.target.result === 'string') {
              profilePhoto.src = e.target.result;
          }
      };

      reader.readAsDataURL(file);
  } else {
      fileNameDisplay.textContent = '';
  }
}

function uploadPhoto(): void {
  const fileInput = document.getElementById('photoInput') as HTMLInputElement;
  const file = fileInput.files ? fileInput.files[0] : null;

  if (!file) {
      alert('Please select a photo to upload.');
      return;
  }

  const formData = new FormData();
  formData.append('photo', file);

  fetch('YOUR_SERVER_UPLOAD_ENDPOINT', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      alert('Photo uploaded successfully.');
  })
  .catch(error => {
      console.error('Error:', error);
      alert('Failed to upload photo.');
  });
}
