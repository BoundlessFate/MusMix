import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-search',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './searchPage.html',
  styleUrl: './search.css'
})

// adding in variables
export class SearchComponent {
  title = 'Search Page';
  ngOnInit() {
    this.checkForSubmission();
  }
  async checkForSubmission() {
    console.log("hi");
    window.addEventListener('DOMContentLoaded', (event) => {
      const songInput = document.getElementById('songInput') as HTMLInputElement;
      const artistInput = document.getElementById('artistInput') as HTMLInputElement;
  
      songInput.addEventListener('keydown', (e: KeyboardEvent) => {
          if (e.key === 'Enter') {
              console.log("pressed enter")
              this.search_song()
          }
      });
      artistInput.addEventListener('keydown', (e: KeyboardEvent) => {
        if (e.key === 'Enter') {
            console.log("pressed enter")
            this.search_song()
        }
    });
    });
  }
  async search_song() {
    try {
      const name = (document.getElementById('songInput') as HTMLInputElement).value;
      const artist = (document.getElementById('artistInput') as HTMLInputElement).value;
      console.log(name)
      console.log(artist)
      var details = "";
      const cookieName = "login=";
      const allCookies = document.cookie.split(';');
      for (let i = 0; i < allCookies.length; i++) {
        let c = allCookies[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(cookieName) === 0) { details = c.substring(cookieName.length, c.length); }
      }
      var body;
      if (details === "") {
        body = JSON.stringify({ name, artist })
      } else {
        body = JSON.stringify({ name, artist, details })
      }
      const response = await fetch('http://127.0.0.1:5000/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: body
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



      (document.getElementById('songInput') as HTMLInputElement).style.display = 'none';
      (document.getElementById('artistInput')as HTMLInputElement).style.display = 'none';
      (document.getElementById('caption') as HTMLInputElement).style.display = 'none';

      const caption = document.getElementById('caption') as HTMLInputElement;

      if (data.song == undefined && data.artist == undefined) {
        caption.innerHTML  = `<h2><i>Showing similar songs to "${name}" by ${artist}</i></h2>`;
      }else{
        caption.innerHTML  = `<h2><i>Showing similar songs to "${data.song}" by ${data.artist}</i></h2>`;
      }
      alert("success");
      caption.style.display = 'flex';
      caption.style.position = 'absolute';
      caption.style.top = '18%';

    } catch (error) {
      console.error('Error:', error);
      alert("error");
      window.location.reload();
    }
  }
}