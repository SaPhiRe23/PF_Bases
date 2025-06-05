import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private API_URL = 'http://localhost:8000';
  private isBrowser: boolean;
  private authState = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.authState.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(this.platformId);

    if (this.isBrowser) {
      const token = localStorage.getItem('token');
      this.authState.next(!!token);
    }
  }

  storeSession(token: string, role: string) {
    if (this.isBrowser) {
      localStorage.setItem('token', token);
      localStorage.setItem('role', role);
    }
    this.authState.next(true);
  }

  logout() {
    if (this.isBrowser) {
      localStorage.clear();
    }
    this.authState.next(false);
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    if (this.isBrowser) {
      return !!localStorage.getItem('token');
    }
    return false;
  }

  getUserRole(): string | null {
    if (this.isBrowser) {
      return localStorage.getItem('role');
    }
    return null;
  }

  // Usuarios
  register(data: any) {
    return this.http.post(`${this.API_URL}/usuarios/`, data);
  }

  obtenerUsuarios(params?: any) {
    return this.http.get(`${this.API_URL}/usuarios/`, { params });
  }

  // Citas
  crearCita(data: any) {
    return this.http.post(`${this.API_URL}/citas/`, data);
  }

  login(email: string, password: string): Observable<any> {
    const params = new HttpParams().set('email', email);
    return new Observable(observer => {
      this.http.get<any[]>(`${this.API_URL}/usuarios/`, { params }).subscribe({
        next: users => {
          const user = users.find(u => u.email === email);
          if (user && password === '123') {
            if (this.isBrowser) {
              localStorage.setItem('token', 'mock-token');
              localStorage.setItem('role', 'usuario');
            }
            this.authState.next(true);
            observer.next(user);
          } else {
            observer.error({ detail: 'Credenciales inválidas' });
          }
        },
        error: err => observer.error(err)
      });
    });
  }
}
