import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router'


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  constructor(private router: Router) { }
  title = 'MusMix'
  async login(event: Event){
    event.preventDefault(); 

    const username = (document.getElementById('uname') as HTMLInputElement).value;
    const password = (document.getElementById('pwd') as HTMLInputElement).value;
    try {
        const response = await fetch('http://127.0.0.1:80/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            alert('Login successful!');
            this.setCookie(username+" "+password);
            this.router.navigate(['/']);
        } else {
            alert('Login failed.');
            window.location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
    }
  }
  async setCookie(value: string) {
    const date = new Date();
    date.setTime(date.getTime() + (6*60*60*1000)); // Set cookies to reset after 6 hours
    const expires = "expires=" + date.toUTCString();
    document.cookie = `login=${value}; ${expires}; path=/`;
  }
}
