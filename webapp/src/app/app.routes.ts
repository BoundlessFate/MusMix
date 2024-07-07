import { CommonModule } from '@angular/common';
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { SearchComponent } from './search/search.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'login', component: LoginComponent },
    { path: 'searchPage', component: SearchComponent}
];