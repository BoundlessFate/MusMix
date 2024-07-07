import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './searchPage.html',
  styleUrl: './search.css'
})

// adding in variables
export class SearchComponent {
  title = 'Search Page';
  username = "NEW USER"
}

console.log("hi");
window.addEventListener('DOMContentLoaded', (event) => {
  const searchInput = document.getElementById('input') as HTMLInputElement;

  searchInput.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
          alert('You have submitted a song with query: ' + searchInput.value);
      }
  });
});

