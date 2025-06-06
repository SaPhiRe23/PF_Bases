import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';

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
  styleUrls: ['./citas.component.scss']
})
export class CitasComponent implements OnInit {
  citaForm!: FormGroup;
  servicios: any[] = [];
  citas: Cita[] = [];
  userId: number | null = null;
  loading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  ngOnInit() {
    this.initForm();
    this.loadServices();
    this.checkAuthentication();
  }

  private initForm() {
    this.citaForm = this.fb.group({
      nombre: ['', Validators.required],
      fecha: ['', Validators.required],
      hora: ['', Validators.required],
      servicio: ['', Validators.required],
      notas: ['']
    });
  }

  private checkAuthentication() {
    const userIdStr = this.authService.getUserId();
    if (!userIdStr || !this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    this.userId = Number(userIdStr);
    this.cargarCitas();
  }

  private loadServices() {
    this.loading = true;
    this.authService.obtenerServicios().subscribe({
      next: (servicios) => {
        this.servicios = servicios;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando servicios:', err);
        this.errorMessage = 'No se pudieron cargar los servicios';
        this.loading = false;
      }
    });
  }

  agendarCita() {
    if (this.citaForm.invalid || !this.userId || this.loading) return;

    this.loading = true;
    this.errorMessage = null;
    this.successMessage = null;

    const { fecha, hora, servicio, notas } = this.citaForm.value;

    const nuevaCita = {
      usuario_id: this.userId,
      servicio_id: Number(servicio),
      fecha: fecha,
      hora: hora,
      notas: notas || '',
    };

    this.authService.crearCita(nuevaCita).subscribe({
      next: () => {
        this.successMessage = 'Cita agendada exitosamente';
        this.citaForm.reset();
        this.cargarCitas();
        this.loading = false;
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = error.error?.message || 'Error al agendar la cita';
        this.loading = false;
      }
    });
  }

  cargarCitas() {
    if (!this.userId) return;

    this.loading = true;
    this.authService.obtenerCitas({ usuario_id: this.userId }).subscribe({
      next: (citas: Cita[]) => {
        this.citas = citas;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando citas:', err);
        this.errorMessage = 'Error al cargar las citas';
        this.loading = false;
      }
    });
  }

  eliminarCita(id: number) {
    if (!confirm('¿Estás seguro de eliminar esta cita?') || this.loading) return;

    this.loading = true;
    this.errorMessage = null;

    this.authService.eliminarCita(id).subscribe({
      next: () => {
        this.successMessage = 'Cita eliminada correctamente';
        this.cargarCitas();
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'No se pudo eliminar la cita';
        this.loading = false;
      }
    });
  }

  formatFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-ES');
  }

  getNombreServicio(servicioId: number): string {
    const servicio = this.servicios.find(s => s.id === servicioId);
    return servicio ? servicio.nombre : 'Servicio desconocido';
  }

  clearMessages() {
    this.errorMessage = null;
    this.successMessage = null;
  }
}