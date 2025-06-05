import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-empresa',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './empresa.component.html',
  styleUrls: ['./empresa.component.scss']
})
export class EmpresaComponent implements OnInit {
  citas: any[] = [];

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.cargarCitas();
  }

  cargarCitas() {
    this.authService.obtenerCitas().subscribe({
      next: (data: any) => {
        this.citas = data;
      },
      error: err => {
        console.error('Error al obtener citas:', err);
      }
    });
  }

  eliminarCita(id: number) {
    this.authService.eliminarCita(id).subscribe({
      next: () => {
        this.citas = this.citas.filter(c => c.id !== id);
      },
      error: err => {
        console.error('Error al eliminar cita:', err);
      }
    });
  }
}
