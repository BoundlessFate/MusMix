export interface cookieInterface {
    setCookie(value: string): Promise<void>;
}
export interface loginsHandler extends cookieInterface {
    login(event: Event): Promise<void>;
}
export interface registrationsHandler extends cookieInterface {
    register(event: Event): Promise<void>;
}

export class DefaultLoginsHandler implements loginsHandler {
    async login(event: Event){
        event.preventDefault(); 
    
        const username = (document.getElementById('uname') as HTMLInputElement).value;
        const password = (document.getElementById('pwd') as HTMLInputElement).value;
        console.log("Your Username Is " + username)
        console.log("Your Password Is " + password)
        try {
            const response = await fetch('https://musmix.site/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            if (response.ok) {
                alert('Login wouldve been successful!');
                // Default function will not set cookies or redirect
            } else {
                alert('Login wouldve failed.');
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

export class DefaultRegistrationsHandler implements registrationsHandler {
    // Default handler will not reload page or set cookies
    // Default handler also does not validate password is strong
    async register(event: Event){
        event.preventDefault(); 
        const username = (document.getElementById('uname') as HTMLInputElement).value;
        const password = (document.getElementById('pwd') as HTMLInputElement).value;
        try {
          const response = await fetch('https://musmix.site/register', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ username, password })
            });
          
          if (response.ok) {
              alert('Register woudlve been successful!');
          } else {
              alert('Register wouldve failed.');
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