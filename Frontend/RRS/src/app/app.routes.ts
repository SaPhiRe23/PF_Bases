import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: 'citas', loadComponent: () => import('./citas/citas.component').then(m => m.CitasComponent) },
    {path: 'home', loadComponent: () => import('./home/home.component').then(m => m.HomeComponent) },
    {path: '', redirectTo: '/home', pathMatch: 'full'},
];
