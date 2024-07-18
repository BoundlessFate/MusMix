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
  finalString = "";
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
      const response = await fetch('http://127.0.0.1:5002/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name, artist })
        })
        const data = await response.json();
      this.finalString = data.message;
      alert("success");
    } catch (error) {
      console.error('Error:', error);
      alert("error");
      window.location.reload();
      this.finalString = "";
    }
  }
}