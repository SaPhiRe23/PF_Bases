import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
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

  // ------------------------ SESSION ------------------------

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

  getUserId(): string | null {
    if (this.isBrowser) {
      return localStorage.getItem('user_id');
    }
    return null;
  }

  // ------------------------ LOGIN ------------------------

  login(email: string, password: string): Observable<any> {
    return new Observable(observer => {
      this.http.post<any>(`${this.API_URL}/usuarios/login`, { email, contrasena: password }).subscribe({
        next: user => {
          const token = 'mock-token';
          this.storeSession(token, user.rol);
          localStorage.setItem('user_id', user.id.toString());
          observer.next(user);
        },
        error: err => observer.error(err)
      });
    });
  }

  // ------------------------ USUARIOS ------------------------

  obtenerUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_URL}/usuarios/`);
  }

  crearUsuario(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/usuarios/`, data);
  }

  eliminarUsuario(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/usuarios/${id}`);
  }

  // ------------------------ CITAS ------------------------

  crearCita(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/citas/`, data);
  }

  obtenerCitas(params?: any): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_URL}/citas/`, { params });
  }

  eliminarCita(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/citas/${id}`);
  }

  actualizarEstadoCita(id: number, estado: string): Observable<any> {
    return this.http.patch(`${this.API_URL}/citas/${id}/estado?estado=${estado}`, {});
  }

  // ------------------------ SERVICIOS ------------------------

  obtenerServicios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_URL}/servicios/`);
  }

  crearServicio(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/servicios/`, data);
  }

  eliminarServicio(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/servicios/${id}`);
  }

  actualizarServicio(id: number, data: any): Observable<any> {
    return this.http.patch(`${this.API_URL}/servicios/${id}`, data);
  }
}
