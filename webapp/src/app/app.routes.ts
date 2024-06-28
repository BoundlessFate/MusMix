import { CommonModule } from '@angular/common';
import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SearchComponent } from './search.component';

export const routes: Routes = [
    { path: '', redirectTo: '/mainPage', pathMatch: 'full'},
    { path: 'mainPage', component: AppComponent },
    { path: 'login', component: LoginComponent },
    { path: 'searchPage', component: SearchComponent}
];