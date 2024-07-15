import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './profilePage.html',
  styleUrl: './profilePage.css'
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
        this.router.navigate(['/']);
    }
    // Cookies found -- Run as normal
  }
}
