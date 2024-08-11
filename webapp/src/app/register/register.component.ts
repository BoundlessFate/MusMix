import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { DefaultRegistrationsHandler } from '../loginsHandler';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent extends DefaultRegistrationsHandler {
  title = 'MusMix'
  constructor(private router: Router) {super();}

  override async register(event: Event){
    event.preventDefault(); 
    const username = (document.getElementById('uname') as HTMLInputElement).value;
    const password = (document.getElementById('pwd') as HTMLInputElement).value;
    const confirmpassword = (document.getElementById('conpwd') as HTMLInputElement).value;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    try {
      if (confirmpassword.localeCompare(password) != 0) {
        alert('Password and Confirm Password Do Not Match!');
        window.location.reload();
      }
      if (!(hasUppercase && hasLowercase && hasNumber)) {
        alert('Password Does Not Fulfill Requirements Below!');
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
}
