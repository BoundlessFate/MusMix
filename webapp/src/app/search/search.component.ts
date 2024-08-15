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
      const searchButton = document.getElementById('searchButton') as HTMLButtonElement;
  
      // assures that when "enter" is pressed, the backend algorithm for finding similar songs begins
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

      // Trigger search when the search button is clicked
      searchButton.addEventListener('click', () => {
        console.log("search button clicked");

        this.search_song();
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
      //fetch algorithm output from backend
      const response = await fetch('https://musmix.site/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: body
        })
        const data = await response.json();

      //list of elements holding album art / artist name / song name
      const outElementIds = [
        'out1', 'out2', 'out3', 'out4', 'out5',
        'out6', 'out7', 'out8', 'out9', 'out10'
      ];

      //parse through elements and make them visable / fade in
      outElementIds.forEach((id, index) => {
        const element = document.getElementById(id) as HTMLDivElement; 

        if (element) {
            element.innerHTML = data[`m${index + 1}`]; 

            element.style.display = 'inline-block';

            const image = element.querySelector('img') as HTMLImageElement;
            if (image) {
                //make all images the same size with a border radius
                image.style.width = '50%';   
                image.style.height = '50%'; 
                image.style.objectFit = 'cover';
                image.style.borderRadius = '10px'; 
            }
            //select all h3 and i elements (aka elements that arent images)
            const h3 = element.querySelector('h3') as HTMLImageElement;
            const i = element.querySelector('i') as HTMLImageElement;
            if(h3 || i){
              //set fond sizes and font colors
              h3.style.fontSize = '15px';
              i.style.fontSize = '15px';
              h3.style.color='white';
              i.style.color='white';

            }
        }
      });

      //make the input fields disappear
      (document.getElementById('songInput') as HTMLInputElement).style.display = 'none';
      (document.getElementById('artistInput')as HTMLInputElement).style.display = 'none';
      (document.getElementById('searchButton') as HTMLButtonElement).style.display = 'none';

      //change color of caption
      const caption = document.getElementById('caption') as HTMLInputElement;
      caption.style.color='white';

      //change the text in caption depending on if the song was found
      if (data.song == undefined && data.artist == undefined) {
        caption.innerHTML  = `<h2><i>Showing similar songs to "${name}" by ${artist}</i></h2>`;
      }else{
        caption.innerHTML  = `<h2><i>Showing similar songs to "${data.song}" by ${data.artist}</i></h2>`;
      }

      //change caption styling
      caption.style.position = 'absolute';
      caption.style.top = '18%';

    } catch (error) {
      console.error('Error:', error);
      alert("We searched everywhere under the sun, and no songs could be found!");
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

  // Add keydown event listener for "Enter" on songInput and artistInput
  songInput.addEventListener('keydown', async (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
          e.preventDefault(); // Prevent form submission if inside a form
          await search_song();
      }
  });

  //event listener for "enter" key
  artistInput.addEventListener('keydown', async (e: KeyboardEvent) => {
      if (e.key === 'Enter') { 
          //add an await so that the delay does not begin until the songs have been found
          await search_song();
      }
  });

  async function search_song(): Promise<void> {
      try {
          //simulate delay from fetching data from an API
          await new Promise((resolve) => setTimeout(resolve, 1000)); 

          //parse all "out" elements
          const elements = document.querySelectorAll('[id^="out"]');
          elements.forEach((element, index) => {
            const delay = index * 0.2 +3.5; // Stagger delays
            const elementStyle = element as HTMLElement;

            // Start elements as hidden
            elementStyle.style.opacity = '0'; 
             // Transition with delay
            elementStyle.style.transition = `opacity 1s ease-in-out ${delay}s`;
            // Set opacity to 1 (full opacity)
            elementStyle.style.opacity = '1';
        });
      } catch (error) {
          console.error('Error during song search:', error);
      }
  }
});