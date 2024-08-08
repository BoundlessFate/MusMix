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
    this.checkForPhotoUpload();
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
      const response = await fetch('http://127.0.0.1:5000/getProfileData', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ details })
        });
      
      if (response.ok) {
        const result = await response.json();
        if (result.description) {
          (document.getElementById('description') as HTMLInputElement).value = result.description;
          console.log("description set");
        } else {
          console.log("description not set");
        }
        if (result.photo) {
          const photoElement = (document.getElementById('profilePhoto') as HTMLImageElement);
          console.log(result.photo)
          photoElement.src = 'https://musmix.site/uploads/' + result.photo;
          console.log("photo set");
        } else {
          console.log("photo not set");
        }
        if (result.favorite_songs) {
          (document.getElementById('favorite_songs') as HTMLParagraphElement).textContent = result.favorite_songs;
          console.log("favorite songs set");
        } else {
          console.log("favorite songs not set");
        }
        if (result.favorite_genres) {
          (document.getElementById('favorite_genres') as HTMLInputElement).textContent = result.favorite_genres;
          console.log("favorite genres set");
        } else {
          console.log("favorite genres not set");
        } 
      } else {
        console.log("user couldnt be found");
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
      const response = await fetch('http://127.0.0.1:5000/setProfileData', {
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
  async checkForPhotoUpload() {
    console.log("hi")
    document.getElementById('photoInput')?.addEventListener('change', (event: Event) => {
      const fileInput = event.target as HTMLInputElement;
      const file = fileInput.files?.[0];
      if(file) {
        const approvedExtensions = ['jpg', 'jpeg', 'png'];
        const curExtension = file.name.split('.')[1];
        if (!approvedExtensions.includes(curExtension)) {
          alert('Incorrect file type! Only use jpg, jpeg, or png');
          window.location.reload();
        }
        if (file.size > 1024*1024) {
          alert('File Size Too Large! Max size is 1MB');
          window.location.reload();
        }
      }
      // After validating the uploaded file is correct, push to the google
      this.uploadPhoto();
    });
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

  async uploadPhoto() {
    console.log("hi2")
    const fileInput = document.getElementById('photoInput') as HTMLInputElement;
    const file = fileInput.files ? fileInput.files[0] : null;
    // Get details from cookies
    var details = "";
    const cookieName = "login=";
    const allCookies = document.cookie.split(';');
    for (let i = 0; i < allCookies.length; i++) {
      let c = allCookies[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(cookieName) === 0) { details = c.substring(cookieName.length, c.length); }
    }
    if (!file) {
        alert('Please select a photo to upload.');
        return;
    }
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('details', details);
      const response = await fetch('http://127.0.0.1:5000/uploadPhoto', {
          method: 'POST',
          body: formData
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
