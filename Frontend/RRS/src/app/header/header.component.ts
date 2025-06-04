import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // ✅ FALTABA ESTO

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule], // ✅ AGREGA RouterModule AQUÍ
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  constructor(private router: Router) {}

  logout() {
    localStorage.removeItem('auth');
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token') !== null;
    }
    return false;
  }
}
