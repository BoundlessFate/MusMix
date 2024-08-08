import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  title = 'MusMix'
  constructor(private router: Router) { }

  async register(event: Event){
    event.preventDefault(); 
    const username = (document.getElementById('uname') as HTMLInputElement).value;
    const password = (document.getElementById('pwd') as HTMLInputElement).value;
    const confirmpassword = (document.getElementById('conpwd') as HTMLInputElement).value;
    try {
      if (confirmpassword.localeCompare(password) != 0) {
        alert('Password and Confirm Password Do Not Match!');
        window.location.reload();
      }
      const response = await fetch('https://musmix.site/register', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });
      
      if (response.ok) {
          alert('Register successful!');
          this.setCookie(username+" "+password);
          this.router.navigate(['/']);
      } else {
          alert('Register failed.');
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
