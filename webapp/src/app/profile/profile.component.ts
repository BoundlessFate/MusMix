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
      const response = await fetch('http://127.0.0.1:5004/getProfileData', {
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
      const response = await fetch('http://127.0.0.1:5003/setProfileData', {
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
  }
}
