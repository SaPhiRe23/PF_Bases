import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: 'citas', loadComponent: () => import('./citas/citas.component').then(m => m.CitasComponent) },
    {path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) },
    {path: 'dashboard', loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent)},
    {path: 'dashboard/admin', loadComponent: () => import('./dashboard/admin/admin.component').then(m => m.AdminComponent)},
    {path: 'dashboard/empresa', loadComponent: () => import('./dashboard/empresa/empresa.component').then(m => m.EmpresaComponent)},
    {path: 'home', loadComponent: () => import('./home/home.component').then(m => m.HomeComponent) },
    {path: '', redirectTo: '/home', pathMatch: 'full'},
];
