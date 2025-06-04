import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: 'citas', loadComponent: () => import('./citas/citas.component').then(m => m.CitasComponent) },
    {path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) },
    {path: 'register', loadComponent: () => import('./register/register.component').then(m => m.RegisterComponent) },
    {path: 'home', loadComponent: () => import('./home/home.component').then(m => m.HomeComponent) },
    {path: '', redirectTo: '/home', pathMatch: 'full'},
];
