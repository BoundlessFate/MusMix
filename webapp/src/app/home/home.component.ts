import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './homePage.html',
  styleUrl: './homePage.css'
})
export class HomeComponent {
  title = 'MusMix';
}
