import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-recommended',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './recommendedPage.html',
  styleUrls: ['./recommended.css']
})
export class RecommendedComponent implements OnInit {
  title = 'Recommended Page';

  constructor(private router: Router) { }

  ngOnInit() {
    this.searchRecommended();
  }

  async searchRecommended() {
    let details = '';
    const cookieName = 'login=';
    const allCookies = document.cookie.split(';');
    for (let i = 0; i < allCookies.length; i++) {
      let c = allCookies[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(cookieName) === 0) { details = c.substring(cookieName.length, c.length); }
    }
    if (details === '') {
      // Cookie not found -- Redirect to login
      alert('Not logged in!');
      this.router.navigate(['/login']);
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/recommended', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ details })
      });
      const data = await response.json();

      if (response.ok) {
        this.updateContent(data);
        this.showCaption('<h2><i>Showing songs you might enjoy!</i></h2>', 'white');
      } else {
        this.showCaption('<h2><i>No results found... Search More Songs!</i></h2>', 'white');
      }
    } catch (error) {
      console.error('Error during song search:', error);
      this.showCaption('<h2><i>Error fetching data. Please try again later.</i></h2>', 'white');
    }
  }

  updateContent(data: any) {
    const outElementIds = [
      'out1', 'out2', 'out3', 'out4', 'out5',
      'out6', 'out7', 'out8', 'out9', 'out10'
    ];

    outElementIds.forEach((id, index) => {
      const element = document.getElementById(id) as HTMLDivElement;

      if (element) {
        element.innerHTML = data[`m${index + 1}`];
        element.style.display = 'inline-block';

        const image = element.querySelector('img') as HTMLImageElement;
        if (image) {
          image.style.width = '50%';
          image.style.height = '50%';
          image.style.objectFit = 'cover';
          image.style.borderRadius = '10px';
        }

        const h3 = element.querySelector('h3') as HTMLElement;
        const i = element.querySelector('i') as HTMLElement;
        if (h3) {
          h3.style.fontSize = '15px';
          h3.style.color = 'white';
        }
        if (i) {
          i.style.fontSize = '15px';
          i.style.color = 'white';
        }
      }
    });
  }

  showCaption(content: string, color: string) {
    const caption = document.getElementById('caption') as HTMLElement;
    if (caption) {
      caption.innerHTML = content;
      caption.style.color = color;
      caption.style.display = 'flex';
      caption.style.position = 'absolute';
      caption.style.top = '18%';
    }
  }
}
