import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';


@Component({
  selector: 'app-recommended',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './recommendedPage.html',
  styleUrl: './recommended.css'
})

// adding in variables
export class RecommendedComponent {
  title = 'Recommended Page';
  constructor(private router: Router) { }
  ngOnInit() {
    this.searchRecommended();
  }
  async searchRecommended() {
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
    // Cookies found -- Search recommended as normal
      const response = await fetch('http://127.0.0.1:5000/recommended', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({details})
        })
        const data = await response.json();
      // (document.getElementById('outputString') as HTMLInputElement).innerHTML = data.message;


      (document.getElementById('out1') as HTMLInputElement).innerHTML = data.m1;
      (document.getElementById('out1') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out2') as HTMLInputElement).innerHTML = data.m2;
      (document.getElementById('out2') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out3') as HTMLInputElement).innerHTML = data.m3;
      (document.getElementById('out3') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out4') as HTMLInputElement).innerHTML = data.m4;
      (document.getElementById('out4') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out5') as HTMLInputElement).innerHTML = data.m5;
      (document.getElementById('out5') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out6') as HTMLInputElement).innerHTML = data.m6;
      (document.getElementById('out6') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out7') as HTMLInputElement).innerHTML = data.m7;
      (document.getElementById('out7') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out8') as HTMLInputElement).innerHTML = data.m8;
      (document.getElementById('out8') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out9') as HTMLInputElement).innerHTML = data.m9;
      (document.getElementById('out9') as HTMLInputElement).style.display = 'inline-block';

      (document.getElementById('out10') as HTMLInputElement).innerHTML = data.m10;
      (document.getElementById('out10') as HTMLInputElement).style.display = 'inline-block';
      (document.getElementById('caption') as HTMLInputElement).style.display = 'none';

      const caption = document.getElementById('caption') as HTMLInputElement;

      caption.innerHTML  = `<h2><i>Showing songs you might enjoy!</i></h2>`;
      alert("success");
      caption.style.display = 'flex';
      caption.style.position = 'absolute';
      caption.style.top = '18%';
  }
}