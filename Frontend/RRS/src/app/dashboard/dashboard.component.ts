import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {

  tipoUsuario: string | null = null;

  constructor(private router: Router) {}

  ngOnInit() {
    const role = localStorage.getItem('role');

    if (role === 'admin') {
      this.router.navigate(['/dashboard/admin']);
    } else if (role === 'empresa') {
      this.router.navigate(['/dashboard/empresa']);
    } else {
      this.router.navigate(['/login']); // fallback por seguridad
    }
  }
}

