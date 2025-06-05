import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: 'citas', loadComponent: () => import('./citas/citas.component').then(m => m.CitasComponent) },
    {path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) },
    {path: 'register', loadComponent: () => import('./register/register.component').then(m => m.RegisterComponent) },

    {
    path: 'dashboard',
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent),
    children: [
      {
        path: 'admin',
        loadComponent: () => import('./dashboard/admin/admin.component').then(m => m.AdminComponent),
      },
      {
        path: 'empresa',
        loadComponent: () => import('./dashboard/empresa/empresa.component').then(m => m.EmpresaComponent),
      },
    ]
  },

    {path: 'home', loadComponent: () => import('./home/home.component').then(m => m.HomeComponent) },
    {path: '', redirectTo: '/home', pathMatch: 'full'},
];
