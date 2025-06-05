import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  form: FormGroup;

  constructor(private fb: FormBuilder, private router: Router) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    console.log('Formulario válido:', this.form.valid);
    console.log('Valores del formulario:', this.form.value);

    if (this.form.valid) {
      const { email, password } = this.form.value;

      // Usuarios simulados
      const mockUsers = [
        { email: 'admin@e.com', password: 'admin123', role: 'admin' },
        { email: 'empresa@e.com', password: 'empresa123', role: 'empresa' }
      ];

      const user = mockUsers.find(u => u.email === email && u.password === password);

      if (user) {
        localStorage.setItem('token', 'mock-token');
        localStorage.setItem('role', user.role);
        this.router.navigate(['/dashboard']);
      } else {
        alert('Credenciales inválidas');
      }
    }
  }
}
