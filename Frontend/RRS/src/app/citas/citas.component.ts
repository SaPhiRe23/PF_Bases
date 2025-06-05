import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';
import { HttpClient } from '@angular/common/http';

interface Cita {
  id: number;
  usuario_id: number;
  servicio_id: number;
  fecha: string;
  hora: string;
  duracion: number;
  estado: string;
  notas?: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
  nombre_usuario?: string;
  nombre_servicio?: string;
}




@Component({
  selector: 'app-citas',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './citas.component.html',
  styleUrl: './citas.component.scss'
})
export class CitasComponent implements OnInit {
  citaForm!: FormGroup;
  servicios = [
    { id: 1, nombre: 'Corte de cabello' },
    { id: 2, nombre: 'Barba' },
    { id: 3, nombre: 'Corte + Barba' }
  ];
  citas: Cita[] = [];
  userId: number = 0;

  private fb = inject(FormBuilder);
  private authService = inject(AuthService);

  ngOnInit() {
    const userIdStr = this.authService.getUserId();
    if (userIdStr) {
      this.userId = Number(userIdStr);
      this.cargarCitas();
    }

    this.citaForm = this.fb.group({
      nombre: ['', Validators.required],
      fecha: ['', Validators.required],
      hora: ['', Validators.required],
      servicio: ['', Validators.required],
      notas: ['']
    });
  }

  agendarCita() {
    if (this.citaForm.invalid || !this.userId) return;

    const { fecha, hora, servicio, notas } = this.citaForm.value;

    const nuevaCita = {
      usuario_id: this.userId,
      servicio_id: Number(servicio),
      fecha: fecha,
      hora: hora,
      notas: notas || '',
    };

    this.authService.crearCita(nuevaCita).subscribe({
      next: (respuesta) => {
        alert('Cita agendada exitosamente.');
        this.citaForm.reset();
        this.cargarCitas();
      },
      error: (error) => {
        console.error(error);
        alert('Error al agendar la cita.');
      }
    });
  }

cargarCitas() {
  this.authService.obtenerCitas().subscribe(
    (todasLasCitas: any) => {
      this.citas = (todasLasCitas as Cita[]).filter(cita => cita.usuario_id === this.userId);
    },
    err => {
      console.error('Error cargando citas:', err);
    }
  );
}


  eliminarCita(id: number) {
    if (!confirm('¿Estás seguro de eliminar esta cita?')) return;

    this.authService.eliminarCita(id).subscribe({
      next: () => {
        alert('Cita eliminada.');
        this.cargarCitas();
      },
      error: err => {
        console.error(err);
        alert('No se pudo eliminar la cita.');
      }
    });
  }
}
