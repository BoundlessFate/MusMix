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
    let cleanedStr = details.replace(/^["']|["']$/g, ''); // Remove the quotes from the beginning and end
    let parts = cleanedStr.split(" ").filter(part => part !== ""); // Split by spaces and filter out empty parts
    let firstPart = parts[0];   
    user.innerHTML  = `<h2><i>"${firstPart}" </i></h2>`;
    user.style.display = 'block';
    //(document.getElementById('output') as HTMLInputElement).style.display = 'flex';
  }
}
