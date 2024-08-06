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
      (document.getElementById('bottom-left') as HTMLInputElement).style.display='none';
      console.log(name)
      console.log(artist)
      const response = await fetch('https://musmix.site/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name, artist })
        })
        const data = await response.json();
      // (document.getElementById('outputString') as HTMLInputElement).innerHTML = data.message;


    // Array of element IDs
      const outElementIds = [
        'out1', 'out2', 'out3', 'out4', 'out5',
        'out6', 'out7', 'out8', 'out9', 'out10'
      ];

      // Loop through each element ID and apply styles and content
      outElementIds.forEach((id, index) => {
        const element = document.getElementById(id) as HTMLDivElement; // Use HTMLDivElement instead of HTMLInputElement

        if (element) {
            element.innerHTML = data[`m${index + 1}`]; // Set the content from data object

            element.style.display = 'inline-block';


            // Specific styles for the image inside the element with id 'out1'
            const image = element.querySelector('img') as HTMLImageElement;
            if (image) {
                image.style.width = '50%';   // Adjust width as needed
                image.style.height = '50%';  // Adjust height as needed
                image.style.objectFit = 'cover'; // Ensure the image covers the set dimensions
                image.style.borderRadius = '10px'; // Optional: rounded corners
            }
            const h3 = element.querySelector('h3') as HTMLImageElement;
            const i = element.querySelector('i') as HTMLImageElement;
            if(h3 || i){
              h3.style.marginTop = '10px';
              h3.style.fontSize = '15px';
              i.style.fontSize = '15px';
              h3.style.margin = '0px';
              i.style.margin = '0px';
              h3.style.padding = '0px';
              i.style.padding = '0px';
              i.style.marginTop = '-10px';
              h3.style.color='white';
              i.style.color='white';

            }
        }
      });




      (document.getElementById('songInput') as HTMLInputElement).style.display = 'none';
      (document.getElementById('artistInput')as HTMLInputElement).style.display = 'none';
      (document.getElementById('caption') as HTMLInputElement).style.display = 'none';

      const caption = document.getElementById('caption') as HTMLInputElement;
      caption.style.color='white';

      if (data.song == undefined && data.artist == undefined) {
        caption.innerHTML  = `<h2><i>Showing similar songs to "${name}" by ${artist}</i></h2>`;
      }else{
        caption.innerHTML  = `<h2><i>Showing similar songs to "${data.song}" by ${data.artist}</i></h2>`;
      }

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
document.addEventListener('DOMContentLoaded', () => {
  const searchButton = document.getElementById('searchButton');
  const songInput = document.getElementById('songInput') as HTMLInputElement;
  const artistInput = document.getElementById('artistInput') as HTMLInputElement;

  // Add click event listener to the search button
  searchButton?.addEventListener('click', async () => {
      await search_song();
  });

  // Add keydown event listener for Enter key on songInput
  songInput.addEventListener('keydown', async (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
          e.preventDefault(); // Prevent form submission if inside a form
          await search_song();
      }
  });

  // Add keydown event listener for Enter key on artistInput
  artistInput.addEventListener('keydown', async (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
          e.preventDefault(); // Prevent form submission if inside a form
          await search_song();
      }
  });

  async function search_song(): Promise<void> {
      try {
          // Simulate an async search operation (e.g., fetching data from an API)
          await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulating delay

          const elements = document.querySelectorAll('[id^="out"]');
          elements.forEach((element, index) => {
            const delay = index * 0.5 +2; // Stagger delay in seconds
            const elementStyle = element as HTMLElement;

            elementStyle.style.opacity = '0'; // Start hidden
            elementStyle.style.transition = `opacity 1s ease-in-out ${delay}s`; // Transition with delay

            // Force a reflow to ensure transition is applied
            void elementStyle.offsetWidth; // Trigger reflow

            // Set opacity to 1 to trigger fade-in
            elementStyle.style.opacity = '1';
        });
      } catch (error) {
          console.error('Error during song search:', error);
      }
  }
});
