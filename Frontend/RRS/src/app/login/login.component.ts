import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  form: FormGroup;
  loading = false;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.form.invalid || this.loading) return;

    this.errorMessage = null;
    this.loading = true;
    
    const { email, password } = this.form.value;
    
    this.authService.login(email, password).subscribe({
      next: (user) => {
        // Redirigir según el rol del usuario
        const redirectRoute = this.getRedirectRoute(user.rol);
        this.router.navigate([redirectRoute]);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || err.message || 'Error al iniciar sesión';
        console.error('Login error:', err);
      },
      complete: () => {
        this.loading = false;
      }
    });
  }

  private getRedirectRoute(role: string): string {
    // Personaliza las rutas según los roles de tu aplicación
    switch (role.toLowerCase()) {
      case 'admin':
        return '/dashboard/admin';
      case 'empresa':
        return '/dashboard/empresa';
      default:
        return '/login';
    }
  }
}