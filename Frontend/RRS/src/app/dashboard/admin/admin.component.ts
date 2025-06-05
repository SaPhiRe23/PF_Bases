import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {
  users: any[] = [];

  newUser = {
    nombre: '',
    email: '',
    contrasena: '',
    confirmar_contrasena: '',
    rol: 'empresa'
  };

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.obtenerUsuarios();
  }

  obtenerUsuarios() {
    this.authService.obtenerUsuarios().subscribe({
      next: data => this.users = data,
      error: err => console.error('Error al obtener usuarios:', err)
    });
  }

  deleteUser(id: number) {
    this.authService.eliminarUsuario(id).subscribe({
      next: () => {
        this.users = this.users.filter(u => u.id !== id);
        alert('Usuario eliminado correctamente');
      },
      error: err => console.error('Error al eliminar usuario:', err)
    });
  }

  // Getter para verificar si las contraseñas no coinciden
  get passwordsDontMatch(): boolean {
    return this.newUser.contrasena !== this.newUser.confirmar_contrasena;
  }

  addUser() {
    if (this.passwordsDontMatch) {
      alert('Las contraseñas no coinciden');
      return;
    }

    this.authService.crearUsuario(this.newUser).subscribe({
      next: () => {
        alert('Usuario creado correctamente');
        this.obtenerUsuarios();
        this.newUser = {
          nombre: '',
          email: '',
          contrasena: '',
          confirmar_contrasena: '',
          rol: 'empresa'
        };
      },
      error: err => {
        console.error('Error al crear usuario:', err);
        alert(err.error.detail || 'Error al crear usuario');
      }
    });
  }
}
