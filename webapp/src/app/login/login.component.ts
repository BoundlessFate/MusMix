import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router'
import { DefaultLoginsHandler } from '../loginsHandler';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent extends DefaultLoginsHandler {
  constructor(private router: Router) {super();}
  title = 'MusMix'
  override async login(event: Event){
    event.preventDefault(); 

    const username = (document.getElementById('uname') as HTMLInputElement).value;
    const password = (document.getElementById('pwd') as HTMLInputElement).value;
    try {
        const response = await fetch('https://musmix.site/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            alert('Login success');
            this.setCookie(username+" "+password);
            this.router.navigate(['/']);
        } else {
            alert('Incorrect username or password');
            window.location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
    }
  }
}
